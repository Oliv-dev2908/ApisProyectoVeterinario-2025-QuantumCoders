import pandas as pd
import numpy as np
import os, json
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler 
from datetime import datetime
from catboost import CatBoostRegressor 

from synthetic_data import generate_synthetic 

#Rutas de salida
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(OUTPUT_DIR, 'catboost_regressor_model.cbm') 
METRICS_PATH = os.path.join(OUTPUT_DIR, 'model_metrics.json')
CATEGORICAL_FEATURES = ['zona_codificada']

#NUEVA VARIABLE OBJETIVO: La señal continua pura
TARGET_COLUMN = 'puntuacion_abandono_ideal'

def preprocess_data(df: pd.DataFrame):
    
    #La variable objetivo es 'puntuacion_abandono_ideal'
    target_col = TARGET_COLUMN
    
    #Quitamos columnas que no son features, incluyendo la variable binaria de evaluación
    cols_to_drop = ['id_cliente', 'abandono', TARGET_COLUMN]
    cols_to_drop = [c for c in cols_to_drop if c in df.columns and c != target_col]
    
    X = df.drop(columns=cols_to_drop, errors='ignore') 
    y = df[target_col]
    
    #Manejo de Nulos (Imputación)
    for col in X.columns:
        if X[col].isnull().any():
            if col in CATEGORICAL_FEATURES:
                X[col] = X[col].fillna(X[col].mode()[0] if not X[col].mode().empty else '0')
            else:
                X[col] = X[col].fillna(X[col].median())
                
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        X[col] = X[col].astype(np.float64)

    # Estandarización
    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols]) 
    
    return X, y

def train_catboost(df: pd.DataFrame):
    
    X, y = preprocess_data(df)
    
    gasto_std = X['gasto_total'].std()
    print(f"DEPURACIÓN (Estandarizado): Desviación estándar de Gasto Total: {gasto_std:.2f} (Debe ser ≈ 1.0)")
    
    class_balance = df['abandono'].value_counts(normalize=True) # Usamos el abandono binario para ver la distribución
    print(f"Distribución de clases:\n{class_balance}")
    
    #Hacemos el split en base al target binario para estratificar correctamente
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=df['abandono']
    )

    print("🛠️ Inicializando CatBoostRegressor: PREDICIENDO LA SEÑAL IDEAL...")
    model = CatBoostRegressor(
        iterations=500, 
        learning_rate=0.07, 
        depth=4, 
        loss_function='RMSE',
        eval_metric='R2',
        random_seed=42,
        allow_writing_files=False,
        cat_features=CATEGORICAL_FEATURES,
        verbose=50, 
        od_type='None', 
    )

    print(f"🚀 Iniciando entrenamiento con {len(X_train):,} muestras...")
    model.fit(
        X_train, y_train,
        eval_set=(X_test, y_test),
        use_best_model=True
    )
    
    model.save_model(MODEL_PATH)

    #EVALUACIÓN: Usar la columna 'abandono' original para calcular las métricas finales
    y_test_abandono = df.loc[X_test.index, 'abandono']
    y_proba = model.predict(X_test)
    y_pred = (y_proba >= 0.5).astype(int)
    
    metrics = {
        "accuracy": round(accuracy_score(y_test_abandono, y_pred), 4),
        "auc_roc": round(roc_auc_score(y_test_abandono, y_proba), 4),
        "samples": len(df),
        "model_type": "Regressor",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("-" * 50)
    print(f"Entrenamiento completado y modelo guardado en: {MODEL_PATH}")
    print(f"Resultado FINAL: Accuracy: {metrics['accuracy']}, AUC-ROC: {metrics['auc_roc']}")
    print("-" * 50)
    return model

if __name__ == "__main__":
    N_SAMPLES = 2000000 
    
    print(f"Generando datos sintéticos ({N_SAMPLES:,} muestras)...")
    df = generate_synthetic(n=N_SAMPLES, vet_realism=2.0)
    
    train_catboost(df)
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

# Rutas de guardado del modelo
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'catboost_model.cbm') 
TEMP_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'rf_fallback_model.pkl')
USE_CATBOOST = True 

try:
    from catboost import CatBoostClassifier, Pool
except ImportError:
    print("CatBoost not found. Falling back to RandomForestClassifier for training.")
    from sklearn.ensemble import RandomForestClassifier
    USE_CATBOOST = False

#Variable categórica que CatBoost maneja directamente
CATEGORICAL_FEATURES = ['zona_codificada'] 

#Almacén de modelos cargados para evitar recargas constantes
_loaded_model = None 
_model_columns = None # Para manejar la consistencia de columnas en el fallback

#--- Funciones de Utilidad del Modelo ---

def preprocess_data(df: pd.DataFrame):
    """Prepara los datos para el entrenamiento/predicción, eliminando IDs."""
    
    # 1. Separar características (X) y etiqueta (y)
    X = df.drop(columns=['id_cliente', 'abandono', 'puntuacion_abandono_ideal'], errors='ignore')
    y = df['abandono'] if 'abandono' in df.columns else None

    # 2. Relleno de Nulos (Imputación)
    for col in X.columns:
        if X[col].isnull().any():
            if col in CATEGORICAL_FEATURES:
                # Usar '0' (que ya está codificado) o 'Missing'
                X[col] = X[col].fillna(X[col].mode()[0] if not X[col].mode().empty else '0')
            else:
                # Usar la mediana para las numéricas
                X[col] = X[col].fillna(X[col].median())

    return X, y

def train_catboost(df: pd.DataFrame):
    """Entrena el modelo y lo guarda en disco."""
    global _model_columns
    
    X, y = preprocess_data(df)
    
    if y is None:
        raise ValueError('Target column "abandono" not found in the dataframe for training.')
    if y.isnull().all():
         raise ValueError('Target column "abandono" contains only null values in the training set.')

    if len(X) < 100 or len(y.unique()) < 2:
        raise ValueError("Insufficient data or only one class detected. Cannot train model.")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    if USE_CATBOOST:
        model = CatBoostClassifier(
            iterations=300, 
            learning_rate=0.05, 
            depth=6, 
            loss_function='Logloss', 
            random_seed=42, 
            verbose=0,
            allow_writing_files=False, 
            cat_features=CATEGORICAL_FEATURES
        )
        model_path = MODEL_PATH
        model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=10)
        
        feature_importance = list(zip(X.columns.tolist(), model.get_feature_importance()))
        # Guardar el modelo
        model.save_model(model_path)
    else:
        # Fallback a Random Forest (necesita codificación OHE)
        X_train_enc = pd.get_dummies(X_train, columns=CATEGORICAL_FEATURES, drop_first=True)
        X_test_enc = pd.get_dummies(X_test, columns=CATEGORICAL_FEATURES, drop_first=True)
        X_test_enc = X_test_enc.reindex(columns=X_train_enc.columns, fill_value=0) 
        
        # Guardar las columnas usadas para la consistencia en 'predict'
        _model_columns = X_train_enc.columns.tolist() 

        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model_path = TEMP_MODEL_PATH
        model.fit(X_train_enc, y_train)
        
        feature_importance = list(zip(X_train_enc.columns.tolist(), model.feature_importances_))
        # Guardar el modelo y las columnas
        joblib.dump({'model': model, 'columns': _model_columns}, model_path)
        
    # 4. Evaluación
    X_test_eval = X_test if USE_CATBOOST else X_test_enc
    
    y_pred_proba = model.predict_proba(X_test_eval)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    accuracy = accuracy_score(y_test, model.predict(X_test_eval))
            
    # 5. Preparar el resumen de resultados
    return {
        'status': 'success',
        'model_used': 'CatBoost' if USE_CATBOOST else 'RandomForest (Fallback)',
        'accuracy': round(accuracy, 4),
        'auc_roc': round(auc, 4),
        'num_samples': len(df),
        'feature_importance': feature_importance
    }

def load_model():
    """Carga el modelo persistente desde disco y las columnas si usa fallback."""
    global _loaded_model, _model_columns
    if _loaded_model is not None:
        return _loaded_model

    model_path = MODEL_PATH if USE_CATBOOST else TEMP_MODEL_PATH

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please run the /train endpoint first.")
    
    if USE_CATBOOST:
        from catboost import CatBoostClassifier
        model = CatBoostClassifier()
        model.load_model(model_path)
    else:
        # Carga el modelo y las columnas para RF
        data = joblib.load(model_path)
        model = data['model']
        _model_columns = data['columns']
            
    _loaded_model = model
    return model

def predict(df: pd.DataFrame) -> np.ndarray:
    """Realiza predicciones de probabilidad de abandono sobre nuevos datos."""
    
    model = load_model()
    
    # 1. Preprocesar (solo obtenemos X, sin la etiqueta 'abandono')
    X_pred, _ = preprocess_data(df.drop(columns=['abandono'], errors='ignore'))
    
    # 2. Aplicar la codificación OHE si se usó el modelo de fallback (Random Forest)
    if not USE_CATBOOST:
        global _model_columns
        if _model_columns is None:
             raise RuntimeError("RandomForest model loaded but training columns are missing.")
             
        X_pred = pd.get_dummies(X_pred, columns=CATEGORICAL_FEATURES, drop_first=True)
        # Asegurar que las columnas coinciden con las usadas en el entrenamiento
        X_pred = X_pred.reindex(columns=_model_columns, fill_value=0)
        
    # 3. Realizar la predicción
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X_pred)[:, 1]
    else:
        return model.predict(X_pred)

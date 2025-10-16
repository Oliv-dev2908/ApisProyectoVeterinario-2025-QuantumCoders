from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import os, io, base64, matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from app.ml.synthetic_data import generate_synthetic
from app.ml.catboost_model import train_catboost, predict
from app.ml.hdbscan_analysis import run_hdbscan_and_plot
from app.data_reader import read_query_to_df
from app.database import SUPABASE_DB_URL
router = APIRouter(prefix="/ml", tags=["Machine Learning"])

PRODUCTION = os.getenv('PRODUCTION', 'false').lower() == 'true'

def _load_data(use_synthetic: bool, n_samples: int, vet_realism: float) -> pd.DataFrame:
    """Función de utilidad para cargar datos, centralizando la lógica DB/Synthetic."""
    if use_synthetic:
        # Carga de datos sintéticos
        df = generate_synthetic(n=n_samples, vet_realism=vet_realism)
        print(f"Loaded {len(df)} synthetic samples.")
        return df
    else:
        # Carga de datos reales de la BBDD
        # Chequeamos que la URL de la DB esté configurada.
        if not SUPABASE_DB_URL:
            raise RuntimeError('Real DB connection not enabled: DB URL is not configured. Set SUPABASE_DB_URL.')

        try:
            # Leer el query SQL desde el archivo
            with open('app/data/query.sql', 'r') as f:
                sql_query = f.read()
        except FileNotFoundError:
            raise RuntimeError("query.sql file not found in app/data/. Cannot load real data query.")

        # Llamar a la función que usa la URL de la DB internamente
        df = read_query_to_df(sql_query) 
        print(f"Loaded {len(df)} samples from real database.")
        
        # Limitar datos reales si es necesario
        if len(df) > n_samples:
            df = df.sample(n=n_samples, random_state=42).reset_index(drop=True)
            print(f"Downsampled to {len(df)} real samples.")

        return df


@router.get('/train')
def train_endpoint(use_synthetic: bool = True, n_samples: int = 20000, vet_realism: float = 1.0):
    """Entrena el modelo de abandono. Debe hacerse con datos sintéticos robustos (por defecto)."""
    if PRODUCTION:
        raise HTTPException(status_code=403, detail='Training is disabled in production.')
    
    try:
        df = _load_data(use_synthetic, n_samples, vet_realism)
        res = train_catboost(df)
        return JSONResponse(res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@router.get('/analyze')
def analyze_endpoint(use_synthetic: bool = True, n_samples: int = 100000, vet_realism: float = 1.0):
    """Realiza clustering HDBSCAN y predicción de abandono sobre los datos cargados (reales o sintéticos)."""
    try:
        # Carga los datos (Reales o Sintéticos) para hacer clustering y predicción
        df_target = _load_data(use_synthetic, n_samples, vet_realism)
        
        # Eliminamos 'id_cliente', 'abandono' y 'zona_codificada' (categórica) antes del PCA/HDBSCAN
        features = df_target.drop(columns=['id_cliente','abandono', 'zona_codificada'], errors='ignore') 
        
        # Análisis de clustering sobre los datos cargados
        labels, img_b64 = run_hdbscan_and_plot(features)
        
        try:
            # Predicción con el modelo guardado (entrenado previamente con /train)
            probs = predict(df_target) 
            df_target['prob_abandono'] = probs
            # Crear la lista de diccionarios de predicciones
            preds = df_target[['id_cliente','prob_abandono']].to_dict(orient='records')
        except Exception as e:
            # Si la predicción falla (ej. modelo no entrenado), devolvemos el error
            preds = {'error': f"Prediction failed (Model likely not trained): {str(e)}"}
            
        return {'num_clients': len(df_target),
                'clusters_detected': int(len(set(labels)) - (1 if -1 in labels else 0)),
                'hdbscan_plot_base64': img_b64,
                'predictions': preds}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get('/visuals')
def visuals_endpoint(use_synthetic: bool = False, n_samples: int = 10000, vet_realism: float = 1.0):
    """Genera el gráfico de clustering (con datos reales o sintéticos) y el de importancia de características (con entrenamiento sintético)."""
    try:
        # 1. Cargar datos para HDBSCAN (Datos Reales o Sintéticos, lo que el usuario pida)
        df_target = _load_data(use_synthetic, n_samples, vet_realism)

        # Preprocesar para HDBSCAN
        features_target = df_target.drop(columns=['id_cliente','abandono', 'zona_codificada'], errors='ignore')
        
        # HDBSCAN Plot (Clusterización de los datos cargados)
        labels, hdb_img = run_hdbscan_and_plot(features_target)
        
        # 2. Feature Importance Plot (SIEMPRE usando entrenamiento sintético robusto para estabilidad)
        fi_b64 = None
        try:
            # Cargamos un gran dataset sintético *temporalmente* (10k) para FI estable
            df_fi = generate_synthetic(n=10000, vet_realism=1.0, random_state=123) 
            
            # Entrenamos *solo* para obtener la importancia de características
            res = train_catboost(df_fi) 
            
            names = [n for n,_ in res['feature_importance']]
            vals = [v for _,v in res['feature_importance']]
            
            # Crear DataFrame para ordenar y graficar
            fi_df = pd.DataFrame({'feature': names, 'importance': vals}).sort_values(by='importance', ascending=True)
            
            fig, ax = plt.subplots(figsize=(8,4))
            ax.barh(fi_df['feature'], fi_df['importance'])
            ax.set_title('Feature Importance (Synthetic Training)', fontsize=14)
            ax.set_xlabel('Importancia')
            fig.tight_layout()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)
            fi_b64 = base64.b64encode(buf.read()).decode('ascii')
        except Exception as e:
            print(f"Feature Importance plotting failed: {e}")
            fi_b64 = None
            
        return {'hdbscan_plot_base64': hdb_img, 'catboost_feature_importance_base64': fi_b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visuals failed: {str(e)}")

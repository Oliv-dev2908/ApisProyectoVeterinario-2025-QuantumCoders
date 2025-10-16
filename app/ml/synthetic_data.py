import numpy as np
import pandas as pd

def generate_synthetic(n=2000000, random_state=42, vet_realism=2.0):
    """
    Genera datos sintéticos con una señal de abandono pura y sin colinealidad
    para forzar un aprendizaje casi perfecto.
    """
    rng = np.random.default_rng(random_state)

    cluster_id = rng.choice([1, 2, 3], size=n, p=[0.45, 0.35, 0.20])
    params = {
        1: {'vol': 0.8, 'est': 1.7, 'info': 4, 'disp': 2.5},
        2: {'vol': 1.0, 'est': 2.4, 'info': 6, 'disp': 3.0},
        3: {'vol': 1.3, 'est': 2.8, 'info': 8, 'disp': 3.8},
    }

    zona = rng.choice([0,1,2,3,4,5], size=n).astype(str)
    num_mascotas = rng.choice([1,2,3], size=n, p=[0.65,0.3,0.05])
    num_especies = np.minimum(num_mascotas, rng.choice([1,2], size=n, p=[0.85,0.15]))
    edad_promedio = np.clip(rng.normal(5, 3, size=n), 0.1, 18).round(1)

    gasto_total = np.zeros(n)
    estado_promedio = np.zeros(n)
    nivel_informacion = np.zeros(n)
    gravedad_promedio = np.zeros(n)
    complejidad_promedio = np.zeros(n)
    disposicion_tiempo = np.zeros(n)

    for k in params:
        mask = cluster_id == k
        N_k = np.sum(mask)

        gasto_total[mask] = np.round(rng.exponential(scale=180 * params[k]['vol'], size=N_k),2)
        estado_promedio[mask] = np.clip(rng.normal(params[k]['est'], 0.02 / vet_realism, size=N_k), 1, 3)
        nivel_informacion[mask] = np.clip(rng.normal(params[k]['info'], 0.02 / vet_realism, size=N_k), 1, 10)
        disposicion_tiempo[mask] = np.clip(rng.normal(params[k]['disp'], 0.02 / vet_realism, size=N_k), 1, 5)
        gravedad_promedio[mask] = np.clip(rng.normal(1.8, 0.02 / vet_realism, size=N_k), 1, 3)
        duracion_promedio = np.clip(rng.normal(10, 0.3 / vet_realism, size=N_k), 1, 60)
        complejidad_promedio[mask] = (duracion_promedio * gravedad_promedio[mask]).round(1)

    # Probabilidad de abandono - Fórmula de señal PURA y AISLADA
    logits = (
        -1.0 * (estado_promedio - 2)
        + 0.9 * (gravedad_promedio - 0.9)
        - 1.0 * ((nivel_informacion - 5)/5)
        - 0.8 * ((disposicion_tiempo - 3)/2)
        - 0.75 * (gasto_total / 100)
        + 0.1 * (complejidad_promedio / 10)
    )
    
    # 1. TARGET IDEAL (CONTINUO): Es la señal perfecta que el modelo aprende.
    puntuacion_abandono_ideal = 1 / (1 + np.exp(-logits))
    
    # 2. TARGET BINARIO (RUIDOSO): Generamos la clasificación con ruido simple
    # El ruido se añade al score ideal (sin doble generación de ruido) para asegurar alta correlación.
    noise = rng.normal(0, 0.01, size=n) 
    abandono_score = puntuacion_abandono_ideal + noise
    abandono = (abandono_score >= 0.5).astype(int)

    df = pd.DataFrame({
        "id_cliente": np.arange(1, n+1),
        "zona_codificada": zona,
        "gasto_total": gasto_total,
        "num_mascotas": num_mascotas,
        "num_especies": num_especies,
        "edad_promedio_mascotas": edad_promedio,
        "estado_promedio": estado_promedio.round(1),
        "gravedad_promedio": gravedad_promedio.round(1),
        "complejidad_promedio": complejidad_promedio,
        "nivel_informacion": nivel_informacion.round(1),
        "disposicion_tiempo": disposicion_tiempo.round(1),
        
        # ✅ TARGET CONTINUO PARA EL ENTRENAMIENTO
        "puntuacion_abandono_ideal": puntuacion_abandono_ideal.round(4),
        
        # ✅ TARGET BINARIO PARA LA EVALUACIÓN (Ahora fuertemente correlacionado)
        "abandono": abandono,
    })

    return df
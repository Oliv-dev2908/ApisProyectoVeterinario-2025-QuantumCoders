import io, base64
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import hdbscan

def run_hdbscan_and_plot(df: pd.DataFrame, target_variance: float = 0.90, min_cluster_size: int = None, min_samples: int = None):
    """
    Ejecuta HDBSCAN ajustado dinámicamente y genera un gráfico informativo:
      - PCA con límite adaptativo (máx. 15 componentes).
      - Parámetros HDBSCAN autorregulados.
      - Etiquetas de PCA1/PCA2 muestran la variable más dominante.
    """
    X = df.copy()
    cols_to_drop = ['id_cliente', 'zona_codificada', 'abandono', 'cluster_base']
    X = X.drop(columns=[c for c in cols_to_drop if c in X.columns], errors='ignore')
    
    # 0. Preprocesamiento
    X_num = X.select_dtypes(include=np.number).fillna(X.median())
    column_names = X_num.columns # Guardamos los nombres para los loadings

    if len(X_num) < 20:
        raise ValueError("No hay suficientes filas para clusterizar.")

    # 1. Escalado
    X_scaled = StandardScaler().fit_transform(X_num)

    # --- PCA adaptativo para HDBSCAN ---
    pca_limit = min(X_num.shape[1], 15)
    pca = PCA(n_components=min(target_variance, 0.95))
    X_pca_full = pca.fit_transform(X_scaled)
    
    # Aseguramos que el número de PCs usados no exceda el límite ni la cantidad disponible
    n_pcs = min(pca.n_components_, pca_limit)
    X_pca = X_pca_full[:, :n_pcs]
    explained_var = np.sum(pca.explained_variance_ratio_[:n_pcs]) * 100

    # --- Parámetros dinámicos para HDBSCAN ---
    n_samples_total = len(X_num)
    if min_cluster_size is None:
        # 3% de los datos o mínimo 10. Si tu dataset es 100k, esto es 3000.
        min_cluster_size = max(10, int(0.01 * n_samples_total))
    if min_samples is None:
        min_samples = max(5, int(min_cluster_size / 2))

    # Aseguramos que los valores estén en un rango razonable para evitar 1400+ clusters o solo 1.
    min_cluster_size = min(min_cluster_size, n_samples_total // 10) # No más del 10% del total
    min_samples = min(min_samples, n_samples_total // 20)

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        cluster_selection_epsilon=0.3,
        cluster_selection_method='eom',
        metric='euclidean',
        prediction_data=True,
        allow_single_cluster=False
    )

    labels = clusterer.fit_predict(X_pca)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    # --- PCA 2D para visualización y Loadings ---
    pca2 = PCA(n_components=2)
    X_2d = pca2.fit_transform(X_scaled)
    var2d = pca2.explained_variance_ratio_ * 100
    
    # CÁLCULO DE LOADINGS Y ETIQUETAS DOMINANTES
    loadings = pca2.components_ # Matriz de rotación (correlación entre variables y PCs)
    
    abs_loadings_pca1 = np.abs(loadings[0])
    abs_loadings_pca2 = np.abs(loadings[1])
    
    # Encontrar la variable con el mayor peso (loadings) para cada componente
    dominant_feature_pca1 = column_names[np.argmax(abs_loadings_pca1)].replace('_', ' ').title()
    dominant_feature_pca2 = column_names[np.argmax(abs_loadings_pca2)].replace('_', ' ').title()

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(7,6))
    mask_noise = labels == -1
    mask_cluster = ~mask_noise
    cmap = plt.cm.get_cmap('tab10', max(2, n_clusters + 1))

    ax.scatter(X_2d[mask_noise,0], X_2d[mask_noise,1], c='lightgray', s=8, alpha=0.4, label='Ruido')
    sc = ax.scatter(X_2d[mask_cluster,0], X_2d[mask_cluster,1],
                     c=labels[mask_cluster], cmap=cmap, s=25, alpha=0.9)

    ax.set_title(f'HDBSCAN: {n_clusters} Clusters detectados')
    
    # ETIQUETAS MEJORADAS
    ax.set_xlabel(f'PCA1 ({var2d[0]:.1f}% Varianza) - Domina: {dominant_feature_pca1}')
    ax.set_ylabel(f'PCA2 ({var2d[1]:.1f}% Varianza) - Domina: {dominant_feature_pca2}')
    
    # Etiqueta de Varianza Total
    ax.text(0.02, 0.98,
            f'{n_pcs} PCs retenidos ({explained_var:.1f}% var. total)',
            transform=ax.transAxes, va='top',
            fontsize=9, bbox=dict(boxstyle='round', fc='white', alpha=0.7))
    ax.grid(alpha=0.3)
    plt.colorbar(sc, ax=ax, label='Etiqueta de cluster')

    # --- Codificación Base64 ---
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')

    return labels, img_b64  
import pandas as pd
# Importamos la variable de entorno ya cargada desde el primer archivo.
# Suponiendo que el primer archivo se llama 'database.py'
from app.database import SUPABASE_DB_URL

def read_query_to_df(sql: str) -> pd.DataFrame:
    """
    Ejecuta un query SQL y retorna un DataFrame de Pandas,
    utilizando la URL de conexión de la base de datos de Supabase.
    """
    # 1. Verificación: Aseguramos que la URL esté disponible.
    if not SUPABASE_DB_URL:
        # Esto lanzará el mismo error que en 'database.py' si no está seteada.
        raise RuntimeError('SUPABASE_DB_URL no está seteada para la conexión.')
    
    try:
        print(f"Ejecutando SQL: {sql}")
        
        # 2. Conexión con Pandas: Pasamos la URL directamente a Pandas,
        # tal como lo hiciste en tu segundo ejemplo, para que maneje
        # la conexión interna y evitar problemas de concurrencia.
        df = pd.read_sql(sql, SUPABASE_DB_URL)
        
        print(f"Se cargaron {len(df)} filas.")
            
    except Exception as e:
        # Manejo de errores
        raise RuntimeError(f"Fallo en la consulta a la base de datos. Error: {e.__class__.__name__}: {e}") from e

    # 3. Conversión (Opcional, según tu ejemplo)
    if 'zona_codificada' in df.columns:
        df['zona_codificada'] = df['zona_codificada'].astype(str) 
            
    return df

# Ejemplo de uso (opcional, para probar)
if __name__ == '__main__':
    # Necesitas que el archivo 'database.py' se ejecute primero o que
    # sus variables estén disponibles, y que tengas tu archivo .env configurado.
    
    # Intenta una consulta de ejemplo (reemplaza 'nombre_de_tu_tabla' y 'columna' con datos reales)
    try:
        sample_sql = "SELECT * FROM public.items LIMIT 5;"
        df_result = read_query_to_df(sample_sql)
        print("\nDataFrame resultante:")
        print(df_result.head())
    except Exception as e:
        print(f"Error al intentar la prueba: {e}")
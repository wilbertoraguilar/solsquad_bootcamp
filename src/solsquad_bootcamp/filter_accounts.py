from datetime import datetime, timedelta
import pandas as pd
from src.solsquad_bootcamp.main import extract_all


def filter_accounts_younger_than_3_years(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra las cuentas con menos de 3 años de antigüedad.
    Se asume que el DataFrame tiene una columna llamada 'account_creation_date'.
    """
    # Fecha límite (3 años atrás desde hoy)
    three_years_ago = datetime.now() - timedelta(days=3 * 365)

    # Convertir la columna a datetime, ignorando valores inválidos
    df["account_creation_date"] = pd.to_datetime(df["account_creation_date"], errors="coerce")

    # Filtrar las cuentas creadas después de la fecha límite
    filtered = df[df["account_creation_date"] > three_years_ago].copy()

    return filtered


def main():
    """
    Ejecuta el proceso completo:
    - Extrae los datos con extract_all()
    - Filtra las cuentas de menos de 3 años
    - Guarda el resultado en un CSV
    """
    print("📥 Extrayendo datos...")
    df = extract_all()

    print("🔍 Filtrando cuentas con menos de 3 años...")
    filtered_df = filter_accounts_younger_than_3_years(df)

    output_path = "data/accounts_filtered.csv"
    filtered_df.to_csv(output_path, index=False)

    print(f"✅ Proceso completado. CSV guardado en: {output_path}")
    print(f"📊 Total de filas filtradas: {len(filtered_df)}")


if __name__ == "__main__":
    main()

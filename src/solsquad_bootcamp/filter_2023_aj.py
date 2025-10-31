from __future__ import annotations
import os
import pandas as pd
import typer


def read_csv_to_df(path: str):
    """Lee un CSV y devuelve un DataFrame."""
    if not os.path.isabs(path):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        path = os.path.join(repo_root, path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found at: {path}")

    return pd.read_csv(path)


def main(path: str = "data/mock-data.csv"):
    """Filtra cuentas del año 2023 y guarda un nuevo CSV."""
    try:
        df = read_csv_to_df(path)
    except Exception as exc:
        typer.echo(f"Error loading CSV: {exc}")
        raise typer.Exit(code=1)

    typer.echo(f"Loaded '{path}': {len(df)} rows x {len(df.columns)} cols")
    typer.echo("First 5 rows:")
    typer.echo(df.head(n=5).to_string(index=False))

    # Convertir la columna 'birthdate' a tipo fecha
    df["birthdate"] = pd.to_datetime(df["birthdate"], errors="coerce")

    # Filtrar solo las cuentas del año 2023
    filtered_df = df[df["birthdate"].dt.year == 2023]

    typer.echo(f"Filtered accounts from year 2023: {len(filtered_df)} rows")

    # Pedir al usuario un nombre para el archivo
    output = typer.prompt("Extracted file name (e.g. filtered_2023.csv)")
    os.makedirs("data", exist_ok=True)
    filtered_df.to_csv(os.path.join("data", output), index=False)

    typer.echo(f"✅ File saved as: data/{output}")


if __name__ == "__main__":
    typer.run(main)

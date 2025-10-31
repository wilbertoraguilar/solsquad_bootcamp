from __future__ import annotations

import os
from typing import Any

import typer
import pandas as pd
from datetime import datetime 

def read_csv_to_df(path: str) -> Any:
    """
    Lee un CSV desde una ruta relativa al raíz del proyecto.
    """
    if not os.path.isabs(path):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        path = os.path.join(repo_root, path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found at: {path}")

    return pd.read_csv(path)


def main(path: str = "data/mock-data.csv") -> None:
    """
    Esta es la función original de 'extract_all'.
    Carga un CSV, pregunta por un nombre y lo guarda.
    """
    try:
        df = read_csv_to_df(path)
    except Exception as exc:
        typer.echo(f"Error loading CSV: {exc}")
        raise typer.Exit(code=1)

    typer.echo(f"Loaded '{path}': {len(df)} rows x {len(df.columns)} cols")
    typer.echo("First 5 rows:")
    try:
        typer.echo(df.head(n=5).to_string(index=False))
    except Exception:
        typer.echo(str(df.head()))
    
    output = typer.prompt("Extracted file name")
    df.to_csv("data/" + output, index=False)
    print("File saved as: data/" + output)


# --- Codigo para la tarea ---

def filter_accounts(path: str = "data/mock-data.csv") -> None:
    """
        Filtra cuentas de menos de 3 años (basado en 'birthdate') y guarda un CSV.
    """
    try:
        # Carga el CSV
        df = read_csv_to_df(path) 
        # Convierte la columna 'birthdate' a un formato de fecha
        df['birthdate'] = pd.to_datetime(df['birthdate'])

    except Exception as exc:
        typer.echo(f"Error loading CSV or parsing 'birthdate': {exc}")
        raise typer.Exit(code=1)

    typer.echo(f"Loaded '{path}': {len(df)} rows x {len(df.columns)} cols")

    # --- 1. FILTRO ---
    
    try:
        # Calcula la fecha de corte (exactamente 3 años atrás desde hoy)
        three_years_ago = datetime.now() - pd.DateOffset(years=3)
        
        # Filtra el DataFrame:
        # Quedarse con las filas donde 'birthdate' es MÁS RECIENTE que 'three_years_ago'
        df_filtrado = df[df['birthdate'] > three_years_ago]
    
    except KeyError:
        typer.echo(f"Error: La columna 'birthdate' no se encontró en el CSV.")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error desconocido durante el filtrado: {e}")
        raise typer.Exit(code=1)

# --- 2. GUARDAR EL ARCHIVO ---
    output_filename = "data/filtered_accounts.csv"
    
    df_filtrado.to_csv(output_filename, index=False)

    typer.echo(f"¡Filtrado con éxito! {len(df_filtrado)} filas (cuentas de < 3 años) guardadas en:")
    typer.echo(output_filename)

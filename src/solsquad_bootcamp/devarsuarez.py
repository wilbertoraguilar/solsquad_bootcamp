import pandas as pd
from datetime import datetime

def main():
    """
    Filters accounts belonging to people younger than 30 years old 
    based on the 'birthdate' column.
    Reads 'data/test.csv' and generates 'data/test_filtered_devarsuarez.csv'.
    """

    input_file = "data/test.csv"
    output_file = "data/test_filtered_devarsuarez.csv"

    try:
        df = pd.read_csv(input_file)
        print("✅ File loaded successfully.")
    except FileNotFoundError:
        print(f"❌ File '{input_file}' not found.")
        return

    # Convert 'birthdate' column to datetime
    df["birthdate"] = pd.to_datetime(df["birthdate"], errors="coerce")

    # Calculate age in years
    today = datetime.today()
    df["age"] = df["birthdate"].apply(lambda x: (today - x).days // 365 if pd.notnull(x) else None)

    # Filter people younger than 30 years old
    filtered = df[df["age"] < 30]

    print(f"📊 Found {len(filtered)} accounts belonging to people younger than 30 years old.")

    # Show a few rows as preview
    print(filtered.head())

    # Save the filtered results
    filtered.to_csv(output_file, index=False)
    print(f"💾 Result saved to '{output_file}'")

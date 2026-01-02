import pandas as pd
from database.db_handler import verified_table

def export_to_csv(filename="raksh_dataset.csv"):
    """
    Converts all verified database records into a professional CSV file.
    """
    data = verified_table.all()
    if not data:
        print("No data found to export.")
        return
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"🚀 Dataset generated: {filename} ({len(df)} rows)")

if __name__ == "__main__":
    export_to_csv()
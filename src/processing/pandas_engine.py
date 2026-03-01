import pandas as pd

def process_with_pandas(data: dict):
    df = pd.DataFrame([data])

    df["processing_mode"] = "NORMAL"
    df["value_processed"] = df["value"] * 2

    print(df)

    return {
        "processed_value": float(df["value_processed"].iloc[0])
    }


import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def preprocess(df: pd.DataFrame):
    """
    Encode gender, scale numeric features.
    Returns: scaled array, scaler, feature list
    """
    df = df.copy()

    # Encode gender
    le = LabelEncoder()
    df["gender_enc"] = le.fit_transform(df["gender"])  # 'Genre' in original dataset

    features = ["gender_enc", "age", "annual_income_(k$)", "spending_score_(1-100)"]
    # Gracefully handle column name variants
    available = [f for f in features if f in df.columns]

    X = df[available].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler, available, df
# src/data_processing.py
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def load_csv(path):
    df = pd.read_csv(path)
    return df

def split_features_target(df, target_col='deposit'):
    # Normaliza target (yes/no -> 1/0)
    y = df[target_col].apply(lambda v: 1 if str(v).strip().lower() in ['yes','si','sí','1','true'] else 0)
    X = df.drop(columns=[target_col])
    return X, y

def build_preprocessor(X):
    # Defino a mano columnas numéricas conocidas del dataset
    numeric_defaults = ['age','balance','day','duration','campaign','pdays','previous']
    num_cols = [c for c in numeric_defaults if c in X.columns]

    # Categóricas = resto de object/category
    cat_cols = [c for c in X.columns if c not in num_cols]

    from sklearn.pipeline import Pipeline
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('ohe', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ], remainder='drop')

    return preprocessor, num_cols, cat_cols

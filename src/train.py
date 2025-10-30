# src/train.py
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import Pipeline
import numpy as np
import argparse
from src.data_processing import load_csv, split_features_target, build_preprocessor

def train(path_csv, target_col='deposit', out_model='src/model_pipeline.pkl'):
    print("Cargando datos desde:", path_csv)
    df = load_csv(path_csv)
    X, y = split_features_target(df, target_col)
    preprocessor, num_cols, cat_cols = build_preprocessor(X)

    clf = DecisionTreeClassifier(random_state=42)

    pipe = Pipeline([
        ('pre', preprocessor),
        ('clf', clf)
    ])

    param_grid = {
        'clf__max_depth': [3, 5, 7, None],
        'clf__min_samples_split': [2, 5, 10],
        'clf__min_samples_leaf': [1, 2, 4]
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    grid = GridSearchCV(pipe, param_grid, cv=cv, scoring='roc_auc', n_jobs=-1, verbose=1)
    grid.fit(X, y)

    best = grid.best_estimator_
    joblib.dump(best, out_model)
    print("Modelo guardado en:", out_model)
    print("Mejores parámetros:", grid.best_params_)

    scores = cross_val_score(best, X, y, cv=cv, scoring='accuracy')
    print("Accuracy CV:", np.mean(scores))

    preds = best.predict(X)
    proba = best.predict_proba(X)[:,1]
    print(classification_report(y, preds))
    print("AUC:", roc_auc_score(y, proba))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path_csv', help='Ruta al CSV de entrenamiento')
    parser.add_argument('--target', default='deposit', help='Nombre de la columna target (por defecto "deposit")')
    parser.add_argument('--out', default='src/model_pipeline.pkl', help='Ruta de salida del modelo pickle')
    args = parser.parse_args()
    train(args.path_csv, args.target, args.out)

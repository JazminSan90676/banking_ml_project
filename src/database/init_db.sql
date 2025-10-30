CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    input_json JSONB,
    predicted INTEGER,
    probability FLOAT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_metrics (
    id SERIAL PRIMARY KEY,
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1 FLOAT,
    auc FLOAT,
    created_at TIMESTAMP DEFAULT now()
);

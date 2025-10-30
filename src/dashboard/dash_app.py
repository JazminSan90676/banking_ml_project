# src/dashboard/dash_app.py
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import os

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/predictions")
engine = create_engine(DB_URL)
app = dash.Dash(__name__, suppress_callback_exceptions=True)

def load_predictions(limit=1000):
    try:
        df = pd.read_sql("SELECT * FROM predictions ORDER BY created_at DESC LIMIT %s", engine, params=(limit,))
    except Exception:
        # Si falla o DB vacía, devolver df vacío
        df = pd.DataFrame(columns=['id','input_json','predicted','probability','created_at'])
    return df

app.layout = html.Div([
    html.H1("Dashboard de Métricas - Campañas Bancarias"),
    dcc.Graph(id='prob-dist'),
    dcc.Interval(id='interval', interval=10*1000, n_intervals=0)
])

@app.callback(
    dash.dependencies.Output('prob-dist','figure'),
    [dash.dependencies.Input('interval','n_intervals')]
)
def update(n):
    df = load_predictions()
    if df.empty:
        fig = px.histogram(pd.DataFrame({'probability': []}), x='probability', title='Distribución de probabilidades')
    else:
        fig = px.histogram(df, x='probability', nbins=30, title='Distribución de probabilidades')
    return fig

if __name__=='__main__':
    app.run_server(host='0.0.0.0', port=8050)

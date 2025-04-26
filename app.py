import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Carica i dati
df = pd.read_excel('CryptoData.xlsx')
df['Date'] = pd.to_datetime(df['Date'])

# Inizializza l'app Dash
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1('Crypto Dashboard', style={'textAlign': 'center'}),

    html.Label('Seleziona una criptovaluta:'),
    dcc.Dropdown(
        id='crypto-selector',
        options=[{'label': name, 'value': name} for name in df['Name'].unique()],
        value='Bitcoin'
    ),

    dcc.Graph(id='line-chart'),

    html.H3('Top 5 Criptovalute per Prezzo Massimo'),
    dcc.Graph(id='top5-bar-chart')
])

# Callback per aggiornare il grafico
@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('crypto-selector', 'value')]
)
def update_line_chart(selected_crypto):
    filtered_df = df[df['Name'] == selected_crypto]
    fig = px.line(filtered_df, x='Date', y='Close', title=f'{selected_crypto} - Prezzo nel tempo')
    return fig

# Callback per il grafico Top 5 (statico)
@app.callback(
    dash.dependencies.Output('top5-bar-chart', 'figure'),
    [dash.dependencies.Input('crypto-selector', 'value')]  # solo per attivare il rendering
)
def update_bar_chart(_):
    max_close = df.groupby('Name')['Close'].max().sort_values(ascending=False).head(5)
    top5_df = max_close.reset_index()
    fig = px.bar(top5_df, x='Name', y='Close', title='Top 5 Criptovalute per Prezzo Massimo')
    return fig


# Avvia l'app
if __name__ == '__main__':
    app.run(debug=True)

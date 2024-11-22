import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from pathlib import Path

# Funkcja przygotowująca dane
def prepare_data(y_pred, y_true, urls):
    """
    Przygotowuje dane do interaktywnego histogramu.

    Parametry:
    y_pred (array-like): Przewidywane wartości.
    y_true (array-like): Rzeczywiste wartości.
    urls (array-like): URL-e powiązane z danymi.

    Zwraca:
    DataFrame zawierający różnice procentowe i szczegóły.
    """
    percentage_errors = ((y_true - y_pred) / y_true) * 100
    return pd.DataFrame({
        "percentage_error": percentage_errors,
        "actual_price": y_true,
        "predicted_price": y_pred,
        "url": urls
    })

# Bieżąca lokalizacja pliku i wczytanie danych
current_dir = Path(__file__).parent
data_file = current_dir / "../data/interactive_data.json"

if not data_file.exists():
    raise FileNotFoundError(f"Plik {data_file} nie istnieje.")

data_df = pd.read_json(data_file, orient="records", lines=True)
data = prepare_data(data_df["y_pred"], data_df["y_true"], data_df["url"])

# Tworzenie aplikacji Dash
app = Dash(__name__)

# Layout aplikacji
app.layout = html.Div([
    html.H1("Interaktywny histogram różnic procentowych", style={'text-align': 'center'}),
    
    # Histogram
    dcc.Graph(
        id="histogram",
        config={"scrollZoom": False}
    ),
    
    # Tabela z detalami
    html.Div(id="details", style={'margin-top': '20px'})
])

# Callback do aktualizacji histogramu
@app.callback(
    Output("histogram", "figure"),
    Input("histogram", "id")  # Dummy input, by załadować histogram raz
)
def update_histogram(_):
    fig = px.histogram(
        data,
        x="percentage_error",
        nbins=40,
        labels={"percentage_error": "Procentowy błąd przewidywań (%)"},
        title="Histogram różnic procentowych"
    )
    fig.update_traces(marker_line_width=1.5, opacity=0.7)
    fig.update_layout(
        xaxis_title="Procentowy błąd przewidywań (%)",
        yaxis_title="Liczba wystąpień",
        bargap=0.1
    )
    return fig

# Callback do wyświetlania szczegółów po kliknięciu słupka
@app.callback(
    Output("details", "children"),
    Input("histogram", "clickData")
)
def display_details(clickData):
    if not clickData:
        return html.Div("Kliknij słupek, aby zobaczyć szczegóły", style={'text-align': 'center'})

    # Wyciągnięcie zakresu słupka (start i przybliżony end)
    bin_start = clickData["points"][0]["x"]
    bin_end = bin_start + 1  # Przyjmujemy szerokość binu 1 (można dostosować)

    # Filtrowanie danych w zakresie słupka
    filtered_data = data[(data["percentage_error"] >= bin_start) & (data["percentage_error"] < bin_end)]

    # Tworzenie tabeli z detalami
    table = html.Table(
        # Nagłówki tabeli
        [html.Tr([html.Th("Cena faktyczna"), html.Th("Cena przewidywana"), html.Th("URL")])] +
        # Wiersze tabeli
        [html.Tr([
            html.Td(f"{row['actual_price']:.2f} PLN"),
            html.Td(f"{row['predicted_price']:.2f} PLN"),
            html.Td(html.A("Link", href=row["url"], target="_blank"))
        ]) for _, row in filtered_data.iterrows()],
        style={'width': '100%', 'border': '1px solid black', 'border-collapse': 'collapse'}
    )
    return table

# Uruchomienie aplikacji
if __name__ == "__main__":
    app.run_server(debug=True)

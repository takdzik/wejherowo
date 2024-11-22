import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import shap
    
import plotly.express as px

def residuals_hist(y_pred, y_test):
    residuals = y_test - y_pred
    plt.hist(residuals, bins=20, edgecolor='k')
    plt.xlabel('Reszty')
    plt.ylabel('Liczba wystąpień')
    plt.title('Histogram reszt')
    plt.show()
    
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

def plot_percentage_error_histogram(y_pred, y_true, bins=40):
    """
    Tworzy histogram procentowych błędów przewidywań z liczbą wystąpień nad każdym słupkiem.

    Parametry:
    y_pred (array-like): Przewidywane wartości.
    y_true (array-like): Rzeczywiste wartości.
    bins (int): Liczba przedziałów histogramu (domyślnie 40).
    """
    # Obliczenie procentowych błędów
    percentage_errors = ((y_true - y_pred) / y_true) * 100

    # Tworzenie histogramu
    plt.figure(figsize=(12, 6))
    counts, edges, patches = plt.hist(percentage_errors, bins=bins, edgecolor='black', color='blue', alpha=0.7)
    plt.title("Histogram procentowych błędów przewidywań", fontsize=16)
    plt.xlabel("Procentowy błąd przewidywań (%)", fontsize=14)
    plt.ylabel("Liczba wystąpień", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Dodanie liczby wystąpień nad każdym słupkiem
    for count, edge in zip(counts, edges[:-1]):
        plt.text(edge + (edges[1] - edges[0]) / 2, count, f"{int(count)}", 
                 ha='center', va='bottom', fontsize=9)

    # Dostosowanie osi X
    x_ticks = np.arange(edges[0], edges[-1], 10)  # Co 10 jednostek kreska
    x_labels = np.arange(edges[0], edges[-1], 50)  # Co 50 jednostek wartość
    plt.xticks(x_ticks, [str(int(x)) if x in x_labels else '' for x in x_ticks])

    plt.show()


def real_vs_predicted_prices(y_pred, y_test):
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    plt.xlabel('Rzeczywiste ceny')
    plt.ylabel('Przewidywane ceny')
    plt.title('Rzeczywiste vs. Przewidywane ceny')
    plt.show()
    
def feature_importances(X, model):
    importances = model.feature_importances_
    features = X.columns
    indices = np.argsort(importances)[-10:]

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(indices)), importances[indices], align='center')
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Ważność cechy')
    plt.title('Wykres ważności cech')
    plt.show()
    
def plot_categorical_boxplots(data):
    plt.figure(figsize=(15, 5))

    # Boxplot dla cechy `fuel_type`
    plt.subplot(1, 3, 1)
    sns.boxplot(x='fuel_type', y='price', data=data)
    plt.title('Cena w zależności od typu paliwa')
    plt.xlabel('Typ paliwa')
    plt.ylabel('Cena')
    plt.xticks(rotation=75)

    # Boxplot dla cechy `gearbox`
    plt.subplot(1, 3, 2)
    sns.boxplot(x='gearbox', y='price', data=data)
    plt.title('Cena w zależności od skrzyni biegów')
    plt.xlabel('Skrzynia biegów')
    plt.ylabel('')
    plt.xticks(rotation=75)

    # Boxplot dla cechy `model`
    plt.subplot(1, 3, 3)
    sns.boxplot(x='model', y='price', data=data)
    plt.title('Cena w zależności od modelu')
    plt.xlabel('Model')
    plt.ylabel('')
    plt.xticks(rotation=75)

    plt.tight_layout()
    plt.show()
    
def plot_shap(model, X_test):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    # Globalna ważność cech
    shap.summary_plot(shap_values, X_test, plot_type="bar")
    

def create_interactive_histogram_with_details(y_pred, y_true, urls, bins=40):
    """
    Tworzy interaktywny histogram różnic procentowych z przewijanymi szczegółami (cena faktyczna, przewidywana i URL).

    Parametry:
    y_pred (array-like): Przewidywane wartości.
    y_true (array-like): Rzeczywiste wartości.
    urls (array-like): Lista URL-i powiązanych z danymi.
    bins (int): Liczba przedziałów histogramu (domyślnie 40).
    """
    # Obliczenie różnic procentowych
    percentage_errors = ((y_true - y_pred) / y_true) * 100

    # Tworzenie DataFrame do analizy
    data = pd.DataFrame({
        "percentage_error": percentage_errors,
        "actual_price": y_true,
        "predicted_price": y_pred,
        "url": urls
    })

    # Dodanie kolumny bin (przedziałów histogramu)
    data["bin"] = pd.cut(data["percentage_error"], bins=bins)

    # Grupowanie danych i przygotowanie szczegółów do hover
    def format_hover_details(group):
        return "<br>".join([
            f"Cena faktyczna: {row['actual_price']:.2f}, Cena przewidywana: {row['predicted_price']:.2f}, "
            f"<a href='{row['url']}' target='_blank'>URL</a>"
            for _, row in group.iterrows()
        ])

    grouped_data = data.groupby("bin").apply(format_hover_details).reset_index(name="details")

    # Tworzenie histogramu
    fig = px.histogram(
        data,
        x="percentage_error",
        nbins=bins,
        title="Interaktywny histogram różnic procentowych",
        labels={"percentage_error": "Procentowy błąd przewidywań (%)"},
        opacity=0.7
    )

    # Dodanie szczegółowych informacji do hover
    fig.update_traces(
        hovertemplate="<b>Przedział: %{x}</b><br><b>Szczegóły:</b><br><div style='max-height:150px;overflow-y:auto;'>%{customdata}</div><extra></extra>",
        customdata=grouped_data["details"]
    )

    # Stylizacja wykresu
    fig.update_layout(
        xaxis_title="Procentowy błąd przewidywań (%)",
        yaxis_title="Liczba wystąpień",
        bargap=0.1
    )

    # Wyświetlenie wykresu
    fig.show()



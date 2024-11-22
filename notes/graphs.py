import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
    
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
    
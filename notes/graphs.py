import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import shap

def residuals_hist(y_pred, y_test):
    residuals = y_test - y_pred
    plt.hist(residuals, bins=20, edgecolor='k')
    plt.xlabel('Reszty')
    plt.ylabel('Liczba wystąpień')
    plt.title('Histogram reszt')
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
    

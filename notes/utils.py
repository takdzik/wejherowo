import pandas as pd
import json
from pathlib import Path

def save_to_json(y_pred, y_true, urls, path="../data/interactive_data.json"):
    """
    Zapisuje dane do pliku JSON w formacie 'lines', wykorzystując json.dumps.

    Parametry:
    y_pred (array-like): Przewidywane wartości.
    y_true (array-like): Rzeczywiste wartości.
    urls (array-like): URL-e powiązane z danymi.
    path (str or Path): Ścieżka do pliku wyjściowego.
    """
    # Tworzenie DataFrame
    data = pd.DataFrame({
        "y_pred": y_pred,
        "y_true": y_true,
        "url": urls
    })

    # Tworzenie folderu, jeśli nie istnieje
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Zapis do pliku JSON w formacie 'lines'
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in data.to_dict(orient='records'):
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"Dane zostały zapisane do {output_path}")

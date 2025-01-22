import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np
import os

# Ścieżka do bieżącego pliku
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

# Wczytanie ofert z pliku JSON
def load_offers(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Funkcja do sortowania ofert
def sort_offers(offers, criterion, ascending):
    return sorted(
        offers,
        key=lambda x: x.get("evaluations", {}).get(criterion["category"], {}).get(criterion["subcategory"], 0),
        reverse=not ascending
    )

# Funkcja do renderowania wykresu
def render_evaluation_chart(evaluations):
    if not evaluations:
        return None

    labels = list(evaluations.keys())
    scores = [max(evaluations[cat].values()) for cat in labels]

    fig, ax = plt.subplots(figsize=(7.5, 3))  # Zwiększono rozmiar wykresu o 150%
    bars = ax.barh(labels, scores, color="skyblue", edgecolor="black")
    ax.set_xlim(0, 1)
    ax.set_title("Oceny dla kategorii")
    ax.set_xlabel("Prawdopodobieństwo")
    for bar in bars:
        ax.text(
            bar.get_width() + 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width():.2f}",
            va="center"
        )
    st.pyplot(fig)

# Funkcja do renderowania aplikacji Streamlit
def render_app():
    st.title("Car Offers Listing")

    # Ładowanie danych
    json_path = current_dir + "/../data/all_offers_with_scores.json"
    offers = load_offers(json_path)

    # Opcje sortowania
    st.sidebar.header("Opcje sortowania")
    categories = {
        "sprzedaz_pilna": ["Sprzedaż jest pilna", "Sprzedaż nie jest pilna"],
        "negocjacje_ceny": ["Cena podlega dużej negocjacji", "Cena podlega małej negocjacji", "Cena nie podlega negocjacji"],
        "nastawienie_na_zysk": ["Sprzedający nastawiony na zysk", "Sprzedający nie nastawiony na zysk"],
        "ukryte_wady": ["Auto może zawierać ukryte wady", "Auto nie zawiera ukrytych wad"]
    }

    category = st.sidebar.selectbox("Wybierz kategorię", list(categories.keys()), format_func=lambda x: x.replace("_", " ").capitalize())
    subcategory = st.sidebar.selectbox("Wybierz podkategorię", categories[category])
    ascending = st.sidebar.radio("Kolejność sortowania", ("Rosnąco", "Malejąco")) == "Rosnąco"
    num_offers = st.sidebar.slider("Liczba ofert do wyświetlenia", min_value=1, max_value=50, value=10)

    # Dodanie przycisku odświeżania
    if st.sidebar.button("Odśwież"):
        st.experimental_rerun()

    # Sortowanie ofert
    sorted_offers = sort_offers(offers, {"category": category, "subcategory": subcategory}, ascending)[:num_offers]

    # Wyświetlanie ofert w kafelkach
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")  # Kolumny szerokości 1/3 strony
    cols = [col1, col2, col3]

    for idx, offer in enumerate(sorted_offers):
        col = cols[idx % 3]
        with col:
            st.container()
            st.subheader(f"{offer['marka']} {offer['model']} ({offer['rok_produkcji']})")
            st.write(f"**Cena:** {offer['cena']} {offer['waluta']}")
            st.write(f"[Zobacz ogłoszenie]({offer['url']})")

            # Wyświetlanie zdjęcia 2x2
            if "zdjecia" in offer and len(offer["zdjecia"]) > 0:
                st.markdown("<div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 5px;'>", unsafe_allow_html=True)
                for img_url in offer["zdjecia"][:4]:
                    st.image(img_url, use_column_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Scrollowany opis
            st.markdown(
                f"<div style='max-height:100px;overflow-y:scroll;border:1px solid #ddd;padding:5px;border-radius:5px;'>{offer['opis'][0]}</div>",
                unsafe_allow_html=True,
            )

            # Wykres ocen
            st.write("**Oceny:**")
            render_evaluation_chart(offer.get("evaluations", {}))

# Uruchom aplikację Streamlit
if __name__ == "__main__":
    render_app()

import streamlit as st
import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os

st.set_page_config(layout="wide")  # Ustawienie pełnej szerokości strony

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

# Funkcja do renderowania wykresu Nightingale chart
def render_evaluation_chart(evaluations):
    if not evaluations:
        return None

    categories = list(evaluations.keys())
    max_scores = [max(evaluations[cat].values()) for cat in categories]

    # Radar chart setup
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    max_scores += max_scores[:1]  # Close the loop for radar chart
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
    ax.fill(angles, max_scores, color='skyblue', alpha=0.4)
    ax.plot(angles, max_scores, color='blue', linewidth=2)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=10)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_title("Radar Chart - Maksymalne wartości dla kategorii", fontsize=14, pad=20)

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
    ascending = st.sidebar.radio("Kolejność sortowania", ("Rosnąco", "Malejąco"), index=1) == "Rosnąco"  # Domyślnie malejąco
    num_offers = st.sidebar.slider("Liczba ofert do wyświetlenia", min_value=1, max_value=50, value=10)

    # Dodanie przycisku odświeżania
    if st.sidebar.button("Odśwież"):
        st.experimental_rerun()

    # Sortowanie ofert
    sorted_offers = sort_offers(offers, {"category": category, "subcategory": subcategory}, ascending)[:num_offers]

    # Wyświetlanie ofert w kafelkach
    col1, col2 = st.columns([1, 1], gap="medium")  # Dwie kolumny zajmujące całą szerokość strony  # Dwie kolumny szerokości 3/4 strony
    cols = [col1, col2]

    for idx, offer in enumerate(sorted_offers):
        col = cols[idx % 2]
        with col:
            st.container()
            st.subheader(f"{offer['marka']} {offer['model']} ({offer['rok_produkcji']})")
            st.write(f"**Cena:** {offer['cena']} {offer['waluta']}")
            st.write(f"[Zobacz ogłoszenie]({offer['url']})")

            # Wyświetlanie zdjęcia 2x2
            if "zdjecia" in offer and len(offer["zdjecia"]) > 0:
                st.markdown(
                    """
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px;'>
                    """,
                    unsafe_allow_html=True
                )
                for img_url in offer["zdjecia"][:2]:
                    st.markdown(
                        f"<div style='width: 100%; height: 150px; overflow: hidden; border: 1px solid #ddd; border-radius: 5px;'>"
                        f"<img src='{img_url}' style='width: 100%; height: 100%; object-fit: cover;'>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                st.markdown("</div>", unsafe_allow_html=True)



            # Wykres ocen
            st.write("**Oceny:**")
            render_evaluation_chart(offer.get("evaluations", {}))

            # Scrollowany opis
            st.markdown(
                f"<div style='max-height:150px;overflow-y:scroll;border:1px solid #ddd;padding:10px;border-radius:5px;'>{offer['opis'][0]}</div>",
                unsafe_allow_html=True,
            )

# Uruchom aplikację Streamlit
if __name__ == "__main__":
    render_app()

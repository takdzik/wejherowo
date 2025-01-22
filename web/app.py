import json
from lightning.app import LightningApp, LightningFlow
from lightning.app.frontend import StreamlitFrontend
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class CarOffersFlow(LightningFlow):
    def __init__(self, json_path):
        super().__init__()
        self.json_path = json_path
        self.offers = self.load_offers()

    def load_offers(self):
        """Wczytaj oferty z pliku JSON."""
        with open(self.json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def sort_offers(self, offers, criterion):
        """Sortuj oferty według wybranego kryterium."""
        return sorted(offers, key=lambda x: x['evaluations'].get(criterion, {}).get(criterion, 0), reverse=True)

    def configure_frontend(self):
        return StreamlitFrontend(render_fn=self.render)

    def render(self):
        st.title("Car Offers Listing")

        # Sortowanie i wybór kryteriów
        st.sidebar.header("Opcje sortowania")
        criteria = {
            "sprzedaz_pilna": "Sprzedaż jest pilna",
            "negocjacje_ceny": "Cena podlega dużej negocjacji",
            "nastawienie_na_zysk": "Sprzedający nastawiony na zysk",
            "ukryte_wady": "Auto może zawierać ukryte wady"
        }
        sort_criterion = st.sidebar.selectbox("Sortuj według", list(criteria.keys()), format_func=lambda x: criteria[x])
        num_offers = st.sidebar.slider("Liczba ofert do wyświetlenia", min_value=1, max_value=50, value=10)

        sorted_offers = self.sort_offers(self.offers, sort_criterion)[:num_offers]

        # Wyświetlanie ofert
        for offer in sorted_offers:
            st.subheader(f"{offer['marka']} {offer['model']} ({offer['rok_produkcji']})")
            st.write(f"**Cena:** {offer['cena']} {offer['waluta']}")
            st.write(f"**Opis:** {offer['opis'][0]}")
            st.write(f"[Zobacz ogłoszenie]({offer['url']})")

            # Wyświetlanie wykresu dla kategorii
            st.write("**Wykres oceny kategorii:**")
            evaluations = offer.get("evaluations", {})
            if evaluations:
                labels = list(evaluations.keys())
                scores = [max(evaluations[cat].values()) for cat in labels]

                fig, ax = plt.subplots()
                ax.bar(labels, scores, color="skyblue")
                ax.set_ylabel("Prawdopodobieństwo")
                ax.set_title("Oceny dla kategorii")
                st.pyplot(fig)

            # Wyświetlanie zdjęć
            if "zdjecia" in offer:
                st.write("**Zdjęcia:**")
                for img_url in offer["zdjecia"]:
                    st.image(img_url, width=150)

# Ścieżka do pliku JSON
json_path = "../data/all_offers_with_scores.json"

# Inicjalizacja aplikacji
app = LightningApp(CarOffersFlow(json_path))

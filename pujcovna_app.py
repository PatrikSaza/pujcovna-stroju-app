import streamlit as st
import sqlite3
import pandas as pd

# Připojení k databázi
conn = sqlite3.connect("pujcovna.db")

# Načtení klientů a strojů
clients = pd.read_sql_query("SELECT * FROM clients", conn)
machines = pd.read_sql_query("SELECT * FROM machines", conn)

st.title("Půjčovna strojů 🏗️")

st.header("Výběr klienta a stroje")
client_name = st.selectbox("Vyber klienta", clients["Firma"].tolist())
client = clients[clients["Firma"] == client_name].iloc[0]

machine_name = st.selectbox("Vyber stroj", machines["Nazev"].tolist())
machine = machines[machines["Nazev"] == machine_name].iloc[0]

st.write("**Popis stroje:**", machine["Popis"])
st.write("**Cena za den:**", f'{machine["Cena_za_den"]} Kč')
st.write("**Dostupnost:**", machine["Dostupnost"])

# Počet dní a kusů
days = st.number_input("Počet dní", min_value=1, value=1)
quantity = st.number_input("Počet kusů", min_value=1, value=1)

# Výpočet ceny
if machine["Dostupnost"].lower() != "ano":
    total_price = "Nedostupné"
else:
    total_price = machine["Cena_za_den"] * days * quantity * (1 - client["Sleva"])

st.subheader("Výpočet půjčovného")
st.write("**Celková cena:**", total_price)

import streamlit as st
import sqlite3
import pandas as pd
import os
import random

DB_FILE = "pujcovna.db"

# --- Funkce pro vytvoření databáze ---
def create_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Tabulka klientů
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            name TEXT,
            address TEXT,
            ico INTEGER,
            discount REAL,
            contact TEXT
        )
    ''')

    # Tabulka strojů
    c.execute('''
        CREATE TABLE IF NOT EXISTS machines (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            price_per_day REAL,
            available TEXT
        )
    ''')

    # Přidej náhodné klienty
    cities = ["Praha", "Brno", "Ostrava", "Plzeň", "Liberec"]
    streets = ["Masarykova", "Hlavní", "Komenského", "Nádražní", "Školní"]
    company_types = ["s.r.o.", "a.s.", "v.o.s."]
    for i in range(1, 101):
        client_id = f"K{i:03d}"
        name = f"{random.choice(['Stavex','BuildPro','Cementix','BetonServis'])} {random.choice(company_types)}"
        address = f"{random.choice(streets)} {random.randint(1,200)}, {random.choice(cities)}"
        ico = random.randint(10000000, 99999999)
        discount = round(random.randint(0,15)/100,2)
        contact = f"{random.choice(['Jan','Petr','Eva','Lucie','Martin'])} {random.choice(['Novák','Svoboda','Dvořák'])}"
        c.execute("INSERT OR IGNORE INTO clients VALUES (?,?,?,?,?,?)",
                  (client_id, name, address, ico, discount, contact))

    # Přidej stroje
    machine_names = ["Míchačka", "Vrtačka", "Lešení", "Pila", "Bagr", "Jeřáb", "Valec", "Bruska", "Fukar", "Kompresor"]
    machine_descriptions = ["malá", "střední", "velká", "profesionální", "přenosná"]
    for i, name in enumerate(machine_names, 1):
        machine_id = f"S{i:03d}"
        description = f"{name} {random.choice(machine_descriptions)}"
        price = random.randint(100,1000)
        available = random.choice(["Ano","Ne"])
        c.execute("INSERT OR IGNORE INTO machines VALUES (?,?,?,?,?)",
                  (machine_id, name, description, price, available))

    conn.commit()
    conn.close()

# --- Vytvoření DB pokud neexistuje ---
if not os.path.exists(DB_FILE):
    create_db()

# --- Připojení k DB ---
conn = sqlite3.connect(DB_FILE)
clients = pd.read_sql_query("SELECT * FROM clients", conn)
machines = pd.read_sql_query("SELECT * FROM machines", conn)

# --- Streamlit UI ---
st.title("Půjčovna strojů")

st.header("Výběr klienta a stroje")
client_name = st.selectbox("Vyber klienta", clients['name'])
machine_name = st.selectbox("Vyber stroj", machines['name'])

num_days = st.number_input("Počet dní", min_value=1, value=1)
num_units = st.number_input("Počet kusů", min_value=1, value=1)

# Načtení ceny a slevy
machine_row = machines[machines['name'] == machine_name].iloc[0]
client_row = clients[clients['name'] == client_name].iloc[0]

price_per_day = machine_row['price_per_day']
discount = client_row['discount']
available = machine_row['available']

if available == "Ne":
    st.warning("Tento stroj není dostupný.")
    total_price = 0
else:
    total_price = price_per_day * num_days * num_units * (1 - discount)
    st.success(f"Celková cena půjčovného: {total_price:.2f} Kč")

st.write("---")
st.subheader("Informace o klientovi a stroji")
st.write(client_row)
st.write(machine_row)

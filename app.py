import streamlit as st
from mongo_db import connect_mongo

# Connexion MongoDB
collection = connect_mongo()

st.set_page_config(page_title="Projet NoSQL", layout="wide")
st.title("Projet NoSQL - Films Database")

menu = st.sidebar.radio(
    "Navigation",
    [
        "MongoDB - Questions 1 à 6",
        "MongoDB - Questions 7 à 13",
        "Neo4j - Questions 14 à 20",
        "Neo4j - Questions 21 à 26",
        "Questions transversales"
    ]
)

if menu == "MongoDB - Questions 1 à 6":
    st.header("MongoDB — Requêtes de base")
    st.subheader("Q1 — Année avec le plus de films")
    st.info("À venir...")
    st.subheader("Q2 — Nombre de films après 1999")
    st.info("À venir...")
    st.subheader("Q3 — Moyenne des votes en 2007")
    st.info("À venir...")
    st.subheader("Q4 — Histogramme films par année")
    st.info("À venir...")
    st.subheader("Q5 — Genres disponibles")
    st.info("À venir...")
    st.subheader("Q6 — Film avec le plus de revenus")
    st.info("À venir...")

elif menu == "MongoDB - Questions 7 à 13":
    st.header("MongoDB — Requêtes avancées")
    st.info("À venir...")

elif menu == "Neo4j - Questions 14 à 20":
    st.header("Neo4j — Requêtes de base")
    st.info("À venir...")

elif menu == "Neo4j - Questions 21 à 26":
    st.header("Neo4j — Requêtes avancées")
    st.info("À venir...")

elif menu == "Questions transversales":
    st.header("Questions transversales")
    st.info("À venir...")
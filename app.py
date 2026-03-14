import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from queries_mongo import (
    q1_annee_plus_de_films,
    q2_films_apres_1999,
    q3_moyenne_votes_2007,
    q4_films_par_annee,
    q5_genres_disponibles,
    q5_nombre_films_par_genre,
    q6_film_plus_revenu,
    q7_realisateurs_plus_5_films,
    q8_genre_plus_revenu_moyen,
    q9_top_films_par_decennie
)

st.set_page_config(page_title="Projet NoSQL", layout="wide")

st.title("Projet NoSQL - Films Database")

menu = st.sidebar.radio(
    "Navigation",
    [
        "MongoDB - Questions 1 à 5",
        "MongoDB - Questions 6 à 13",
        "Neo4j - Questions 14 à 20",
        "Neo4j - Questions 21 à 26",
        "Questions transversales"
    ]
)

# ===============================
# MongoDB Questions 1 à 5
# ===============================

if menu == "MongoDB - Questions 1 à 5":

    st.header("MongoDB — Requêtes de base")

    # Q1
    st.subheader("Q1 — Année avec le plus de films")

    res = q1_annee_plus_de_films()

    st.success(f"Année : {res['_id']} avec {res['nombre']} films")

    # Q2
    st.subheader("Q2 — Nombre de films après 1999")

    res = q2_films_apres_1999()

    st.success(f"Nombre de films après 1999 : {res}")

    # Q3
    st.subheader("Q3 — Moyenne des votes en 2007")

    res = q3_moyenne_votes_2007()

    st.success(f"Moyenne des votes : {round(res,2)}")

    # ===============================
    # Q4 Histogramme
    # ===============================

    st.subheader("Q4 — Histogramme films par année")

    data = q4_films_par_annee()

    df = pd.DataFrame(data)

    df = df.rename(columns={
        "_id": "Année",
        "nombreFilms": "Nombre de films"
    })

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(df["Année"], df["Nombre de films"])

    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de films")
    ax.set_title("Nombre de films par année")

    plt.tight_layout()

    st.pyplot(fig)

    # ===============================
    # Q5 Genres
    # ===============================

    st.subheader("Q5 — Genres disponibles")

    genres = q5_genres_disponibles()

    # Tableau des genres
    st.write("### Tableau des genres")

    df_genres = pd.DataFrame(genres, columns=["Genres disponibles"])

    st.dataframe(df_genres)

    # Nombre total genres
    st.write(f"Nombre total de genres : {len(genres)}")

    # ===============================
    # Graphique horizontal
    # ===============================

    st.write("### Nombre de films par genre")

    data_genre = q5_nombre_films_par_genre()

    df_genre_films = pd.DataFrame(data_genre)

    df_genre_films = df_genre_films.rename(columns={
        "_id": "Genre",
        "nombreFilms": "Nombre de films"
    })

    fig2, ax2 = plt.subplots(figsize=(10,8))

    ax2.barh(df_genre_films["Genre"], df_genre_films["Nombre de films"])

    ax2.set_xlabel("Nombre de films")
    ax2.set_ylabel("Genre")
    ax2.set_title("Nombre de films par genre")

    plt.tight_layout()

    st.pyplot(fig2)

# ===============================
# MongoDB Questions 6 à 13
# ===============================

elif menu == "MongoDB - Questions 6 à 13":

    st.header("MongoDB — Requêtes avancées")
#question 6 
    st.subheader("Q6 — Film avec le plus de revenu")

    film = q6_film_plus_revenu()

    st.success(
        f"{film['title']} — Revenue : {film['Revenue (Millions)']} millions"
    )
#question 7 

    st.subheader("Q7 — Réalisateurs ayant réalisé plus de 5 films")

    realisateurs = q7_realisateurs_plus_5_films()

    if realisateurs:
        df = pd.DataFrame(realisateurs)

        df = df.rename(columns={
            "_id": "Réalisateur",
            "nombreFilms": "Nombre de films"
        })

        st.dataframe(df)

    else:
        st.warning("Aucun réalisateur avec plus de 5 films dans la base.")
    
    #question 8 
    
        st.subheader("Q8 — Genre avec revenu moyen le plus élevé")

    genre = q8_genre_plus_revenu_moyen()

    st.success(
        f"Genre : {genre['_id']} — Revenu moyen : {round(genre['avgRevenue'],2)} millions"
    )
    
    #question 9 
    
    st.subheader("Q9 — Top 3 films par décennie")

    data = q9_top_films_par_decennie()

    df = pd.DataFrame(data)

    df = df.rename(columns={
        "_id": "Décennie",
        "topFilms": "Top films"
    })

    st.dataframe(df)
    
    

# ===============================
# Neo4j
# ===============================

elif menu == "Neo4j - Questions 14 à 20":

    st.header("Neo4j — Requêtes de base")

    st.info("À venir...")


elif menu == "Neo4j - Questions 21 à 26":

    st.header("Neo4j — Requêtes avancées")

    st.info("À venir...")


elif menu == "Questions transversales":

    st.header("Questions transversales")

    st.info("À venir...")
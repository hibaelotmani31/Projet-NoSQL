import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    q9_top_films_par_decennie,
    q10_film_plus_long_par_genre,
    q11_vue_films_top,
    q12_correlation_runtime_revenue,
    q13_duree_moyenne_par_decennie
)

from queries_neo4j import (
    q14_acteur_plus_films,
    q15_acteurs_avec_anne_hathaway,
    q16_acteur_plus_revenus,
    q17_moyenne_votes,
    q19_films_coacteurs,
    q20_realisateur_plus_acteurs,
    q21_films_plus_connectes,
    q22_acteurs_plus_realisateurs
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

    st.subheader("Q1 — Année avec le plus de films")
    res = q1_annee_plus_de_films()
    st.success(f"Année : {res['_id']} avec {res['nombre']} films")

    st.subheader("Q2 — Nombre de films après 1999")
    res = q2_films_apres_1999()
    st.success(f"Nombre de films après 1999 : {res}")

    st.subheader("Q3 — Moyenne des votes en 2007")
    res = q3_moyenne_votes_2007()
    st.success(f"Moyenne des votes : {round(res,2)}")

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

    st.pyplot(fig)

    st.subheader("Q5 — Genres disponibles")

    genres = q5_genres_disponibles()

    df_genres = pd.DataFrame(genres, columns=["Genres disponibles"])
    st.dataframe(df_genres)

    st.write(f"Nombre total de genres : {len(genres)}")

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

    st.pyplot(fig2)

# ===============================
# MongoDB Questions 6 à 13
# ===============================

elif menu == "MongoDB - Questions 6 à 13":

    st.header("MongoDB — Requêtes avancées")

    st.subheader("Q6 — Film avec le plus de revenu")
    film = q6_film_plus_revenu()
    st.success(f"{film['title']} — Revenue : {film['Revenue (Millions)']} millions")

    st.subheader("Q7 — Réalisateurs ayant réalisé plus de 5 films")
    realisateurs = q7_realisateurs_plus_5_films()

    if realisateurs:
        df = pd.DataFrame(realisateurs)

        df = df.rename(columns={
            "_id": "Réalisateur",
            "nombreFilms": "Nombre de films"
        })

        st.dataframe(df)

    st.subheader("Q8 — Genre avec revenu moyen le plus élevé")

    genre = q8_genre_plus_revenu_moyen()

    st.success(
        f"Genre : {genre['_id']} — Revenu moyen : {round(genre['avgRevenue'],2)} millions"
    )

    st.subheader("Q9 — Top 3 films par décennie")

    data = q9_top_films_par_decennie()
    df = pd.DataFrame(data)

    df = df.rename(columns={
        "_id": "Décennie",
        "topFilms": "Top films"
    })

    st.dataframe(df)

    st.subheader("Q10 — Film le plus long par genre")
    data = q10_film_plus_long_par_genre()
    df = pd.DataFrame(data)

    df = df.rename(columns={
        "_id": "Genre",
        "film": "Film",
        "duree": "Durée (min)"
    })

    st.dataframe(df)

    st.subheader("Q11 — Films avec Metascore > 80 et Revenue > 50M")
    data = q11_vue_films_top()
    df = pd.DataFrame(data)
    st.dataframe(df)

    st.subheader("Q12 — Corrélation durée / revenus")

    resultat = q12_correlation_runtime_revenue()

    df_corr = resultat["df"]
    correlation = resultat["correlation"]
    p_value = resultat["p_value"]

    st.metric("Coefficient de corrélation", correlation)
    st.metric("P-value", p_value)

    fig, ax = plt.subplots()

    ax.scatter(
        df_corr["Runtime (Minutes)"],
        df_corr["Revenue (Millions)"]
    )

    ax.set_xlabel("Durée")
    ax.set_ylabel("Revenue")

    st.pyplot(fig)

    st.subheader("Q13 — Durée moyenne par décennie")

    data = q13_duree_moyenne_par_decennie()
    df = pd.DataFrame(data)

    df = df.rename(columns={
        "_id": "Décennie",
        "dureeMoyenne": "Durée moyenne"
    })

    st.dataframe(df)

# ===============================
# Neo4j Questions 14 à 20
# ===============================

elif menu == "Neo4j - Questions 14 à 20":

    st.header("Neo4j — Requêtes de base")

    st.subheader("Q14 — Acteur ayant joué dans le plus grand nombre de films")

    res = q14_acteur_plus_films()

    st.success(
        f"Acteur : {res['acteur']} — Nombre de films : {res['nombreFilms']}"
    )

    st.subheader("Q15 — Acteurs ayant joué avec Anne Hathaway")

    acteurs = q15_acteurs_avec_anne_hathaway()

    df = pd.DataFrame(acteurs, columns=["Acteurs"])

    st.dataframe(df)

    st.subheader("Q16 — Acteur ayant généré le plus de revenus")

    res = q16_acteur_plus_revenus()

    st.success(
        f"Acteur : {res['acteur']} — Revenus : {round(res['totalRevenue'],2)} millions"
    )

    st.subheader("Q17 — Moyenne des votes")

    moyenne = q17_moyenne_votes()

    st.success(
        f"Moyenne des votes : {round(moyenne,2)}"
    )

    st.subheader("Q19 — Films dans lesquels les co-acteurs de Matt Damon ont joué")

    films = q19_films_coacteurs()

    df = pd.DataFrame(films, columns=["Films"])

    st.dataframe(df)

    st.subheader("Q20 — Réalisateur ayant travaillé avec le plus d’acteurs")

    res = q20_realisateur_plus_acteurs()

    st.success(
        f"Réalisateur : {res['realisateur']} — Nombre d'acteurs : {res['nombreActeurs']}"
    )

# ===============================
# Neo4j Questions 21 à 26
# ===============================

elif menu == "Neo4j - Questions 21 à 26":

    st.header("Neo4j — Requêtes avancées")

    st.subheader("Q21 — Films les plus connectés")

    data = q21_films_plus_connectes()

    df = pd.DataFrame(data)

    df = df.rename(columns={
        "film": "Film",
        "connexions": "Connexions"
    })

    st.dataframe(df)

    st.subheader("Q22 — Acteurs ayant travaillé avec le plus de réalisateurs")

    data = q22_acteurs_plus_realisateurs()

    df = pd.DataFrame(data)

    df = df.rename(columns={
        "acteur": "Acteur",
        "nombreRealisateurs": "Nombre de réalisateurs"
    })

    st.dataframe(df)

    st.info("Q23 à Q26 — À venir...")

# ===============================
# Questions transversales
# ===============================

elif menu == "Questions transversales":

    st.header("Questions transversales")

    st.info("À venir...")
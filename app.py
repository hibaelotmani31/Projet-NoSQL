import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['figure.facecolor'] = '#141414'
matplotlib.rcParams['axes.facecolor'] = '#1f1f1f'
matplotlib.rcParams['axes.edgecolor'] = '#333333'
matplotlib.rcParams['text.color'] = '#ffffff'
matplotlib.rcParams['axes.labelcolor'] = '#cccccc'
matplotlib.rcParams['xtick.color'] = '#cccccc'
matplotlib.rcParams['ytick.color'] = '#cccccc'
matplotlib.rcParams['grid.color'] = '#333333'

from queries_mongo import (
    q1_annee_plus_de_films,
    q2_films_apres_1999,
    q3_moyenne_votes_2007,
    q4_films_par_annee,
    q5_genres_disponibles,
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
    q18_genre_plus_represente,
    q19_films_coacteurs,
    q20_realisateur_plus_acteurs,
    q21_films_plus_connectes,
    q22_acteurs_plus_realisateurs,
    q23_recommander_film,
    q24_influence_par,
    q25_chemin_plus_court,
    q26_communautes_acteurs,
    q27_films_genres_communs_realisateurs_differents,
    q28_recommander_films_utilisateur,
    q29_concurrence_realisateurs,
    q30_collaborations_succes
)

# CONFIG & STYLE

st.set_page_config(
    page_title="CineBase",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap');

    .stApp { background-color: #0a0a0a; color: #e5e5e5; }
    header[data-testid="stHeader"] { background-color: #0a0a0a !important; border-bottom: 1px solid #1a1a1a !important; }
    section[data-testid="stSidebar"] { background-color: #111111; }
    #MainMenu, footer { visibility: hidden; }

    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 5rem;
        color: #e50914;
        letter-spacing: 4px;
        line-height: 1;
        margin: 0;
    }
    .hero-sub {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #808080;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 6px;
    }
    .metric-card {
        background: #141414;
        border: 1px solid #222222;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.8rem;
        color: #e50914;
        line-height: 1;
    }
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 6px;
    }
    .section-header {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.2rem;
        color: #ffffff;
        letter-spacing: 2px;
        border-left: 4px solid #e50914;
        padding-left: 16px;
        margin-bottom: 8px;
    }
    .section-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #555555;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 32px;
        padding-left: 20px;
    }
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        color: #e50914;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .stat-title {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #cccccc;
        margin-bottom: 14px;
    }
    .red-divider {
        height: 1px;
        background: linear-gradient(to right, #e50914, transparent);
        margin: 32px 0;
    }
    .stButton > button {
        background: #e50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        padding: 10px 24px !important;
    }
    .stButton > button:hover { background: #b00710 !important; }
    .stTextInput input {
        background: #1a1a1a !important;
        border: 1px solid #333333 !important;
        color: #e5e5e5 !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# SESSION STATE

if "page" not in st.session_state:
    st.session_state.page = "accueil"

def go_to(page):
    st.session_state.page = page
    st.rerun()

# ACCUEIL
#q1, q2, q17, q18
#affiche 102 filmss

if st.session_state.page == "accueil":

    st.markdown("""
    <div style="padding: 60px 0 40px 0;">
        <h1 class="hero-title">CineBase</h1>
        <p style="font-family:'Bebas Neue',sans-serif; color:#333; font-size:1.4rem; 
        letter-spacing:4px; margin-top:8px;">
        102 films. Des donnees. Des histoires.
        </p>
    </div>
    """, unsafe_allow_html=True)

    #métriques clés : q1, q2, q18,  q17
    q1  = q1_annee_plus_de_films()
    q2  = q2_films_apres_1999()
    q18 = q18_genre_plus_represente()
    q17 = q17_moyenne_votes()

    #les colonnes en haut
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-value">102</div><div class="metric-label">Films dans la base</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{q1["_id"]}</div><div class="metric-label">Annee la plus productive</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{q2}</div><div class="metric-label">Films apres 1999</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{q18["genre"]}</div><div class="metric-label">Genre dominant</div></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{round(q17/1000)}K</div><div class="metric-label">Votes en moyenne</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    st.markdown('<p style="font-family:Inter,sans-serif; font-size:0.75rem; color:#555; letter-spacing:3px; text-transform:uppercase; margin-bottom:20px;">Explorer par categorie</p>', unsafe_allow_html=True)

    #les colonness des categories
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div style="background:#141414; border:1px solid #222; border-radius:8px; padding:24px; margin-bottom:8px;"><div style="font-family:Bebas Neue,sans-serif; font-size:1.4rem; color:#fff; letter-spacing:2px;">Tendances</div><div style="font-family:Inter,sans-serif; font-size:0.78rem; color:#555; margin-top:6px;">Sorties, genres, evolution dans le temps</div></div>', unsafe_allow_html=True)
        if st.button("Explorer", key="b1", use_container_width=True):   #key=b1 pour chaque boutton / pour que streamlit differe
            go_to("stats")
    with c2:
        st.markdown('<div style="background:#141414; border:1px solid #222; border-radius:8px; padding:24px; margin-bottom:8px;"><div style="font-family:Bebas Neue,sans-serif; font-size:1.4rem; color:#fff; letter-spacing:2px;">Revenus</div><div style="font-family:Inter,sans-serif; font-size:0.78rem; color:#555; margin-top:6px;">Performances commerciales et critiques</div></div>', unsafe_allow_html=True)
        if st.button("Explorer", key="b2", use_container_width=True):
            go_to("revenus")
    with c3:
        st.markdown('<div style="background:#141414; border:1px solid #222; border-radius:8px; padding:24px; margin-bottom:8px;"><div style="font-family:Bebas Neue,sans-serif; font-size:1.4rem; color:#fff; letter-spacing:2px;">Acteurs</div><div style="font-family:Inter,sans-serif; font-size:0.78rem; color:#555; margin-top:6px;">Relations, collaborations et reseau</div></div>', unsafe_allow_html=True)
        if st.button("Explorer", key="b3", use_container_width=True):
            go_to("acteurs")
    with c4:
        st.markdown('<div style="background:#141414; border:1px solid #222; border-radius:8px; padding:24px; margin-bottom:8px;"><div style="font-family:Bebas Neue,sans-serif; font-size:1.4rem; color:#fff; letter-spacing:2px;">Recommandations</div><div style="font-family:Inter,sans-serif; font-size:0.78rem; color:#555; margin-top:6px;">Decouvrir de nouveaux films</div></div>', unsafe_allow_html=True)
        if st.button("Explorer", key="b4", use_container_width=True):  #-> le bouton prend toute la largeur de la colonne
            go_to("recommandations")

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-family:Inter,sans-serif; font-size:0.72rem; color:#333; text-align:center;">MongoDB Atlas — Neo4j AuraDB — Python 3.12 — Streamlit</p>', unsafe_allow_html=True)


# TENDANCES ET STATISTIQUES
#q1, q2, q3, q4, q5, q9, q12

elif st.session_state.page == "stats":

    if st.button("Retour", key="back_stats"):
        go_to("accueil")

    st.markdown('<div class="section-header">Tendances et statistiques</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Evolution, genres et analyse des sorties</div>', unsafe_allow_html=True)

    #métriques : q1 q3 et q2
    q1 = q1_annee_plus_de_films()
    q2 = q2_films_apres_1999()
    q3 = q3_moyenne_votes_2007()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{q1["_id"]}</div><div class="metric-label">Annee avec le plus de sorties ({q1["nombre"]} films)</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{q2}</div><div class="metric-label">Films sortis apres 1999</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{round(q3):,}</div><div class="metric-label">Votes moyens des films de 2007</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    # q4 - histogramme films par année
    st.markdown('<div class="stat-label">Distribution</div><div class="stat-title">Nombre de films par annee de sortie</div>', unsafe_allow_html=True)
    data = q4_films_par_annee()
    df = pd.DataFrame(data).rename(columns={"_id": "Annee", "nombreFilms": "Films"})
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(df["Annee"], df["Films"], color="#e50914", alpha=0.85, width=0.7)
    ax.set_xlabel("Annee", fontsize=9)
    ax.set_ylabel("Nombre de films", fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    # q5- genres disponibles
    st.markdown('<div class="stat-label">Catalogue</div><div class="stat-title">Genres disponibles dans la base</div>', unsafe_allow_html=True)
    genres = q5_genres_disponibles()
    st.info(f"{len(genres)} genres distincts identifies dans la base.")
    df_genres = pd.DataFrame(genres, columns=["Genre"])
    st.dataframe(df_genres, use_container_width=True, height=250)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    # q9- top 3 films par decennie
    st.markdown('<div class="stat-label">Par decennie</div><div class="stat-title">Top 3 films les mieux notes par decennie</div>', unsafe_allow_html=True)
    data = q9_top_films_par_decennie()
    df = pd.DataFrame(data).rename(columns={"_id": "Decennie", "topFilms": "Top 3 films"})
    st.dataframe(df, use_container_width=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q13 - evolution duree par decennie
    st.markdown('<div class="stat-label">Evolution</div><div class="stat-title">Duree moyenne des films par decennie</div>', unsafe_allow_html=True)
    data = q13_duree_moyenne_par_decennie()
    df = pd.DataFrame(data).rename(columns={"_id": "Decennie", "dureeMoyenne": "Duree moyenne (min)"})
    df["Duree moyenne (min)"] = df["Duree moyenne (min)"].round(1)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Decennie"], df["Duree moyenne (min)"], marker="o", color="#e50914", linewidth=2, markersize=8)
    for _, row in df.iterrows():
        ax.annotate(f"{row['Duree moyenne (min)']} min",
                    (row["Decennie"], row["Duree moyenne (min)"]),
                    textcoords="offset points", xytext=(0, 12),
                    ha="center", fontsize=8, color="#cccccc")
    ax.set_xlabel("Decennie", fontsize=9)
    ax.set_ylabel("Duree moyenne (min)", fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    # q12 - corrélation durée / revenus
    st.markdown('<div class="stat-label">Analyse statistique</div><div class="stat-title">Correlation entre la duree des films et leurs revenus</div>', unsafe_allow_html=True)
    resultat = q12_correlation_runtime_revenue()
    df_corr = resultat["df"]
    correlation = resultat["correlation"]
    p_value = resultat["p_value"]

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Coefficient de Pearson", correlation)
    with c2:
        st.metric("P-value", p_value)

    if correlation > 0.5:
        st.success("Correlation positive forte — les films longs rapportent davantage.")
    elif correlation > 0.2:
        st.info("Correlation positive faible — legere tendance observee.")
    elif correlation < -0.2:
        st.warning("Correlation negative — les films longs rapportent moins.")
    else:
        st.warning("Pas de correlation significative entre duree et revenus.")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(df_corr["Runtime (Minutes)"], df_corr["Revenue (Millions)"],
               alpha=0.7, color="#e50914", s=40)
    z = np.polyfit(df_corr["Runtime (Minutes)"], df_corr["Revenue (Millions)"], 1)
    p = np.poly1d(z)
    ax.plot(sorted(df_corr["Runtime (Minutes)"]),
            p(sorted(df_corr["Runtime (Minutes)"])),
            "--", color="#ffffff", alpha=0.4, label="Tendance")
    ax.set_xlabel("Duree (minutes)", fontsize=9)
    ax.set_ylabel("Revenus (millions $)", fontsize=9)
    ax.legend(fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)


# REVENUS ET POPULARITE
#q6, q7, q8, q10, q11

elif st.session_state.page == "revenus":

    if st.button("Retour", key="back_revenus"):
        go_to("accueil")

    st.markdown('<div class="section-header">Revenus et popularite</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Performances commerciales et notes critiques</div>', unsafe_allow_html=True)

    #métriques : q6 et q8
    film = q6_film_plus_revenu()
    genre = q8_genre_plus_revenu_moyen()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1.8rem;">{film["title"]}</div><div class="metric-label">Film le plus rentable — {film["Revenue (Millions)"]}M$</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{genre["_id"]}</div><div class="metric-label">Genre le plus rentable — {round(genre["avgRevenue"], 1)}M$ en moyenne</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    # q7 - realisateurs prolifiques
    st.markdown('<div class="stat-label">Realisateurs</div><div class="stat-title">Realisateurs ayant signe plus de 5 films</div>', unsafe_allow_html=True)
    realisateurs = q7_realisateurs_plus_5_films()
    if realisateurs:
        df = pd.DataFrame(realisateurs).rename(columns={"_id": "Realisateur", "nombreFilms": "Films"})
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Aucun realisateur n'a signe plus de 5 films dans cette base.")

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q10 - film le plus long par genre
    st.markdown('<div class="stat-label">Duree</div><div class="stat-title">Film le plus long par genre</div>', unsafe_allow_html=True)
    data = q10_film_plus_long_par_genre()
    df = pd.DataFrame(data).rename(columns={"_id": "Genre", "film": "Film", "duree": "Duree (min)"})
    st.dataframe(df, use_container_width=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q11 - vue films top
    st.markdown('<div class="stat-label">Selection</div><div class="stat-title">Films avec Metascore superieur a 80 et revenus superieurs a 50M</div>', unsafe_allow_html=True)
    st.caption("Selection issue d'une vue creee directement dans MongoDB sur la base entertainment.films")
    data = q11_vue_films_top()
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)


# ACTEURS ET REALISATEURS
#q14 à q22, q24, q26, q27, q29, q30


elif st.session_state.page == "acteurs":

    if st.button("Retour", key="back_acteurs"):
        go_to("accueil")

    st.markdown('<div class="section-header">Acteurs et realisateurs</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Relations, collaborations et analyse du reseau</div>', unsafe_allow_html=True)

    #métriques : q14,q16 , q20
    res14 = q14_acteur_plus_films()
    res16 = q16_acteur_plus_revenus()
    res20 = q20_realisateur_plus_acteurs()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1.6rem;">{res14["acteur"]}</div><div class="metric-label">Acteur le plus prolifique — {res14["nombreFilms"]} films</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1.6rem;">{res16["acteur"]}</div><div class="metric-label">Acteur le plus rentable — {round(res16["totalRevenue"])}M$</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1.6rem;">{res20["realisateur"]}</div><div class="metric-label">Realisateur avec le plus d\'acteurs — {res20["nombreActeurs"]}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q15, acteurs avec Anne Hathaway
    st.markdown('<div class="stat-label">Connexions</div><div class="stat-title">Acteurs ayant partage l\'affiche avec Anne Hathaway</div>', unsafe_allow_html=True)
    acteurs = q15_acteurs_avec_anne_hathaway()
    df = pd.DataFrame(acteurs, columns=["Acteur"])
    st.dataframe(df, use_container_width=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q19, co-acteurs de Matt Damon
    st.markdown('<div class="stat-label">Reseau</div><div class="stat-title">Films dans lesquels les co-acteurs de Matt Damon ont joue</div>', unsafe_allow_html=True)
    films = q19_films_coacteurs()
    df = pd.DataFrame(films, columns=["Film"])
    st.dataframe(df, use_container_width=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q21, films les plus connectés
    st.markdown('<div class="stat-label">Connectivite</div><div class="stat-title">Films partageant le plus d\'acteurs avec d\'autres films</div>', unsafe_allow_html=True)
    data = q21_films_plus_connectes()
    df = pd.DataFrame(data).rename(columns={"film": "Film", "connexions": "Films connectes"})
    st.dataframe(df, use_container_width=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q22 acteurs avec le plus de réalisateurs
    st.markdown('<div class="stat-label">Versatilite</div><div class="stat-title">Acteurs ayant travaille avec le plus de realisateurs differents</div>', unsafe_allow_html=True)
    data = q22_acteurs_plus_realisateurs()
    df = pd.DataFrame(data).rename(columns={"acteur": "Acteur", "nombreRealisateurs": "Realisateurs differents"})
    st.dataframe(df, use_container_width=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q26 communautés d'acteurs
    st.markdown('<div class="stat-label">Communautes</div><div class="stat-title">Groupes d\'acteurs travaillant regulierement ensemble</div>', unsafe_allow_html=True)
    st.caption("Detection par films communs — alternative a l'algorithme Louvain (Neo4j GDS non disponible sur AuraDB Free)")
    data = q26_communautes_acteurs()
    df = pd.DataFrame(data).rename(columns={
        "acteur1": "Acteur 1", "acteur2": "Acteur 2",
        "filmsCommuns": "Films en commun", "nbFilms": "Nb films"
    })
    st.dataframe(df, use_container_width=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q31 collaborations et succès
    st.markdown('<div class="stat-label">Collaborations</div><div class="stat-title">Duos realisateur-acteur les plus frequents et leur succes commercial</div>', unsafe_allow_html=True)
    data = q30_collaborations_succes()
    df = pd.DataFrame(data).rename(columns={
        "realisateur": "Realisateur", "acteur": "Acteur",
        "filmsEnsemble": "Films ensemble",
        "nbCollaborations": "Nb collaborations",
        "revenuMoyen": "Revenu moyen (M$)",
        "votesMoyen": "Votes moyen"
    })
    st.dataframe(df, use_container_width=True)
    st.info("Les collaborations frequentes sont generalement associees a un meilleur succes commercial.")

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q27, genres communs, réalisateurs différents
    st.markdown('<div class="stat-label">Comparaison</div><div class="stat-title">Films de genres similaires realises par des realisateurs differents</div>', unsafe_allow_html=True)
    data = q27_films_genres_communs_realisateurs_differents()
    df = pd.DataFrame(data).rename(columns={
        "film1": "Film 1", "film2": "Film 2",
        "realisateur1": "Realisateur 1", "realisateur2": "Realisateur 2",
        "genres1": "Genres 1", "genres2": "Genres 2"
    })
    st.dataframe(df, use_container_width=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q29 concurrence entre réalisateurs 
    st.markdown('<div class="stat-label">Concurrence</div><div class="stat-title">Realisateurs ayant sorti des films similaires la meme annee</div>', unsafe_allow_html=True)
    if st.button("Analyser la concurrence", key="btn_q29"):
        data = q29_concurrence_realisateurs()
        df = pd.DataFrame(data).rename(columns={
            "realisateur1": "Realisateur 1", "realisateur2": "Realisateur 2",
            "annee": "Annee", "film1": "Film 1", "film2": "Film 2"
        })
        st.dataframe(df, use_container_width=True)

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q24 INFLUENCE_PAR 
    st.markdown('<div class="stat-label">Influences</div><div class="stat-title">Realisateurs partageant des genres similaires</div>', unsafe_allow_html=True)
    if st.button("Analyser les influences", key="btn_q24"):
        data = q24_influence_par()
        df = pd.DataFrame(data).rename(columns={
            "realisateur1": "Realisateur 1",
            "realisateur2": "Realisateur 2",
            "genresCommuns": "Genres communs"
        })
        st.dataframe(df, use_container_width=True)


# RECOMMANDATIONS
#q23, q25,  q28

elif st.session_state.page == "recommandations":

    if st.button("Retour", key="back_reco"):
        go_to("accueil")

    st.markdown('<div class="section-header">Recommandations</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Decouvrir des films selon vos preferences</div>', unsafe_allow_html=True)

    #q23 - recommandation par genres favoris
    st.markdown('<div class="stat-label">Par acteur</div><div class="stat-title">Films recommandes selon les genres favoris d\'un acteur</div>', unsafe_allow_html=True)
    st.caption("Le systeme detecte automatiquement les genres les plus frequents dans la filmographie de l'acteur.")
    acteur = st.text_input("Entrez le nom d'un acteur", "Leonardo DiCaprio", key="q23_input")
    if st.button("Obtenir des recommandations", key="btn_q23"):
        recs = q23_recommander_film(acteur)
        if recs:
            df = pd.DataFrame(recs).rename(columns={"recommandation": "Film recommande", "genre": "Genre"})
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Aucune recommandation trouvee pour cet acteur.")

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q28 - recommandation triée par revenus
    st.markdown('<div class="stat-label">Selection commerciale</div><div class="stat-title">Films recommandes tries par succes commercial</div>', unsafe_allow_html=True)
    st.caption("Meme logique que ci-dessus, mais les recommandations sont triees par revenus decroissants.")
    acteur_q28 = st.text_input("Entrez le nom d'un acteur", "Leonardo DiCaprio", key="q28_input")
    if st.button("Voir les films les plus rentables du genre", key="btn_q28"):
        recs = q28_recommander_films_utilisateur(acteur_q28)
        if recs:
            df = pd.DataFrame(recs).rename(columns={
                "recommandation": "Film recommande", "genre": "Genre",
                "revenue": "Revenue (M$)", "votes": "Votes"
            })
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Aucune recommandation trouvee.")

    st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

    #q25 - chemin le plus court
    st.markdown('<div class="stat-label">Connexions</div><div class="stat-title">Chemin le plus court entre deux acteurs</div>', unsafe_allow_html=True)
    st.caption("Trouve la chaine de films reliant deux acteurs qui n'ont jamais joue ensemble.")
    c1, c2 = st.columns(2)
    with c1:
        acteur1 = st.text_input("Acteur 1", "Tom Hanks", key="q25_a1")
    with c2:
        acteur2 = st.text_input("Acteur 2", "Scarlett Johansson", key="q25_a2")
    if st.button("Trouver le chemin", key="btn_q25"):
        resultat = q25_chemin_plus_court(acteur1, acteur2)
        if resultat:
            st.success(f"Chemin de {resultat['longueur']} etapes.")
            st.write(" — ".join(resultat["chemin"]))
        else:
            st.warning("Aucun chemin trouve entre ces deux acteurs.")
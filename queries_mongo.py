from mongo_db import connect_mongo
import pandas as pd
from scipy import stats

collection = connect_mongo()


#q1 : année avec le plus de films
def q1_annee_plus_de_films():
    resultat = collection.aggregate([
        {"$group": {"_id": "$year", "nombre": {"$sum": 1}}},
        {"$sort": {"nombre": -1}},
        {"$limit": 1}
    ])
    return list(resultat)[0]


#q2 : nombre de films après 1999
def q2_films_apres_1999():
    return collection.count_documents({"year": {"$gt": 1999}})


#q3 : moyenne des votes en 2007
def q3_moyenne_votes_2007():
    resultat = collection.aggregate([
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "moyenneVotes": {"$avg": "$Votes"}}}
    ])
    return list(resultat)[0]["moyenneVotes"]


#q4 : nombre de films par année
def q4_films_par_annee():
    resultat = collection.aggregate([
        {"$group": {"_id": "$year", "nombreFilms": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ])
    return list(resultat)


#q5 : genres disponibles
def q5_genres_disponibles():
    resultat = collection.aggregate([
        {"$project": {"genres": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres"}},
        {"$sort": {"_id": 1}}
    ])
    return [g["_id"] for g in resultat]


#q5 : nombre de films par genre  //bonus
def q5_nombre_films_par_genre():
    resultat = collection.aggregate([
        {"$project": {"genres": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres", "nombreFilms": {"$sum": 1}}},
        {"$sort": {"nombreFilms": -1}}
    ])
    return list(resultat)

#q6 : film avec le plus de revenu
def q6_film_plus_revenu():
    resultat = collection.find(
        {"Revenue (Millions)": {"$ne": ""}}
    ).sort("Revenue (Millions)", -1).limit(1)

    return list(resultat)[0]

#q7 : réalisateurs ayant réalisé plus de 5 films
def q7_realisateurs_plus_5_films():
    resultat = collection.aggregate([
        {
            "$group": {
                "_id": "$Director",
                "nombreFilms": {"$sum": 1}
            }
        },
        {
            "$match": {"nombreFilms": {"$gt": 5}}
        },
        {
            "$sort": {"nombreFilms": -1}
        }
    ])
    return list(resultat)

#q8 : genre qui rapporte le plus en moyenne
def q8_genre_plus_revenu_moyen():
    resultat = collection.aggregate([
        {
            "$match": {
                "Revenue (Millions)": {"$ne": ""}
            }
        },
        {
            "$group": {
                "_id": "$genre",
                "avgRevenue": {"$avg": "$Revenue (Millions)"}
            }
        },
        {
            "$sort": {"avgRevenue": -1}
        },
        {
            "$limit": 1
        }
    ])
    return list(resultat)[0]

#q9 : 3 films les mieux notés par décennie
def q9_top_films_par_decennie():
    resultat = collection.aggregate([
        {
            "$match": {"year": {"$ne": None}}
        },
        {
            "$addFields": {
                "decade": {
                    "$multiply": [
                        {"$floor": {"$divide": ["$year", 10]}},
                        10
                    ]
                }
            }
        },
        {
            "$sort": {"Votes": -1}
        },
        {
            "$group": {
                "_id": "$decade",
                "topFilms": {"$push": "$title"}
            }
        },
        {
            "$project": {
                "topFilms": {"$slice": ["$topFilms", 3]}
            }
        }
    ])

    return list(resultat)


#q10 : Film le plus long par genre
def q10_film_plus_long_par_genre():
    resultat = collection.aggregate([
        {"$match": {"Runtime (Minutes)": {"$ne": ""}}},
        {"$project": {
            "title": 1,
            "Runtime (Minutes)": 1,
            "genres": {"$split": ["$genre", ","]}
        }},
        {"$unwind": "$genres"},
        {"$group": {
            "_id": "$genres",
            "film": {"$first": "$title"},
            "duree": {"$max": "$Runtime (Minutes)"}
        }},
        {"$sort": {"_id": 1}}
    ])
    return list(resultat)


#q11 : Vue MongoDB films avec Metascore > 80 et Revenue > 50M
def q11_vue_films_top():
    #la vue films_top a déjà été créé dans MongoDB et cette fonction lit le contenu de la vue
    resultat = collection.database["films_top"].find(
        {}, {"title": 1, "Metascore": 1, "Revenue (Millions)": 1, "_id": 0}
    )
    return list(resultat)


#q12 : corrélation entre durée et revenu
def q12_correlation_runtime_revenue():
    #elle récupère les données depuis MongoDB et elle calcule la corrélation avec scipy
    
    #étape 1 : récupérer les films qui ont les deux champs renseignés
    films = collection.find(
        {
            "Runtime (Minutes)": {"$ne": ""},
            "Revenue (Millions)": {"$ne": ""}
        },
        {
            "title": 1,
            "Runtime (Minutes)": 1,
            "Revenue (Millions)": 1,
            "_id": 0
        }
    )

    #étape 2 : convertir en DataFrame pandas
    df = pd.DataFrame(list(films))

    #étape 3 : nettoyer les valeurs nulles
    df = df.dropna(subset=["Runtime (Minutes)", "Revenue (Millions)"])

    #étape 4 — calculer la corrélation de pearson
    correlation, p_value = stats.pearsonr(
        df["Runtime (Minutes)"],
        df["Revenue (Millions)"]
    )

    return {
        "df": df,
        "correlation": round(correlation, 3),
        "p_value": round(p_value, 3)
    }

#q13 : évolution de la durée moyenne des films par décennie
def q13_duree_moyenne_par_decennie():
    resultat = collection.aggregate([
        {
            "$match": {
                "Runtime (Minutes)": {"$ne": ""},
                "year": {"$ne": None}
            }
        },
        {
            "$addFields": {
                "decennie": {
                    "$multiply": [
                        {"$floor": {"$divide": ["$year", 10]}},
                        10
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$decennie",
                "dureeMoyenne": {"$avg": "$Runtime (Minutes)"}
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ])
    return list(resultat)
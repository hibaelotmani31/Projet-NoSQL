from mongo_db import connect_mongo

collection = connect_mongo()


# Q1 — Année avec le plus de films
def q1_annee_plus_de_films():
    resultat = collection.aggregate([
        {"$group": {"_id": "$year", "nombre": {"$sum": 1}}},
        {"$sort": {"nombre": -1}},
        {"$limit": 1}
    ])
    return list(resultat)[0]


# Q2 — Nombre de films après 1999
def q2_films_apres_1999():
    return collection.count_documents({"year": {"$gt": 1999}})


# Q3 — Moyenne des votes en 2007
def q3_moyenne_votes_2007():
    resultat = collection.aggregate([
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "moyenneVotes": {"$avg": "$Votes"}}}
    ])
    return list(resultat)[0]["moyenneVotes"]


# Q4 — Nombre de films par année
def q4_films_par_annee():
    resultat = collection.aggregate([
        {"$group": {"_id": "$year", "nombreFilms": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ])
    return list(resultat)


# Q5 — Genres disponibles
def q5_genres_disponibles():
    resultat = collection.aggregate([
        {"$project": {"genres": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres"}},
        {"$sort": {"_id": 1}}
    ])
    return [g["_id"] for g in resultat]


# Q5 — Nombre de films par genre
def q5_nombre_films_par_genre():
    resultat = collection.aggregate([
        {"$project": {"genres": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres", "nombreFilms": {"$sum": 1}}},
        {"$sort": {"nombreFilms": -1}}
    ])
    return list(resultat)
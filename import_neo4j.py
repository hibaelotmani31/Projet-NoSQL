from pymongo import MongoClient
from neo4j import GraphDatabase
from config import MONGO_URI, MONGO_DB, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# connexion MongoDB
mongo_client = MongoClient(MONGO_URI)
collection = mongo_client[MONGO_DB]["films"]

# connexion Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def importer_donnees():
    films = list(collection.find())
    print(f"{len(films)} films trouvés dans MongoDB")

    with driver.session() as session:
        for film in films:
            # créer le nœud Film
            session.run("""
                MERGE (f:Film {id: $id})
                SET f.title = $title,
                    f.year = $year,
                    f.Votes = $votes,
                    f.Revenue = $revenue,
                    f.rating = $rating,
                    f.director = $director,
                    f.genre = $genre
            """,
                id=str(film.get("_id")),
                title=film.get("title", ""),
                year=film.get("year", 0),
                votes=film.get("Votes", 0),
                revenue=film.get("Revenue (Millions)", 0),
                rating=film.get("rating", ""),
                director=film.get("Director", ""),
                genre=film.get("genre", "")
            )

            # créer le nœud Realisateur et la relation
            director = film.get("Director", "")
            if director:
                session.run("""
                    MERGE (r:Realisateur {name: $name})
                    MERGE (f:Film {id: $id})
                    MERGE (r)-[:A_RÉALISÉ]->(f)
                """,
                    name=director,
                    id=str(film.get("_id"))
                )

            # créer les nœuds Acteurs et les relations
            actors = film.get("Actors", "")
            if actors:
                for actor in actors.split(","):
                    actor = actor.strip()
                    if actor:
                        session.run("""
                            MERGE (a:Actor {name: $name})
                            MERGE (f:Film {id: $id})
                            MERGE (a)-[:A_JOUÉ_DANS]->(f)
                        """,
                            name=actor,
                            id=str(film.get("_id"))
                        )

            print(f"✓ {film.get('title')} importé")

    print("Import terminé !")


def ajouter_genre():
    """Met à jour uniquement le champ genre sur les nœuds Film existants"""
    films = list(collection.find())
    print(f"Mise à jour genres pour {len(films)} films...")

    with driver.session() as session:
        for film in films:
            session.run("""
                MATCH (f:Film {id: $id})
                SET f.genre = $genre
            """,
                id=str(film.get("_id")),
                genre=film.get("genre", "")
            )

    print("Genres ajoutés !")


if __name__ == "__main__":
    ajouter_genre()
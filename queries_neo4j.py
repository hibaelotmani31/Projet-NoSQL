from neo4j_db import connect_neo4j

driver = connect_neo4j()

# Q14 — Acteur ayant joué dans le plus grand nombre de films
def q14_acteur_plus_films():

    query = """
    MATCH (a:Actor)-[:A_JOUÉ_DANS]->(f:Film)
    RETURN a.name AS acteur, count(f) AS nombreFilms
    ORDER BY nombreFilms DESC
    LIMIT 1
    """

    with driver.session() as session:
        result = session.run(query)
        return result.single().data()
    
# Q15 — Acteurs ayant joué dans des films avec Anne Hathaway
def q15_acteurs_avec_anne_hathaway():

    query = """
    MATCH (anne:Actor {name:"Anne Hathaway"})-[:A_JOUÉ_DANS]->(f:Film)<-[:A_JOUÉ_DANS]-(a:Actor)
    WHERE a.name <> "Anne Hathaway"
    RETURN DISTINCT a.name AS acteur
    """

    with driver.session() as session:
        result = session.run(query)
        return [record["acteur"] for record in result]

# Q16 — Acteur ayant joué dans les films générant le plus de revenus
def q16_acteur_plus_revenus():

    query = """
    MATCH (a:Actor)-[:A_JOUÉ_DANS]->(f:Film)
    WHERE f.Revenue <> ""
    RETURN a.name AS acteur, sum(toFloat(f.Revenue)) AS totalRevenue
    ORDER BY totalRevenue DESC
    LIMIT 1
    """

    with driver.session() as session:
        result = session.run(query)
        return result.single().data()

# Q17 — Moyenne des votes
def q17_moyenne_votes():

    query = """
    MATCH (f:Film)
    WHERE f.Votes <> ""
    RETURN avg(toFloat(f.Votes)) AS moyenneVotes
    """

    with driver.session() as session:
        result = session.run(query)
        return result.single()["moyenneVotes"]
    
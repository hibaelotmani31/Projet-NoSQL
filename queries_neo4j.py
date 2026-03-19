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


# Q19 — Films dans lesquels les acteurs ayant joué avec Matt Damon ont également joué
def q19_films_coacteurs():

    query = """
    MATCH (a:Actor {name:"Matt Damon"})-[:A_JOUÉ_DANS]->(f:Film)<-[:A_JOUÉ_DANS]-(co:Actor)
    MATCH (co)-[:A_JOUÉ_DANS]->(other:Film)
    WHERE other <> f
    RETURN DISTINCT other.title AS film
    """

    with driver.session() as session:
        result = session.run(query)
        return [record["film"] for record in result]


# Q20 — Réalisateur ayant travaillé avec le plus d’acteurs distincts
def q20_realisateur_plus_acteurs():

    query = """
    MATCH (r:Realisateur)-[:A_RÉALISÉ]->(f:Film)<-[:A_JOUÉ_DANS]-(a:Actor)
    RETURN r.name AS realisateur, COUNT(DISTINCT a) AS nombreActeurs
    ORDER BY nombreActeurs DESC
    LIMIT 1
    """

    with driver.session() as session:
        result = session.run(query)
        return result.single().data()


# Q21 — Films les plus connectés (partageant des acteurs avec d’autres films)
def q21_films_plus_connectes():

    query = """
    MATCH (f1:Film)<-[:A_JOUÉ_DANS]-(a:Actor)-[:A_JOUÉ_DANS]->(f2:Film)
    WHERE f1 <> f2
    RETURN f1.title AS film, COUNT(DISTINCT f2) AS connexions
    ORDER BY connexions DESC
    LIMIT 10
    """

    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]


# Q22 — Les 5 acteurs ayant travaillé avec le plus de réalisateurs différents
def q22_acteurs_plus_realisateurs():

    query = """
    MATCH (a:Actor)-[:A_JOUÉ_DANS]->(f:Film)<-[:A_RÉALISÉ]-(r:Realisateur)
    RETURN a.name AS acteur, COUNT(DISTINCT r) AS nombreRealisateurs
    ORDER BY nombreRealisateurs DESC
    LIMIT 5
    """

    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]
#q14...

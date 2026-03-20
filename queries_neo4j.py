from neo4j_db import connect_neo4j

driver = connect_neo4j()


#q14 - acteur ayant joué dans le plus grand nombre de films
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


#q15 - acteurs ayant joué dans des films avec Anne Hathaway
def q15_acteurs_avec_anne_hathaway():

    query = """
    MATCH (anne:Actor {name:"Anne Hathaway"})-[:A_JOUÉ_DANS]->(f:Film)<-[:A_JOUÉ_DANS]-(a:Actor)
    WHERE a.name <> "Anne Hathaway"
    RETURN DISTINCT a.name AS acteur
    """

    with driver.session() as session:
        result = session.run(query)
        return [record["acteur"] for record in result]


#q16 - acteur ayant joué dans les films générant le plus de revenus
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


#q17 - moyenne des votes
def q17_moyenne_votes():

    query = """
    MATCH (f:Film)
    WHERE f.Votes <> ""
    RETURN avg(toFloat(f.Votes)) AS moyenneVotes
    """

    with driver.session() as session:
        result = session.run(query)
        return result.single()["moyenneVotes"]
    

#q18 genre le plus représenté
def q18_genre_plus_represente():
    query = """
    MATCH (f:Film)
    WHERE f.genre IS NOT NULL
    WITH split(f.genre, ",") AS genres
    UNWIND genres AS genre
    RETURN trim(genre) AS genre, COUNT(*) AS nombre
    ORDER BY nombre DESC
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query)
        return result.single().data()


#q19 - films dans lesquels les acteurs ayant joué avec Matt Damon ont également joué
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


#q20 - realisateur ayant travaillé avec le plus d’acteurs distincts
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


#q21 - films les plus connectés (partageant des acteurs avec d’autres films)
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


#q22 - les 5 acteurs ayant travaillé avec le plus de réalisateurs différents
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
    

#q23 - recommander un film à un acteur selon ses genres
def q23_recommander_film(nom_acteur):
    """
    on cherche les genres des films où l'acteur a joué
    puis on recommande des films de ces genres où il n'a pas encore joué
    """
    query = """
    MATCH (a:Actor {name: $nom})-[:A_JOUÉ_DANS]->(f:Film)
    WITH a, split(f.genre, ",") AS genres
    UNWIND genres AS genre
    WITH a, trim(genre) AS genre
    MATCH (autre:Film)
    WHERE autre.genre CONTAINS genre
    AND NOT (a)-[:A_JOUÉ_DANS]->(autre)
    RETURN DISTINCT autre.title AS recommandation, autre.genre AS genre
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query, nom=nom_acteur)
        return [record.data() for record in result]
    

#q24 - créer la relation INFLUENCE_PAR entre réalisateurs
def q24_influence_par():
    """
    on crée une relation INFLUENCE_PAR entre deux réalisateurs
    s'ils ont réalisé des films avec des genres en commun
    """
    query = """
    MATCH (r1:Realisateur)-[:A_RÉALISÉ]->(f1:Film)
    MATCH (r2:Realisateur)-[:A_RÉALISÉ]->(f2:Film)
    WHERE r1 <> r2
    WITH r1, r2, 
         split(f1.genre, ",") AS genres1,
         split(f2.genre, ",") AS genres2
    WITH r1, r2,
         [g IN genres1 WHERE trim(g) IN [x IN genres2 | trim(x)]] AS genresCommuns
    WHERE size(genresCommuns) > 0
    MERGE (r1)-[:INFLUENCE_PAR {genresCommuns: genresCommuns}]->(r2)
    RETURN r1.name AS realisateur1, r2.name AS realisateur2, genresCommuns
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]
    

#q25 - hemin le plus court entre deux acteurs
def q25_chemin_plus_court(acteur1, acteur2):
    """
    on utilise shortestPath pour trouver le chemin le plus court
    entre deux acteurs en passant uniquement par les films
    """
    query = """
    MATCH p = shortestPath(
        (a1:Actor {name: $acteur1})-[:A_JOUÉ_DANS*]-(a2:Actor {name: $acteur2})
    )
    RETURN [n IN nodes(p) | 
        CASE 
            WHEN n:Actor THEN n.name 
            WHEN n:Film THEN n.title 
        END
    ] AS chemin, length(p) AS longueur
    """
    with driver.session() as session:
        result = session.run(query, acteur1=acteur1, acteur2=acteur2)
        record = result.single()
        if record:
            return record.data()
        return None
    

#q26 communautés d'acteurs (alternative à Louvain)
def q26_communautes_acteurs():
    """
    on détecte les groupes d'acteurs qui travaillent souvent ensemble
    en trouvant les paires qui ont joué dans au moins 2 films communs
    (alternative à l'algorithme Louvain qui nécessite Neo4j GDS)
    """
    query = """
    MATCH (a1:Actor)-[:A_JOUÉ_DANS]->(f:Film)<-[:A_JOUÉ_DANS]-(a2:Actor)
    WHERE a1.name < a2.name
    WITH a1, a2, collect(f.title) AS filmsCommuns, count(f) AS nbFilms
    WHERE nbFilms >= 2
    RETURN a1.name AS acteur1, a2.name AS acteur2, 
           filmsCommuns AS filmsCommuns, nbFilms AS nbFilms
    ORDER BY nbFilms DESC
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]
    
#q27 - films avec genres communs mais réalisateurs différents
def q27_films_genres_communs_realisateurs_differents():
    """
    on cherche des paires de films qui partagent au moins un genre
    mais qui ont été réalisés par des personnes différentes
    """
    query = """
    MATCH (f1:Film), (f2:Film)
    WHERE f1.title < f2.title
    AND f1.director <> f2.director
    AND ANY(g IN split(f1.genre, ",") 
        WHERE trim(g) IN [x IN split(f2.genre, ",") | trim(x)])
    RETURN f1.title AS film1, f2.title AS film2,
           f1.director AS realisateur1, f2.director AS realisateur2,
           f1.genre AS genres1, f2.genre AS genres2
    LIMIT 20
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]
    
#q28 - recommander des films à un utilisateur selon les préférences d'un acteur
def q28_recommander_films_utilisateur(nom_acteur):
    """
    version améliorée de Q23 — on recommande les films les mieux notés
    du genre favori de l'acteur, triés par revenus décroissants
    """
    query = """
    MATCH (a:Actor {name: $nom})-[:A_JOUÉ_DANS]->(f:Film)
    WITH a, split(f.genre, ",") AS genres
    UNWIND genres AS genre
    WITH a, trim(genre) AS genre, COUNT(*) AS freq
    ORDER BY freq DESC
    WITH a, collect(genre)[0] AS genreFavori
    MATCH (autre:Film)
    WHERE autre.genre CONTAINS genreFavori
    AND NOT (a)-[:A_JOUÉ_DANS]->(autre)
    RETURN autre.title AS recommandation, autre.genre AS genre,
           autre.Revenue AS revenue, autre.Votes AS votes
    ORDER BY toFloat(autre.Revenue) DESC
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query, nom=nom_acteur)
        return [record.data() for record in result]
    
#q29 - relation CONCURRENT_DE entre réalisateurs
def q29_concurrence_realisateurs():
    """
    on crée une relation CONCURRENT_DE entre deux réalisateurs
    s'ils ont sorti des films du même genre la même année
    """
    query = """
    MATCH (r1:Realisateur)-[:A_RÉALISÉ]->(f1:Film)
    MATCH (r2:Realisateur)-[:A_RÉALISÉ]->(f2:Film)
    WHERE r1 <> r2
    AND f1.year = f2.year
    AND ANY(g IN split(f1.genre, ",") 
        WHERE trim(g) IN [x IN split(f2.genre, ",") | trim(x)])
    MERGE (r1)-[:CONCURRENT_DE {annee: f1.year}]->(r2)
    RETURN r1.name AS realisateur1, r2.name AS realisateur2,
           f1.year AS annee, f1.title AS film1, f2.title AS film2
    LIMIT 20
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]
    

#q30 - collaborations réalisateurs/acteurs et succès commercial
def q30_collaborations_succes():
    """
    on identifie les duos réalisateur-acteur les plus fréquents
    et on analyse si ces collaborations sont associées à un succès commercial
    """
    query = """
    MATCH (r:Realisateur)-[:A_RÉALISÉ]->(f:Film)<-[:A_JOUÉ_DANS]-(a:Actor)
    WITH r, a, collect(f.title) AS films,
         count(f) AS nbCollabs,
         avg(toFloat(f.Revenue)) AS revenuMoyen,
         avg(toFloat(f.Votes)) AS votesMoyen
    WHERE nbCollabs >= 2
    RETURN r.name AS realisateur, a.name AS acteur,
           films AS filmsEnsemble,
           nbCollabs AS nbCollaborations,
           round(revenuMoyen, 2) AS revenuMoyen,
           round(votesMoyen, 0) AS votesMoyen
    ORDER BY nbCollabs DESC, revenuMoyen DESC
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

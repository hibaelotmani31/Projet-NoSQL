# CineBase - Exploration NoSQL de Films

Application web d'analyse et de visualisation de données cinématographiques, développée avec MongoDB, Neo4j et Streamlit.

---

## Aperçu

CineBase explore une base de **102 films** à travers deux bases de données NoSQL :
- **MongoDB Atlas** - pour les requêtes d'agrégation et analyses statistiques
- **Neo4j AuraDB** - pour l'analyse des relations entre acteurs et réalisateurs

L'application répond à **30 questions** réparties en 4 sections : Tendances, Revenus, Acteurs et Recommandations.

---

## Stack technique

| Technologie | Usage |
|---|---|
| Python 3.12 | Langage principal |
| MongoDB Atlas | Base de données documents |
| Neo4j AuraDB | Base de données graphe |
| Streamlit | Interface web |
| Pandas | Manipulation des données |
| Matplotlib | Visualisation |
| Scipy | Analyse statistique |
| Pymongo | Driver MongoDB |
| Neo4j Python Driver | Driver Neo4j |

---

## Structure du projet

```
projet-nosql/
├── app.py               # Application Streamlit principale
├── config.py            # Credentials (non versionné)
├── mongo_db.py          # Connexion MongoDB
├── neo4j_db.py          # Connexion Neo4j
├── queries_mongo.py     # Requêtes MongoDB (Q1 à Q13)
├── queries_neo4j.py     # Requêtes Neo4j (Q14 à Q30)
├── import_neo4j.py      # Script d'import MongoDB → Neo4j
├── images/
│   └── cinema.jpg       # Image hero page d'accueil
├── .gitignore
└── requirements.txt
```

---

## Installation

### 1. Cloner le repo

```bash
git clone https://github.com/hibaelotmani31/projet-sql.git
cd projet-sql
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les credentials

Créer un fichier `config.py` à la racine du projet :

```python
# MongoDB Atlas
MONGO_URI = "mongodb+srv://USER:PASSWORD@cluster.mongodb.net/"
MONGO_DB  = "entertainment"

# Neo4j AuraDB
NEO4J_URI      = "neo4j+s://XXXX.databases.neo4j.io"
NEO4J_USER     = "neo4j"
NEO4J_PASSWORD = "VOTRE_MOT_DE_PASSE"
```

> Ce fichier est dans `.gitignore` et ne doit jamais être commité.

### 5. Importer les données dans Neo4j

À lancer **une seule fois** pour peupler Neo4j depuis MongoDB :

```bash
python import_neo4j.py
```

### 6. Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement sur `http://localhost:8501`

---

## Base de données MongoDB

- **Base** : `entertainment`
- **Collection** : `films`
- **Documents** : 102 films (1978 → 2016)
- **Champs** : title, year, genre, Director, Actors, Runtime (Minutes), Revenue (Millions), Votes, Metascore, rating

## Base de données Neo4j

- **Noeuds** : Film (102), Actor (~400), Realisateur (~80)
- **Relations** : A_JOUÉ_DANS, A_RÉALISÉ, INFLUENCE_PAR, CONCURRENT_DE
- **Total** : 514 noeuds, 5000+ relations

---

## Questions répondues

| Section | Questions |
|---|---|
| Tendances | Q1, Q2, Q3, Q4, Q5, Q9, Q12, Q13 |
| Revenus | Q6, Q7, Q8, Q10, Q11 |
| Acteurs | Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q24, Q26, Q27, Q29, Q30 |
| Recommandations | Q23, Q25, Q28 |

---

## Équipe

Projet réalisé dans le cadre du cours NoSQL - ESIEA 2025-2026

- Hiba EL OTMANI
- Hadil BEN SOUSSIA
- Mayssam TOUINSI  

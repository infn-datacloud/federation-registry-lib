from neo4j import GraphDatabase


db = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

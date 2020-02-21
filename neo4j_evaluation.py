# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 12:18:42 2020

@author: Lia
"""
from neo4j import GraphDatabase

# Database Credentials
uri             = "bolt://localhost:7687"
userName        = "neo4j"
password        = "12345678"

# Connect to the neo4j database server
graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password)) 

def drop_db():
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run("MATCH (n) DETACH DELETE n");
        
def create_entreprises_default():
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run("CREATE (a:Entreprise { nom: 'Orange', secteur: 'Telecom et  Reseaux', description: 'Enterprise Francaise', taille: '600' })")
        graphDB_Session.run("CREATE (b:Entreprise { nom: 'Mc Donalds', secteur: 'Nourtiture', description: 'Enterprise Americaine', taille: '3000' })")

def create_entrepise(name,secteur,description,taille):
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run("CREATE (c:Entreprise {nom:'"+ name+"', secteur:'"+secteur+"', description: '"+description+"', taille: '"+taille+"'})")

def create_utilisateurs_default():
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run("CREATE (a:Utilisateur { nom: 'Sucupira', prenom:'Lia', description: 'Etudiante', competences: ['inteligent', 'responsable','otimiste'] })")
        graphDB_Session.run("CREATE (b:Utilisateur { nom: 'James', prenom:'Francois', description: 'Salariee', competences: ['leader', 'responsable'] })")
        graphDB_Session.run("CREATE (c:Utilisateur { nom: 'Gurd', prenom:'Frederic', description: 'Stagiare', competences: ['motivee', 'agreable'] })")

def create_utilisateur(nom,prenom,description,competences):
     with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run("CREATE (a:Utilisateur { nom:'"+ nom +"', prenom:'"+ prenom+"', description: '"+ description+"', competences:'"+ competences +"' })")

def create_relations_travaille_pour():
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run("MATCH (a:Utilisateur),(b:Entreprise) WHERE a.nom = 'Sucupira' AND b.nom ='Orange' CREATE (a)-[r:TRAVAILLE_POUR { date_debut: '5 fevrier 2010', date_fin: '10 avril 2020', status: 'Salarie'}]->(b) RETURN type(r), r")
        graphDB_Session.run("MATCH (a:Utilisateur),(b:Entreprise) WHERE a.nom = 'James' AND b.nom ='Orange' CREATE (a)-[r:TRAVAILLE_POUR { date_debut: '5 fevrier 2010', date_fin: '10 avril 2020', status: 'Salarie'}]->(b) RETURN type(r), r")

def create_relations_travaille_avec():
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run("MATCH (a:Utilisateur),(b:Utilisateur) WHERE a.nom = 'James' AND b.nom ='Gurd' CREATE (a)-[r:TRAVAILLE_AVEC]->(b) RETURN type(r), r")
        
def create_relations_connait():
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run("MATCH (a:Utilisateur),(b:Utilisateur) WHERE a.nom = 'Sucupira' AND b.nom ='Gurd' CREATE (a)-[r:CONNAIT]->(b) RETURN type(r), r")
        graphDB_Session.run("MATCH (a:Utilisateur),(b:Utilisateur) WHERE a.nom = 'Sucupira' AND b.nom ='James' CREATE (a)-[r:CONNAIT]->(b) RETURN type(r), r")

def create_relations_meme_connaissance(nom):
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run("MATCH ((a:Utilisateur)-[:CONNAIT]-(c:Utilisateur {nom:'"+nom+"'})), ((b:Utilisateur)-[:CONNAIT]-(c:Utilisateur {nom:'"+nom+"'})) WHERE a.nom <> b.nom CREATE (a)-[r:CONNUS_EM_COMUM]->(b) RETURN type(r), r.name")

def search_utilisateur(nom):
     with graphDB_Driver.session() as graphDB_Session:
        node = graphDB_Session.run("MATCH (a:Utilisateur {nom:'" + nom + "'}) RETURN a")
        print(node)

def search_entreprise(nom):
     with graphDB_Driver.session() as graphDB_Session:
        node = graphDB_Session.run("MATCH (a:Entreprise {nom:'" + nom + "'}) RETURN a")
        print(node)

#Delete database to start the querys
drop_db()
#Create queries for insertion of default companies and users
create_entreprises_default()
create_utilisateurs_default()
#Create insertion of a company
create_entrepise('Louis Vitton','Mode','High Fashion','2000')
#Create insertion of a utilisateur
create_utilisateur('Juiy','Li','Etudiante','confiante')
#Create relations beetween nodes
create_relations_travaille_pour()
create_relations_travaille_avec()
create_relations_connait()
#Search a utilisateur by name 
search_utilisateur("Sucupira")
#Search company by name
search_entreprise("Orange")
#Create relations beetween utilisateurs with the same connaissance
create_relations_meme_connaissance("Sucupira")
 
from pymongo import MongoClient
from random import randint
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bson.objectid import ObjectId

# on fait la connexion avec le serveur
client = MongoClient('localhost',27017)

# on recupere la base de donnee
db = client["projetMongo"]

# on fabrique les differentes collections
Joueurs = db["Joueurs"]
Equipes = db["Equipes"]
Matchs = db["Matchs"]

# on fait les classes metiers Joueur, Equipe et Match
class Joueur:
    def __init__(self, nom, prenom, dateDeNaissance, poste, poids):
        self.nom = nom
        self.prenom = prenom
        self.dateDeNaissance = datetime.strptime(dateDeNaissance, '%d/%m/%Y')
        self.poste = poste
        self.poids = poids

    # on fait la méthode pour enregistrer l'objet dans la collection de joueurs
    def enregistrer(self):
        Joueurs.insert_one({
            "nom" : self.nom,
            "prenom" : self.prenom,
            "date de naissance" : self.dateDeNaissance,
            "poste" : self.poste,
            "poids" : self.poids})



class Equipe:
    def __init__(self, nom, couleurs, stade):
        self.nom = nom
        self.couleurs = couleurs
        self.stade = stade
        self.effectifs = []

    # la méthode pour ajouter un joueur à l'equipe, à partir du nom on cherche l'id pour enregistrer l'id
    def ajouterJoueur(self, nomJoueur):
        self.effectifs.append(Joueurs.find_one({"nom" : nomJoueur}).get("_id"))

    # on fait la méthode pour enregistrer l'objet dans la collection d'equipes
    def enregistrer(self):
        Equipes.insert_one({
            "nom" : self.nom,
            "couleurs" : self.couleurs,
            "stade" : self.stade,
            "effectifs" : self.effectifs})

class Match:
    def __init__(self, nomEquipeDom, nomEquipeExt, scoreDom, scoreExt):
        self.equipeDom = Equipes.find_one({"nom" : nomEquipeDom}).get("_id")
        self.equipeExt = Equipes.find_one({"nom" : nomEquipeExt}).get("_id")
        self.scoreDom = scoreDom
        self.scoreExt = scoreExt
        # pour mettre les joueurs domiciles et exterieurs on boucle sur les joueurs des equipes et on les ajoute avec leur note (un entier aléatoire entre 0 et 20)
        self.joueursDom = [{"idJoueur":x, "noteJoueur":randint(0,20)} for x in Equipes.find_one({"_id" : self.equipeDom})["effectifs"]]
        self.joueursExt = [{"idJoueur":x, "noteJoueur":randint(0,20)} for x in Equipes.find_one({"_id" : self.equipeExt})["effectifs"]]

    # on fait la méthode pour enregistrer l'objet dans la collection de matchs
    def enregistrer(self):
        Matchs.insert_one({
            "equipe domicile" : self.equipeDom,
            "equipe exterieur" : self.equipeExt,
            "score domicile" : self.scoreDom,
            "score exterieur" : self.scoreExt,
            "joueurs domiciles" : self.joueursDom,
            "joueurs exterieurs" : self.joueursExt
            })

# retrouver un joueur depuis son nom
def getJoueur(nomJoueur):
    return Joueurs.find_one({"nom" : nomJoueur})

# retrouver une equipe depuis son nom
def getEquipe(nomEquipe):
    return Equipes.find_one({"nom" : nomEquipe})

# recuperer les joueurs plus jeunes qu'un certain age qui occupent un certain poste
def getJoueurPosteAgeMax(nomPoste, ageMax):
    # datemax et la date apres laquelle le joueur doit etre née pour etre plus jeune que ageMax
    datemax = datetime.now() - relativedelta(years = ageMax)
    jous = Joueurs.find({"date de naissance" : {"$gt" : datemax}, "poste" : nomPoste})
    # on affiche tout les resultats de la recherche
    for j in jous:
        print(j)

# creer une nouvelle collection avec les joueurs qui on joue plus d'un certain nombre de matche avec la moyenne de leur notes
def nouvelleCollectionXmatchs(n):
    # dans un premier temps on recupere tout les joueurs
    a = {}
    for joueur in Joueurs.find():
        a[joueur.get("_id")] = [0,0] # le premier nombre du doublon est le nombre de matchs joués, le deuxieme nombre et la somme des notes

    # dans un deuxieme temps on recupere tout les matchs et on met a jour les joueurs pour chaque matchs qu'ils on joués
    for match in Matchs.find():
        for joueur in match["joueurs domiciles"]:
            a[joueur["idJoueur"]][0]+=1
            a[joueur["idJoueur"]][1]+=joueur["noteJoueur"]
        for joueur in match["joueurs exterieurs"]:
            a[joueur["idJoueur"]][0]+=1
            a[joueur["idJoueur"]][1]+=joueur["noteJoueur"]

    # on cree la nouvelle collection pour ce nombre de matchs
    noteJoueursXmatchs = db["noteJoueurs" + str(n) + "matchs"]

    # tout les joueurs qui ont joués suffisamment de matchs sont rajoutés à la collection
    for jou in a:
        if a[jou][0]>=n:
            try:
                noteJoueursXmatchs.insert_one({
                    "_id" : ObjectId(jou),
                    "moyenne" : a[jou][1]/a[jou][0]})
            except : # si le joueur existe deja dans cette collection on met juste a jour son score
                noteJoueursXmatchs.update_one({
                    "_id" : ObjectId(jou)},
                    {"$set" : {"moyenne" : a[jou][1]/a[jou][0]}})


# initialisation de la base de donnée
joueur1 = Joueur("Jost", "Adrien", "09/04/1995", "ailier", 12)
joueur2 = Joueur("Ittel", "Etienne", "25/12/1996", "goal", 47)
joueur3 = Joueur("Laidouni", "Nabil", "01/01/2003", "arriere droit", 74)
joueur4 = Joueur("Succupira", "Lia", "01/01/1994", "arriere droit", 22)
joueur5 = Joueur("Peyrard", "Antoine", "01/01/2000", "arriere droit", 54)
joueur6 = Joueur("Peyraud", "Guillaume", "01/01/2000", "goal", 65)

joueur1.enregistrer()
joueur2.enregistrer()
joueur3.enregistrer()
joueur4.enregistrer()
joueur5.enregistrer()
joueur6.enregistrer()

equipe1 = Equipe("aigle", ["rouge"], "Lille")
equipe2 = Equipe("tigre", ["bleu", "noir"], "Strasbourg")
equipe3 = Equipe("cheval", ["jaune", "gris"], "Renne")


equipe1.ajouterJoueur("Jost")
equipe1.ajouterJoueur("Succupira")
equipe2.ajouterJoueur("Ittel")
equipe2.ajouterJoueur("Laidouni")
equipe3.ajouterJoueur("Peyrard")
equipe3.ajouterJoueur("Peyraud")


equipe1.enregistrer()
equipe2.enregistrer()
equipe3.enregistrer()

match1 = Match("aigle", "tigre", 3,2)
match2 = Match("tigre", "aigle", 3,4)
match3 = Match("aigle", "cheval", 1,1)
match4 = Match("cheval", "aigle", 1,2)
match5 = Match("cheval", "tigre", 2,4)

match1.enregistrer()
match2.enregistrer()
match3.enregistrer()
match4.enregistrer()
match5.enregistrer()

# affichage des résultats des fonctions
print(getJoueur("Jost"))
print(getEquipe("aigle"))

print("joueur de moins de 25 ans arriere droit : ")
print(getJoueurPosteAgeMax("arriere droit", 25))

nouvelleCollectionXmatchs(4)



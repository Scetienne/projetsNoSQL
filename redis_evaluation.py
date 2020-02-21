 # -*- coding: utf-8 -*-
import redis

redis_host = "localhost"
redis_port = 6379
#Connect with database
r = redis.StrictRedis(host=redis_host, port=redis_port,
                             db = 0, decode_responses=True)
#Test connection to database
def test_connection_database():
    try:
       
        r.hmset("msg","Hello")
        
        msg= r.hmget("msg")
        print(msg)
    except Exception as e:
        print(e)

#Create the appels with certains properties
def create_appels():
    try:
        appel1 = {"id":"1","heure":"3:54","numero_origine":"0749048614","statut":"Non affecte", "duree":"1:40", "operateur_id":"2", "description":"Appel domiciliare"}
        appel2 = {"id":"2","heure":"2:39","numero_origine":"0649048814","statut":"Non pris en compte", "duree":"1:59", "operateur_id":"1", "description":"Appel formelle"}
        appel3 = {"id":"3","heure":"1:23","numero_origine":"0949048667","statut":"En cours", "duree":"0:40", "operateur_id":"1", "description":"Appel"}
        appel4 = {"id":"4","heure":"22:56","numero_origine":"0756048615","statut":"En cours", "duree":"0:04", "operateur_id":"3", "description":"Appel travail"}
        
        r.hmset("appel1", appel1)
        r.hmset("appel2", appel2)
        r.hmset("appel3", appel3)
        r.hmset("appel4", appel4)
    except Exception as e:
        print(e)
#To vizualize the properties of a appel
def view_appel(id):
    msg = r.hgetall("appel"+id)
    print(msg)
#Create the operateurs with certains properties
def create_operateurs():
    try:
        op1 = {"id":"1","nom":"James", "prenom":"Clara", "age":"15"} 
        op2 = {"id":"2","nom":"Silva", "prenom":"Augusto", "age":"67"}
        op3 = {"id":"3","nom":"Costa", "prenom":"Maria", "age":"34"}
        
        r.hmset("op1", op1)
        r.hmset("op2", op2)
        r.hmset("op3", op3)
    except Exception as e:
        print(e)
#Delete database informations
def delete_db():
    r.flushall()
#Get all the appels of a especific Status
def search_statut(status):
    for key in r.scan_iter():
        if r.hmget(key,'statut'):
            for hash in r.hscan_iter(key, 'statut'):
                if status  in hash[1]:
                    print(key)
                    return key
#Get all the elements of the database
def get_all():
    for key in r.scan_iter():
        print(key)
#Get all the operatus of the appels in Cours de traitement
def get_operateurs(key):
    print(key)
    for op_id in r.hscan_iter(key,'operateur_id'):
        for op in r.scan_iter():
            if r.hmget(op,'nom'):
                for hash in r.hscan_iter(op,'id'):
                    if op_id[1] == hash[1]:
                        print(r.hmget(op,'nom'))
                        
#Calling out the functions made

#Testing database connection
test_connection_database()
#Create db
create_appels()
view_appel("2")
create_operateurs()
#Search appels en cours, non affecte
search_statut("En cours")
search_statut("Non affecte")
#all operateurs of the appels
get_operateurs(search_statut("En cours"))

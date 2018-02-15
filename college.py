import pymongo
import urllib, json

url = "https://www.reddit.com/r/ApplyingToCollege.json"
response = urllib.urlopen(url)
#data = json.load(response)
#rint response.read()

connection = pymongo.MongoClient("149.89.150.100")
db = connection.fourthTermJuniors
collection = db.a2c

f = open("ApplyingToCollege.json", "r")
for line in f:
    print line + '/n'



def boro(name):
    cursor = collection.find({ "borough" : name, "borough." + name + ".name" : {"$ne" : ""} } )
    for i in cursor:
        print i["name"]
        #print i["borough"]

def zipcode(code):
    cursor = collection.find({ "address.zipcode" : code })
    for i in cursor:
        print i["name"]
        #print i["address"]["zipcode"]

def zipgrade(code, grade):
    cursor = collection.find({ "address.zipcode" : code, "grades.grade" : grade })
    for i in cursor:
        print i["name"]
        #print i["grades"][0]["grade"]

def zipbelowscore(code, score):
    cursor = collection.find({ "address.zipcode" : code, "grades.score" : {"$lt" : score} })
    for i in cursor:
        print i["name"]
        #print i["grades"][0]["score"]
                
#boro("Manhattan")
#zipcode("10282")
#zipgrade("10282", "A")
#zipbelowscore("10282", 2)

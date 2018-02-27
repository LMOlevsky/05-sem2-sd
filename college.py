from flask import Flask, render_template, request, session, redirect, url_for, flash
import pymongo, json, requests

app = Flask(__name__)

'''
Reddit
Subreddit: Applying To College
Descrpition from site:
    "/r/ApplyingToCollege is the premier forum for college 
     admissions questions, advice, and discussions, from 
     college essays and scholarships to SAT/ACT test prep, 
     career guidance, and more."

Dataset Link: https://www.reddit.com/r/ApplyingToCollege.json

Import mechanism:
    From the url above, we use the requests module to decode 
    the json file from the website and read the data into our python script. 
    1) Import json and requests
    2) Store json link in a variable
    3) Read the url using requests.get()
    4) Decode webpage to json file using json()
'''


link = 'https://www.reddit.com/r/ApplyingToCollege.json'
r = requests.get(link, headers = {'User-agent': 'fourthTermJuniors'})
data = r.json()
posts = data["data"]["children"]

connection = pymongo.MongoClient("149.89.150.100")
connection.drop_database("fourthTermJuniors")
db = connection.fourthTermJuniors
collection = db.a2c


#==========================================helper functions
def addToCollection(collection):
    for each in posts:
        #print collection.update({ "data.title" : each["data"]["title"] }, each, upsert=True)
        collection.update({ "data.title" : each["data"]["title"] }, each, upsert=True)

        
def suggested_sort(suggested):
    print "==========printing posts with suggested_sort = " + suggested + "...=========="
    cursor = collection.find({ "data.suggested_sort" : suggested })
    ans = ""
    for i in cursor:
        ans += "\t" + i["data"]["title"]
    return ans
        
def upvotes(number):
    print "==========printing posts with upvotes > " + str(number) + "...=========="
    cursor = collection.find({ "data.ups" : {"$gt" : number} })
    ans = ""
    for i in cursor:
        ans += "\t" + str(i["data"]["ups"]) + ": " + i["data"]["title"]
    return ans

def score(number):
    print "==========printing posts with score > " + str(number) + "...=========="
    cursor = collection.find({ "data.score" : {"$gt" : number} })
    ans = ""
    for i in cursor:
        ans += "\t" + str(i["data"]["score"]) + ": " + i["data"]["title"]
    return ans
        
def stickied():
    print "==========printing stickied posts...=========="
    cursor = collection.find({ "data.stickied" : True })
    ans = ""
    for i in cursor:
        ans += "\t" + i["data"]["title"]
    return ans

def nonstickied():
    print "==========printing nonstickied posts...=========="
    cursor = collection.find({ "data.stickied" : False })
    ans = ""
    for i in cursor:
        ans += "\t" + i["data"]["title"]
    return ans


addToCollection(collection)
'''
suggested_sort("confidence")
upvotes(15)
upvotes(300)
score(15)
score(300)
stickied()
nonstickied()
'''

@app.route('/', methods=["GET", "POST"])
def root():
    return render_template("college.html")

@app.route('/submit', methods=["GET", "POST"])
def getValue():
    votes = request.args["votes"]
    return render_template("college.html", value=upvotes(int(votes)))


if __name__ == '__main__':
    app.debug = True
    app.run()

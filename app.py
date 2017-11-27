import numpy as np
import pandas as pd
from flask import request
import time

from flask import Flask
from flask import make_response
import json
import pickle
import re
import os

app = Flask(__name__)
"""
file=open("data/cities.txt","r")
cities=[]
for l in file:
    city=l.split("\t")[2]
    city=city.lower()
    cities.append(city)
pickle.dump(cities,open("data/cities.p","wb"))
"""
"""
def check_cities(words):
    c=[]
    cities=pickle.load(open("data/cities.p","rb"))
    for w in words:
        for city in cities:
            if w==city or w==city[0:3]:
                print(city)
                c.append(city)
    return c

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    text=req.get("text")

    _WORD_SPLIT = re.compile("([-.,!?\"':;)<>(])")

    text=text.lower()
    words=[]
    for w in text.strip().split():
        words.extend(_WORD_SPLIT.split(w))
    cities=check_cities(words)
    res = {
        "destinations":cities
    }
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r




if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

"""""

import datetime
@app.route('/webhook', methods=['POST'])
def webhook():
    info={}
    info["case1"]={}
    phase=["morning","noon","evening","night"]
    months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec","january","february","march","april","may","june","july","august","september","october","november","december"]
    airlines=["indigo","jet","spice"]
    iata2city, partial_names, cities,spaced_cities=get_info()
    req = request.get_json(silent=True, force=True)
    text = req.get("text")
    text=text.lower()
    l=splitted_text(text)
    print(l)
    last_int=""
    #data=pd.read_csv("data/airports.csv")
    #cities=data.ix[:,2].values
    i=1
    word_index=0
    combined_word=""
    for word in l:
        if word_index<len(l)-1:
            combined_word=l[word_index]+" "+l[word_index+1]

        if word in cities:

            if "source" in info["case"+str(i)].keys() and "destination" in info["case"+str(i)].keys():
                i=i+1
                info["case" + str(i)] = {}


        if word in cities:
            if "source" in info["case"+str(i)].keys():
                info["case"+str(i)]["destination"]=word
            else:

            #info["case"+str(i)]={}
                info["case"+str(i)]["source"]=word

        if combined_word in spaced_cities:

            if "source" in info["case"+str(i)].keys() and "destination" in info["case"+str(i)].keys():
                i=i+1
                info["case" + str(i)] = {}


        if combined_word in spaced_cities:
            if "source" in info["case"+str(i)].keys():
                info["case"+str(i)]["destination"]=combined_word
            else:

            #info["case"+str(i)]={}
                info["case"+str(i)]["source"]=combined_word

        if word in iata2city.keys():

            if "source" in info["case"+str(i)].keys() and "destination" in info["case"+str(i)].keys():
                i=i+1
                info["case" + str(i)] = {}


        if word in iata2city.keys():
            if "source" in info["case"+str(i)].keys():
                info["case"+str(i)]["destination"]=iata2city[word]
            else:

            #info["case"+str(i)]={}
                info["case"+str(i)]["source"]=iata2city[word]

        if word in partial_names.keys():

            if "source" in info["case"+str(i)].keys() and "destination" in info["case"+str(i)].keys():
                i=i+1
                info["case" + str(i)] = {}


        if word in partial_names.keys():
            if "source" in info["case"+str(i)].keys():
                info["case"+str(i)]["destination"]=partial_names[word]
            else:

            #info["case"+str(i)]={}
                info["case"+str(i)]["source"]=partial_names[word]


        try:
            datetime.datetime.strptime(word, '%d/%m/%Y')
            info["case"+str(i)]["date"]=word
        except ValueError:
            pass

        try:
            time.strptime(word,"%H:%M")
            if word_index<len(l)-1:
                if l[word_index+1]=="am" or l[word_index+1]=="pm":
                    word=word+" "+l[word_index+1]
            if "time" in info["case" + str(i)].keys():
                info["case" + str(i)]["max_time"] = word

            else:
                info["case" + str(i)]["time"] = word

        except ValueError:
            pass

        try:
            if len(word)==4:
                time.strptime(word,"%H%M")
                if word !="2017" and word !="2018":
                    if "time" in info["case" + str(i)].keys():
                        info["case" + str(i)]["max_time"] = word
                    else:
                        info["case" + str(i)]["time"] = word

        except ValueError:
                pass


        if word in phase:
            info["case"+str(i)]["period_of_day"]=word
        else:
            pass

        if word.isdigit():
            last_int=word

        if word in months:
            if "date" in info["case"+str(i)].keys():
                i = i + 1
                info["case" + str(i)] = {}
            info["case" + str(i)]["date"] = last_int+word
        word_index=word_index+1

        if word in airlines and "airline" not in info["case" + str(i)].keys() :
            info["case" + str(i)]["airline"] = word



    res=json.dumps(info)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def get_info():
    iata2city, partial_names, cities,spaced_cities=pickle.load(open("data/short_names_and_iata_1.p","rb"))
    return iata2city,partial_names,cities,spaced_cities

def mysplit(s):
    head = s.rstrip('abcdefghijklmnopqrstuvwxyz')
    tail = s[len(head):]
    return head, tail

def splitted_text(text):
    splitted_txt = []
    for s in split_into_words(text):
        if any(i.isdigit() for i in s):
            head, tail = mysplit(s)
            splitted_txt.append(head)
            splitted_txt.append(tail)
        else:
            splitted_txt.append(s)
    splitted_txt = list(filter(None, splitted_txt))

    return splitted_txt

def split_into_words(sentence):
    #expression for splitting
    _WORD_SPLIT = re.compile("([-.,!?\"';)<>(])")
    #to store words
    words=[]
    #first split by space
    for space_separated_fragment in sentence.strip().split():
        #and then split by expression
        words.extend(_WORD_SPLIT.split(space_separated_fragment))
    return words

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')




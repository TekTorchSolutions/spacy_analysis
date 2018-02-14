import numpy as np
import pandas as pd
from flask import request
import time
from flask_cors import CORS
from pymongo import MongoClient

from flask import Flask
from flask import make_response
import json
import pickle
import re
import os

from core import solve
app = Flask(__name__)
CORS(app)

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
    month_dict={"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12,"january":1,"february":2,"march":3,"april":4,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11,"december":12}
    airlines=["indigo","jet","spice"]
    iata2city, partial_names, cities,spaced_cities,city2iata,city2airport=get_info()
    #city2iata={city:iata for iata,city in iata2city.items()}

    city2iata['bangalore']="BLR"
    city2iata['delhi']='DEL'
    city2iata['mumbai']="BOM"
    city2iata["lucknow"]="LKO"
    print(city2iata)
    req = request.get_json(silent=True, force=True)
    text = req.get("text")
    small_text=text.lower()
    l=splitted_text(small_text)
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
                try:
                    info["case" + str(i)]["destination_code"] = city2iata[word].upper()
                    info["case" + str(i)]["destination_airport"] = city2airport[word]
                except:
                    pass
            else:

            #info["case"+str(i)]={}
                info["case"+str(i)]["source"]=word
                try:
                    info["case" + str(i)]["source_code"] = city2iata[word].upper()
                    info["case" + str(i)]["source_airport"] = city2airport[word]
                except:
                    pass

        if combined_word in spaced_cities:

            if "source" in info["case"+str(i)].keys() and "destination" in info["case"+str(i)].keys():
                i=i+1
                info["case" + str(i)] = {}


        if combined_word in spaced_cities:
            if "source" in info["case"+str(i)].keys():
                info["case"+str(i)]["destination"]=combined_word
                try:
                    info["case"+str(i)]["destination_code"]=city2iata[combined_word].upper()
                    info["case" + str(i)]["destination_airport"] = city2airport[word]
                except:
                    pass
            else:

            #info["case"+str(i)]={}
                info["case"+str(i)]["source"]=combined_word
                try:
                    info["case" + str(i)]["source_code"] = city2iata[combined_word].upper()
                    info["case" + str(i)]["source_airport"] = city2airport[word]
                except:
                    pass
        if word in iata2city.keys():

            if "source" in info["case"+str(i)].keys() and "destination" in info["case"+str(i)].keys():
                i=i+1
                info["case" + str(i)] = {}


        if word in iata2city.keys():
            if "source" in info["case"+str(i)].keys():
                info["case"+str(i)]["destination"]=iata2city[word]
                try:
                    info["case" + str(i)]["destination_code"] = word.upper()
                    info["case" + str(i)]["destination_airport"] = city2airport[iata2city[word]]
                except:
                    pass
            else:

            #info["case"+str(i)]={}
                info["case"+str(i)]["source"]=iata2city[word]
                try:
                    info["case" + str(i)]["source_code"] = word.upper()
                    info["case" + str(i)]["source_airport"] = city2airport[iata2city[word]]
                except:
                    pass

        if word in partial_names.keys():

            if "source" in info["case"+str(i)].keys() and "destination" in info["case"+str(i)].keys():
                i=i+1
                info["case" + str(i)] = {}


        if word in partial_names.keys():
            if "source" in info["case"+str(i)].keys():
                info["case"+str(i)]["destination"]=partial_names[word]
                try:
                    info["case" + str(i)]["destination_code"] = city2iata[partial_names[word].lower()].upper()
                    info["case" + str(i)]["destination_airport"] = city2airport[word]
                except:
                    pass
            else:

            #info["case"+str(i)]={}
                info["case"+str(i)]["source"]=partial_names[word]
                try:
                    info["case" + str(i)]["source_code"] = city2iata[partial_names[word].lower()].upper()
                    info["case" + str(i)]["source_airport"] = city2airport[word]
                except:
                    pass


        try:
            datetime.datetime.strptime(word, '%d/%m/%Y')

            info["case"+str(i)]["date"]=word
            split_date=word.split("/")
            if split_date[2]=='18' or split_date[2]=='2018':
                str_date='2018-'+split_date[1]+"-"+split_date[0]
                info["case" + str(i)]["date"] = str_date
            else:
                str_date = '2017-' + split_date[1] + "-" + split_date[0]
                info["case" + str(i)]["date"] = str_date

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
            if word=="dec"or word=="december":
                date_str="2017-12"+"-"+str(last_int)
                info["case" + str(i)]["date"] = date_str
            else:
                date_str="2018-"+str(month_dict[word])+"-"+str(last_int)
                info["case" + str(i)]["date"] = date_str


        word_index=word_index+1

        if word in airlines and "airline" not in info["case" + str(i)].keys() :
            info["case" + str(i)]["airline"] = word

    print(check_for_second_opinion(info))
    if check_for_second_opinion(info):
        unstructured_info=get_second_opinion(text)
        print(unstructured_info)
        final_info=compare_opinions(info,unstructured_info)
    else:
        final_info=info

    #send_to_db(text,str(final_info))
    res=json.dumps(final_info)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def get_info():
    iata2city, partial_names, cities,spaced_cities=pickle.load(open("data/short_names_and_iata_1.p","rb"))
    iata2city["blr"]="bangalore"
    city2iata=pickle.load(open("data/city2iata.p","rb"))
    city2airport=pickle.load(open("data/city2airport.p","rb"))
    return iata2city,partial_names,cities,spaced_cities,city2iata,city2airport

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



def send_to_db(request_text="",response_text=""):
    print("Connecting")
    client = MongoClient("mongodb://jas1994:biology12@ds133476.mlab.com:33476/adroint_logs")
    print("Connected")

    db = client['adroint_logs']
    print("Sending")


    collection=db["plain_logs_direct"]
    db_dict = {
            "req": request_text,
            "resp": response_text,


        }
    collection.insert(db_dict)
    print("Sent")


def check_for_second_opinion(info):
    for case, struct in info.items():
        if "date" in struct.keys():
            continue
        else:
            return True

    return False

def get_second_opinion(text):
    info=solve(text)
    return info

def compare_opinions(structured_info,unstructured_info):
    structured_score=0
    unstructured_score=0
    for case, struct in structured_info.items():
        if "date" in struct.keys():
            structured_score=structured_score+1

        else:
            continue
    for case, struct in unstructured_info.items():
        if "date" in struct.keys():
            unstructured_score = unstructured_score + 1

        else:
            continue

    if structured_score >= unstructured_score:
        print(structured_score)
        return structured_info
    else:
        unstructured_info=enhance_unstructured_output(unstructured_info)
        return unstructured_info


def enhance_unstructured_output(unstructured_info):
    iata2city, partial_names, cities, spaced_cities, city2iata, city2airport = get_info()
    for case,struct in unstructured_info.items():
        if "source" in struct.keys():

            struct["source_code"]=city2iata[struct["source"].lower()].upper()
            struct["source_airport"]=city2airport[struct["source"].lower()]
        if "destination" in struct.keys():
            struct["destination_code"]=city2iata[struct["destination"].lower()].upper()
            struct["destination_airport"]=city2airport[struct["destination"].lower()]

    return unstructured_info




if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')




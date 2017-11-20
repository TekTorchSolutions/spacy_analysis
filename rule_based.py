import numpy as np
import pandas as pd
from flask import request

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
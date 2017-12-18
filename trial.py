""""
import pandas as pd
import pickle
data=pd.read_csv("data/global_airports.csv")
city=data["city"].values
iata=data["iata_faa"].values
city2iata={}
cities=[]
for i in range(len(city)):
    city2iata[str(iata[i]).lower()]=str(city[i]).lower()
    cities.append(str(city[i]).lower())
city2iata["BOM"]="mumbai"
print(city2iata)
print(city2iata["BOM"])

partial_names={}
partial_names["mum"]="Mumbai"
partial_names["ahm"]="Ahmedabad"
partial_names["ny"]="New York"
partial_names["la"]="Los Angeles"

obj=[city2iata,partial_names,cities]

pickle.dump(obj,open("data/short_names_and_iata.p","wb"))

import pandas as pd
import pickle
data=pd.read_csv("data/airport100.csv")
airport=data["Airport location"].values
iata=data["CODE"].values
cities=[]
iata2city={}
data_1=pd.read_csv("data/global_airports.csv")
city=data_1["city"].values
city2iata={}
cities_iata=[]
for i in range(len(city)):
    cities.append(str(city[i]).lower())
for ap in airport:
    cities_iata.append(ap.split(",")[0].lower())
for i in range(100):
    iata2city[iata[i].lower()]=cities_iata[i]
iata2city['bah']="bahrain"
print(iata2city)
print(cities)
cities.append("mumbai")
cities.append("bahrain")
partial_names={}
partial_names["mum"]="Mumbai"
partial_names["ahm"]="Ahmedabad"
partial_names["ny"]="New York"
partial_names["la"]="Los Angeles"

spaced_cities=["new york","los angeles","las vegas"]
obj=[iata2city,partial_names,cities,spaced_cities]

pickle.dump(obj,open("data/short_names_and_iata_1.p","wb"))
"""

import pandas as pd
import pickle
df=pd.read_csv("data/airports_large.csv")
city=df.iloc[:, 2].values
airport_code=df.iloc[:, 4].values
print(len(city))
print(len(airport_code))
#city2code=dict(zip(city,airport_code))
city2iata={}
for i in range(len(city)):
    city2iata[str(city[i]).lower()]=airport_code[i]
print(city2iata["hyderabad"])
pickle.dump(city2iata,open("data/city2iata.p","wb"))

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
default_airport=pd.read_csv("data/airport100.csv")
#print(df.head())
cities=df.iloc[:, 2].values
airport_code=df.iloc[:, 4].values
airport=df.iloc[:,1].values
default_city=default_airport.iloc[:,4].values
default_iata=default_airport.iloc[:,2].values
for i in range(len(default_city)):
    default_city[i]=default_city[i].split(",")[0].lower()



#city2code=dict(zip(city,airport_code))
"""""
city2iata={}
city2airport={}

for i in range(len(city)):
    city2iata[str(city[i]).lower()]=airport_code[i]
    city2airport[str(city[i]).lower()] = airport[i]
print(city2iata["hyderabad"])
print(city2airport["mexico"])
iata2city, partial_names, cities, spaced_cities = pickle.load(open("data/short_names_and_iata_1.p", "rb"))
print(len(iata2city))

"""""
#city2iata=pickle.load(open("data/city2iata.p","rb"))
#city2airport=pickle.load(open("data/city2airport.p","rb"))

#print(city2iata["new york"])#pickle.dump(city2iata,open("data/city2iata.p","wb"))
#pickle.dump(city2airport,open("data/city2airport.p","wb"))
city_2_all_airports={}
airport2iata={}
city_2_default_iata={}
for i in range(len(cities)):
    if type(cities[i])==str:
        if cities[i].lower() in city_2_all_airports.keys():
            city_2_all_airports[cities[i].lower()].append(airport[i].lower())
        else:
            city_2_all_airports[cities[i].lower()]=[]
            city_2_all_airports[cities[i].lower()].append(airport[i].lower())


for i in range(len(cities)):
    if type(airport_code[i]) == str:
        airport2iata[airport[i].lower()]=airport_code[i].lower()
default_city=list(reversed(default_city))
default_iata=list(reversed(default_iata))
for i in range(len(default_city)):
    city_2_default_iata[default_city[i]]=default_iata[i]

print(city_2_all_airports)
print(city_2_default_iata)
print(airport2iata)
#pickle.dump((city_2_all_airports,city_2_default_iata,airport2iata),open("data/city_airport_iata.p","wb"))
iata2city, partial_names, cities,spaced_cities=pickle.load(open("data/short_names_and_iata_1.p","rb"))
print(spaced_cities)
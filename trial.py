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
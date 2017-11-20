import pickle
file=open("data/cities.txt","r")
cities=[]
for l in file:
    city=l.split("\t")[2]
    city=city.lower()
    cities.append(city)
pickle.dump(cities,open("data/cities.p","wb"))
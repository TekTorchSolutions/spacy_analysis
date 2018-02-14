import spacy
import dateparser
import pandas as pd


df=pd.read_csv("data/airports_large.csv")
#print(df.head())
cities=df.iloc[:, 2].values
quantifier_reference={"first":1,"second":2,"third":3,"fourth":4,"fifth":5}
month_reference={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
time_entities=["week","month","year"]


"""""
article = '''

Let's go to Delhi in the third week of January on Monday around 9pm and fly to Goa on the next Tuesday.I will then depart to Indore.

'''

doc = nlp(article)
for ent in doc.ents:
   print(ent.label_, ent.text,ent.start)

"""""


"""""
{
    "case1": {
        "source": "new delhi",
        "source_code": "DEL",
        "destination": "bangalore",
        "destination_code": "BLR",
        "destination_airport": "HAL Airport",
        "date": "2018-1-21",
        "period_of_day": "morning",
        "time": "9:00"
    }
}
"""""

def get_all_info(content):
    response_dict={}
    sentences = [sent.string.strip() for sent in doc.sents]
    print(sentences)
    for sentence in sentences:
        splitted_sentence=sentence.split(" ")
        for city in cities:
            if city in splitted_sentence:

                if "city" not in response_dict.keys():
                    response_dict["city"]=city
                    city_index=sentence.index(city)



#def get_positionals(sentence):


#get_all_info("Let's go to Delhi in the third week of January on a Monday afternoon and fly to Goa on the next Tuesday.I will then depart to Indore.")

def spacy_analysis(sentence):
    nlp = spacy.load('en')
    datelist=[]
    timelist=[]
    doc = nlp(sentence)
    for ent in doc.ents:
        if ent.label_=="DATE":
            datelist.append(ent.text)
        if ent.label_=="TIME":
            timelist.append(ent.text)

        #print(ent.label_, ent.text)

    return datelist,timelist

print(spacy_analysis("Let's go to Delhi in the third week of January on a Monday afternoon and fly to Goa on the next Tuesday"))


def resolve_date_time(sentence,city_index):
    date_time_dict={}
    datelist,timelist=spacy_analysis(sentence)
    for dt in datelist:
        dt_index=sentence.index(dt)
        if dt_index>city_index:
            segmented_dt=dt.split(" ")
            for tm in time_entities:
                if tm in segmented_dt:
                    tm_index=segmented_dt.index(tm)
                    quantifier=segmented_dt[tm_index-1]
                    #if quantifier=="next":
                        #date_time_dict[tm]=










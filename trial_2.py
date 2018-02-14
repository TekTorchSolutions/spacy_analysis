import spacy
import pandas as pd
from datetime import datetime
import parsedatetime
import string
from datetime import date

cal = parsedatetime.Calendar()

nlp = spacy.load('en')


#s="Let's go to Delhi in the third week of January and on next Tuesday go to Mumbai.I prefer afternoon filghts."
s="Lets go to Delhi on the fifth Monday of February."
#s="Let's visit Delhi tomorrow night at 10pm."
m="Let's go to Delhi after two days."

quantifier_reference={"first":1,"second":2,"third":3,"fourth":4,"fifth":5}
month_reference={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
time_entities=["week","month","year"]
time_jump=["after","next","tomorrow"]
time_duration=["morning","evening","afternoon","night"]
text_to_int={"one":1,"two":2,"three":3,"four":4,"five":5,"six":6}
day_reference={"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6}

doc2=nlp(s)
#sentences = [sent.string.strip() for sent in doc.sents]
sentences = [sent.string.strip() for sent in doc2.sents]

def get_all_children(token,boss,lst,glob):

    if list(token.children)==[] or (token.pos_=="VERB" and token!=boss):
        #print(list(token.children)==[] , token.pos_=="VERB",  token!=boss)
        #if list(token.children)==[]:
        glob.append(lst)
            #print(lst)
        return
    for child in list(token.children):
        if child.pos_!="VERB":
            lst.append(child.text)
            #print(child.text)

        get_all_children(child,boss,lst,glob)





def spacy_analysis(sentence):
    #nlp = spacy.load('en')
    datelist=[]
    timelist=[]
    place_list=[]
    doc = nlp(sentence)
    for ent in doc.ents:
        if ent.label_=="DATE":
            datelist.append(ent.text)
        if ent.label_=="TIME":
            timelist.append(ent.text)
        if ent.label_=="GPE":
            place_list.append(ent.text)


        #print(ent.label_, ent.text)
    print(datelist,timelist,place_list)
    return datelist,timelist,place_list



def collapse_punctuations_and_phrases(doc):
    spans = []
    for word in doc[:-1]:
        if word.is_punct:
            continue
        if not word.nbor(1).is_punct:
            continue
        start = word.i
        end = word.i + 1
        while end < len(doc) and doc[end].is_punct:
            end += 1
        span = doc[start: end]
        spans.append(
            (span.start_char, span.end_char,
             {'tag': word.tag_, 'lemma': word.lemma_, 'ent_type': word.ent_type_})
        )
    for start, end, attrs in spans:
        doc.merge(start, end, **attrs)

    for np in list(doc.noun_chunks):
        np.merge(tag=np.root.tag_, lemma=np.root.lemma_, ent_type=np.root.ent_type_)

    return doc



def get_children(sentences):
    verbs=[]

    all_children_list=[]
#print(s.index("the third week of January"))
    for sentence in sentences:
        children_list=[]
        doc1=nlp(sentence)

        doc1=collapse_punctuations_and_phrases(doc1)
        for token in doc1:
            if token.pos_=="VERB":
                glob=[]


                verbs.append(token.text)


                #print(token.text, token.pos_)

                #for child in token.subtree:
                #   print(child!=token,child.pos_=="VERB")
                #   if child.pos_=="VERB" and child!=token :

                #        break
                #    else:
                #        children_list.append(child.text)
                #print(children_list)

                #print(list(token.children))
                #print("-------------------")
                get_all_children(token,token,[],glob)
                #print(glob)
                children_list.append(glob[0])
                #if bool(glob):
                #    children_list.append(glob[0])
                #else:
                #    children_list.append([])



                #print("---------------------")
        all_children_list.append(children_list)


    #print(all_children_list)
    return all_children_list

#df=pd.read_csv("data/airports_large.csv")
#print(df.head())
#city=df.iloc[:, 2].values

#child_list=[[[],["'s", 'to', 'Delhi', 'in', 'the third week', 'of', 'January', 'and'],['on', 'next Tuesday', 'to', 'Mumbai.']],[['I', 'afternoon filghts.']]]
#verb_list=[['Let', 'go', 'go'], ['prefer']]
#print(city)
#date_time=['the third Monday of January', 'next Tuesday']


def check_for_city(child_list,place_list,date_list,time_list,solution,count):
    city_is_there=False

    for place in place_list:
        for child in child_list:
            if bool(child)==False:
                continue
            else:
                for word in child:
                    if place in word:
                        city_is_there=True
                        solution["case"+str(count)]={}
                        solution["case"+str(count)]["city"]=place
                        alloted_child_date=alot_child(date_list, child_list)

                        alloted_child_time=alot_child(time_list,child_list)

                        for i in range(len(alloted_child_date)):
                            if alloted_child_date[i]==child:
                                solution=check_when(date_list[i],solution,count)
                        for i in range(len(alloted_child_time)):
                            if alloted_child_time[i]==child:
                                solution=check_when(time_list[i],solution,count)

                        count = count + 1

    if city_is_there==False:
        for c in range(len(solution.keys())):
            for dt in date_list:
                solution=check_when(dt,solution,c)

            for tm in time_list:
                solution = check_when(tm, solution, c)











    return solution,count
"""""
{
city:
date:
month:
year:
day:
week:
}
"""""
def check_when(date_string,solution,count):
    print(count)
    for month in month_reference.keys():
        for day in day_reference.keys():

            if month in date_string and ("week" in date_string or day in date_string):
                print(month in date_string , "week" in date_string ,day in date_string)
                for  quantifier in quantifier_reference.keys():
                    if quantifier in date_string:
                        week_no=quantifier_reference[quantifier]
                        break

                    else:
                        week_no=1
                        continue
                print(week_no)
                month_no=month_reference[month]
                print(month_no)

                print(week_no)
                if day in date_string:
                    print(day)
                    try:
                        solution["case" + str(count)]["date"]=str(get_date_from_week_no(week_no=week_no,weekday=day_reference[day],month_no=month_no))
                    except:
                        print("The date you are looking for does not exist")
                        solution["case" + str(count)]["date"]="DNE"


                    print(count)
                    print(solution["case" + str(count)]["date"])
                else:
                    try:
                        solution["case" + str(count)]["date"]=str(get_date_from_week_no(week_no=week_no,month_no=month_no))
                    except:
                        print("The date you are looking for does not exist")
                        solution["case" + str(count)]["date"] = "DNE"


                return solution



            else:
                continue

    time_struct, parse_status = cal.parse(date_string)
    if parse_status==1:
        solution["case" + str(count)]["date"]=str(datetime(*time_struct[:6]).date())
    elif parse_status==2:
        solution["case"+str(count)]["time"]=str(datetime(*time_struct[:6]).time())
    elif parse_status==3:
        solution["case" + str(count)]["date"] = str(datetime(*time_struct[:6]).date())
        solution["case"+str(count)]["time"]=str(datetime(*time_struct[:6]).time())



    return solution





def get_date_from_week_no(week_no,weekday=6,month_no=0):

    min_day=7*(week_no-1)+1
    max_day=7*(week_no)+1

    for day in range(min_day,max_day):
        date_str=str(2018)+"-"+str(month_no)+"-"+str(day)
        date=datetime.strptime(date_str,"%Y-%m-%d")
        if date.weekday()==weekday:
            return date.date()
        else:
            continue










def alot_child(date_time,child_list):
    output=[]
    for dt_tm in date_time:

        max_char_match = -2

        for children in child_list:
            char_match = 0
            for child in children:
                child=child.rstrip(string.punctuation)

                if child in dt_tm:

                    char_match=char_match+len(child)

                else:
                    continue
            if char_match>max_char_match:
                max_char_match=char_match
                temp=children
            else:
                continue
        output.append(temp)
    return output

#print(alot_child(date_time,child_list[0]))




#def check_when(date_list,time_list,solution,count,child):





def solve():
    solution={}
    child_list = get_children(sentences)
    count=0
    for i in range(len(sentences)):
        date_list,time_list,place_list=spacy_analysis(sentences[i])

        solution,count=check_for_city(child_list[i],place_list,date_list,time_list,solution,count)
        print(solution)
        print(count)



solve()
#print(get_children(["Let's go to Delhi after two days."]))











#print(deduce_when())
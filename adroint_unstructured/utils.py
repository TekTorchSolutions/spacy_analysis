from datetime import datetime
import string
from datetime import date
import parsedatetime
import pandas as pd


cal = parsedatetime.Calendar()

quantifier_reference={"first":1,"second":2,"third":3,"fourth":4,"fifth":5}
month_reference={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
time_entities=["week","month","year"]
time_jump=["after","next","tomorrow"]
time_duration=["morning","evening","afternoon","night"]
text_to_int={"one":1,"two":2,"three":3,"four":4,"five":5,"six":6}
day_reference={"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6}



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


def get_place_list():
    df = pd.read_csv("data/airports_large.csv")
    place_list=df.iloc[:, 2].values
    place_list = [x for x in place_list if str(x) != 'nan']

    place_list=list(set(place_list))
    return place_list



def check_for_city(child_list,place_list,date_list,time_list,solution,count):
    city_is_there=False
    for child in child_list:
        print(child)
        found_a_city = False
        for place in place_list:



            if bool(child)==False:
                continue
            else:
                for word in child:
                    #print(place)
                    if place in word:
                        if found_a_city==False:
                            print(place)
                            print(count)
                            print(found_a_city)

                            found_a_city=True
                            city_is_there=True
                            solution["case"+str(count)]={}
                            solution["case"+str(count)]["destination"]=place
                            alloted_child_date = alot_child(date_list, child_list)

                            alloted_child_time = alot_child(time_list, child_list)

                            for i in range(len(alloted_child_date)):
                                if alloted_child_date[i] == child:
                                    solution = check_when(date_list[i], solution, count)
                            for i in range(len(alloted_child_time)):
                                if alloted_child_time[i] == child:
                                    solution = check_when(time_list[i], solution, count)

                            count = count + 1
                        else:
                            print(place)
                            print(count)
                            print(found_a_city)
                            solution["case" + str(count-1)]["source"] = solution["case" + str(count-1)].pop("destination")
                            solution["case" + str(count-1)]["destination"] = place
                            break




    if city_is_there==False:
        for c in range(len(solution.keys())):
            for dt in date_list:
                solution=check_when(dt,solution,c)

            for tm in time_list:
                solution = check_when(tm, solution, c)











    return solution,count


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

def check_when(date_string,solution,count):
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
                month_no=month_reference[month]
                if day in date_string:
                    try:
                        solution["case" + str(count)]["date"]=str(get_date_from_week_no(week_no=week_no,weekday=day_reference[day],month_no=month_no))
                    except:
                        print("The date you are looking for does not exist")
                        solution["case" + str(count)]["date"]="DNE"

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



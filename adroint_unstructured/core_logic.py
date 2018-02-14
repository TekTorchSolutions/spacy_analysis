
import en_core_web_sm
import parsedatetime
from adroint_unstructured.utils import collapse_punctuations_and_phrases,check_for_city,get_place_list
cal = parsedatetime.Calendar()

nlp = en_core_web_sm.load()

"""
#s="Let's go to Delhi in the third week of January and on next Tuesday go to Mumbai.I prefer afternoon filghts."
s="I want to go to Delhi.Planning to travel next Monday.I prefer travelling at night."
#s="Let's visit Delhi tomorrow night at 10pm."
m="Let's go to Delhi after two days."
"""

def create_sentences(text):
    doc2=nlp(text)
    sentences = [sent.string.strip() for sent in doc2.sents]

    return sentences

def get_all_children(token,boss,lst,glob):

    if list(token.children)==[] or (token.pos_=="VERB" and token!=boss):

        glob.append(lst)
        return
    for child in list(token.children):
        if child.pos_!="VERB":
            lst.append(child.text)

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
    #print(datelist,timelist,place_list)
    return datelist,timelist




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





def solve(text):

    sentences=create_sentences(text)
    solution={}
    child_list = get_children(sentences)
    count=0
    for i in range(len(sentences)):
        date_list,time_list=spacy_analysis(sentences[i])
        place_list=get_place_list()

        solution,count=check_for_city(child_list[i],place_list,date_list,time_list,solution,count)


    return solution












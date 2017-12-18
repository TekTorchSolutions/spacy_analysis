import spacy
nlp = spacy.load('en')
article = '''
let's go to delhi in the afternoon on monday next week.

'''
doc = nlp(article)
for ent in doc.ents:
   print(ent.label_, ent.text)
import spacy
nlp = spacy.load('en')
article = '''
Hi

Please book the following tickets for

 Jasdeep Singh
Mrs JUTTA GROENING

5-Nov-2017     Mum – Ahm – Indigo – 7:35am arrv 8:50
5-Nov-2017     Ahm – Mum – Indigo – 18:40 – arrv 20:05

Regards
Maryann


Dear Venessa,

Please provide me below details :

Name : Mohd Mohtashim
Delhi to Lucknow 16/11/2017 Evening between 16:00 to 18:00
Lucknow to Delhi 18/11/2017 Noon between 12:00 to 15:00

Thanks & Regards,
Rupa Bhatt

'''
doc = nlp(article)
for ent in doc.ents:
   print(ent.label_, ent.text)
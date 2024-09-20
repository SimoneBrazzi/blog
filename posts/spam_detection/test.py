import pandas as pd
import numpy as np
import spacy
import nltk
import string
from nltk.corpus import stopwords

nltk.download('stopwords')

file = "~/R/blog/posts/toxic_comment_filter/spam_dataset.csv"
df = pd.read_csv(file, index_col=0)

stop_words = stopwords.words('english')
nlp = spacy.load("en_core_web_lg")

doc = list(nlp.pipe(df.text))

lemmas = [[t.lemma_ for t in d if not t.is_punct and t.text.lower() != "subject" and not t.is_stop and not t.is_space and len(t.text) >= 3] for d in doc]

df["lemmas"] = lemmas

ent = [[t.text for t in d if not t.is_punct and t.text.lower() != "subject" and not t.is_stop and not t.is_space and len(t.text) >= 3 and str(t.ent_type_) == "ORG"] for d in doc]
df["ent"] = ent

ham = df[df.label == "ham"]
x = ent

d = {}
for i in ["apple", "orange", "pineapple", "apple"]:
  if i in d:
    d[i] += 1
  else:
    d[i] = 1









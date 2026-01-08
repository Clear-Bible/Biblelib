"""Create a spaCy Corpus and Doc instances."""

import spacy
from spacy.training import Corpus
from spacy.tokens import Doc, DocBin
import pandas as pd

from biblelib import

# Load your model
nlp = spacy.blank("en")  # or spacy.load("en_core_web_sm")

# Read the TSV file
df = pd.read_csv("tokens.tsv", sep="\t")

# Example: assume columns are ["doc_id", "token"]
# Group tokens by document
documents = df.groupby("doc_id")["token"].apply(list)

# Create Doc objects
docs = []
for tokens in documents:
    doc = Doc(nlp.vocab, words=tokens)
    docs.append(doc)

# Option 1: Use a DocBin if you want to serialize
doc_bin = DocBin(docs=docs)

# Option 2: Directly create a spaCy Corpus
corpus = Corpus.from_docs(docs)

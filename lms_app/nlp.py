import spacy

print("Loading spacy model")
nlp = spacy.load('en_core_web_sm')
print("Spacy model was loaded successfully")

def get_sentences(text):
    tokens = nlp(text)
    return [sent.text.strip() for sent in tokens.sents]
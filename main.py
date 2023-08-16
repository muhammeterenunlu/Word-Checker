import spacy
import string
from docx import Document
from spellchecker import SpellChecker

#
# SpaCy modelini yükleme
nlp = spacy.load("en_core_web_sm")

def split_text(text):
    words = text.split()
    cleaned_words = []
    for word in words:
        cleaned_word = word.strip(string.punctuation)
        cleaned_words.append(cleaned_word.lower())  # Küçük harfe dönüştürülüyor
    return cleaned_words

def extract_proper_nouns(text):
    """Metinden özel isimleri çıkarma."""
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ == "PROPN"]

def correct_word_doc(file_path):
    doc = Document(file_path)
    spell = SpellChecker(language='en')

    corrections_log = []

    for paragraph in doc.paragraphs:
        proper_nouns = extract_proper_nouns(paragraph.text)
        words = split_text(paragraph.text)
        misspelled = spell.unknown(words)

        for word in misspelled:
            if word in proper_nouns or word.capitalize() in proper_nouns:  # Özel isimleri atla
                continue

            correction = spell.correction(word)
            if word.istitle():
                correction = correction.capitalize()

            corrections_log.append(f"'{word}' -> '{correction}'")

            for run in paragraph.runs:
                if word in run.text:
                    run.text = run.text.replace(word, correction)

    corrected_file_path = "corrected_" + file_path
    doc.save(corrected_file_path)

    return corrected_file_path, corrections_log

corrected_path, corrections = correct_word_doc("test.docx")

print(f"Corrections made and the new file saved at: {corrected_path}\n")
print("Corrections:")
for entry in corrections:
    print(entry)

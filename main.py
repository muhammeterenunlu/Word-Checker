from spellchecker import SpellChecker
import string

def split_text(text):
    words = text.split()
    cleaned_words = []
    for word in words:
        is_title = word.istitle()
        cleaned_word = word.strip(string.punctuation).lower()
        cleaned_words.append((cleaned_word, is_title))
    return cleaned_words

def correct_word_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    spell = SpellChecker(language='en')
    words = split_text(content)
    unique_words = {word[0] for word in words}
    misspelled = spell.unknown(unique_words)

    corrections_log = []

    for word_tuple in words:
        word = word_tuple[0]
        is_title = word_tuple[1]

        if word in misspelled:
            correction = spell.correction(word)

            # Eğer kelime cümlede büyük harfle başlıyorsa, düzeltmeyi büyük harfle yapalım
            if is_title:
                word = word.capitalize()
                correction = correction.capitalize()

            corrections_log.append(f"'{word}' -> '{correction}'")
            content = content.replace(word, correction)

    corrected_file_path = "corrected_" + file_path
    with open(corrected_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    return corrected_file_path, corrections_log

corrected_path, corrections = correct_word_txt("test.txt")

print(f"Corrections made and the new file saved at: {corrected_path}\n")
print("Corrections:")
for entry in corrections:
    print(entry)

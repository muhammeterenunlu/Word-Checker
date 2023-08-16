from transformers import BertTokenizer, BertForMaskedLM
import torch
from spellchecker import SpellChecker

# Model ve tokenize ediciyi yükle
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased').eval()
spell = SpellChecker()

def correct_with_bert(sentence):
    words = sentence.split()
    corrected_sentence = sentence

    for word in words:
        # SpellChecker ile kontrol edelim
        if spell.unknown([word]):
            masked_sentence = corrected_sentence.replace(word, "[MASK]", 1)  # Sadece ilk rastladığımızı değiştiriyoruz
            tokenized = tokenizer(masked_sentence, return_tensors="pt")
            with torch.no_grad():
                output = model(**tokenized)
            predictions = output.logits[0][tokenized["input_ids"][0] == tokenizer.mask_token_id]
            predicted_token = torch.argmax(predictions).item()
            corrected_sentence = corrected_sentence.replace(word, tokenizer.decode([predicted_token]), 1)  # İlk rastladığımızı değiştiriyoruz

    return corrected_sentence

text = """Hello everyone. My name is Jon. I'm from the Unites States. I have a deadline for my assignment tomorrow. I'm tring to finish it in time. By the way, I went to the Clifornia last summer. It was a wonderful trip. The pacific can is so beautiful."""

corrected_text = correct_with_bert(text)
print(corrected_text)
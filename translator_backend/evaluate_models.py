# backend/evaluate_models.py
# Usage: python evaluate_models.py
from transformers import MarianMTModel, MarianTokenizer
from deep_translator import GoogleTranslator
import sacrebleu
import time

# Example parallel sentences (small sample). Replace with a proper testset for real BLEU.
pairs = [
    ("Hello, how are you?", "नमस्ते, आप कैसे हैं?"),
    ("I love programming.", "मुझे प्रोग्रामिंग पसंद है।"),
    ("This is a test sentence.", "यह एक परीक्षण वाक्य है।")
]

# Configure HF model for en->hi
hf_model_name = "Helsinki-NLP/opus-mt-en-hi"
tokenizer = MarianTokenizer.from_pretrained(hf_model_name)
model = MarianMTModel.from_pretrained(hf_model_name)

def hf_translate(texts):
    batch = tokenizer.prepare_seq2seq_batch(texts, return_tensors="pt")
    gen = model.generate(**batch)
    return tokenizer.batch_decode(gen, skip_special_tokens=True)

def google_translate(texts, target="hi"):
    out = []
    for t in texts:
        out.append(GoogleTranslator(source="auto", target=target).translate(t))
    return out

src_texts = [p[0] for p in pairs]
refs = [[p[1] for p in pairs]]  # sacrebleu wants list-of-list for references

# HF
start = time.time()
hf_out = hf_translate(src_texts)
hf_time = time.time() - start

# Google
start = time.time()
g_out = google_translate(src_texts, target="hi")
g_time = time.time() - start

print("HF outputs:", hf_out)
print("Google outputs:", g_out)

hf_bleu = sacrebleu.corpus_bleu(hf_out, refs)
g_bleu = sacrebleu.corpus_bleu(g_out, refs)

print(f"HF BLEU: {hf_bleu.score:.2f}, time: {hf_time:.2f}s")
print(f"Google BLEU: {g_bleu.score:.2f}, time: {g_time:.2f}s")

# bleu_eval.py
from deep_translator import GoogleTranslator
from sacrebleu import corpus_bleu

# Sample test dataset
# Reference sentences must be HUMAN translation
# Hypothesis will be model translation
test_data = [
    ("Hello, how are you?", "नमस्ते, आप कैसे हैं?"),
    ("Where is the nearest hospital?", "सबसे नजदीकी अस्पताल कहाँ है?"),
    ("I want to learn artificial intelligence.", "मैं कृत्रिम बुद्धिमत्ता सीखना चाहता हूँ।"),
    ("What is your name?", "आपका नाम क्या है?"),
    ("This system translates text in real-time.", "यह प्रणाली वास्तविक समय में पाठ का अनुवाद करती है।"),
]

def evaluate_bleu(model="google", source_lang="en", target_lang="hi"):
    references = []
    hypotheses = []

    for src, ref in test_data:
        # Add human reference
        references.append(ref)

        # Get model translation
        translated = GoogleTranslator(source="auto", target=target_lang).translate(src)
        hypotheses.append(translated)

    # Evaluate BLEU score
    bleu = corpus_bleu(hypotheses, [references])
    return bleu.score

if __name__ == "__main__":
    score = evaluate_bleu()
    print("====================================")
    print(f"BLEU Score (GoogleTranslator en→hi): {score:.2f}")
    print("====================================")

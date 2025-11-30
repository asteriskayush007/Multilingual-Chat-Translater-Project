# translator_backend/optimize_translation.py
import time
import json
import random
from statistics import mean
from typing import List

import sacrebleu
import optuna  # for Bayesian search
from transformers import MarianTokenizer, MarianMTModel

# --- CONFIG ---
HF_MODEL = "Helsinki-NLP/opus-mt-en-hi"  # change to model you use
VAL_SRC = [
    "Hello, how are you?",
    "I love programming.",
    "Where is the nearest hospital?",
    "What is your name?",
    "This system translates text in real-time.",
    "Can you help me?",
    "I want to learn artificial intelligence.",
    "Please send me the file.",
    "How much does it cost?",
    "Good night and sweet dreams."
]
VAL_REF = [
    "नमस्ते, आप कैसे हैं?",
    "मुझे प्रोग्रामिंग पसंद है।",
    "सबसे नजदीकी अस्पताल कहाँ है?",
    "आपका नाम क्या है?",
    "यह प्रणाली वास्तविक समय में पाठ का अनुवाद करती है।",
    "क्या आप मेरी मदद कर सकते हैं?",
    "मैं कृत्रिम बुद्धिमत्ता सीखना चाहता हूँ।",
    "कृपया मुझे फ़ाइल भेजें।",
    "यह कितना खर्च होता है?",
    "शुभ रात्रि और मीठे सपने।"
]

# --- load HF model once
tokenizer = MarianTokenizer.from_pretrained(HF_MODEL)
model = MarianMTModel.from_pretrained(HF_MODEL)
model.eval()

def translate_batch(texts: List[str], num_beams=4, max_length=80, length_penalty=1.0, no_repeat_ngram_size=0, early_stopping=True):
    batch = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    start = time.perf_counter()
    gen = model.generate(
        **batch,
        num_beams=num_beams,
        max_length=max_length,
        length_penalty=length_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        early_stopping=early_stopping,
    )
    end = time.perf_counter()
    outputs = tokenizer.batch_decode(gen, skip_special_tokens=True)
    latency_ms = (end - start) * 1000.0
    return outputs, latency_ms

def evaluate_params(params):
    # params: dict with num_beams, max_length, length_penalty, no_repeat_ngram_size
    # Translate validation set in small batches
    preds = []
    latencies = []
    batch_size = 5
    for i in range(0, len(VAL_SRC), batch_size):
        batch_src = VAL_SRC[i:i+batch_size]
        out, ms = translate_batch(
            batch_src,
            num_beams=params["num_beams"],
            max_length=params["max_length"],
            length_penalty=params["length_penalty"],
            no_repeat_ngram_size=params["no_repeat_ngram_size"],
            early_stopping=True
        )
        preds.extend(out)
        latencies.append(ms)
    avg_latency = mean(latencies)
    bleu = sacrebleu.corpus_bleu(preds, [VAL_REF]).score
    return bleu, avg_latency, preds

# -------------------------
# 1) Grid search example (small)
# -------------------------
def run_grid_search():
    grid = {
        "num_beams": [1, 2, 4],
        "max_length": [60, 80],
        "length_penalty": [0.6, 1.0],
        "no_repeat_ngram_size": [0, 2]
    }

    best = {"score": -1e9, "params": None, "bleu": 0, "latency": None}
    import itertools
    keys = list(grid.keys())
    for vals in itertools.product(*[grid[k] for k in keys]):
        params = dict(zip(keys, vals))
        bleu, lat, preds = evaluate_params(params)
        # define score: BLEU minus alpha*latency_seconds
        alpha = 0.05
        score = bleu - alpha * (lat / 1000.0)
        print("Grid try:", params, "BLEU:", bleu, "lat(ms):", round(lat,2), "score:", round(score,3))
        if score > best["score"]:
            best.update({"score": score, "params": params, "bleu": bleu, "latency": lat})
    print("Grid best:", best)
    with open("best_grid.json", "w") as f:
        json.dump(best, f, indent=2)

# -------------------------
# 2) Random search example
# -------------------------
def run_random_search(trials=20):
    best = {"score": -1e9, "params": None}
    for t in range(trials):
        params = {
            "num_beams": random.choice([1,2,4,6]),
            "max_length": random.choice([50,60,80,100]),
            "length_penalty": random.choice([0.6,0.8,1.0,1.2]),
            "no_repeat_ngram_size": random.choice([0,1,2,3])
        }
        bleu, lat, preds = evaluate_params(params)
        alpha = 0.05
        score = bleu - alpha * (lat / 1000.0)
        print(f"Random {t+1}/{trials}:", params, "BLEU:", round(bleu,2), "lat_ms:", round(lat,2), "score:", round(score,3))
        if score > best["score"]:
            best.update({"score": score, "params": params, "bleu": bleu, "latency": lat})
    print("Random best:", best)
    with open("best_random.json", "w") as f:
        json.dump(best, f, indent=2)

# -------------------------
# 3) Optuna Bayesian search (recommended)
# -------------------------
def optuna_objective(trial):
    params = {
        "num_beams": trial.suggest_categorical("num_beams", [1,2,4,6,8]),
        "max_length": trial.suggest_int("max_length", 40, 140, step=10),
        "length_penalty": trial.suggest_float("length_penalty", 0.6, 1.5),
        "no_repeat_ngram_size": trial.suggest_int("no_repeat_ngram_size", 0, 3)
    }
    bleu, lat, preds = evaluate_params(params)
    # We maximize BLEU but also penalize latency, so return negative of combined loss
    alpha = 0.05
    score = bleu - alpha * (lat / 1000.0)
    # Optuna maximizes objective by returning a number; return score
    return score

def run_optuna(study_name="translation_opt", n_trials=30):
    study = optuna.create_study(direction="maximize", study_name=study_name)
    study.optimize(optuna_objective, n_trials=n_trials)
    print("Best trial:", study.best_trial.params, "value:", study.best_value)
    with open("best_optuna.json", "w") as f:
        json.dump({"params": study.best_trial.params, "value": study.best_value}, f, indent=2)

# -------------------------
# CLI
# -------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["grid","random","optuna"], default="optuna")
    parser.add_argument("--trials", type=int, default=30)
    args = parser.parse_args()

    if args.mode == "grid":
        run_grid_search()
    elif args.mode == "random":
        run_random_search(args.trials)
    else:
        run_optuna(n_trials=args.trials)

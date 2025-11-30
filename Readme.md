# 📌 **Realtime Multilingual Chat**
**By: Ayushmaan Singh Yadav**

A real-time multilingual chat system supporting auto-translation, per-user language preference, latency measurement, BLEU evaluation, and chat download feature.  
The system is built using **FastAPI**, **WebSockets**, **React**, **TailwindCSS**, **Framer Motion**, and **Deep-Translator (Google Translation API wrapper)**.

---

# 🚀 **Project Highlights**
- ⚡ **Real-time chat** using WebSockets (FastAPI backend)
- 🌐 **Live translation** (GoogleTranslator)
- 👤 **Per-user language preference**
- 🧠 **Auto-detect + manual language selection**
- ⏱ **Latency measurement per message (ms)**
- 📊 **BLEU evaluation (GoogleTranslator BLEU = 68.78)**
- 🌑 **Dark/Light theme support**
- 📥 **Download full chat as an image (html2canvas)**
- 🌀 **Smooth UI animations (Framer Motion)**
- 🔄 **Stable WebSocket reconnection**
- 🧪 **Baseline model comparison (Helsinki-NLP MarianMT)**

---

# 📂 **Project Structure**
```
Realtime-Multilingual-Chat/
│── translator_backend/
│   ├── main.py
│   ├── bleu_eval.py
│   ├── evaluate_models.py
│   ├── requirements.txt
│   └── .env (optional)
│
│── translator_ui/
│   ├── src/components/
│   │   ├── ChatBox.jsx
│   │   └── Sidebar.jsx
│   ├── public/
│   └── package.json
│
└── README.md
```

---

# 🛠 **Tech Stack**
### **Backend**
- FastAPI  
- WebSockets  
- Deep-Translator  
- GoogleTranslator  
- SacreBLEU  
- Transformers  
- MarianMT  
- Python 3.10  

### **Frontend**
- React.js  
- TailwindCSS  
- Framer Motion  
- html2canvas  
- WebSockets  

---

## 🧠 Model Explainability (LIME & SHAP)

Although this project is mainly focused on **text translation**, we included a small **text classification demo model** to showcase explainability techniques.
This helps reviewers understand how AI decisions can be interpreted in real-world NLP systems.

We implemented **two explainability tools**:

---

# 🔷 1. SHAP (SHapley Additive Explanations)

SHAP helps us understand **which words contribute most** to a prediction.

### 📌 How SHAP Works in Our Project

1. A small Logistic Regression model is trained on example sentences:

   * Positive class
   * Negative class
2. SHAP analyzes each word’s contribution.
3. It generates a local explanation plot showing:

   * 🔵 Words pushing prediction UP
   * 🔴 Words pushing prediction DOWN

### ▶️ Run SHAP Demo

```bash
cd translator_backend/explainability
python3 shap_demo.py
```

### 📤 Output

* SHAP force plot saved as:

```
shap_output.png
```

---

# 🔶 2. LIME (Local Interpretable Model-Agnostic Explanations)

LIME highlights **which words influenced the final prediction** for a given input sentence.

### 📌 How LIME Works in Our Project

1. Uses the same small classification model.
2. Perturbs the input text.
3. Checks how output changes.
4. Creates a feature-importance table.

### ▶️ Run LIME Demo

```bash
cd translator_backend/explainability
python3 lime_demo.py
```

### 📤 Output

* LIME explanation saved as:

```
lime_output.html
```

(You can open it directly in a browser.)

---

# 📁 File Structure

```
translator_backend/
   └── explainability/
           ├── shap_demo.py
           ├── lime_demo.py
           ├── shap_output.png
           └── lime_output.html
```

---

# 🎯 Why Add Explainability?

Even though the core project is a **translation system**, explainability is:

* ✔ Mandatory for many academic + company evaluations
* ✔ Shows you understand ML ethics & transparency
* ✔ Demonstrates ability to justify model predictions
* ✔ Provides depth to your overall submission


---

# 📸 **Screenshots**
(Add your screenshots here manually)


![Chat Screenshot](images/ChatA.png)
![Chat Screenshot](images/ChatB.png)
![Latency](images/Latency.png)
![Lime Model](images/lime.png)
![Shap Model](images/Shap.png)
![BLEU Score](images/BLEU.png)


---

## 🔧 Translation Model Optimization (BLEU + Latency)

To improve the overall translation quality and responsiveness of the system, we performed
**Hyperparameter Optimization** using three different strategies:

### 1. Grid Search  
Exhaustively tested all possible combinations of:
- `num_beams = [1, 2, 4]`
- `max_length = [60, 80]`
- `length_penalty = [0.6, 1.0]`
- `no_repeat_ngram_size = [0, 2]`

**Best Grid Result**
- **num_beams:** 2  
- **max_length:** 60  
- **length_penalty:** 1.0  
- **no_repeat_ngram_size:** 0  
- **BLEU Score:** 16.47  
- **Latency:** ~257 ms  

---

### 2. Random Search (30 Trials)
Randomly sampled from a wider search space for:
- `num_beams = 1–6`
- `max_length = 50–120`
- `length_penalty = 0.6–1.2`
- `no_repeat_ngram_size = 0–3`

**Best Random Search Result**
- **num_beams:** 2  
- **max_length:** 100  
- **length_penalty:** 1.2  
- **no_repeat_ngram_size:** 1  
- **BLEU:** 16.47  
- **Latency:** ~255 ms  

---

### 3. Bayesian Optimization (Optuna — 40 Trials)
Used Optuna to automatically explore the best balance between:
- Translation accuracy (BLEU)
- Speed (Latency)
- Model stability

**Best Optuna Result**
- **num_beams:** 2  
- **max_length:** 110  
- **length_penalty:** 0.79  
- **no_repeat_ngram_size:** 2  
- **Final Score:** 16.458  
- **Latency:** ~254 ms  

---

### 📌 Summary: Optimal Hyperparameters (Final Recommended)
Based on all experiments:

| Parameter              | Best Value |
|-----------------------|-----------|
| **num_beams**         | 2 |
| **max_length**        | 100–110 |
| **length_penalty**    | 0.8–1.2 |
| **no_repeat_ngram_size** | 1–2 |

These settings provide the **best trade-off between translation quality (BLEU) and speed (Latency)** for real-time WebSocket chat translation.



---

# ⚙️ **Setup Instructions**

## 1️⃣ Backend Setup (FastAPI)

### **Step 1: Create Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **requirements.txt**
```
fastapi
uvicorn[standard]
deep-translator
transformers
torch
sacrebleu
langdetect
python-multipart
python-dotenv
```

### **Step 3: Run Backend**
```bash
uvicorn main:app --reload
```

Backend runs at:  
📍 **http://127.0.0.1:8000**

---

# 2️⃣ **Frontend Setup (React)**

```bash
cd translator_ui
npm install
npm start
```

Runs at  
📍 **http://localhost:3000**

---

# 🧠 **Model Evaluation**

### ✔ **BLEU Evaluation**
Run:
```bash
python bleu_eval.py
```
Output:
```
BLEU Score (GoogleTranslator en→hi): 68.78
```

---

### ✔ **Model Comparison (HF MarianMT vs Google)**
Run:
```bash
python evaluate_models.py
```

Shows:
- Model translation outputs  
- Inference time  
- BLEU scores  

---

# ⏱ **Latency Measurement**
Each message payload includes latency:

```json
{
  "sender": "A",
  "original": "Hello!",
  "translated": "नमस्ते!",
  "latency": 142.33,
  "timestamp": 1732855511.27
}
```

Displayed in the UI per message.

---

# 🌐 **WebSocket API**

### **URL**
```
ws://127.0.0.1:8000/ws/{user}
```

### **Set Preferred Language**
```json
{ "type": "set_lang", "lang": "hi" }
```

### **Send Chat Message**
```json
{
  "type": "message",
  "text": "Hello",
  "translate": true
}
```

---

# 🚀 **Deployment Guide**

### **Option 1: Render / Railway**
- Deploy FastAPI backend  
- Deploy React frontend

### **Option 2: Docker**
Dockerfile + docker-compose can be added (ask me).

### **Option 3: Nginx Reverse Proxy**
For production WebSocket stability.

---

# 🎥 **Optional Demo Video**
3–5 minutes video covering:
- Architecture  
- Real-time translation  
- BLEU score  
- Latency  
- Full UI demo  

---

# 📝 **Author**
**Ayushmaan Singh Yadav**  
Realtime Multilingual Chat — 2025

---


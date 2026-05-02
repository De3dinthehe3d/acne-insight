# 🌸 Acne Insight & Skincare Advisor

An ML-powered web application that classifies acne type based on skin profile and lifestyle inputs, then provides personalised cause analysis, ingredient recommendations, and skincare routines.

> **No deep learning. No images. No gimmicks. Just solid ML + domain logic.**

---

## 🗂️ Project Structure

```
acne_project/
│
├── data/
│   └── acne_dataset.csv          # Training dataset (600 rows)
│
├── models/                        # Auto-generated after training
│   ├── acne_rf_model.pkl
│   ├── label_encoders.pkl
│   └── feature_cols.pkl
│
├── src/
│   ├── train_model.py             # Trains + saves the Random Forest model
│   └── predictor.py               # Prediction + cause analysis + recommendations
│
├── notebooks/
│   └── eda.ipynb                  # Exploratory Data Analysis (optional)
│
├── app.py                         # Gradio UI — main entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the model (run once)
```bash
python src/train_model.py
```
This saves the trained model to the `models/` directory.

### 3. Launch the app
```bash
python app.py
```
Open your browser at `http://localhost:7860`

---

## 🧠 ML Architecture

| Component | Detail |
|---|---|
| **Algorithm** | Random Forest Classifier |
| **Features** | Skin type, acne location, severity, sleep, water, stress, diet, exercise, sweat |
| **Target** | Acne type: Hormonal / Fungal / Bacterial / Lifestyle |
| **Balancing** | `class_weight='balanced'` + stratified split |
| **Extras** | Rule-based cause analysis, severity scoring formula |

---

## 📊 Dataset Notes

- 600 synthetic rows generated using domain-informed rules
- Class distribution: Lifestyle 35% · Hormonal 25% · Bacterial 20% · Fungal 20%
- Logical consistency enforced (e.g. back acne + high sweat → fungal)

---

## 🚀 Deployment on Hugging Face Spaces

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select **Gradio** as the SDK
3. Upload all project files
4. The Space auto-runs `app.py`

> **Important:** Run `train_model.py` locally first and upload the `models/` folder.
> Hugging Face Spaces does not run training scripts automatically.

---

## ⚠️ Disclaimer

This tool is for educational purposes only. It does not replace professional dermatological advice.

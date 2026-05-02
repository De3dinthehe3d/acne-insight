"""
app.py — Professional 🌸 Acne Insight (User-Centric Version)
Theme: Light Brownish / Nude Aesthetic
"""
import tempfile
import sys, os
from predictor import predict
import gradio as gr

# ── LOGIC CONSTANTS ──────────────────────────────────────────────────────────
# Descriptive labels instead of just numbers for Severity
SEVERITY_LABELS = {1: "Mild", 2: "Moderate", 3: "Severe"}

TYPE_EMOJI  = {
    "hormonal":  "⚡ Hormonal Acne",
    "fungal":    "🍄 Fungal Acne",
    "bacterial": "🦠 Bacterial Acne",
    "lifestyle": "🌿 Lifestyle-Related Acne",
}

# ── PROFESSIONAL CSS ─────────────────────────────────────────────────────────
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Playfair+Display:wght@700&display=swap');

/* ── LIGHT MODE DEFAULTS ── */
:root {
  --terra: #c4714a;
  --terra-dark: #a85a36;
  --bg: #f8f2ed;
  --card-bg: #ffffff;
  --text: #2d1b0e;
  --text-muted: #6b5244;
  --border: #e8dcd0;
  --input-bg: #ffffff;
}

/* ── DARK MODE OVERRIDES ── */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #111111;
    --card-bg: #1e1e1e;
    --text: #f0f0f0;
    --text-muted: #aaaaaa;
    --border: #333333;
    --input-bg: #2a2a2a;
  }
}

html, body {
    background-color: var(--bg) !important;
    min-height: 100vh;
}

/* Gradio container adapts to mode */
.gradio-container {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* All component blocks */
.gradio-container .block,
.gradio-container .form,
.gradio-container .wrap,
.gradio-container .panel,
.gradio-container fieldset {
    background-color: var(--card-bg) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}

/* Labels */
.gradio-container label,
.gradio-container .label-wrap span,
.gradio-container span.svelte-1p9xokt {
    color: var(--text) !important;
}

/* Inputs, dropdowns, selects */
.gradio-container select,
.gradio-container input,
.gradio-container textarea,
.gradio-container .wrap-inner {
    background-color: var(--input-bg) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
}

/* Tab buttons */
.gradio-container .tabs > .tab-nav button {
    color: var(--text-muted) !important;
    background: transparent !important;
}
.gradio-container .tabs > .tab-nav button.selected {
    color: var(--terra) !important;
    border-bottom-color: var(--terra) !important;
}

/* Markdown */
.gradio-container .prose,
.gradio-container .prose * {
    color: var(--text) !important;
}

.wizard-card {
    background: var(--card-bg) !important;
    border-radius: 25px !important;
    padding: 35px !important;
    box-shadow: 0 20px 45px rgba(0,0,0,0.12) !important;
    border: 1px solid var(--border) !important;
    max-width: 900px !important;
    margin: 20px auto !important;
}

.hero-title {
    font-family: 'Playfair Display', serif !important;
    color: var(--text) !important;
    font-size: 2.8rem !important;
    text-align: center;
    margin-top: 1rem !important;
}

.primary-btn {
    background: linear-gradient(135deg, var(--terra) 0%, var(--terra-dark) 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 15px !important;
    font-weight: 700 !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer;
}
"""
def save_report(html_content):
    file_path = tempfile.mktemp(suffix=".html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return file_path

def run_prediction(skin_type, acne_location, severity, sleep_hours,
                   water_intake, stress_level, diet_type, exercise, sweat_level):
    
    u = {
        "skin_type": skin_type,
        "acne_location": acne_location,
        "severity": int(severity),
        "sleep_hours": int(round(sleep_hours)),          
        "water_intake_liters": round(float(water_intake), 1),
        "stress_level": int(round(stress_level)),
        "diet_type": diet_type,
        "exercise": exercise,
        "sweat_level": int(round(sweat_level)),
    }

    r = predict(u)

    acne_label = TYPE_EMOJI.get(r["acne_type"], r["acne_type"].title())

    # ── IMPROVED METRICS ──
    strength = f"{r['confidence']}%"
    strength_label = "Confidence in Analysis"

    score = r['severity_score']
    if score <= 3:
        severity_text = "Mild"
    elif score <= 7:
        severity_text = "Moderate"
    else:
        severity_text = "High"

    display_severity = f"{severity_text} ({score}/10)"
    severity_label = "Overall Intensity (Based on all factors)"

    TERRA = "#c4714a"

    # ── WHY THIS IS HAPPENING ──
    causes_html = ""
    if "causes" in r:
        causes_html = """
        <h3 style="border-bottom:1px solid var(--border,#e0d0c8); padding-bottom:5px;">🔍 Why This Is Happening</h3>
        <ul style="line-height:1.8; padding-left:20px;">
        """
        for c in r["causes"]:
            causes_html += f"<li style='margin-bottom:5px;'>{c}</li>"
        causes_html += "</ul>"

    # ── EMOTIONAL INSIGHT ──
    insight = f"""
    <p style="font-size:1rem; margin-bottom:20px; opacity:0.85;">
    Your skin is currently reacting mainly due to <b>{r['top_factor'].lower()}</b>.
    The good news? This is manageable with consistent care and small lifestyle adjustments.
    </p>
    """

    # ── BUILD REPORT HTML ──
    # No hardcoded colors — inherits from Gradio's theme which already respects dark/light mode
    out = f"""
    <div style="font-family:'Outfit',sans-serif; padding:10px;">

        <div style="background:rgba(196,113,74,0.12); border:2px dashed {TERRA}; padding:15px;
                    border-radius:12px; margin-bottom:25px; text-align:center;">
            <span style="color:{TERRA}; font-weight:700;">✨ YOUR #1 PRIORITY:</span><br>
            <span style="font-size:1.1rem;">{r['top_factor']}</span>
        </div>

        {causes_html}

        <h2 style="color:{TERRA}; font-size:1.8rem; margin-bottom:0;">
            {acne_label} Analysis
        </h2>

        <p style="opacity:0.7; margin-bottom:10px;">
            Based on your skin profile and environmental triggers.
        </p>

        {insight}

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:30px;">
            <div style="background:rgba(196,113,74,0.08); padding:15px; border-radius:12px; border:1px solid rgba(196,113,74,0.2);">
                <small style="color:{TERRA}; font-weight:600; display:block; margin-bottom:4px;">{strength_label}</small>
                <span style="font-size:1.3rem; font-weight:700;">{strength}</span>
            </div>
            <div style="background:rgba(196,113,74,0.08); padding:15px; border-radius:12px; border:1px solid rgba(196,113,74,0.2);">
                <small style="color:{TERRA}; font-weight:600; display:block; margin-bottom:4px;">{severity_label}</small>
                <span style="font-size:1.3rem; font-weight:700;">{display_severity}</span>
            </div>
        </div>

        <h3 style="border-bottom:1px solid rgba(196,113,74,0.3); padding-bottom:5px;">⚡ Action Plan</h3>
        <ul style="line-height:1.8; padding-left:20px;">
    """

    for tip in r["lifestyle_tips"]:
        out += f"<li style='margin-bottom:6px;'>{tip}</li>"

    out += "</ul>"

    out += f"""
    <h3 style="margin-top:25px;">💊 Recommended Ingredients</h3>
    <table style="width:100%; text-align:left; border-collapse:collapse; margin-top:10px;">
        <tr style="background:rgba(196,113,74,0.1);">
            <th style="padding:10px; color:{TERRA};">Ingredient</th>
            <th style="padding:10px; color:{TERRA};">Benefit</th>
        </tr>
    """

    for name, reason in r["ingredients"]:
        out += f"""
        <tr>
            <td style="padding:10px; border-bottom:1px solid rgba(196,113,74,0.15);"><b>{name}</b></td>
            <td style="padding:10px; border-bottom:1px solid rgba(196,113,74,0.15); opacity:0.85;">{reason}</td>
        </tr>
        """

    out += "</table>"

    out += f"""
        <h3 style="margin-top:25px;">🌅 Personalized Routine</h3>
        <div style="padding:20px; background:rgba(196,113,74,0.08); border-left:5px solid {TERRA}; border-radius:8px;">
            <p style="margin-bottom:10px;"><b>Morning:</b> {", ".join(r['routine']['morning'])}</p>
            <p><b>Night:</b> {", ".join(r['routine']['night'])}</p>
        </div>

        <p style="text-align:center; margin-top:40px; font-size:0.85rem; opacity:0.6;
                  border-top:1px solid rgba(196,113,74,0.2); padding-top:20px;">
            💪 <b>Consistency is key.</b> Follow this routine for 2–4 weeks to see visible improvements.<br>
            <small>Educational tool only. Consult a dermatologist for persistent or severe acne.</small>
        </p>
    </div>
    """

    file_path = save_report(out)
    return out, gr.Tabs(selected=2), file_path



# ── APP INTERFACE ──
with gr.Blocks(css=custom_css, title="Acne Insight", theme=gr.themes.Default(
    primary_hue=gr.themes.colors.orange,
    neutral_hue=gr.themes.colors.stone,
)) as demo:
    
    gr.HTML("""
    <div class="hero">
        <h1 class="hero-title">🌸Acne <em>Insight</em> & Skincare Advisor</h1>
        <p style="text-align:center; color: #c4714a; font-weight: 500; margin-bottom:20px;">
            Data-driven skin analysis with specific, actionable advice.
        </p>
    </div>
    """)

    with gr.Column(elem_classes=["wizard-card"]):
        with gr.Tabs() as main_tabs:
            
            with gr.Tab("1. Your Skin", id=0):
                gr.Markdown("### 🧴 Skin Profile")
                with gr.Row():
                    skin_type = gr.Dropdown(["oily", "dry", "combination"], label="Skin Type", value="combination")
                    acne_location = gr.Dropdown(["forehead", "cheeks", "chin", "jawline", "back"], label="Breakout Zone", value="cheeks")
                severity = gr.Slider(1, 3, 2, step=1, label="Visual Severity (1: Mild, 3: Severe)")
                
                btn_to_2 = gr.Button("CONTINUE TO LIFESTYLE →", elem_classes=["primary-btn"])

            with gr.Tab("2. Lifestyle", id=1):
                gr.Markdown("### 🏃 Habits & Environment")
                with gr.Row():
                    sleep_hours = gr.Slider(3, 10, 7, step=1, label="Sleep (Hours)")  
                    water_intake = gr.Slider(0.5, 4.0, 2.0, step=0.1, label="Water Intake (Litres)") 
                with gr.Row():
                    stress_level = gr.Slider(1, 10, 5, step=1, label="Stress (1: Calm, 10: High)")
                    diet_type = gr.Dropdown(["healthy", "balanced", "junk"], label="Diet Quality", value="balanced")
                with gr.Row():
                    exercise = gr.Radio(["yes", "no"], label="Regular Exercise?", value="no")
                    sweat_level = gr.Slider(1, 10, 3, step=1, label="Sweat Intensity")

                submit_btn = gr.Button("🔍 ANALYSE MY ACNE", elem_classes=["primary-btn"])

            with gr.Tab("3. Report", id=2):
                report_area = gr.HTML(value="<div style='text-align:center; padding:50px; color:#c4ada0;'>Please complete the analysis steps to generate your report.</div>")
                download_file = gr.File(label="📥 Download Your Report")

    # Navigation Logic
    btn_to_2.click(fn=lambda: gr.Tabs(selected=1), outputs=main_tabs)
    
    submit_btn.click(
        fn=run_prediction,
        inputs=[skin_type, acne_location, severity, sleep_hours, 
                water_intake, stress_level, diet_type, exercise, sweat_level],
        outputs=[report_area, main_tabs, download_file]
    )

if __name__ == "__main__":
    demo.launch()
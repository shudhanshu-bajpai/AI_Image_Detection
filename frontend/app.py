import base64
import time
import random
from PIL import Image
import streamlit as st
from bytez import Bytez

# ── API Key (hardcoded) ──────────────────────────────────────────────────────
API_KEY = "9dd5f8c4a32df7c41d3552ee371c9ecc"

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Image Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Global ─────────────────────────────────────── */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px;}

    /* ── Hero section ───────────────────────────────── */
    .hero {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
    }
    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero p {
        font-size: 1.05rem;
        color: #6b7280;
        max-width: 560px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* ── Top-right flow button (key-targeted) ──────── */
    div[data-testid="stButton"]:has(button[kind="secondary"]) {
        position: fixed;
        top: 14px;
        right: 24px;
        z-index: 9999;
    }
    #btn-how-it-works {
        position: fixed;
        top: 14px;
        right: 24px;
        z-index: 9999;
    }
    #btn-how-it-works button {
        background: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.45rem 1.2rem !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        cursor: pointer;
        transition: border-color 0.2s, color 0.2s;
    }
    #btn-how-it-works button:hover {
        border-color: #667eea !important;
        color: #667eea !important;
    }

    /* ── Upload area ────────────────────────────────── */
    .upload-zone {
        border: 2px dashed #d1d5db;
        border-radius: 16px;
        padding: 2.5rem 1rem;
        text-align: center;
        transition: border-color 0.2s, background 0.2s;
        background: #fafbfc;
        margin-bottom: 1rem;
    }
    .upload-zone:hover {
        border-color: #667eea;
        background: #f3f0ff;
    }

    /* ── Image container ────────────────────────────── */
    [data-testid="stImage"] img {
        border-radius: 16px;
    }

    /* ── Results panel ───────────────────────────────── */
    .results-panel {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1.8rem 1.6rem;
        margin-top: 0.5rem;
    }

    /* ── Verdict card ───────────────────────────────── */
    .verdict-card {
        border-radius: 16px;
        padding: 1.4rem;
        text-align: center;
        margin-bottom: 1.6rem;
        position: relative;
        overflow: hidden;
    }
    .verdict-card::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 16px;
        opacity: 0.12;
    }
    .verdict-card .verdict-icon {
        font-size: 2.4rem;
        display: block;
        margin-bottom: 0.4rem;
    }
    .verdict-card .verdict-label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        opacity: 0.7;
        margin-bottom: 0.2rem;
    }
    .verdict-card .verdict-text {
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: 0.01em;
    }
    .verdict-real {
        background: linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(52,211,153,0.08) 100%);
        border: 1px solid rgba(16,185,129,0.3);
    }
    .verdict-real .verdict-text { color: #34d399; }
    .verdict-real .verdict-label { color: #6ee7b7; }
    .verdict-ai {
        background: linear-gradient(135deg, rgba(239,68,68,0.15) 0%, rgba(248,113,113,0.08) 100%);
        border: 1px solid rgba(239,68,68,0.3);
    }
    .verdict-ai .verdict-text { color: #f87171; }
    .verdict-ai .verdict-label { color: #fca5a5; }

    /* ── Confidence section ──────────────────────────── */
    .confidence-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #9ca3af;
        margin-bottom: 1rem;
    }

    /* ── Individual score row ────────────────────────── */
    .score-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.2rem;
    }
    .score-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .score-icon-real {
        background: rgba(16,185,129,0.15);
    }
    .score-icon-fake {
        background: rgba(239,68,68,0.15);
    }
    .score-info {
        flex: 1;
        min-width: 0;
    }
    .score-top {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.35rem;
    }
    .score-name {
        font-size: 0.88rem;
        font-weight: 600;
        color: #e5e7eb;
        text-transform: capitalize;
    }
    .score-pct {
        font-size: 0.95rem;
        font-weight: 800;
        font-variant-numeric: tabular-nums;
    }
    .score-pct-real { color: #34d399; }
    .score-pct-fake { color: #f87171; }
    .score-track {
        background: rgba(255,255,255,0.08);
        border-radius: 999px;
        height: 8px;
        overflow: hidden;
    }
    .score-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .score-fill-real {
        background: linear-gradient(90deg, #10b981, #34d399);
    }
    .score-fill-fake {
        background: linear-gradient(90deg, #ef4444, #f87171);
    }

    /* ── Footer badge ───────────────────────────────── */
    .app-footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
        color: #9ca3af;
        font-size: 0.82rem;
    }

    /* ── Button ─────────────────────────────────────── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        transition: transform 0.15s, box-shadow 0.15s;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(102,126,234,0.35);
    }
    .stButton > button[kind="primary"]:active {
        transform: translateY(0);
    }

    /* ── Divider ────────────────────────────────────── */
    .section-divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #d1d5db, transparent);
        margin: 1.5rem 0;
    }

    /* ── Flow diagram ───────────────────────────────── */
    .flow-container {
        padding: 1rem 0;
    }
    .flow-step {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .flow-step:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    }
    .flow-step .step-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.5rem;
    }
    .flow-step .step-num {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        font-weight: 800;
        font-size: 0.85rem;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .flow-step .step-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1f2937;
    }
    .flow-step .step-body {
        color: #6b7280;
        font-size: 0.88rem;
        line-height: 1.55;
        padding-left: 2.6rem;
    }
    .flow-step .step-body code {
        background: #f3f4f6;
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-size: 0.82rem;
        color: #7c3aed;
    }
    .flow-arrow {
        text-align: center;
        font-size: 1.4rem;
        color: #c4b5fd;
        padding: 0.2rem 0;
        line-height: 1;
    }
    .flow-detail-box {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-top: 0.5rem;
        margin-left: 2.6rem;
        font-size: 0.82rem;
        color: #4b5563;
        line-height: 1.5;
    }
    .flow-detail-box strong {color: #374151;}
    .flow-tag {
        display: inline-block;
        background: #ede9fe;
        color: #6d28d9;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.15rem 0.5rem;
        border-radius: 999px;
        margin-left: 0.4rem;
        vertical-align: middle;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>AI Image Detector</h1>
        <p>Upload any image — our AI model will instantly tell you
        whether it's a <strong>real photograph</strong> or <strong>AI-generated</strong>.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Flow Button (top-right via JS repositioning) ────────────────────────────
show_flow = st.button("Get the Flow", key="how_it_works_btn")
st.markdown(
    """
    <script>
    const btns = window.parent.document.querySelectorAll('button');
    btns.forEach(btn => {
        if (btn.innerText.includes('Get the Flow')) {
            const wrapper = btn.closest('[data-testid="stButton"]')
                         || btn.closest('.stButton')
                         || btn.parentElement.parentElement;
            wrapper.id = 'btn-how-it-works';
        }
    });
    </script>
    """,
    unsafe_allow_html=True,
)
# Fallback: also use an iframe-based script for Streamlit versions that block inline JS
st.components.v1.html(
    """
    <script>
    const btns = window.parent.document.querySelectorAll('button');
    btns.forEach(btn => {
        if (btn.innerText.includes('Get the Flow')) {
            const wrapper = btn.closest('[data-testid="stButton"]')
                         || btn.closest('.stButton')
                         || btn.parentElement.parentElement;
            wrapper.style.position = 'fixed';
            wrapper.style.top = '14px';
            wrapper.style.right = '24px';
            wrapper.style.zIndex = '9999';
            wrapper.style.width = 'auto';
        }
    });
    </script>
    """,
    height=0,
)

# ── Flow Dialog ──────────────────────────────────────────────────────────────
if show_flow:

    @st.dialog("How the AI Detection Model Works", width="large")
    def flow_dialog():
        st.markdown('<div class="flow-container">', unsafe_allow_html=True)

        # Step 1
        st.markdown(
            """
            <div class="flow-step">
                <div class="step-header">
                    <span class="step-num">1</span>
                    <span class="step-title">Dataset Collection <span class="flow-tag">Data</span></span>
                </div>
                <div class="step-body">
                    <strong>Real faces</strong> are sourced from the <strong>FFHQ</strong>
                    (Flickr-Faces-HQ) dataset — 70,000 high-quality real human face images.<br/>
                    <strong>Fake faces</strong> are generated using <strong>DALL-E 2</strong>
                    by creating AI variations of each real face at 1024×1024 resolution.
                </div>
                <div class="flow-detail-box">
                    <strong>Storage:</strong> AWS S3 bucket with <code>real/</code> and
                    <code>fake/</code> folders &nbsp;|&nbsp;
                    <strong>~5,300 images</strong> total (balanced classes)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="flow-arrow">▼</div>', unsafe_allow_html=True)

        # Step 2
        st.markdown(
            """
            <div class="flow-step">
                <div class="step-header">
                    <span class="step-num">2</span>
                    <span class="step-title">Preprocessing <span class="flow-tag">Transform</span></span>
                </div>
                <div class="step-body">
                    Every image goes through the same pipeline before entering the model:
                </div>
                <div class="flow-detail-box">
                    <strong>1.</strong> Resize to <code>180 × 180</code> pixels<br/>
                    <strong>2.</strong> Convert to RGB (3 channels)<br/>
                    <strong>3.</strong> Normalize pixel values to <code>0 – 1</code> range (÷ 255)<br/>
                    <strong>4.</strong> Split into <strong>80% training</strong> / <strong>20% validation</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="flow-arrow">▼</div>', unsafe_allow_html=True)

        # Step 3
        st.markdown(
            """
            <div class="flow-step">
                <div class="step-header">
                    <span class="step-num">3</span>
                    <span class="step-title">Model Architecture <span class="flow-tag">ResNet50</span></span>
                </div>
                <div class="step-body">
                    The model uses <strong>transfer learning</strong> with a pre-trained
                    <strong>ResNet50</strong> backbone (ImageNet weights).
                </div>
                <div class="flow-detail-box">
                    <strong>Backbone:</strong> ResNet50 (frozen, 25M params) — extracts visual features<br/>
                    <strong>↓ Flatten</strong><br/>
                    <strong>Dense:</strong> 512 neurons, ReLU activation<br/>
                    <strong>↓</strong><br/>
                    <strong>Output:</strong> 1 neuron, Sigmoid → probability between 0 (fake) and 1 (real)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="flow-arrow">▼</div>', unsafe_allow_html=True)

        # Step 4
        st.markdown(
            """
            <div class="flow-step">
                <div class="step-header">
                    <span class="step-num">4</span>
                    <span class="step-title">Training <span class="flow-tag">GPU</span></span>
                </div>
                <div class="step-body">
                    The model is trained end-to-end on a GPU with carefully chosen hyperparameters.
                </div>
                <div class="flow-detail-box">
                    <strong>Optimizer:</strong> Adam (learning rate = 0.01)<br/>
                    <strong>Loss:</strong> Binary Cross-Entropy<br/>
                    <strong>Epochs:</strong> 50 &nbsp;|&nbsp; <strong>Batch size:</strong> 200<br/>
                    <strong>Metrics:</strong> Accuracy, AUC, Precision, Recall
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="flow-arrow">▼</div>', unsafe_allow_html=True)

        # Step 5
        st.markdown(
            """
            <div class="flow-step">
                <div class="step-header">
                    <span class="step-num">5</span>
                    <span class="step-title">Inference <span class="flow-tag">Prediction</span></span>
                </div>
                <div class="step-body">
                    When you upload a new image, the trained model processes it and outputs a verdict.
                </div>
                <div class="flow-detail-box">
                    <strong>Input:</strong> Your uploaded image<br/>
                    <strong>→</strong> Resize to 180×180, normalize to 0–1<br/>
                    <strong>→</strong> Pass through ResNet50 backbone<br/>
                    <strong>→</strong> Dense layers produce a confidence score<br/>
                    <strong>→</strong> Score &gt; 0.5 = <strong style="color:#065f46;">Real</strong>
                    &nbsp;|&nbsp; Score ≤ 0.5 = <strong style="color:#991b1b;">AI-Generated</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="flow-arrow">▼</div>', unsafe_allow_html=True)

        # Step 6
        st.markdown(
            """
            <div class="flow-step">
                <div class="step-header">
                    <span class="step-num">6</span>
                    <span class="step-title">Visualization & Analysis <span class="flow-tag">Insights</span></span>
                </div>
                <div class="step-body">
                    Model decisions are analysed using <strong>UMAP</strong> embeddings and
                    <strong>feature maps</strong> to visualize how the model separates real
                    from AI-generated faces in high-dimensional feature space.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    flow_dialog()

# ── Input ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag and drop or browse",
    type=["png", "jpg", "jpeg", "webp"],
    help="Supports PNG, JPG, JPEG, WebP",
)

# ── Resolve image source ────────────────────────────────────────────────────
display_image = None
analyse_input = None

if uploaded_file is not None:
    display_image = Image.open(uploaded_file)
    uploaded_file.seek(0)
    img_bytes = uploaded_file.read()
    b64_image = base64.b64encode(img_bytes).decode("utf-8")
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
    mime_map = {
        "png": "image/png", "jpg": "image/jpeg",
        "jpeg": "image/jpeg", "webp": "image/webp",
    }
    mime_type = mime_map.get(ext, "image/png")
    analyse_input = f"data:{mime_type};base64,{b64_image}"

# ── Display & Analyse ────────────────────────────────────────────────────────
if display_image is not None:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    col_img, col_gap, col_result = st.columns([5, 0.5, 4])

    with col_img:
        st.image(display_image, width="stretch")

    with col_result:
        st.markdown("")  # spacing

        analyse_btn = st.button(
            "🔍  Analyse Image",
            type="primary",
            use_container_width=True,
        )

        if analyse_btn:
            with st.spinner("Running AI analysis…"):
                try:
                    sdk = Bytez(API_KEY)
                    model = sdk.model("jacoballessio/ai-image-detect")
                    results = model.run(analyse_input)

                    if results.error:
                        st.error(f"Analysis error: {results.error}")
                    else:
                        output = results.output

                        if isinstance(output, list) and len(output) > 0:
                            top = max(output, key=lambda x: x.get("score", 0))
                            top_label = top.get("label", "").lower()
                            is_ai = any(
                                kw in top_label
                                for kw in ("ai", "fake", "artificial", "generated")
                            )

                            # ── Build the results panel HTML
                            verdict_cls = "verdict-ai" if is_ai else "verdict-real"
                            verdict_icon = "🚨" if is_ai else "✅"
                            verdict_text = "AI-Generated Image" if is_ai else "Real Photograph"

                            scores_html = ""
                            for item in output:
                                lbl = item.get("label", "Unknown")
                                scr = item.get("score", 0)
                                pct = scr * 100
                                lbl_lower = lbl.lower()
                                is_real = any(
                                    kw in lbl_lower
                                    for kw in ("real", "human", "photo", "genuine")
                                )
                                kind = "real" if is_real else "fake"
                                icon = "🟢" if is_real else "🔴"

                                scores_html += f"""
                                <div class="score-row">
                                    <div class="score-icon score-icon-{kind}">{icon}</div>
                                    <div class="score-info">
                                        <div class="score-top">
                                            <span class="score-name">{lbl}</span>
                                            <span class="score-pct score-pct-{kind}">{pct:.1f}%</span>
                                        </div>
                                        <div class="score-track">
                                            <div class="score-fill score-fill-{kind}"
                                                 style="width:{pct:.1f}%;"></div>
                                        </div>
                                    </div>
                                </div>
                                """

                            st.markdown(
                                f"""
                                <div class="results-panel">
                                    <div class="verdict-card {verdict_cls}">
                                        <span class="verdict-icon">{verdict_icon}</span>
                                        <div class="verdict-label">Detection Result</div>
                                        <div class="verdict-text">{verdict_text}</div>
                                    </div>
                                    <div class="confidence-title">Confidence Breakdown</div>
                                    {scores_html}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.info("Analysis complete — see raw output below.")
                            st.json(output)

                except Exception as e:
                    st.error(f"Analysis error: {e}")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="app-footer">Detecting AI-Generated Fake Images</div>',
    unsafe_allow_html=True,
)

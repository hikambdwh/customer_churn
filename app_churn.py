# app_streamlit.py
import streamlit as st
import pickle
import pandas as pd
from pathlib import Path

# =========================
# CONFIG & GLOBAL STYLE
# =========================
st.set_page_config(
    page_title="Customer Churn Insight",
    page_icon="📉",
    layout="wide"
)

# Palet warna & styling global
st.markdown(
    """
    <style>
        :root {
            --bg-main: #f3f4f6;
            --card-bg: #ffffff;
            --accent: #6366f1;
            --accent-soft: rgba(99, 102, 241, 0.08);
            --text-primary: #111827;
            --text-muted: #6b7280;
            --danger: #ef4444;
            --success: #22c55e;
        }

        .stApp {
            background: radial-gradient(circle at top left, #e0e7ff 0, #f3f4f6 45%, #f9fafb 100%);
            color: var(--text-primary);
        }

        .big-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            padding: 0.15rem 0.6rem;
            border-radius: 999px;
            background-color: var(--accent-soft);
            color: var(--accent);
            font-size: 0.75rem;
            font-weight: 500;
        }

        .section-card {
            padding: 1.5rem 1.8rem;
            border-radius: 1.1rem;
            background-color: var(--card-bg);
            box-shadow: 0 14px 35px rgba(15, 23, 42, 0.10);
            margin-bottom: 1.5rem;
        }

        .result-card {
            padding: 1.2rem 1.4rem;
            border-radius: 1rem;
            background-color: var(--card-bg);
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.12);
            margin-top: 0.5rem;
        }
        .result-positive {
            border-left: 6px solid var(--danger);
            background: linear-gradient(to right, rgba(239, 68, 68, 0.05), #ffffff);
        }
        .result-negative {
            border-left: 6px solid var(--success);
            background: linear-gradient(to right, rgba(34, 197, 94, 0.05), #ffffff);
        }
        .result-title {
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 0.4rem;
        }
        .result-text {
            font-size: 0.95rem;
            color: #4b5563;
        }

        .metric-label {
            font-size: 0.8rem;
            color: var(--text-muted);
        }
        .metric-value {
            font-size: 1.4rem;
            font-weight: 600;
        }

        /* Rapikan tab */
        button[data-baseweb="tab"] {
            font-size: 0.9rem;
            padding: 0.45rem 0.9rem;
        }

        /* Hilangkan footer Streamlit & burger menu */
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        
        /* Container tab */
        div[data-baseweb="tab-list"] {
            background-color: rgba(255,255,255,0.9);
            border-radius: 999px;
            padding: 0.35rem;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.12);
            border: 1px solid #e5e7eb;
        }

    /* Tab umum (tidak aktif) */
        button[data-baseweb="tab"] {
            border-radius: 999px !important;
            padding: 0.45rem 1.2rem;
            font-size: 0.9rem;
            color: #4b5563 !important;          /* abu‑abu gelap, jelas terbaca */
            background-color: transparent;
        }

    /* Tab yang sedang aktif */
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #6366f1 !important;          /* warna utama (ungu/biru) */
            background-color: #ffffff !important;
            font-weight: 600;
        }
        [data-testid="stWidgetLabel"] > div > p {
            color: #111827 !important;
            font-weight: 500;
            font-size: 0.9rem;
        }

        label {
            color: #111827 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# LOAD MODEL
# =========================
with open("model/customer_churn_model.pkl", "rb") as f:
    model = pickle.load(f)

# =========================
# HEADER
# =========================
col_title, col_meta = st.columns([4, 1.4])

with col_title:
    st.markdown('<div class="pill">Customer Analytics • Telco</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-title">Customer Churn Dashboard & Predictor</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Pantau churn secara global dan prediksi risiko churn per pelanggan untuk membantu tim bisnis mengambil keputusan yang lebih tepat dan cepat.</div>',
        unsafe_allow_html=True,
    )

with col_meta:
    st.markdown(
        """
        <div class="section-card" style="padding:0.9rem 1.1rem;">
            <div class="metric-label">Model</div>
            <div class="metric-value">Churn Classifier</div>
            <div class="metric-label" style="margin-top:0.4rem;">Basis: data historis pelanggan telco</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# TABS: DASHBOARD & PREDIKSI
# =========================
tab_dashboard, tab_predict = st.tabs(["📊 Dashboard Churn", "🤖 Prediksi Pelanggan"])

# =========================
# TAB 1: DASHBOARD
# =========================
with tab_dashboard:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        st.subheader("Snapshot Dashboard Churn")
        st.write(
            "Gambar di bawah adalah export dari dashboard Power BI yang kamu buat. "
            "Gunakan ini sebagai konteks visual saat membaca hasil prediksi di tab sebelah."
        )
    with right:
        st.markdown(
            """
            <div style="font-size:0.9rem; color:#4b5563; margin-top:0.4rem;">
                • Tingkat churn total<br>
                • Rata-rata tenure churn vs non-churn<br>
                • Distribusi churn per jenis layanan & pembayaran<br>
                • Insight perilaku pelanggan yang berhenti
            </div>
            """,
            unsafe_allow_html=True,
        )

    dashboard_path = Path("assets/dashboard_churn.png")

    st.write("")  # spacing kecil

    if dashboard_path.exists():
        st.image(
            str(dashboard_path),
            caption="Customer Churn Dashboard (Power BI)",
            use_column_width=True,
        )
    else:
        st.warning(
            "Gambar dashboard tidak ditemukan. "
            "Simpan file gambar di `assets/dashboard_churn.png` atau sesuaikan path di kode."
        )

    with st.expander("Tips membaca dashboard ini"):
        st.markdown(
            """
            - **Customer Churn (No/Yes)** – lihat komposisi pelanggan bertahan vs berhenti.
            - **Average Tenure** – pelanggan churn cenderung punya masa langganan lebih pendek.
            - **Internet Service / Payment Method vs Churn** – segmen mana yang paling berisiko.
            - Gunakan informasi di sini untuk menginterpretasi hasil prediksi per pelanggan di tab *Prediksi Pelanggan*.
            """
        )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB 2: PREDIKSI
# =========================
with tab_predict:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.subheader("Prediksi Risiko Churn per Pelanggan")
    st.write(
        "Isi profil pelanggan dan detail layanan di sisi kiri. "
        "Di sisi kanan, kamu akan melihat hasil prediksi model beserta probabilitas churn dan rekomendasi aksi bisnis."
    )

    # Dua kolom: kiri = form, kanan = hasil
    col_form, col_result = st.columns([2.3, 1.7])

    with col_form:
        with st.form("churn_form"):
            col_profile, col_service, col_billing = st.columns(3)

            # ---------- PROFIL ----------
            with col_profile:
                st.markdown("**Profil Pelanggan**")
                gender = st.selectbox("Gender", ["Female", "Male"])
                senior_display = st.selectbox("Senior Citizen", ["No", "Yes"])
                SeniorCitizen = 1 if senior_display == "Yes" else 0
                Partner = st.selectbox("Partner", ["No", "Yes"])
                Dependents = st.selectbox("Dependents", ["No", "Yes"])
                tenure = st.number_input(
                    "Tenure (bulan berlangganan)",
                    min_value=0,
                    max_value=100,
                    value=12,
                    help="Jumlah bulan pelanggan sudah berlangganan."
                )

            # ---------- LAYANAN ----------
            with col_service:
                st.markdown("**Layanan yang Diambil**")
                PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
                MultipleLines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
                InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
                OnlineSecurity = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
                OnlineBackup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
                DeviceProtection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
                TechSupport = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
                StreamingTV = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
                StreamingMovies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

            # ---------- PEMBAYARAN ----------
            with col_billing:
                st.markdown("**Kontrak & Pembayaran**")
                Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
                PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
                PaymentMethod = st.selectbox(
                    "Payment Method",
                    [
                        "Electronic check",
                        "Mailed check",
                        "Bank transfer (automatic)",
                        "Credit card (automatic)",
                    ],
                )
                MonthlyCharges = st.number_input(
                    "Monthly Charges",
                    min_value=0.0,
                    value=70.0,
                    help="Tagihan rata-rata per bulan."
                )
                TotalCharges = st.number_input(
                    "Total Charges",
                    min_value=0.0,
                    value=800.0,
                    help="Total tagihan yang sudah dibayarkan pelanggan."
                )

            submitted = st.form_submit_button("🔍 Prediksi Churn")

    # ---------- HASIL DI KANAN ----------
    with col_result:
        if submitted:
            # ⚠️ Pastikan kolom ini sesuai dengan fitur saat training
            data = pd.DataFrame(
                [
                    {
                        "gender": gender,
                        "SeniorCitizen": SeniorCitizen,
                        "Partner": Partner,
                        "Dependents": Dependents,
                        "tenure": tenure,
                        "PhoneService": PhoneService,
                        "MultipleLines": MultipleLines,
                        "InternetService": InternetService,
                        "OnlineSecurity": OnlineSecurity,
                        "OnlineBackup": OnlineBackup,
                        "DeviceProtection": DeviceProtection,
                        "TechSupport": TechSupport,
                        "StreamingTV": StreamingTV,
                        "StreamingMovies": StreamingMovies,
                        "Contract": Contract,
                        "PaperlessBilling": PaperlessBilling,
                        "PaymentMethod": PaymentMethod,
                        "MonthlyCharges": MonthlyCharges,
                        "TotalCharges": TotalCharges,
                    }
                ]
            )

            pred = model.predict(data)[0]
            proba = float(model.predict_proba(data)[0, 1])
            proba_pct = round(proba * 100, 1)

            is_churn = int(pred) == 1

            if is_churn:
                verdict_text = "Pelanggan berpotensi **CHURN**"
                detail_text = (
                    "Pelanggan ini memiliki risiko cukup tinggi untuk berhenti berlangganan. "
                    "Pertimbangkan aksi retensi seperti penawaran diskon, upgrade paket, atau "
                    "pendekatan personal oleh tim CS."
                )
                css_class = "result-card result-positive"
            else:
                verdict_text = "Pelanggan kemungkinan **BERTAHAN**"
                detail_text = (
                    "Pelanggan ini relatif stabil. Tetap jaga pengalaman mereka dengan layanan yang "
                    "konsisten, komunikasi proaktif, dan program loyalitas."
                )
                css_class = "result-card result-negative"

            st.markdown(
                f"""
                <div class="{css_class}">
                    <div class="result-title">{verdict_text}</div>
                    <div class="result-text">
                        Probabilitas churn: <b>{proba_pct}%</b>
                    </div>
                    <div class="result-text" style="margin-top:0.4rem;">
                        {detail_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")
            st.write("**Visualisasi Probabilitas Churn**")
            st.progress(min(max(proba, 0.0), 1.0))

            st.write("")
            st.markdown("**Rekomendasi Tindakan Bisnis**")
            if is_churn:
                st.markdown(
                    """
                    - Hubungi pelanggan dan gali alasan utama ketidakpuasan.
                    - Tawarkan paket yang lebih sesuai (downgrade/upgrade, bonus kuota, atau potongan harga sementara).
                    - Pastikan masalah teknis (internet, billing, support) tertangani dengan cepat.
                    """
                )
            else:
                st.markdown(
                    """
                    - Berikan program loyalitas (poin/reward) untuk mempertahankan kepuasan.
                    - Kirimkan komunikasi proaktif terkait fitur baru atau promo eksklusif.
                    - Pantau terus metrik penggunaan untuk mendeteksi perubahan perilaku dini.
                    """
                )
        else:
            # Placeholder saat belum ada prediksi
            st.markdown(
                """
                <div class="result-card" style="border-left: 4px solid #e5e7eb;">
                    <div class="result-title">Menunggu input pelanggan</div>
                    <div class="result-text">
                        Isi form di sisi kiri lalu klik <b>Prediksi Churn</b> untuk melihat hasil di sini.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Fraud Model Comparison", layout="wide")

# --- ĐƯỜNG DẪN HỆ THỐNG ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(os.path.dirname(CURRENT_DIR), 'models')

@st.cache_resource
def load_assets(file_name):
    path = os.path.join(MODEL_DIR, file_name)
    return joblib.load(path)

# --- GIAO DIỆN SIDEBAR ---
st.sidebar.header("⚙️ Cấu hình Model")

if not os.path.exists(MODEL_DIR):
    st.error("❌ Thư mục 'models' không tồn tại!")
    st.stop()

model_files = [f for f in os.listdir(MODEL_DIR) if f.endswith('.pkl')]

if len(model_files) < 2:
    st.warning("⚠️ Bạn nên có ít nhất 2 file .pkl trong thư mục models để so sánh.")
    
m1_file = st.sidebar.selectbox("Chọn Model 1 (Chính):", model_files, index=0 if model_files else None)
m2_file = st.sidebar.selectbox("Chọn Model 2 (Để so sánh):", model_files, index=1 if len(model_files) > 1 else 0)

# --- GIAO DIỆN CHÍNH ---
st.title("🛡️ Fraud Detection - Model Comparison")
st.markdown(f"Đang so sánh: `{m1_file}` vs `{m2_file}`")

uploaded_file = st.file_uploader("Tải lên file 'fraud_demo_ready.csv'", type="csv")

if uploaded_file and m1_file and m2_file:
    df_raw = pd.read_csv(uploaded_file)
    
    # Load assets của cả 2 model
    assets1 = load_assets(m1_file)
    assets2 = load_assets(m2_file)
    
    with st.spinner('🚀 Đang chạy dự đoán cho cả 2 model...'):
        # --- Dự đoán Model 1 ---
        X1 = assets1['scaler'].transform(df_raw[assets1['features_order']])
        prob1 = assets1['model'].predict_proba(X1)[:, 1]
        pred1 = (prob1 >= assets1['threshold']).astype(int)
        
        # --- Dự đoán Model 2 ---
        X2 = assets2['scaler'].transform(df_raw[assets2['features_order']])
        prob2 = assets2['model'].predict_proba(X2)[:, 1]
        pred2 = (prob2 >= assets2['threshold']).astype(int)
        
        # Gộp kết quả
        df_res = df_raw.copy()
        df_res[f'Prob_{m1_file}'] = prob1
        df_res[f'Pred_{m1_file}'] = pred1
        df_res[f'Prob_{m2_file}'] = prob2
        df_res[f'Pred_{m2_file}'] = pred2

    # --- HIỂN THỊ METRICS ---
    actual_fraud = df_raw['is_fraud'].sum() if 'is_fraud' in df_raw.columns else "N/A"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"📊 **Thực tế (Ground Truth)**\n\n**{actual_fraud}** gian lận")
    with col2:
        st.success(f"🤖 **{m1_file}**\n\nBắt được: **{pred1.sum()}** vụ")
    with col3:
        st.warning(f"🤖 **{m2_file}**\n\nBắt được: **{pred2.sum()}** vụ")

    # --- BẢNG SO SÁNH CHI TIẾT ---
    st.subheader("Bảng so sánh chi tiết")
    
    # Logic tô màu: Đỏ nếu Model 1 bắt được, Cam nếu Model 2 bắt được, Tím nếu cả 2 cùng bắt được
    def highlight_comparison(row):
        style = [''] * len(row)
        p1 = row[f'Pred_{m1_file}']
        p2 = row[f'Pred_{m2_file}']
        
        color = ""
        if p1 == 1 and p2 == 1:
            color = 'background-color: #e1bee7' # Tím - Cả 2 cùng bắt
        elif p1 == 1:
            color = 'background-color: #ffcccc' # Đỏ nhạt - M1 bắt
        elif p2 == 1:
            color = 'background-color: #fff9c4' # Vàng nhạt - M2 bắt
            
        return [color] * len(row)

    st.dataframe(
        df_res.style.apply(highlight_comparison, axis=1)
        .format({f'Prob_{m1_file}': "{:.2%}", f'Prob_{m2_file}': "{:.2%}"}),
        height=600
    )
    
    # Chú thích màu
    st.markdown("""
    **Chú thích màu sắc:**
    - <span style='background-color: #ffcccc; padding: 2px 5px;'>Màu Đỏ</span>: Chỉ Model 1 phát hiện.
    - <span style='background-color: #fff9c4; padding: 2px 5px;'>Màu Vàng</span>: Chỉ Model 2 phát hiện.
    - <span style='background-color: #e1bee7; padding: 2px 5px;'>Màu Tím</span>: Cả 2 model cùng đồng ý là Gian lận.
    """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch
from PIL import Image

# 🎨 إعداد الصفحة
st.set_page_config(page_title="تحليل الكرة السعودية", page_icon="⚽", layout="wide")

# 🌟 الهيدر (الشعار + العنوان)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://i.imgur.com/LSgNYmC.png", width=200)  # ✏️ استبدل الرابط بشعارك الخاص
    st.markdown("""
    ## **تحليل الكرة السعودية**  
    #### Dr. Sami Al-Harbi
    """)

# 🟢 تعريف بالموقع
st.markdown("""
<div style='background-color:#01411C; padding: 20px; border-radius: 10px; color: white;'>
تحليل مرئي شامل لمباريات كرة القدم السعودية:
<ul>
<li>📊 الإحصائيات العامة</li>
<li>🎯 خرائط التمريرات والشبكات</li>
<li>🔥 خريطة الضغط العالي</li>
<li>📈 تحليل xT (Expected Threat)</li>
<li>📸 رفع خرائط وصور تحليلية إضافية</li>
<li>📥 تصدير التقارير إلى PDF</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 📂 رفع ملفات المباريات
with st.expander("📂 رفع ملفات المباراة (CSV/Excel)"):
    match_files = st.file_uploader("اسحب وأسقط الملفات هنا أو اختر من جهازك", type=["csv", "xlsx"], accept_multiple_files=True)

# 📸 رفع صور تحليلية
with st.expander("📸 رفع صور التحليل"):
    uploaded_images = st.file_uploader("ارفع صور PNG/JPG", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_images:
    st.subheader("📊 تقارير بصرية للمباراة")
    for img in uploaded_images:
        st.image(img, use_column_width=True)

# ⚽ بيانات السياق
st.markdown("### ⚽ بيانات المباراة")
col1, col2, col3 = st.columns(3)
with col1:
    league = st.selectbox("اختر البطولة", ["دوري روشن السعودي", "كأس الملك", "ودية"])
with col2:
    round = st.selectbox("اختر الجولة", ["الأولى", "الثانية", "الثالثة"])
with col3:
    match_name = st.text_input("اسم المباراة", placeholder="الهلال × النصر")

# 🎯 نوع التحليل
st.markdown("### 🎯 اختر نوع التحليل")
analysis_type = st.radio("", [
    "تحليل الفرق", "تحليل اللاعبين", "إحصائيات المباراة",
    "أفضل اللاعبين", "أطول سلسلة تمريرات",
    "خريطة xT", "مناطق الضغط العالي"
], horizontal=True)

# 🔎 معالجة البيانات
if match_files:
    for match_file in match_files:
        st.markdown(f"### 📄 جاري معالجة: {match_file.name}")
        try:
            df = pd.read_csv(match_file) if match_file.name.endswith(".csv") else pd.read_excel(match_file)
            st.success("✅ تم تحميل الملف بنجاح")

            if analysis_type == "تحليل الفرق":
                team = st.selectbox("اختر الفريق", df["team"].unique())
                st.dataframe(df[df["team"] == team])

            elif analysis_type == "تحليل اللاعبين":
                player = st.selectbox("اختر اللاعب", df["player_name"].unique())
                st.dataframe(df[df["player_name"] == player])

            elif analysis_type == "إحصائيات المباراة":
                st.dataframe(df.describe())

            elif analysis_type == "أفضل اللاعبين":
                if "rating" in df.columns:
                    st.dataframe(df.sort_values("rating", ascending=False).head(10))
                else:
                    st.warning("⚠️ لا يوجد عمود 'rating' في البيانات.")

            elif analysis_type == "أطول سلسلة تمريرات":
                st.warning("🚧 الميزة تحت التطوير")

            elif analysis_type == "خريطة xT":
                st.subheader("📈 خريطة التهديد المتوقع (xT)")
                pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
                fig, ax = pitch.draw(figsize=(8,6))
                if 'xT' in df.columns:
                    df_passes = df[df['type'] == 'Pass']
                    pitch.scatter(df_passes['x'], df_passes['y'], s=100, c=df_passes['xT'], cmap='viridis', ax=ax)
                    st.pyplot(fig)
                else:
                    st.warning("⚠️ عمود 'xT' غير موجود في البيانات.")

            elif analysis_type == "مناطق الضغط العالي":
                st.subheader("🔥 خريطة الضغط العالي")
                pitch = VerticalPitch(pitch_color='#f7f7f7', line_color='black')
                fig, ax = pitch.draw(figsize=(8,6))
                df_pressure = df[df['type'] == 'Pressure']
                if not df_pressure.empty:
                    pitch.kdeplot(df_pressure['x'], df_pressure['y'], ax=ax, cmap="Reds", fill=True)
                    st.pyplot(fig)
                else:
                    st.warning("⚠️ لا توجد بيانات ضغط في الملف.")

        except Exception as e:
            st.error(f"❌ خطأ: {e}")

# 📤 تصدير PDF (قيد التطوير)
st.markdown("---")
st.markdown("### 📤 تصدير التقرير")
if st.button("إنشاء تقرير PDF"):
    st.warning("🔧 ميزة تصدير PDF ما زالت تحت التطوير")
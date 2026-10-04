import streamlit as st

# 1. إعدادات الصفحة وجعلها بعرض الشاشة الكامل (Wide) لتبدو كالنظام المحترف
st.set_page_config(page_title="ERP - Eng Madbouly", layout="wide", initial_sidebar_state="collapsed")

# 2. حقن ستايل الـ CSS المودرن للبطاقات الكبيرة
st.markdown("""
<style>
    /* إخفاء القوائم الافتراضية لستريمليت لتبدو كبرنامج مخصص */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .top-navbar {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        direction: rtl;
    }
    .system-title { font-size: 22px; font-weight: bold; }
    .user-meta { font-size: 14px; opacity: 0.9; }

    /* تنسيق أزرار ستريمليت لتبدو كبطاقات فخمة */
    div.stButton > button {
        background-color: white !important;
        color: #1e3c72 !important;
        border: 2px solid #eaeaea !important;
        border-radius: 16px !important;
        padding: 40px 20px !important;
        width: 100% !important;
        min-height: 180px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    /* تأثير التحليق والإبهار عند مرور الماوس */
    div.stButton > button:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 12px 20px rgba(42, 82, 152, 0.15) !important;
        border-color: #2a5298 !important;
        background-color: #f8fafd !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. عرض الشريط العلوي الاحترافي
st.markdown("""
<div class="top-navbar">
    <div class="system-title">💼 Enterprise Resource Planning (ERP - Eng Madbouly)</div>
    <div class="user-meta">👤 المدير العام &nbsp;|&nbsp; 📅 2026-10-04</div>
</div>
""", unsafe_allow_html=True)

# 4. بناء شبكة الأعمدة (Grid) للبطاقات الكبيرة باستخدام أعمدة Streamlit
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

# مصفوفة لإدارة التنقل بين الصفحات (Session State)
if "page" not in st.session_state:
    st.session_state.page = "home"

# توزيع البطاقات داخل الأعمدة مع إضافة الأيقونات ونصوص الشرح
with col1:
    if st.button("👥\n\nالموارد البشرية (HR)\nإدارة الموظفين والرواتب"):
        st.session_state.page = "hr"
        st.rerun()

with col2:
    if st.button("📊\n\nالحسابات والمالية\nشجرة الحسابات والقيود"):
        st.session_state.page = "finance"
        st.rerun()

with col3:
    if st.button("📦\n\nالمستودعات والمخازن\nمراقبة المخزون والأصناف"):
        st.session_state.page = "inventory"
        st.rerun()

with col4:
    if st.button("🧾\n\nالفواتير والمبيعات\nإصدار الفواتير والعملاء"):
        st.session_state.page = "sales"
        st.rerun()

with col5:
    if st.button("💰\n\nحركة الخزنة اليومية\nتسجيل الإيرادات والمصروفات"):
        st.session_state.page = "safe"
        st.rerun()

with col6:
    if st.button("📈\n\nالمؤشرات العامة\nالتقارير الإحصائية والأداء"):
        st.session_state.page = "analytics"
        st.rerun()

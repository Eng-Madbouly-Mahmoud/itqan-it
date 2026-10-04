import streamlit as st
from datetime import datetime
from supabase import create_client, Client

# 🔑 إعدادات الاتصال بقاعدة بيانات Supabase السحابية
SUPABASE_URL = "https://stejbrmfjreoguuxohsr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0ZWpicm1manJlb2d1dXhvaHNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA2Nzc4ODUsImV4cCI6MjEwNjI1Mzg4NX0.mCmdj3d5ltZca-nGr7XEQPhBBsTFyGTXn2HOqr8l7M8"

# تهيئة عميل Supabase لمرة واحدة في الجلسة
@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# 📥 دالة جلب البيانات من قاعدة البيانات السحابية Supabase
def load_data():
    try:
        response = supabase.table("tickets").select("*").order("id", desc=False).execute()
        tickets = []
        for row in response.data:
            ticket = row.copy()
            ticket['ID'] = row['id']  # تحويل id الصغير إلى ID الكبير ليتوافق مع كودك
            tickets.append(ticket)
        return tickets
    except Exception as e:
        st.error(f"خطأ في جلب البيانات من السيرفر: {e}")
        return []

# 💾 دالة حفظ تذكرة جديدة مباشرة في السحاب
def insert_ticket(new_ticket):
    try:
        db_data = {
            "id": int(new_ticket["ID"]),
            "name": new_ticket["name"],
            "dept": new_ticket["dept"],
            "issue": new_ticket["issue"],
            "status": new_ticket["status"],
            "solved_by": new_ticket["solved_by"],
            "created_at": new_ticket["created_at"],
            "updated_at": new_ticket["updated_at"]
        }
        supabase.table("tickets").insert(db_data).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ التذكرة: {e}")
        return False

# 🔄 دالة تحديث حالة تذكرة قائمة في السحاب
def update_ticket_in_db(ticket_id, updated_fields):
    try:
        supabase.table("tickets").update(updated_fields).eq("id", ticket_id).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في تحديث التذكرة: {e}")
        return False

# تهيئة مخزن البيانات وجلب التذاكر من السحاب عند تشغيل الموقع
if 'tickets' not in st.session_state:
    st.session_state.tickets = load_data()

# ضبط الترقيم التلقائي للتذاكر بناءً على آخر تذكرة في السحاب
if 'next_id' not in st.session_state:
    if st.session_state.tickets:
        max_id = max([int(t['ID']) for t in st.session_state.tickets])
        st.session_state.next_id = max_id + 1
    else:
        st.session_state.next_id = 101

# إعدادات الصفحة والأيقونة الرئيسية للموقع
st.set_page_config(
    page_title="الدكتور صلاح حسب الله - مركز الدعم الفني - شركة إتقان",
    page_icon="⚖️",
    layout="wide"
)

# =========================================================
# 💻 محتوى نظام شركة إتقان للمحاماة (التصميم البني الجديد)
# =========================================================

st.markdown("""
    <div style='background-color: #8C6239; padding: 25px; border-radius: 12px; margin-bottom: 5px; display: flex; align-items: center; justify-content: center; gap: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://w3.org" style='filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.3));'>
            <path d="M12 2V22M12 5H5M12 5H19M5 5L3 13M19 5L21 13M3 13C3 15 5 15 5 15C5 15 7 15 7 13M21 13C21 15 19 15 19 15C19 15 17 15 17 13M5 15V18C5 19.1 5.9 20 7 20H17C18.1 20 19 19.1 19 18V15" stroke="#F5EBE0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 22H15" stroke="#F5EBE0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div>
            <h1 style='text-align: center; color: #F5EBE0; margin: 0; font-family: "Cairo", sans-serif; font-size: 32px; font-weight: bold;'>لوحة تكنولوجيا المعلومات والشبكات ⚙️</h1>
            <p style='text-align: center; color: #E3D5CA; margin: 5px 0 0 0; font-size: 14px;'>المكتب الذكي لإدارة ومتابعة البلاغات التقنية</p>
        </div>
    </div>
    <div style='background-color: #D5BDAF; padding: 10px; border-radius: 8px; margin-bottom: 25px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
        <marquee direction='right' style='color: #4A3728; font-weight: bold; font-size: 16px; margin: 0;'>
            ⚖️ شركة إتقان للمحاماة والاستشارات القانونية (د. صلاح حسب الله) ترحب بكم .. يرجى تسجيل بلاغات الأعطال بدقة لسرعة توجيه مهندس الـ IT إليكم فوراً 🛠️
        </marquee>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #E3D5CA; border-radius: 4px 4px 0px 0px; padding: 10px 20px; color: #4A3728; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #8C6239 !important; color: #F5EBE0 !important;
    }
    </style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 بوابة الموظفين والمستشارين (تسجيل عطل)", "🖥️ لوحة تحكم الـ IT (إدارة التذاكر)"])

# 📝 بوابة الموظفين
with tab1:
    st.markdown("<h3 style='text-align: right; color: #8C6239;'>📥 تسجيل بلاغ عطل تقني جديد في النظام</h3>", unsafe_allow_html=True)
    st.write("برجاء ملء الخانات التالية بدقة ليتم توجيه الدعم الفني إليك فوراً لتجنب تعطيل العمل القانوني:")
    
    with st.form("ticket_form", clear_on_submit=True):
        name = st.text_input("👤 اسم الموظف / المستشار بالكامل:")
        dept = st.selectbox("🏢 القسم / الإدارة التابع لها:", [
            "قسم الاداره العليا", "بنك مصر", "بنك الاهلي", "التجاري الدولي", "الادمن", "إدارة عامة", "أخرى"
        ])
        issue = st.text_area("⚠️ وصف العطل أو المشكلة التقنية بالتفصيل:")
        submit = st.form_submit_button("🚀 إرسال التذكرة إلى قسم الدعم الفني")
        
        if submit:
            if name.strip() and issue.strip():
                current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                
                new_ticket = {
                    "ID": int(st.session_state.next_id),
                    "name": name,
                    "dept": dept,
                    "issue": issue,
                    "status": "Pending (قيد الانتظار)",
                    "solved_by": "لم تُحل بعد ⏳",
                    "created_at": current_time,
                    "updated_at": "لم تُحدث بعد"
                }
                
                # حفظ التذكرة مباشرة في قاعدة بيانات Supabase السحابية أولاً
                if insert_ticket(new_ticket):
                    st.session_state.tickets.append(new_ticket)
                    st.success(f"🎉 تم تسجيل بلاغك بنجاح في قاعدة البيانات السحابية! رقم التذكرة هو: #{st.session_state.next_id}")
                    st.session_state.next_id += 1
                    st.rerun()
            else:
                st.error("❌ الرجاء كتابة الاسم ووصف العطل أولاً قبل الإرسال!")

# 🖥️ لوحة تحكم الـ IT
with tab2:
    st.markdown("<h3 style='text-align: right; color: #8C6239;'>🖥️ شاشة مراقبة وحل الأعطال الحالية</h3>", unsafe_allow_html=True)
    password = st.text_input("🔑 أدخل كلمة مرور الإدارة لتحديث التذاكر:", type="password")
    
    if password == "1234": 
        st.success("🔓 تم تفعيل صلاحيات المهندس المسؤول.")
        
        # نضمن دائماً تحديث البيانات المعروضة من السحاب مباشرة
        st.session_state.tickets = load_data()
        
        if st.session_state.tickets:
            import pandas as pd
            df_report = pd.DataFrame(st.session_state.tickets)
            
            st.markdown("### 📊 استخراج التقارير وقائمة البلاغات")
            st.dataframe(df_report[["ID", "name", "dept", "issue", "status", "solved_by", "created_at", "updated_at"]], use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🛠️ تحديث حالة تذكرة وإسنادها للمهندس:")
            ticket_ids = [int(t['ID']) for t in st.session_state.tickets]
            selected_id = st.selectbox("اختر رقم التذكرة للتعديل:", ticket_ids)
            
            it_engineer = st.text_input("👨‍💻 اسم المهندس القائم بالحل:")
            new_status = st.selectbox("الحالة الجديدة للتذكرة:", ["Pending (قيد الانتظار)", "In Progress (جاري العمل)", "Solved (تم حل المشكلة بنجاح ✅)"])
            
            if st.button("💾 حفظ تحديث التذكرة"):
                if it_engineer.strip():
                    update_fields = {
                        "status": new_status,
                        "solved_by": it_engineer,
                        "updated_at": datetime.now().strftime("%Y-%m-%d %I:%M %p")
                    }
                    # تحديث السحاب فوراً
                    if update_ticket_in_db(selected_id, update_fields):
                        st.success(f"✅ تم تحديث التذكرة رقم #{selected_id} بنجاح في قاعدة البيانات!")
                        st.rerun()
                else:
                    st.error("❌ يرجى كتابة اسم المهندس المسؤول عن الحل أولاً!")
        else:
            st.info("💡 لا توجد أي تذاكر مسجلة في النظام حالياً.")
    elif password != "":
        st.error("❌ كلمة المرور غير صحيحة!")
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


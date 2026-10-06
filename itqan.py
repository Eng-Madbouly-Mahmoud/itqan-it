import streamlit as st
from datetime import datetime
import pandas as pd
from supabase import create_client, Client

# 🔑 إعدادات الاتصال بقاعدة بيانات Supabase السحابية الفعالة لديك
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0ZWpicm1manJlb2d1dXhvaHNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA2Nzc4ODUsImV4cCI6MjEwNjI1Mzg4NX0.mCmdj3d5ltZca-nGr7XEQPhBBsTFyGTXn2HOqr8l7M8"

# تهيئة عميل Supabase لمرة واحدة في الجلسة
@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔄 استدعاء العميل وتخزينه في متغير للاستخدام في بقية الملف
supabase = get_supabase_client()

# =========================================================
# 📥 دالات الموديول المالي المطورة (الحفظ، التحديث، والجلب)
# =========================================================

def insert_account_to_erp(acc_data):
    try:
        supabase.table("erp_finance").insert(acc_data).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الحساب الجديد بجدول erp_finance: {e}")
        return False

def load_accounts_from_erp():
    try:
        response = supabase.table("erp_finance").select("*").order("acc_id", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"خطأ في جلب شجرة الحسابات: {e}")
        return []

def insert_journal_entries(entries_list):
    try:
        supabase.table("erp_journal_entries").insert(entries_list).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ القيد المالي: {e}")
        return False

# =========================================================
# 📥 دالات نظام التذاكر والدعم الفني الحالية
# =========================================================
def load_data():
    try:
        response = supabase.table("tickets").select("*").order("id", desc=False).execute()
        tickets = []
        for row in response.data:
            ticket = row.copy()
            ticket['ID'] = row['id']
            tickets.append(ticket)
        return tickets
    except Exception as e:
        st.error(f"خطأ في جلب البيانات من السيرفر: {e}")
        return []

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

# تهيئة المخازن الافتراضية للجلسة بنظام التذاكر
if 'tickets' not in st.session_state:
    st.session_state.tickets = load_data()

if 'next_id' not in st.session_state:
    if st.session_state.tickets:
        max_id = max([int(t['ID']) for t in st.session_state.tickets])
        st.session_state.next_id = max_id + 1
    else:
        st.session_state.next_id = 101

# إعدادات الصفحة والأيقونة الرئيسية للموقع
st.set_page_config(
    page_title="الدكتور صلاح حسب الله - مركز الإدارة الشامل - شركة إتقان",
    page_icon="⚖️",
    layout="wide"
)

# =========================================================
# 💻 التصميم والهيدر الأساسي للمنظومة
# =========================================================
st.markdown("""
    <div style='background-color: #8C6239; padding: 25px; border-radius: 12px; margin-bottom: 5px; display: flex; align-items: center; justify-content: center; gap: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <div>
            <h1 style='text-align: center; color: #F5EBE0; margin: 0; font-family: "Cairo", sans-serif; font-size: 32px; font-weight: bold;'>النظام السحابي الذكي المتكامل - شركة إتقان ⚖️</h1>
            <p style='text-align: center; color: #E3D5CA; margin: 5px 0 0 0; font-size: 14px;'>لوحة إدارة البلاغات التقنية والموديول المحاسبي المطور بجوار بعضها البعض</p>
        </div>
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

# تقسيم واجهة المستخدم إلى التبويبات الخمسة المتوازية والمضبوطة هندسياً
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 بوابة الدعم التقني", 
    "🖥️ لوحة تحكم الـ IT", 
    "🗂️ شجرة الحسابات وتحديثها", 
    "💵 إدارة القيود والسندات اليومية",
    "📖 كشف دفتر الأستاذ المساعد"
])

# 1️⃣ بوابة الموظفين (البلاغات)
with tab1:
    st.markdown("<h3 style='text-align: right; color: #8C6239;'>📥 تسجيل بلاغ عطل تقني جديد</h3>", unsafe_allow_html=True)
    with st.form("ticket_form", clear_on_submit=True):
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            name = st.text_input("👤 اسم الموظف / المستشار بالكامل:")
        with col_t2:
            dept = st.selectbox("🏢 القسم / الإدارة التابع لها:", ["قسم الاداره العليا", "بنك مصر", "بنك الاهلي", "التجاري الدولي", "الادمن", "إدارة عامة", "أخرى"])
        issue = st.text_area("⚠️ وصف العطل التقني بالتفصيل:")
        submit = st.form_submit_button("🚀 إرسال التذكرة")
        
        if submit:
            if name.strip() and issue.strip():
                current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                new_ticket = {
                    "ID": int(st.session_state.next_id), "name": name, "dept": dept, "issue": issue,
                    "status": "Pending (قيد الانتظار)", "solved_by": "لم تُحل بعد ⏳", "created_at": current_time, "updated_at": "لم تُحدث بعد"
                }
                if insert_ticket(new_ticket):
                    st.session_state.tickets.append(new_ticket)
                    st.success(f"🎉 تم تسجيل بلاغك بنجاح! رقم التذكرة هو: #{st.session_state.next_id}")
                    st.session_state.next_id += 1
                    st.rerun()

# 2️⃣ لوحة تحكم الـ IT
with tab2:
    st.markdown("<h3 style='text-align: right; color: #8C6239;'>🖥️ شاشة إدارة الأعطال الحالية</h3>", unsafe_allow_html=True)
    password = st.text_input("🔑 أدخل كلمة مرور الإدارة لتحديث التذاكر:", type="password")
    if password == "1234":
        st.success("🔓 تم تفعيل صلاحيات المهندس المسؤول.")
        st.session_state.tickets = load_data()
        if st.session_state.tickets:
            df_report = pd.DataFrame(st.session_state.tickets)
            st.dataframe(df_report[["ID", "name", "dept", "issue", "status", "solved_by", "created_at", "updated_at"]], use_container_width=True)

# 3️⃣ تكويد شجرة الحسابات وحفظها (الخانات بجوار بعضها البعض + ميزة التعديل المباشر)
with tab3:
    st.markdown("<h3 style='text-align: right; color: #8C6239;'>🗂️ إدارة وهيكلة شجرة الحسابات العامة</h3>", unsafe_allow_html=True)
    
    # جلب الحسابات لخيارات الصيانة والتعديل
    accounts_list = load_accounts_from_erp()
    
    col_mode, col_main_type = st.columns(2)
    with col_mode:
        operation_mode = st.radio("اختر العملية المراد تنفيذها:", ["إضافة حساب جديد ➕", "تعديل حساب قائم حالياً ✏️"], horizontal=True)
    with col_main_type:
        acc_type = st.selectbox("نوع الحساب الرئيسي:", ["ميزانية", "قائمة دخل"])
    
    if acc_type == "قائمة دخل":
        st.markdown("<div style='background-color: #FFEB3B; padding: 6px; border-radius: 5px; text-align: center; color: black; font-weight: bold; margin-bottom:15px;'>حسابات قائمة الدخل (أصفر) 🟡</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color: #4CAF50; padding: 6px; border-radius: 5px; text-align: center; color: white; font-weight: bold; margin-bottom:15px;'>حسابات الميزانية (أخضر) 🟢</div>", unsafe_allow_html=True)

    # حالة الإضافة
    if operation_mode == "إضافة حساب جديد ➕":
        with st.form("account_tree_form", clear_on_submit=True):
            # جعل خانات المدخلات بجوار بعضها البعض تماماً في صف واحد متوازن
            col1, col2, col3 = st.columns(3)
            with col1:
                acc_number = st.text_input("رقم الحساب (acc_id):", placeholder="مثال: 10001")
            with col2:
                account_name_input = st.text_input("اسم الحساب (Account Name):", placeholder="مثال: الخزينة الرئيسية")
            with col3:
                open_bal = st.number_input("الرصيد الافتتاحي (amount_num) $:", min_value=0.0, value=0.0, step=10.0)
                
            col4, col5 = st.columns(2)
            with col4:
                class_1 = st.selectbox("التصنيف الأول (class1):", ["أصول", "خصوم", "حقوق ملكية", "إيرادات", "مصروفات"])
            with col5:
                class_2 = st.selectbox("التصنيف الثاني (class2):", ["أصول متداولة", "أصول ثابتة", "مصروفات إدارية وعمومية", "إيرادات نشاط", "أخرى"])
                
            save_acc_btn = st.form_submit_button("💾 حفظ وإدراج الحساب بالشجرة")
            
            if save_acc_btn:
                if acc_number.strip() and account_name_input.strip():
                    new_acc_payload = {
                        "acc_id": acc_number.strip(), "title": account_name_input.strip(), "acc_name": account_name_input.strip(),     
                        "amount_num": float(open_bal), "type": acc_type, "class1": class_1, "class2": class_2
                    }
                    if insert_account_to_erp(new_acc_payload):
                        st.success(f"✅ تم حفظ الحساب [{account_name_input}] بنجاح في قاعدة البيانات السحابية!")
                        st.rerun()
                else:
                    st.error("⚠️ خطأ: يرجى كتابة رقم الحساب واسمه بالكامل.")


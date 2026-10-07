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
# 💻 الهيدر والتصميم الأساسي للمنظومة (المطابق لـ Eng Madbouly)
# =========================================================
st.markdown("""
    <div style='background-color: #1E3A8A; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-family: "Cairo", sans-serif; font-size: 28px; font-weight: bold;'>💼 Enterprise Resource Planning (ERP - Eng Madbouly)</h1>
    </div>
    <div style='text-align: right; color: #555; font-size: 14px; margin-bottom: 20px;'>
        👤 المستخدم: المدير العام | 📅 التاريخ: 2026-10-06
    </div>
""", unsafe_allow_html=True)

# زر الخروج المركزي المنسق
col_exit, _ = st.columns([1, 5])
with col_exit:
    st.button("🚪 خروج", use_container_width=True)

st.markdown("<h2 style='text-align: right; color: #B45309;'>💰 إدارة الحسابات وحركة الخزنة المركزية</h2>", unsafe_allow_html=True)

# =========================================================
# 🛠️ هندسة واجهة التاب الاحترافية (بجوار بعضها البعض تماماً)
# =========================================================
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "تكويد الشجرة"

# إنشاء 4 أزرار متجاورة وممتدة تمثل التبويبات الاحترافية في صف واحد أفقي
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

with btn_col1:
    if st.button("🗂️ تكويد وإدراج حساب بالشجرة", use_container_width=True, type="primary" if st.session_state.current_tab == "تكويد الشجرة" else "secondary"):
        st.session_state.current_tab = "تكويد الشجرة"
        st.rerun()

with btn_col2:
    if st.button("💵 إضافة حركة مالية (قيد سند)", use_container_width=True, type="primary" if st.session_state.current_tab == "إضافة قيد" else "secondary"):
        st.session_state.current_tab = "إضافة قيد"
        st.rerun()

with btn_col3:
    if st.button("📖 دفتر الأستاذ المساعد", use_container_width=True, type="primary" if st.session_state.current_tab == "الأستاذ المساعد" else "secondary"):
        st.session_state.current_tab = "الأستاذ المساعد"
        st.rerun()

with btn_col4:
    if st.button("🛠️ لوحة التعديل والحذف السرية", use_container_width=True, type="primary" if st.session_state.current_tab == "لوحة التحكم" else "secondary"):
        st.session_state.current_tab = "لوحة التحكم"
        st.rerun()

st.markdown("---")

# جلب الحسابات الحالية لتغذية القوائم المنسدلة في كل الأقسام
accounts_list = load_accounts_from_erp()

# =========================================================
# 1️⃣ التبويب الأول: تكويد وإدراج حساب في شجرة الحسابات
# =========================================================
if st.session_state.current_tab == "تكويد الشجرة":
    st.markdown("<h3 style='text-align: right; color: #1E3A8A;'>🗂️ تكويد وإدراج حساب في شجرة الحسابات</h3>", unsafe_allow_html=True)
    
    acc_type = st.selectbox("نوع الحساب الرئيسي:", ["قائمة دخل", "ميزانية"])
    
    if acc_type == "قائمة دخل":
        st.markdown("<div style='background-color: #FFEB3B; padding: 10px; border-radius: 5px; text-align: center; color: black; font-weight: bold; margin-bottom: 20px;'>حسابات قائمة الدخل (أصفر) 🟡</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color: #4CAF50; padding: 10px; border-radius: 5px; text-align: center; color: white; font-weight: bold; margin-bottom: 20px;'>حسابات الميزانية (أخضر) 🟢</div>", unsafe_allow_html=True)

    with st.form("account_tree_form", clear_on_submit=True):
        # 🛠️ جعل الخانات بجوار بعضها البعض تماماً في صف واحد متوازي مريح للعين
        c1, c2, c3 = st.columns(3)
        with c1:
            acc_number = st.text_input("رقم الحساب (acc_id):", placeholder="مثال: 10001")
        with c2:
            account_name_input = st.text_input("اسم الحساب (Account Name):", placeholder="أدخل اسم الحساب هنا")
        with c3:
            open_bal = st.number_input("الرصيد الافتتاحي (amount_num) $:", min_value=0.0, value=0.0, step=10.0)
            
        c4, c5 = st.columns(2)
        with c4:
            class_1 = st.selectbox("التصنيف الأول (class1):", ["إيرادات", "مصروفات", "أصول ثابتة", "أصول متداولة", "التزامات"])
        with c5:
            class_2 = st.selectbox("التصنيف الثاني (class2):", ["مصروفات إدارية وعمومية", "إيرادات نشاط", "تكلفة مبيعات", "أخرى"])
            
        save_acc_btn = st.form_submit_button("💾 حفظ الحساب بالشجرة")
        
        if save_acc_btn:
            if acc_number.strip() and account_name_input.strip():
                new_acc_payload = {
                    "acc_id": acc_number.strip(), "title": account_name_input.strip(), "acc_name": account_name_input.strip(),     
                    "amount_num": float(open_bal), "type": acc_type, "class1": class_1, "class2": class_2
                }
                if insert_account_to_erp(new_acc_payload):
                    st.success(f"🎉 تم حفظ الحساب [{account_name_input}] بنجاح وتحديث الشجرة!")
                    st.rerun()
            else:
                st.error("❌ خطأ: يرجى كتابة رقم الحساب واسمه بالكامل قبل الحفظ.")

# =========================================================
# 2️⃣ التبويب الثاني: إضافة حركة مالية (قيد سند)
# =========================================================
elif st.session_state.current_tab == "إضافة قيد":
    st.markdown("<h3 style='text-align: right; color: #1E3A8A;'>💵 إضافة حركة مالية وتوجيه القيود السندات</h3>", unsafe_allow_html=True)
    
    account_options = [f"{acc['acc_id']} - {acc['title']}" for acc in accounts_list]
    
    if not account_options:
        st.warning("⚠️ لا توجد حسابات متوفرة! يرجى تكويد شجرة الحسابات أولاً من التبويب السابق.")
    else:
        with st.form("journal_form", clear_on_submit=True):
            # جعل الخانات الأساسية للقيد متوازية بجانب بعضها البعض
            cg1, cg2, cg3 = st.columns(3)
            with cg1:
                entry_id = st.number_input("رقم القيد المتسلسل:", min_value=1, step=1, value=1)
            with cg2:
                entry_date = st.date_input("تاريخ استحقاق الحركة:", value=datetime.today())
            with cg3:
                entry_desc = st.text_input("البيان والشرح العام للحركة المالية:")
                
            st.markdown("<p style='color:#B45309; font-weight:bold;'>⚖️ أطراف المعاملة المالية (مدين ودائن متوازيين):</p>", unsafe_allow_html=True)
            
            # صف الطرف المدين
            col_deb_acc, col_deb_val = st.columns([3, 1])
            with col_deb_acc:
                deb_acc_selected = st.selectbox("حساب الطرف المدين (من حـ/):", options=account_options, key="deb_s")
            with col_deb_val:
                deb_val = st.number_input("المبلغ المدين:", min_value=0.0, step=50.0, key="deb_v")
                
            # صف الطرف الدائن مقابله تماماً
            col_cred_acc, col_cred_val = st.columns([3, 1])
            with col_cred_acc:
                cred_acc_selected = st.selectbox("حساب الطرف الدائن (إلى حـ/):", options=account_options, key="cred_s")
            with col_cred_val:
                credit_val = st.number_input("المبلغ الدائن:", min_value=0.0, step=50.0, key="cred_v")
                
            submit_journal = st.form_submit_button("🚀 ترحيل وحفظ القيد ماليًا")
            
            if submit_journal:
                if deb_val <= 0 or credit_val <= 0:
                    st.error("❌ خطأ: لا يمكن تسجيل قيد بقيمة صفر.")
                elif deb_val != credit_val:
                    st.error(f"❌ قيد غير متوازن ماليًا! المدين ({deb_val}) يجب أن يساوي الدائن ({credit_val}).")
                elif deb_acc_selected == cred_acc_selected:
                    st.error("❌ خطأ محاسبي: لا يمكن اختيار نفس الحساب للطرفين المدين والدائن.")
                else:
                    deb_acc_num = deb_acc_selected.split(" - ")[0]
                    cred_acc_num = cred_acc_selected.split(" - ")[0]
                    
                    bulk_entries = [
                        {"entry_number": int(entry_id), "entry_date": str(entry_date), "acc_id": deb_acc_num, "debit": float(deb_val), "credit": 0.0, "description": entry_desc},

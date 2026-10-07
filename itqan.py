import streamlit as st
from datetime import datetime
import pandas as pd
from supabase import create_client, Client

# 🔑 إعدادات الاتصال بقاعدة بيانات Supabase السحابية
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
# 🎨 واجهة النظام المالي النقي والمطور هندسياً
# =========================================================

st.markdown("""
    <div style='background-color: #1E3A8A; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-family: "Cairo", sans-serif; font-size: 28px; font-weight: bold;'>💼 النظام المالي المتكامل (ERP - Eng Madbouly)</h1>
    </div>
    <div style='text-align: right; color: #555; font-size: 14px; margin-bottom: 20px;'>
        👤 المستخدم: المدير العام | 📅 التاريخ: 2026-10-07
    </div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: right; color: #1E3A8A;'>💰 إدارة الحسابات وحركة الخزنة المركزية ⚖️</h2>", unsafe_allow_html=True)

# 🛠️ هندسة التابات الاحترافية المتجاورة (بجوار بعضها البعض تماماً في صف واحد أفقي)
if 'active_financial_tab' not in st.session_state:
    st.session_state.active_financial_tab = "شجرة الحسابات"

# إنشاء 4 أعمدة متساوية تماماً لتمثيل الأزرار التبويبية أفقياً
t_col1, t_col2, t_col3, t_col4 = st.columns(4)

with t_col1:
    if st.button("🗂️ تكويد وحفظ الشجرة", use_container_width=True, type="primary" if st.session_state.active_financial_tab == "شجرة الحسابات" else "secondary"):
        st.session_state.active_financial_tab = "شجرة الحسابات"
        st.rerun()

with t_col2:
    if st.button("💵 إضافة حركة مالية (قيد سند)", use_container_width=True, type="primary" if st.session_state.active_financial_tab == "إضافة قيد" else "secondary"):
        st.session_state.active_financial_tab = "إضافة قيد"
        st.rerun()

with t_col3:
    if st.button("📖 دفتر الأستاذ المساعد", use_container_width=True, type="primary" if st.session_state.active_financial_tab == "الأستاذ المساعد" else "secondary"):
        st.session_state.active_financial_tab = "الأستاذ المساعد"
        st.rerun()

with t_col4:
    if st.button("🔐 صيانة وحذف القيود والشجرة", use_container_width=True, type="primary" if st.session_state.active_financial_tab == "لوحة الصيانة" else "secondary"):
        st.session_state.active_financial_tab = "لوحة الصيانة"
        st.rerun()

st.markdown("---")

# جلب الحسابات الحالية لتغذية القوائم المنسدلة في كل الأقسام
accounts_list = load_accounts_from_erp()

# =========================================================
# 🗂️ التبويب الأول: تكويد وتعديل الشجرة الأساسية (الخانات متجاورة)
# =========================================================
if st.session_state.active_financial_tab == "شجرة الحسابات":
    st.markdown("<h3 style='text-align: right; color: #B45309;'>🗂️ تكويد وإدراج حساب في شجرة الحسابات</h3>", unsafe_allow_html=True)
    
    acc_type = st.selectbox("نوع الحساب الرئيسي:", ["قائمة دخل", "ميزانية"])
    
    if acc_type == "قائمة دخل":
        st.markdown("<div style='background-color: #FFEB3B; padding: 10px; border-radius: 5px; text-align: center; color: black; font-weight: bold; margin-bottom: 20px;'>حسابات قائمة الدخل (أصفر) 🟡</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color: #4CAF50; padding: 10px; border-radius: 5px; text-align: center; color: white; font-weight: bold; margin-bottom: 20px;'>حسابات الميزانية (أخضر) 🟢</div>", unsafe_allow_html=True)

    # اختيار نمط العمل على الشجرة الأساسية
    tree_mode = st.radio("إجراء على الشجرة الأساسية:", ["إضافة حساب جديد الشجرة ➕", "تعديل حساب قائم في الشجرة الأساسية ✏️"], horizontal=True)
    st.markdown("---")

    # حالة إضافة حساب جديد بالشجرة (الخانات بجوار بعضها)
    if tree_mode == "إضافة حساب جديد الشجرة ➕":
        with st.form("account_tree_form", clear_on_submit=True):
            # الصف الأول متوازي أفقي
            row1_c1, row1_c2, row1_c3 = st.columns(3)
            with row1_c1:
                acc_number = st.text_input("رقم الحساب (acc_id):", placeholder="مثال: 10001")
            with row1_c2:
                account_name_input = st.text_input("اسم الحساب (Account Name):", placeholder="أدخل اسم الحساب هنا")
            with row1_c3:
                open_bal = st.number_input("الرصيد الافتتاحي (amount_num) $:", min_value=0.0, value=0.0, step=10.0)
                
            # الصف الثاني متوازي أسفله مباشرة
            row2_c1, row2_c2 = st.columns(2)
            with row2_c1:
                class_1 = st.selectbox("التصنيف الأول (class1):", ["إيرادات", "مصروفات", "أصول ثابتة", "أصول متداولة", "التزامات"])
            with row2_c2:
                class_2 = st.selectbox("التصنيف الثاني (class2):", ["مصروفات إدارية وعمومية", "إيرادات نشاط", "تكلفة مبيعات", "أخرى"])
                
            save_acc_btn = st.form_submit_button("💾 حفظ الحساب بالشجرة 📥")
            
            if save_acc_btn:
                if acc_number.strip() and account_name_input.strip():
                    new_acc_payload = {
                        "acc_id": acc_number.strip(), "title": account_name_input.strip(), "acc_name": account_name_input.strip(),     
                        "amount_num": float(open_bal), "type": acc_type, "class1": class_1, "class2": class_2
                    }
                    if insert_account_to_erp(new_acc_payload):
                        st.success(f"🎉 تم حفظ الحساب [{account_name_input}] بنجاح في الشجرة!")
                        st.rerun()
                else:
                    st.error("⚠️ خطأ: يرجى كتابة رقم الحساب واسمه بالكامل.")

    # حالة التعديل على الشجرة الأساسية
    else:
        if not accounts_list:
            st.info("لا توجد حسابات مكوّدة بعد لتعديلها.")
        else:
            acc_options_map = {f"{acc['acc_id']} - {acc['title']}": acc for acc in accounts_list}
            selected_acc_key = st.selectbox("اختر الحساب المراد تعديل حقوله في الشجرة الأساسية:", list(acc_options_map.keys()))
            target_acc = acc_options_map[selected_acc_key]
            
            with st.form("edit_account_form"):
                re1, re2, re3 = st.columns(3)
                with re1:
                    edit_title = st.text_input("اسم الحساب المعدل:", value=target_acc.get('title', ''))
                with re2:
                    edit_bal = st.number_input("الرصيد الافتتاحي المعدل:", value=float(target_acc.get('amount_num', 0.0)))
                with re3:
                    edit_type = st.selectbox("نوع الحساب المعدل:", ["قائمة دخل", "ميزانية"], index=0 if target_acc.get('type') == "قائمة دخل" else 1)
                
                re4, re5 = st.columns(2)
                with re4:
                    edit_c1 = st.text_input("التصنيف الأول المعدل (class1):", value=target_acc.get('class1', ''))
                with re5:
                    edit_c2 = st.text_input("التصنيف الثاني المعدل (class2):", value=target_acc.get('class2', ''))
                    
                update_acc_btn = st.form_submit_button("💾 حفظ التعديلات بالشجرة الأساسية")
                if update_acc_btn:
                    updated_payload = {
                        "title": edit_title.strip(), "acc_name": edit_title.strip(), 
                        "amount_num": float(edit_bal), "type": edit_type, "class1": edit_c1, "class2": edit_c2
                    }
                    try:
                        supabase.table("erp_finance").update(updated_payload).eq("acc_id", target_acc['acc_id']).execute()
                        st.success("🎉 تم تحديث بيانات شجرة الحسابات الأساسية بنجاح!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"فشل التعديل: {e}")

    st.markdown("---")
    st.markdown("#### 🔍 شجرة الحسابات الحالية المسترجعة:")
    if accounts_list:
        st.dataframe(pd.DataFrame(accounts_list)[["acc_id", "title", "amount_num", "type", "class1", "class2"]], use_container_width=True)

# =========================================================
# 💵 التبويب الثاني: إضافة حركة مالية (قيد سند متوازن)
# =========================================================
elif st.session_state.active_financial_tab == "إضافة قيد":
    st.markdown("<h3 style='text-align: right; color: #1E3A8A;'>💵 إضافة حركة مالية وتوجيه القيود اليومية</h3>", unsafe_allow_html=True)
    
    account_options = [f"{acc['acc_id']} - {acc['title']}" for acc in accounts_list]
    if not account_options:
        st.warning("⚠️ لا توجد حسابات متوفرة! يرجى تكويد شجرة الحسابات أولاً.")
    else:

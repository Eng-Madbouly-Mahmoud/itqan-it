import streamlit as st
from datetime import datetime
import pandas as pd
from supabase import create_client, Client

# 🔑 إعدادات الاتصال الموحدة بقاعدة بيانات Supabase
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0ZWpicm1manJlb2d1dXhvaHNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA2Nzc4ODUsImV4cCI6MjEwNjI1Mzg4NX0.mCmdj3d5ltZca-nGr7XEQPhBBsTFyGTXn2HOqr8l7M8"

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# =========================================================
# 📥 دالات التعامل مع الجداول المالية المستقلة لـ ERP
# =========================================================

def insert_account_to_erp(acc_data):
    try:
        supabase.table("erp_finance").insert(acc_data).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الحساب بجدول erp_finance: {e}")
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
        st.error(f"خطأ في حفظ القيود بجدول erp_journal_entries: {e}")
        return False

# =========================================================
# 🎨 تصميم الواجهة وتنسيق الحقول بجوار بعضها البعض
# =========================================================

st.markdown("""
    <div style='background-color: #1E3A8A; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;'>
        <h1 style='color: white; margin: 0; font-family: "Cairo", sans-serif; font-size: 26px; font-weight: bold;'>💼 النظام المالي المستقل المتكامل (ERP - الحسابات العامة)</h1>
    </div>
""", unsafe_allow_html=True)

# تهيئة حالة التبويب النشط
if 'active_financial_tab' not in st.session_state:
    st.session_state.active_financial_tab = "شجرة الحسابات"

# 🛠️ أزرار التبويبات الاحترافية بجوار بعضها البعض في صف واحد متناسق تماماً
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
    if st.button("🔐 صيانة وحذف السجلات", use_container_width=True, type="primary" if st.session_state.active_financial_tab == "لوحة الصيانة" else "secondary"):
        st.session_state.active_financial_tab = "لوحة الصيانة"
        st.rerun()

st.markdown("---")

accounts_list = load_accounts_from_erp()

# 🗂️ التبويب الأول: إدارة وتكويد شجرة الحسابات
if st.session_state.active_financial_tab == "شجرة الحسابات":
    st.markdown("<h3 style='text-align: right; color: #B45309;'>🗂️ تكويد وإدراج حساب في شجرة الحسابات</h3>", unsafe_allow_html=True)
    
    acc_type = st.selectbox("نوع الحساب الرئيسي:", ["قائمة دخل", "ميزانية"])
    tree_mode = st.radio("إجراء العمليات على الشجرة الأساسية:", ["إضافة حساب جديد الشجرة ➕", "تعديل حساب قائم في الشجرة الأساسية ✏️"], horizontal=True)
    st.markdown("---")

    if tree_mode == "إضافة حساب جديد الشجرة ➕":
        with st.form("account_tree_form", clear_on_submit=True):
            # جعل الخانات متجاورة أفقياً في صف واحد
            row1_c1, row1_c2, row1_c3 = st.columns(3)
            with row1_c1:
                acc_number = st.text_input("رقم الحساب (acc_id):")
            with row1_c2:
                account_name_input = st.text_input("اسم الحساب (Account Name):")
            with row1_c3:
                open_bal = st.number_input("الرصيد الافتتاحي $:", min_value=0.0, value=0.0)
                
            row2_c1, row2_c2 = st.columns(2)
            with row2_c1:
                class_1 = st.selectbox("التصنيف الأول (class1):", ["إيرادات", "مصروفات", "أصول ثابتة", "أصول متداولة", "التزامات"])
            with row2_c2:
                class_2 = st.selectbox("التصنيف الثاني (class2):", ["مصروفات إدارية", "إيرادات نشاط", "تكلفة مبيعات", "أخرى"])
                
            if st.form_submit_button("💾 حفظ وإدراج الحساب بالشجرة"):
                if acc_number.strip() and account_name_input.strip():
                    payload = {
                        "acc_id": acc_number.strip(), "title": account_name_input.strip(), "acc_name": account_name_input.strip(),     
                        "amount_num": float(open_bal), "type": acc_type, "class1": class_1, "class2": class_2
                    }
                    if insert_account_to_erp(payload):
                        st.success(f"🎉 تم حفظ الحساب [{account_name_input}] بنجاح!")
                        st.rerun()
                else:
                    st.error("⚠️ يرجى ملء البيانات المطلوبة أولاً.")
    else:
        if accounts_list:
            acc_options_map = {f"{acc['acc_id']} - {acc['title']}": acc for acc in accounts_list}
            selected_acc_key = st.selectbox("اختر الحساب المراد تعديله في الشجرة الأساسية:", list(acc_options_map.keys()))
            target_acc = acc_options_map[selected_acc_key]
            
            with st.form("edit_account_form"):
                re1, re2, re3 = st.columns(3)
                with re1:
                    edit_title = st.text_input("اسم الحساب المعدل:", value=target_acc.get('title', ''))
                with re2:
                    edit_bal = st.number_input("الرصيد المعدل:", value=float(target_acc.get('amount_num', 0.0)))
                with re3:
                    edit_type = st.selectbox("نوع الحساب المعدل:", ["قائمة دخل", "ميزانية"], index=0 if target_acc.get('type') == "قائمة دخل" else 1)
                
                if st.form_submit_button("💾 حفظ التعديلات بالشجرة الأساسية"):
                    updated_payload = {"title": edit_title.strip(), "acc_name": edit_title.strip(), "amount_num": float(edit_bal), "type": edit_type}
                    supabase.table("erp_finance").update(updated_payload).eq("acc_id", target_acc['acc_id']).execute()
                    st.success("🎉 تم تحديث بيانات الشجرة بنجاح!")
                    st.rerun()

    st.markdown("---")
    if accounts_list:
        st.dataframe(pd.DataFrame(accounts_list)[["acc_id", "title", "amount_num", "type", "class1", "class2"]], use_container_width=True)

# 💵 التبويب الثاني: إضافة حركة مالية (قيد سند متوازن)
elif st.session_state.active_financial_tab == "إضافة قيد":
    st.markdown("<h3 style='text-align: right; color: #1E3A8A;'>💵 إضافة حركة مالية وتوجيه القيود اليومية</h3>", unsafe_allow_html=True)
    
    account_options = [f"{acc['acc_id']} - {acc['title']}" for acc in accounts_list]
    if not account_options:
        st.warning("⚠️ لا توجد حسابات متوفرة! يرجى تكويد الشجرة أولاً.")
    else:
        with st.form("journal_form", clear_on_submit=True):
            cg1, cg2, cg3 = st.columns(3)
            with cg1:
                entry_id = st.number_input("رقم القيد المتسلسل:", min_value=1, step=1)
            with cg2:
                entry_date = st.date_input("تاريخ الحركة المالية:", value=datetime.today())
            with cg3:
                entry_desc = st.text_input("البيان والشرح العام للحركة:")
                
            st.markdown("---")
            col_deb_acc, col_deb_val = st.columns(2)
            with col_deb_acc:
                deb_acc_selected = st.selectbox("حساب الطرف المدين (من حـ/):", options=account_options, key="deb_s")
            with col_deb_val:
                deb_val = st.number_input("المبلغ المدين:", min_value=0.0, step=50.0, key="deb_v")
                
            col_cred_acc, col_cred_val = st.columns(2)
            with col_cred_acc:
                cred_acc_selected = st.selectbox("حساب الطرف الدائن (إلى حـ/):", options=account_options, key="cred_s")
            with col_cred_val:
                credit_val = st.number_input("المبلغ الدائن:", min_value=0.0, step=50.0, key="cred_v")
                
            if st.form_submit_button("🚀 ترحيل وحفظ القيد ماليًا"):
                if deb_val != credit_val:
                    st.error("❌ قيد غير متوازن ماليًا! يجب تساوى الطرفين.")
                elif deb_acc_selected == cred_acc_selected:
                    st.error("❌ خطأ: لا يمكن اختيار نفس الحساب للطرفين.")
                else:
                    deb_acc_num = deb_acc_selected.split(" - ")[0]
                    cred_acc_num = cred_acc_selected.split(" - ")[0]
                    
                    bulk_entries = [
                        {"entry_number": int(entry_id), "entry_date": str(entry_date), "acc_id": deb_acc_num, "debit": float(deb_val), "credit": 0.0, "description": entry_desc},
                        {"entry_number": int(entry_id), "entry_date": str(entry_date), "acc_id": cred_acc_num, "debit": 0.0, "credit": float(credit_val), "description": entry_desc}
                    ]
                    if insert_journal_entries(bulk_entries):
                        st.success(f"🎉 تم ترحيل وحفظ القيد رقم #{entry_id} بنجاح!")

# 📖 التبويب الثالث: كشف دفتر الأستاذ المساعد
elif st.session_state.active_financial_tab == "الأستاذ المساعد":

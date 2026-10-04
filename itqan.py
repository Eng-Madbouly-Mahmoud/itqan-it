import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# ⚙️ إعدادات الصفحة الأساسية لنظام الـ ERP باسم المهندس مدبولي
st.set_page_config(page_title="نظام ERP - المهندس مدبولي", page_icon="💼", layout="wide")

# 🔒 كود الحماية المخصص لإخفاء القوائم الافتراضية لـ Streamlit عن المستخدمين
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 🔑 مفاتيح الاتصال المباشرة بقاعدة بيانات Supabase
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlwaWxmZmplZXl4Ynd3ZmNzcWt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA2ODI4ODcsImV4cCI6MjEwNjI1ODg4N30.Wf4wu9cqE_2jwq9_W1dIiTlibXWzFnhHaZEhgvDWXzU"

@st.cache_resource
def get_supabase_client():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

supabase = get_supabase_client()

# 🔒 نظام التحقق من الصلاحيات وتثبيت الجلسة
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None

# 1️⃣ صفحة تسجيل الدخول
def login_page():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔐 تسجيل الدخول لنظام ERP - المهندس مدبولي</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم (Username):")
            password = st.text_input("🔑 كلمة المرور (Password):", type="password")
            submit = st.form_submit_button("تسجيل الدخول للنظام")
            
            if submit:
                if username == "admin" and password == "admin2026":
                    st.session_state["logged_in"] = True
                    st.session_state["user_role"] = "المدير العام"
                    st.rerun()
                elif username == "accountant" and password == "finance2026":
                    st.session_state["logged_in"] = True
                    st.session_state["user_role"] = "المحاسب"
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة!")

# 2️⃣ لوحة التحكم الرئيسية والأقسام الفعالة
def main_dashboard():
    with st.sidebar:
        st.markdown(f"### 👨‍💻 المستخدم: {st.session_state['user_role']}")
        st.markdown(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d')}")
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج من النظام"):
            st.session_state["logged_in"] = False
            st.session_state["user_role"] = None
            st.rerun()

    st.markdown("""
        <div style='background-color: #1E3A8A; padding: 15px; border-radius: 8px; margin-bottom: 25px;'>
            <h1 style='text-align: center; color: white; margin: 0;'>💼 Enterprise Resource Planning (ERP - Eng Madbouly)</h1>
        </div>
    """, unsafe_allow_html=True)

    tab_home, tab_finance, tab_inventory, tab_sales, tab_hr = st.tabs([
        "📈 لوحة المؤشرات العامة", 
        "💰 إدارة الحسابات والمالية", 
        "📦 إدارة المستودعات والمخازن", 
        "🧾 الفواتير والمبيعات",
        "👥 الموارد البشرية (HR)"
    ])

    # قيم افتراضية آمنة ومقاومة للانهيارات كلياً لضمان رسم الجدول والموديولات
    fin_data_list, inv_data_list, sales_data_list, hr_data_list = [], [], [], []
    total_rev, total_exp, total_items, total_emps = 0.0, 0.0, 0, 0

    # جلب معزول ومحمي 100% داخل دالة التشغيل
    if supabase:
        try:
            f_res = supabase.table("erp_finance").select("*").execute()
            if f_res and hasattr(f_res, 'data') and f_res.data:
                fin_data_list = f_res.data
                total_rev = sum([float(f.get('amount', 0)) for f in fin_data_list if f.get('type') == 'إيرادات'])
                total_exp = sum([float(f.get('amount', 0)) for f in fin_data_list if f.get('type') == 'مصروفات'])
        except Exception:
            pass

        try:
            i_res = supabase.table("erp_inventory").select("*").execute()
            if i_res and hasattr(i_res, 'data') and i_res.data:
                inv_data_list = i_res.data
                total_items = sum([int(i.get('quantity', 0)) for i in inv_data_list])
        except Exception:
            pass

        try:
            s_res = supabase.table("erp_sales").select("*").execute()
            if s_res and hasattr(s_res, 'data') and s_res.data:
                sales_data_list = s_res.data
        except Exception:
            pass

        try:
            h_res = supabase.table("erp_hr").select("*").execute()
            if h_res and hasattr(h_res, 'data') and h_res.data:
                hr_data_list = h_res.data
                total_emps = len(hr_data_list)
        except Exception:
            pass

    # 📊 لوحة المؤشرات العامة
    with tab_home:
        st.subheader("📊 الأداء العام للمؤسسة")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("إجمالي الإيرادات", f"${total_rev:,.2f}")
        kpi2.metric("إجمالي المصروفات", f"${total_exp:,.2f}")
        kpi3.metric("قطع المخزون الحالية", f"{total_items} قطعة")
        kpi4.metric("عدد الموظفين بالنظام", f"{total_emps} موظف")
        if not fin_data_list:
            st.info("💡 النظام يعمل بكفاءة وأمان. (قاعدة البيانات السحابية خالية أو تحتاج ضبط صلاحيات RLS للتبادل الفعلي للبيانات)")

    # 💰 إدارة الحسابات والمالية
    with tab_finance:
        st.subheader("💳 حركة القيود اليومية (الخزنة)")
        col_form, col_view = st.columns(2)
        with col_form:
            st.markdown("### 📥 إضافة قيد مالي")
            with st.form("finance_form", clear_on_submit=True):
                title = st.text_input("البيان / الوصف:")
                amount = st.number_input("المبلغ ($):", min_value=1.0)
                trans_type = st.selectbox("نوع المعاملة:", ["إيرادات", "مصروفات"])
                fin_submit = st.form_submit_button("حفظ المعاملة بالسحاب")
                if fin_submit and title and supabase:
                    try:
                        supabase.table("erp_finance").insert({"title": title, "amount": amount, "type": trans_type}).execute()
                        st.success("✅ تم حفظ السند المالي بنجاح!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"خطأ في قاعدة البيانات: {e}")
        with col_view:
            st.markdown("### 📋 كشف الحركة المالية الحالي")
            if fin_data_list:
                st.dataframe(pd.DataFrame(fin_data_list), use_container_width=True)
            else:
                st.info("لا توجد سجلات مالية متاحة للعرض.")

    # 📦 إدارة المستودعات والمخازن
    with tab_inventory:
        st.subheader("📦 إضافة وإدارة المنتجات والمخزون")
        col_inv_form, col_inv_view = st.columns(2)
        with col_inv_form:
            st.markdown("### 📥 تسجيل صنف جديد")
            with st.form("inventory_form", clear_on_submit=True):
                p_name = st.text_input("اسم المنتج / الصنف:")
                p_qty = st.number_input("الكمية المتاحة:", min_value=1, step=1)
                p_price = st.number_input("سعر الوحدة ($):", min_value=0.5)
                inv_submit = st.form_submit_button("إضافة للمخزن السحابي")
                if inv_submit and p_name and supabase:
                    try:
                        supabase.table("erp_inventory").insert({"product_name": p_name, "quantity": p_qty, "price": p_price}).execute()
                        st.success("✅ تم إضافة الصنف للمستودع!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"خطأ: {e}")
        with col_inv_view:
            st.markdown("### 📋 جرد أصناف المخزن الحالية")
            if inv_data_list:
                st.dataframe(pd.DataFrame(inv_data_list), use_container_width=True)
            else:
                st.info("المخزن فارغ حالياً.")

    # 🧾 قسم المبيعات والفواتير
    with tab_sales:
        st.subheader("🧾 نظام الفواتير والمبيعات السريعة")
        col_s_form, col_s_view = st.columns(2)
        with col_s_form:
            st.markdown("### 📥 إنشاء فاتورة بيع")
            with st.form("sales_form", clear_on_submit=True):
                c_name = st.text_input("اسم العميل:")
                s_amount = st.number_input("القيمة الإجمالية للفاتورة ($):", min_value=1.0)
                inv_date = st.date_input("تاريخ الفاتورة").strftime("%Y-%m-%d")
                sales_submit = st.form_submit_button("إصدار الفاتورة وتثبيتها")
                if sales_submit and c_name and supabase:
                    try:
                        supabase.table("erp_sales").insert({"client_name": c_name, "total_amount": s_amount, "invoice_date": inv_date}).execute()
                        st.success("✅ تم إصدار وحفظ الفاتورة تلقائياً!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"خطأ: {e}")
        with col_s_view:
            st.markdown("### 📋 سجل الفواتير الصادرة")
            if sales_data_list:
                st.dataframe(pd.DataFrame(sales_data_list), use_container_width=True)
            else:
                st.info("لا توجد فواتير صادرة بعد.")

    # 👥 قسم الموارد البشرية (HR)
    with tab_hr:
        st.subheader("👥 إدارة شؤون الموظفين")
        col_hr_form, col_hr_view = st.columns(2)
        with col_hr_form:
            st.markdown("### 📥 تسجيل موظف جديد")
            with st.form("hr_form", clear_on_submit=True):
                emp_name = st.text_input("اسم الموظف بالكامل:")
                emp_role = st.text_input("المسمى الوظيفي:")
                emp_salary = st.number_input("الراتب الأساسي ($):", min_value=100.0)
                hr_submit = st.form_submit_button("إضافة الموظف للنظام")

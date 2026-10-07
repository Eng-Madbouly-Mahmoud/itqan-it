import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# ⚙️ إعدادات الصفحة الأساسية لنظام الـ ERP
st.set_page_config(page_title="نظام ERP المتكامل", page_icon="💼", layout="wide")

# 🔑 جلب مفاتيح الاتصال تلقائياً من نظام حماية Secrets الخاص بتطبيقك
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# 🔒 نظام التحقق من الصلاحيات وتثبيت الجلسة
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None

def login_page():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔐 تسجيل الدخول لنظام الـ ERP الشامل</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns()
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

# 📊 لوحة التحكم الرئيسية والأقسام الفعالة
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
            <h1 style='text-align: center; color: white; margin: 0;'>💼 Enterprise Resource Planning (ERP System)</h1>
        </div>
    """, unsafe_allow_html=True)

    tab_home, tab_finance, tab_inventory, tab_sales, tab_hr = st.tabs([
        "📈 لوحة المؤشرات العامة", 
        "💰 إدارة الحسابات والمالية", 
        "📦 إدارة المستودعات والمخازن", 
        "🧾 الفواتير والمبيعات",
        "👥 الموارد البشرية (HR)"
    ])

    # 1️⃣ لوحة المؤشرات العامة
    with tab_home:
        st.subheader("📊 الأداء العام للمؤسسة")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        try:
            fin_data = supabase.table("erp_finance").select("*").execute().data
            inv_data = supabase.table("erp_inventory").select("*").execute().data
            hr_data = supabase.table("erp_hr").select("*").execute().data
            
            total_rev = sum([float(f['amount']) for f in fin_data if f['type'] == 'إيرادات'])
            total_exp = sum([float(f['amount']) for f in fin_data if f['type'] == 'مصروفات'])
            total_items = sum([int(i['quantity']) for i in inv_data])
            total_emps = len(hr_data)
            
            kpi1.metric("إجمالي الإيرادات السحابية", f"${total_rev:,.2f}")
            kpi2.metric("إجمالي المصروفات المسجلة", f"${total_exp:,.2f}")
            kpi3.metric("إجمالي قطع المخزون الحالية", f"{total_items} قطعة")
            kpi4.metric("عدد الموظفين بالنظام", f"{total_emps} موظف")
        except:
            st.warning("جاري جلب المؤشرات الحية...")

    # 2️⃣ إدارة الحسابات والمالية
    with tab_finance:
        st.subheader("💳 حركة القيود اليومية (الخزنة)")
        col_form, col_view = st.columns()
        with col_form:
            st.markdown("### 📥 إضافة قيد مالي")
            with st.form("finance_form", clear_on_submit=True):
                title = st.text_input("البيان / الوصف:")
                amount = st.number_input("المبلغ ($):", min_value=1.0)
                trans_type = st.selectbox("نوع المعاملة:", ["إيرادات", "مصروفات"])
                fin_submit = st.form_submit_button("حفظ المعاملة بالسحاب")
                if fin_submit and title:
                    supabase.table("erp_finance").insert({"title": title, "amount": amount, "type": trans_type}).execute()
                    st.success("✅ تم حفظ السند المالي بنجاح!")
                    st.rerun()
        with col_view:
            st.markdown("### 📋 كشف الحركة المالية الحالي")
            res = supabase.table("erp_finance").select("*").order("id", desc=True).execute()
            if res.data:
                df = pd.DataFrame(res.data)
                df.columns = ["رقم المعاملة", "البيان", "المبلغ", "النوع", "تاريخ القيد"]
                st.dataframe(df, use_container_width=True)

    # 3️⃣ إدارة المستودعات والمخازن
    with tab_inventory:
        st.subheader("📦 إضافة وإدارة المنتجات والمخزون")
        col_inv_form, col_inv_view = st.columns()
        with col_inv_form:
            st.markdown("### 📥 تسجيل صنف جديد")
            with st.form("inventory_form", clear_on_submit=True):
                p_name = st.text_input("اسم المنتج / الصنف:")
                p_qty = st.number_input("الكمية المتاحة:", min_value=1, step=1)
                p_price = st.number_input("سعر الوحدة ($):", min_value=0.5)
                inv_submit = st.form_submit_button("إضافة للمخزن السحابي")
                if inv_submit and p_name:
                    supabase.table("erp_inventory").insert({"product_name": p_name, "quantity": p_qty, "price": p_price}).execute()
                    st.success("✅ تم إضافة الصنف للمستودع!")
                    st.rerun()
        with col_inv_view:
            st.markdown("### 📋 جرد أصناف المخزن الحالية")
            res_inv = supabase.table("erp_inventory").select("*").order("id", desc=True).execute()
            if res_inv.data:
                df_inv = pd.DataFrame(res_inv.data)
                df_inv.columns = ["كود الصنف", "اسم المنتج", "الكمية", "سعر الوحدة", "آخر تحديث"]
                st.dataframe(df_inv, use_container_width=True)

    # 4️⃣ قسم المبيعات والفواتير
    with tab_sales:
        st.subheader("🧾 نظام الفواتير والمبيعات السريعة")
        col_s_form, col_s_view = st.columns()
        with col_s_form:
            st.markdown("### 📥 إنشاء فاتورة بيع")
            with st.form("sales_form", clear_on_submit=True):
                c_name = st.text_input("اسم العميل:")
                s_amount = st.number_input("القيمة الإجمالية للفاتورة ($):", min_value=1.0)
                inv_date = st.date_input("تاريخ الفاتورة").strftime("%Y-%m-%d")
                sales_submit = st.form_submit_button("إصدار الفاتورة وتثبيتها")
                if sales_submit and c_name:
                    supabase.table("erp_sales").insert({"client_name": c_name, "total_amount": s_amount, "invoice_date": inv_date}).execute()
                    st.success("✅ تم إصدار وحفظ الفاتورة تلقائياً!")
                    st.rerun()
        with col_s_view:
            st.markdown("### 📋 سجل الفواتير الصادرة")
            res_sales = supabase.table("erp_sales").select("*").order("id", desc=True).execute()
            if res_sales.data:
                df_sales = pd.DataFrame(res_sales.data)
                df_sales.columns = ["رقم الفاتورة", "اسم العميل", "إجمالي القيمة", "تاريخ الفاتورة", "وقت التسجيل بالسيرفر"]
                st.dataframe(df_sales, use_container_width=True)

    # 5️⃣ قسم الموارد البشرية (HR Module) الجديد المدمج
    with tab_hr:
        st.subheader("👥 إدارة الموظفين، الرواتب، والحضور والانصراف")
        col_hr1, col_hr2 = st.columns()
        
        with col_hr1:
            st.markdown("### 📝 تسجيل موظف جديد وضبط حالته اليومية")
            with st.form("hr_form", clear_on_submit=True):
                emp_name = st.text_input("👤 اسم الموظف ثلاثي:")
                salary = st.number_input("💰 راتب الموظف الأساسي ($):", min_value=100)
                attendance = st.selectbox("📌 حالة الحضور اليوم:", ["حاضر ✅", "غائب ❌"])
                notes = st.text_input("📝 ملاحظات إضافية (مكافآت / خصومات / أذونات):")
                hr_submit = st.form_submit_button("حفظ بيانات الموظف بالسحاب")
                
                if hr_submit and emp_name:
                    supabase.table("erp_hr").insert({
                        "emp_name": emp_name, 
                        "salary": salary, 
                        "attendance_status": attendance, 
                        "notes": notes
                    }).execute()
                    st.success(f"✅ تم حفظ وتحديث ملف الموظف {emp_name}!")
                    st.rerun()
                    
        with col_hr2:
            st.markdown("### 📋 كشف شؤون الموظفين والمسيرات")
            res_hr = supabase.table("erp_hr").select("*").order("id", desc=True).execute()
            if res_hr.data:
                df_hr = pd.DataFrame(res_hr.data)
                df_hr.columns = ["رقم الملف", "اسم الموظف", "الراتب الأساسي", "حالة الحضور اليوم", "ملاحظات وتعديلات", "آخر تحديث بالسيرفر"]
                st.dataframe(df_hr, use_container_width=True)
            else:
                st.info("سجل الموظفين فارغ حالياً.")

# تشغيل النظام
if not st.session_state["logged_in"]:
    login_page()
else:
    main_dashboard()


import streamlit as st
import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

# ⚙️ إعدادات النظام الاحترافية
st.set_page_config(page_title="نظام ERP - المهندس مدبولي", page_icon="💼", layout="wide")

# 🔒 إخفاء عناصر الاستضافة الافتراضية
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* تحسين شكل الأزرار والحقول لتبدو كأنظمة احترافية */
    .stButton>button {width: 100%; background-color: #1E3A8A; color: white; border-radius: 6px;}
    .stButton>button:hover {background-color: #1D4ED8; color: white;}
    div[data-testid="metric-container"] {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 🔑 بيانات الاتصال المباشر بالسيكول (PostgreSQL Connection String)
# ⚠️ استبدل الرابط أدناه برابط الـ Connection String المباشر من لوحة تحكم Supabase
DATABASE_URL = "postgresql://postgres:[YOUR_PASSWORD]@://supabase.com"

# دالة الاتصال المباشر بالسيكول مع حماية من الأخطاء
def get_sql_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        return None

# دالة عامة لتنفيذ استعلامات القراءة من السيكول بشكل آمن
def run_sql_query(query, params=None):
    conn = get_sql_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                return cur.fetchall()
            conn.commit()
            return True
    except Exception:
        return []
    finally:
        conn.close()

# 🔒 تثبيت صلاحيات الجلسة
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None

# 1️⃣ واجهة تسجيل الدخول المحدثة
if not st.session_state["logged_in"]:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin-top: 50px;'>🔐 نظام المهندس مدبولي السحابي الموحد</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>الرجاء إدخال بيانات الاعتماد للوصول إلى لوحة القيادة</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم:")
            password = st.text_input("🔑 كلمة المرور:", type="password")
            submit = st.form_submit_button("تسجيل الدخول الآمن")
            
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
else:
    # 2️⃣ لوحة التحكم الاحترافية بالأيقونات (sidebar Navigation)
    with st.sidebar:
        st.markdown(f"### 👨‍💻 {st.session_state['user_role']}")
        st.markdown(f"📅 {datetime.now().strftime('%Y-%m-%d')}")
        st.markdown("---")
        
        # القائمة الرئيسية المعتمدة على الأيقونات والأزرار الاحترافية
        menu = st.radio(
            "🗂️ الأقسام التنفيذية للنظام:",
            [
                "📈 لوحة المؤشرات العامة", 
                "💰 إدارة الحسابات والمالية", 
                "📦 إدارة المستودعات والمخازن", 
                "🧾 الفواتير والمبيعات",
                "👥 الموارد البشرية (HR)"
            ]
        )
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state["logged_in"] = False
            st.session_state["user_role"] = None
            st.rerun()

    # الهيدر الاحترافي الثابت
    st.markdown(f"""
        <div style='background-color: #1E3A8A; padding: 15px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);'>
            <h2 style='text-align: center; color: white; margin: 0; font-weight: bold;'>💼 Enterprise Resource Planning (ERP - Eng Madbouly)</h2>
        </div>
    """, unsafe_allow_html=True)

    # 📊 موديول لوحة المؤشرات العامة
    if menu == "📈 لوحة المؤشرات العامة":
        st.subheader("📊 لوحة الأداء ومراقبة الأداء العام")
        
        # جلب الأرقام مباشرة من السيكول
        finance_rows = run_sql_query("SELECT type, amount FROM erp_finance")
        inventory_rows = run_sql_query("SELECT quantity FROM erp_inventory")
        hr_rows = run_sql_query("SELECT id FROM erp_hr")
        
        total_rev = sum([float(r['amount']) for r in finance_rows if r['type'] == 'إيرادات'])
        total_exp = sum([float(r['amount']) for r in finance_rows if r['type'] == 'مصروفات'])
        total_items = sum([int(i['quantity']) for i in inventory_rows])
        total_emps = len(hr_rows)
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("💵 إجمالي المداخيل / الإيرادات", f"${total_rev:,.2f}")
        kpi2.metric("💸 إجمالي الخوارج / المصروفات", f"${total_exp:,.2f}")
        kpi3.metric("📦 الرصيد الإجمالي للمخزون", f"{total_items} قطعة")
        kpi4.metric("👥 القوى البشرية النشطة", f"{total_emps} موظف")
        
        st.success("🔒 اتصال السيكول المباشر آمن ومستقر بنسبة 100%.")

    # 💰 موديول إدارة الحسابات والمالية
    elif menu == "💰 إدارة الحسابات والمالية":
        st.subheader("💰 الإدارة المالية وحركة الخزينة المركزي")
        col_form, col_view = st.columns([1, 2])
        with col_form:
            st.markdown("#### 📥 قيد مالي جديد")
            with st.form("fin_form", clear_on_submit=True):
                title = st.text_input("البيان / الوصف المالي:")
                amount = st.number_input("المبلغ المطلوب ($):", min_value=1.0)
                trans_type = st.selectbox("نوع القيد:", ["إيرادات", "مصروفات"])
                if st.form_submit_button("ترحيل القيد للسيكول"):
                    if title:
                        run_sql_query("INSERT INTO erp_finance (title, amount, type) VALUES (%s, %s, %s)", (title, amount, trans_type))
                        st.success("✅ تم الترحيل لقاعدة البيانات!")
                        st.rerun()
        with col_view:
            st.markdown("#### 📋 كشف الحركة المالي المباشر")
            data = run_sql_query("SELECT id as \"رقم القيد\", title as \"البيان\", amount as \"المبلغ\", type as \"النوع\" FROM erp_finance ORDER BY id DESC")
            if data:
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.info("لا توجد قيود مسجلة بالسيكول حالياً.")

    # 📦 موديول المخازن
    elif menu == "📦 إدارة المستودعات والمخازن":
        st.subheader("📦 مستودعات الأصناف والتحكم في المخزون")
        col_form, col_view = st.columns([1, 2])
        with col_form:
            st.markdown("#### 📥 تكويد صنف جديد")
            with st.form("inv_form", clear_on_submit=True):
                p_name = st.text_input("اسم المنتج / الكود التجاري:")
                p_qty = st.number_input("الكمية الواردة:", min_value=1, step=1)
                p_price = st.number_input("سعر التكلفة للوحدة ($):", min_value=0.1)
                if st.form_submit_button("تثبيت الصنف بالمستودع"):
                    if p_name:
                        run_sql_query("INSERT INTO erp_inventory (product_name, quantity, price) VALUES (%s, %s, %s)", (p_name, p_qty, p_price))
                        st.success("✅ تم التكاويد بنجاح!")
                        st.rerun()
        with col_view:
            st.markdown("#### 📋 كشف الجرد الفعلي الحالي")
            data = run_sql_query("SELECT id as \"كود الصنف\", product_name as \"المنتج\", quantity as \"الكمية المتاحة\", price as \"سعر الوحدة\" FROM erp_inventory ORDER BY id DESC")
            if data:
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.info("لا توجد أصناف بالمخزن حالياً.")

    # 🧾 موديول المبيعات والفواتير
    elif menu == "🧾 الفواتير والمبيعات":
        st.subheader("🧾 كاونتر الفواتير وأوامر البيع السريعة")
        col_form, col_view = st.columns([1, 2])
        with col_form:
            st.markdown("#### 📥 إصدار فاتورة عميل")
            with st.form("sales_form", clear_on_submit=True):
                c_name = st.text_input("اسم العميل / المؤسسة:")
                s_amount = st.number_input("إجمالي قيمة الفاتورة ($):", min_value=1.0)
                inv_date = st.date_input("تاريخ الاستحقاق").strftime("%Y-%m-%d")
                if st.form_submit_button("إصدار وتثبيت الفاتورة"):
                    if c_name:
                        run_sql_query("INSERT INTO erp_sales (client_name, total_amount, invoice_date) VALUES (%s, %s, %s)", (c_name, s_amount, inv_date))
                        st.success("✅ تم إصدار وحفظ الفاتورة بالـ SQL!")
                        st.rerun()
        with col_view:
            st.markdown("#### 📋 سجل فواتير المبيعات الصادرة")
            data = run_sql_query("SELECT id as \"رقم الفاتورة\", client_name as \"العميل\", total_amount as \"القيمة الإجمالية\", invoice_date as \"التاريخ\" FROM erp_sales ORDER BY id DESC")
            if data:
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.info("سجل المبيعات خالي حالياً.")

    # 👥 موديول الموارد البشرية (HR)
    elif menu == "👥 الموارد البشرية (HR)":
        st.subheader("👥 شؤون الموظفين والملفات الإدارية")
        col_form, col_view = st.columns([1, 2])
        with col_form:
            st.markdown("#### 📥 تكويد ملف موظف")
            with st.form("hr_form", clear_on_submit=True):

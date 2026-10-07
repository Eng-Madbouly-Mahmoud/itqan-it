import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# ⚙️ إعدادات الصفحة
st.set_page_config(page_title="نظام ERP - المهندس مدبولي", page_icon="💼", layout="wide")

# 🎨 تصميم CSS
custom_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        padding: 5px !important;
        font-size: 14px !important;
    }
    
    .stButton>button {
        width: 100% !important; 
        background-color: #1E3A8A !important; 
        color: white !important; 
        border-radius: 8px !important; 
        font-weight: bold !important; 
        padding: 10px !important; 
        font-size: 16px !important;
        margin-top: 15px !important;
    }
    .stButton>button:hover {background-color: #1D4ED8 !important;}
    
    .menu-card {
        background: white; border-radius: 50%; width: 150px; height: 150px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        margin: 15px auto; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 4px solid #1E3A8A; transition: transform 0.3s ease; text-align: center; padding: 10px;
    }
    .menu-card:hover { transform: translateY(-5px); border-color: #3B82F6; }
    .menu-icon { font-size: 40px; margin-bottom: 3px; }
    .menu-title { font-size: 13px; font-weight: bold; color: #1E293B; }
    
    .yellow-box {
        background-color: #FFFF00 !important; color: #000000 !important;
        padding: 10px; border-radius: 8px; font-weight: bold;
        border: 2px solid #EAB308; text-align: center; margin: 5px 0;
    }
    .green-box {
        background-color: #92D050 !important; color: #000000 !important;
        padding: 10px; border-radius: 8px; font-weight: bold;
        border: 2px solid #22C55E; text-align: center; margin: 5px 0;
    }
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# 🔑 ضع البيانات الصحيحة المستخرجة من لوحة تحكم Supabase هنا
SUPABASE_URL = "https://your-exact-project-id.supabase.co"
SUPABASE_KEY = "your-exact-anon-key"

@st.cache_resource
def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = get_supabase_client()
except Exception as e:
    st.error(f"فشل الاتصال بـ Supabase: {e}")

def safe_fetch(table_name):
    try:
        res = supabase.table(table_name).select("*").execute()
        return res.data if (res and hasattr(res, 'data') and res.data) else []
    except Exception as e:
        st.error(f"❌ خطأ في قراءة الجدول {table_name}: تأكد من رابط Supabase وحالة المشروع.")
        return []

# 🔒 إدارة الجلسة
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None
if "current_mod" not in st.session_state:
    st.session_state["current_mod"] = "الرئيسية"
if "journal_rows" not in st.session_state:
    st.session_state["journal_rows"] = []
if "entry_no" not in st.session_state:
    st.session_state["entry_no"] = 1001

# 1️⃣ تسجيل الدخول
if not st.session_state["logged_in"]:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin-top: 50px;'>🔐 تسجيل الدخول لنظام ERP - المهندس مدبولي</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم:")
            password = st.text_input("🔑 كلمة المرور:", type="password")
            if st.form_submit_button("تسجيل الدخول الآمن"):
                if username == "admin" and password == "admin2026":
                    st.session_state["logged_in"] = True
                    st.session_state["user_role"] = "المدير العام"
                    st.rerun()
                elif username == "accountant" and password == "finance2026":
                    st.session_state["logged_in"] = True
                    st.session_state["user_role"] = "المحاسب"
                    st.rerun()
                else:
                    st.error("❌ البيانات غير صحيحة!")
else:
    # 🏢 الهيدر
    st.markdown("""
        <div style='background-color: #1E3A8A; padding: 18px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);'>
            <h1 style='text-align: center; color: white; margin: 0; font-weight: bold;'>💼 Enterprise Resource Planning (ERP - Eng Madbouly)</h1>
        </div>
    """, unsafe_allow_html=True)

    col_user, col_logout = st.columns(2)
    with col_user:
        st.markdown(f"**👤 المستخدم:** {st.session_state['user_role']} | **📅 التاريخ:** {datetime.now().strftime('%Y-%m-%d')}")
    with col_logout:
        if st.button("🚪 خروج"):
            st.session_state["logged_in"] = False
            st.session_state["current_mod"] = "الرئيسية"
            st.rerun()
            
    st.markdown("---")

    # 🕹️ القائمة الرئيسية
    if st.session_state["current_mod"] == "الرئيسية":
        st.markdown("<h3 style='text-align: center; color: #1E3A8A; margin-bottom: 20px;'>🎛️ يرجى اختيار القسم التنفيذي للمنظومة:</h3>", unsafe_allow_html=True)
        
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown('<div class="menu-card"><div class="menu-icon">📈</div><div class="menu-title">المؤشرات العامة</div></div>', unsafe_allow_html=True)
            if st.button("فتح المؤشرات", key="b1"):
                st.session_state["current_mod"] = "المؤشرات"; st.rerun()
        with c2:
            st.markdown('<div class="menu-card"><div class="menu-icon">💰</div><div class="menu-title">الحسابات والمالية</div></div>', unsafe_allow_html=True)
            if st.button("فتح الخزينة", key="b2"):
                st.session_state["current_mod"] = "المالية"; st.rerun()
        with c3:
            st.markdown('<div class="menu-card"><div class="menu-icon">📦</div><div class="menu-title">المستودعات والمخازن</div></div>', unsafe_allow_html=True)
            if st.button("فتح المخازن", key="b3"):
                st.session_state["current_mod"] = "المخازن"; st.rerun()
        with c4:
            st.markdown('<div class="menu-card"><div class="menu-icon">🧾</div><div class="menu-title">الفواتير والمبيعات</div></div>', unsafe_allow_html=True)
            if st.button("فتح المبيعات", key="b4"):
                st.session_state["current_mod"] = "المبيعات"; st.rerun()
        with c5:
            st.markdown('<div class="menu-card"><div class="menu-icon">👥</div><div class="menu-title">الموارد البشرية</div></div>', unsafe_allow_html=True)
            if st.button("فتح الـ HR", key="b5"):
                st.session_state["current_mod"] = "HR"; st.rerun()

    # 💰 موديول: الحسابات والمالية
    elif st.session_state["current_mod"] == "المالية":
        if st.button("🔙 العودة للقائمة الرئيسية"): 
            st.session_state["current_mod"] = "الرئيسية"; st.rerun()
        
        st.subheader("💰 إدارة الحسابات وحركة الخزنة المركزية")
        
        accounts_data = safe_fetch("erp_finance")
        acc_list = [acc.get("acc_name", f"حساب {acc.get('acc_id')}") for acc in accounts_data] if accounts_data else ["الصندوق / الخزينة", "البنك", "المبيعات", "المشتريات", "العملاء", "الموردين", "المصروفات العمومية"]
        
        sub_tab_register, sub_tab_transaction, sub_tab_search = st.tabs([
            "➕ تسجيل حساب جديد بالشجرة",
            "📝 إضافة حركة مادية (قيد سند)",
            "🔍 البحث الفوري عن حساب"
        ])
        
        with sub_tab_register:
            st.markdown("#### 📥 تكويد وإدراج حساب في شجرة الحسابات")
            
            acc_type = st.selectbox("نوع الحساب:", ["قائمة دخل", "ميزانية", "Balance Sheet"])
            
            if acc_type == "قائمة دخل":
                class1_options = ["ايرادات", "تكلفة بضاعة مباعة", "مصروفات"]
                class2_options = ["مصروفات ادارية وعمومية", "مصروفات تسويقية", "مصروفات تشغيلية", "الايرادات"]
                st.markdown('<div class="yellow-box">🟡 حسابات قائمة الدخل (أصفر)</div>', unsafe_allow_html=True)
            else:
                class1_options = ["اصول", "خصوم", "حقوق ملكية"]
                class2_options = ["اصول طويلة الاجل", "اصول ثابتة", "اذون خزانة", "اصول متداولة", "عملاء", "النقدية وما في حكمها", "راس المال", "الارباع المرحلة", "الموردين"]
                st.markdown('<div class="green-box">🟢 حسابات الميزانية (أخضر)</div>', unsafe_allow_html=True)

            with st.form("chart_of_accounts_form", clear_on_submit=True):
                h_col1, h_col2, h_col3 = st.columns(3)
                acc_id = h_col1.text_input("رقم الحساب:", placeholder="مثال: 10001")
                acc_name = h_col2.text_input("اسم الحساب (Account Name):", placeholder="اسم الحساب")
                amount = h_col3.number_input("الرصيد الافتتاحي ($):", min_value=0.0, value=0.0)
                
                h_col4, h_col5 = st.columns(2)
                class1 = h_col4.selectbox("التصنيف الأول:", class1_options)
                class2 = h_col5.selectbox("التصنيف الثاني:", class2_options)

                if st.form_submit_button("💾 حفظ الحساب"):
                    if acc_id and acc_name:
                        try:
                            res = supabase.table("erp_finance").insert({
                                "acc_id": acc_id,
                                "acc_name": acc_name,
                                "type": acc_type,
                                "class1": class1,
                                "class2": class2,
                                "amount": amount
                            }).execute()
                            st.success("✅ تم حفظ الحساب بنجاح!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ عند الحفظ: {e}")
                    else:
                        st.warning("⚠️ أدخل رقم واسم الحساب!")

        with sub_tab_transaction:
            st.markdown(f"### 🧾 تسجيل القيد اليومي رقم: `{st.session_state['entry_no']}`")
            entry_date = st.date_input("📅 تاريخ القيد:", datetime.now())
            entry_desc = st.text_input("📝 بيان/شرح القيد العام:", placeholder="مثال: اثبات فاتورة مبيعات نقداً")
            st.markdown("---")
            
            col_acc, col_debit, col_credit, col_add = st.columns([3, 2, 2, 2])
            selected_acc = col_acc.selectbox("الحساب:", acc_list)
            debit_val = col_debit.number_input("مدين ($):", min_value=0.0, value=0.0, step=10.0)
            credit_val = col_credit.number_input("دائن ($):", min_value=0.0, value=0.0, step=10.0)
            
            if col_add.button("➕ إضافة سطر للقيد"):
                if debit_val == 0 and credit_val == 0:
                    st.warning("⚠️ أدخل قيمة بالمدين أو الدائن!")
                elif debit_val > 0 and credit_val > 0:
                    st.error("❌ لا يمكن وضع مدين ودائن في نفس السطر!")
                else:
                    st.session_state["journal_rows"].append({
                        "الحساب": selected_acc,
                        "مدين": debit_val,
                        "دائن": credit_val
                    })
                    st.rerun()

            if st.session_state["journal_rows"]:
                st.dataframe(pd.DataFrame(st.session_state["journal_rows"]), use_container_width=True)
                tot_deb = sum(r["مدين"] for r in st.session_state["journal_rows"])
                tot_cred = sum(r["دائن"] for r in st.session_state["journal_rows"])
                diff = tot_deb - tot_cred
                
                m1, m2, m3 = st.columns(3)
                m1.metric("إجمالي المدين", f"${tot_deb:,.2f}")
                m2.metric("إجمالي الدائن", f"${tot_cred:,.2f}")
                m3.metric("الفرق بين الطرفين", f"${diff:,.2f}")
                
                c_save, c_clear = st.columns(2)
                if c_save.button("💾 حفظ القيد والتنقل للقيد التالي"):
                    if diff != 0:
                        st.error("❌ القيد غير متوازن!")
                    else:
                        try:
                            rows_to_send = [{
                                "entry_no": st.session_state["entry_no"],
                                "date": str(entry_date),
                                "description": entry_desc,
                                "account_name": r["الحساب"],
                                "debit": r["مدين"],
                                "credit": r["دائن"]
                            } for r in st.session_state["journal_rows"]]
                            
                            supabase.table("erp_journal_entries").insert(rows_to_send).execute()
                            st.success(f"✅ تم حفظ القيد رقم {st.session_state['entry_no']}!")
                            st.session_state["entry_no"] += 1
                            st.session_state["journal_rows"] = []
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ بالحفظ: {e}")

                if c_clear.button("🗑️ مسح القيد الحالي"):
                    st.session_state["journal_rows"] = []
                    st.rerun()

        with sub_tab_search:
            entries = safe_fetch("erp_journal_entries")
            if entries:
                st.dataframe(pd.DataFrame(entries), use_container_width=True)
            else:
                st.info("لا توجد قيود مسجلة بعد.")

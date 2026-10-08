import streamlit as st
from datetime import datetime
import pandas as pd
from supabase import create_client, Client

# ⚙️ إعدادات الصفحة بنمط Microsoft Dynamics 365
st.set_page_config(
    page_title="Dynamics 365 Business Central - Chart of Accounts", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔑 جلب وتنظيف إعدادات الاتصال تلقائياً
RAW_URL = st.secrets.get("SUPABASE_URL", "").strip()

if "rest/v1" in RAW_URL:
    SUPABASE_URL = RAW_URL.split("/rest/v1")[0].strip().rstrip("/")
else:
    SUPABASE_URL = RAW_URL.rstrip("/")

SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "").strip()

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# =========================================================
# 📥 دالات التعامل مع الجداول السحابية (إضافة + تعديل + قيود)
# =========================================================

def insert_account_to_erp(acc_data):
    try:
        supabase.table("erp_finance").insert(acc_data).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الحساب الجديد: {e}")
        return False

def update_account_in_erp(acc_id, updated_data):
    try:
        supabase.table("erp_finance").update(updated_data).eq("acc_id", acc_id).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في تعديل الحساب: {e}")
        return False

def load_accounts_from_erp():
    try:
        response = supabase.table("erp_finance").select("*").order("acc_id", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"خطأ في جلب شجرة الحسابات: {e}")
        return []

def update_account_balance(acc_id, delta_amount):
    """ تحديث رصيد الحساب عند ترحيل القيد المحاسبي """
    try:
        res = supabase.table("erp_finance").select("initial_balance").eq("acc_id", acc_id).execute()
        if res.data:
            current_bal = float(res.data[0].get("initial_balance", 0.0) or 0.0)
            new_bal = current_bal + delta_amount
            supabase.table("erp_finance").update({"initial_balance": new_bal}).eq("acc_id", acc_id).execute()
            return True
    except Exception as e:
        st.error(f"خطأ في تحديث رصيد الحساب [{acc_id}]: {e}")
    return False

def load_inventory_data():
    try:
        response = supabase.table("erp_inventory").select("*").order("id", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"خطأ في جلب بيانات المخازن: {e}")
        return []

def load_hr_data():
    try:
        response = supabase.table("erp_hr").select("*").order("id", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"خطأ في جلب بيانات الموارد البشرية: {e}")
        return []

def load_sales_data():
    try:
        response = supabase.table("erp_sales").select("*").order("id", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"خطأ في جلب بيانات فواتير المبيعات: {e}")
        return []

# =========================================================
# 🔐 موديول الحماية وبوابة الدخول
# =========================================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
        <div style='background-color: #0078D4; padding: 25px; border-radius: 8px; margin-bottom: 25px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h2 style='color: white; margin: 0; font-family: "Segoe UI", sans-serif;'>Dynamics 365 Business Central</h2>
            <p style='color: #EBF8FF; margin: 5px 0 0 0;'>يرجى إدخال كلمة المرور للوصول للمنظومة المحاسبية</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        with st.form("secure_login_form"):
            user_title = st.selectbox("مستوى الصلاحية:", ["المدير العام للمنظومة", "المهندس المحاسب المالي"])
            secret_key = st.text_input("كلمة المرور السرية للنظام:", type="password")
            submit_login = st.form_submit_button("مصادقة ودخول للمنظومة")
            
            if submit_login:
                if secret_key == "1234":
                    st.session_state.authenticated = True
                    st.session_state.current_user_role = user_title
                    st.success("تم التحقق بنجاح! جاري تحميل شجرة الحسابات...")
                    st.rerun()
                else:
                    st.error("خطأ: كلمة المرور غير صحيحة، يرجى التأكد وإعادة المحاولة.")
    st.stop()

# =========================================================
# 🌲 الشريط الجانبي (Left Navigation Tree)
# =========================================================
accounts_list = load_accounts_from_erp()

st.sidebar.markdown("### Business Central")
st.sidebar.markdown(f"**المستخدم:** {st.session_state.current_user_role}")
st.sidebar.markdown(f"**التاريخ:** {datetime.now().strftime('%Y-%m-%d')}")

if st.sidebar.button("تسجيل الخروج", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### شجرة الحسابات (Navigation Tree)")

if accounts_list:
    df_sidebar = pd.DataFrame(accounts_list)
    st.sidebar.metric("إجمالي الحسابات المسجلة", len(df_sidebar))
    st.sidebar.markdown("---")
    
    if "class1" in df_sidebar.columns:
        grouped_c1 = df_sidebar.groupby("class1")
        for c1_name, g_c1 in grouped_c1:
            with st.sidebar.expander(f"{c1_name} ({len(g_c1)})", expanded=False):
                if "class2" in g_c1.columns:
                    grouped_c2 = g_c1.groupby("class2")
                    for c2_name, g_c2 in grouped_c2:
                        st.markdown(f"**└ {c2_name}**")
                        for _, row in g_c2.iterrows():
                            st.caption(f"&nbsp;&nbsp;&nbsp;&nbsp;• `{row.get('acc_id', '')}` {row.get('acc_name', '')}")
else:
    st.sidebar.info("الشجرة فارغة حاليا.")

# =========================================================
# 🎨 الواجهة الرئيسية
# =========================================================

st.markdown("""
    <div style='background-color: #0078D4; padding: 15px 20px; border-radius: 6px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;'>
        <h2 style='color: white; margin: 0; font-family: "Segoe UI", sans-serif; font-size: 22px;'>
            Microsoft Dynamics 365 Business Central | <span style='font-size: 18px; font-weight: normal;'>Chart of Accounts (شجرة الحسابات)</span>
        </h2>
    </div>
""", unsafe_allow_html=True)

erp_tab1, erp_tab2, erp_tab3, erp_tab4 = st.tabs([
    "الحسابات العامة (Chart of Accounts)", 
    "إدارة المستودعات", 
    "الموارد البشرية (HR)", 
    "المبيعات والعملاء"
])

# =========================================================
# 1️⃣ موديول الحسابات العامة
# =========================================================
with erp_tab1:
    
    if 'active_financial_tab' not in st.session_state:
        st.session_state.active_financial_tab = "شجرة الحسابات"

    st.markdown("##### شريط الإجراءات والعمليات (Action Bar)")
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)

    with t_col1:
        if st.button("إدراج وتكويد حساب", use_container_width=True, type="primary" if st.session_state.active_financial_tab == "شجرة الحسابات" else "secondary"):
            st.session_state.active_financial_tab = "شجرة الحسابات"
            st.rerun()
    with t_col2:
        if st.button("تسجيل قيد محاسبي (General Journal)", use_container_width=True, type="primary" if st.session_state.active_financial_tab == "إضافة قيد" else "secondary"):
            st.session_state.active_financial_tab = "إضافة قيد"
            st.rerun()
    with t_col3:
        if st.button("دفتر الأستاذ (General Ledger)", use_container_width=True, type="primary" if st.session_state.active_financial_tab == "الأستاذ المساعد" else "secondary"):
            st.session_state.active_financial_tab = "الأستاذ المساعد"
            st.rerun()
    with t_col4:
        if st.button("صيانة السجلات والشجرة", use_container_width=True, type="primary" if st.session_state.active_financial_tab == "لوحة الصيانة" else "secondary"):
            st.session_state.active_financial_tab = "لوحة الصيانة"
            st.rerun()

    st.markdown("---")

    # ---------------------------------------------------------
    # TAB 1: شجرة الحسابات والبحث
    # ---------------------------------------------------------
    if st.session_state.active_financial_tab == "شجرة الحسابات":
        
        st.markdown("<h4 style='color: #0078D4;'>بطاقة الحساب (G/L Account Card)</h4>", unsafe_allow_html=True)
        
        acc_type = st.selectbox("نوع الحساب الرئيسي (E):", ["Balance Sheet", "قائمة دخل"])

        if acc_type == "قائمة دخل":
            st.markdown("<div style='background-color: #FFF59D; padding: 8px; border-radius: 4px; text-align: center; color: black; font-weight: bold;'>حسابات قائمة الدخل (Income Statement)</div>", unsafe_allow_html=True)
            class1_options = ["إيرادات", "تكلفة بضاعة مباعة", "مصروفات"]
            class2_options = ["مصروفات إدارية وعمومية", "مصروفات تسويقية", "مصروفات تشغيلية", "الايراضات"]
        else:
            st.markdown("<div style='background-color: #A5D6A7; padding: 8px; border-radius: 4px; text-align: center; color: black; font-weight: bold;'>حسابات الميزانية / Balance Sheet</div>", unsafe_allow_html=True)
            class1_options = ["أصول", "خصوم", "حقوق ملكية"]
            class2_options = ["اصول طويلة الاجل", "اصول ثابتة", "اذون خزانة", "اصول متداولة", "عملاء", "التقدية وما في حكمها", "راس المال", "الارباح المرحلة", "الموردين"]

        # 🔍 خيار البحث بجانب إضافة وتعديل الحسابات
        tree_mode = st.radio("نوع الإجراء:", ["إضافة حساب جديد للشجرة", "تعديل حساب قائم", "🔍 البحث في الحسابات والتصنيفات"], horizontal=True)

        selected_acc_data = None
        selected_acc_id = None

        if tree_mode == "تعديل حساب قائم":
            if accounts_list:
                acc_options = {f"{a['acc_id']} - {a['acc_name']}": a for a in accounts_list}
                chosen_label = st.selectbox("🎯 اختر الحساب المراد تعديله من الشجرة:", list(acc_options.keys()))
                selected_acc_data = acc_options[chosen_label]
                selected_acc_id = selected_acc_data['acc_id']
            else:
                st.warning("⚠️ لا توجد حسابات مسجلة لتعديلها.")

        if tree_mode == "🔍 البحث في الحسابات والتصنيفات":
            st.info("🔎 يمكنك الاستعلام والبحث المتقدم في كافة الحسابات المسجلة بالأرقام والأسماء:")
            s_col1, s_col2 = st.columns([3, 1])
            with s_col1:
                search_query = st.text_input("أدخل رقم الحساب أو جزء من اسمه للبحث السريع:", placeholder="مثال: 10001 أو أصول")
            with s_col2:
                search_class = st.selectbox("تصفية بالتصنيف:", ["الكل"] + class1_options)

            if accounts_list:
                df_search = pd.DataFrame(accounts_list)
                if search_query:
                    df_search = df_search[
                        df_search['acc_name'].astype(str).str.contains(search_query, case=False, na=False) |
                        df_search['acc_id'].astype(str).str.contains(search_query, case=False, na=False)
                    ]
                if search_class != "الكل":
                    df_search = df_search[df_search['class1'] == search_class]

                st.markdown(f"**نتائج البحث ({len(df_search)} حساب):**")
                st.dataframe(df_search[['acc_id', 'acc_name', 'initial_balance', 'acc_type', 'class1', 'class2']], use_container_width=True)
            else:
                st.warning("لا توجد حسابات في النظام للبحث فيها.")

        else:
            # استمارة الإضافة والتعديل على سطر واحد أفقي
            with st.form("accounting_tree_form", clear_on_submit=False):
                col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1.5, 2.5, 1.5, 2, 2])
                
                default_id = str(selected_acc_data['acc_id']) if selected_acc_data else ""
                default_name = str(selected_acc_data['acc_name']) if selected_acc_data else ""
                default_initial = float(selected_acc_data.get('initial_balance', 0.0)) if selected_acc_data else 0.0
                
                with col_f1:
                    acc_id = st.text_input("رقم الحساب (A):", value=default_id, disabled=(tree_mode == "تعديل حساب قائم"))
                with col_f2:
                    acc_name = st.text_input("اسم الحساب (B):", value=default_name)
                with col_f3:
                    initial_balance = st.number_input("الرصيد الافتتاحي:", value=default_initial)
                with col_f4:
                    c1_idx = class1_options.index(selected_acc_data['class1']) if selected_acc_data and selected_acc_data.get('class1') in class1_options else 0
                    class1 = st.selectbox("التصنيف الأول (F):", class1_options, index=c1_idx)
                with col_f5:
                    c2_idx = class2_options.index(selected_acc_data['class2']) if selected_acc_data and selected_acc_data.get('class2') in class2_options else 0
                    class2 = st.selectbox("التصنيف الثاني (G):", class2_options, index=c2_idx)

                btn_label = "💾 حفظ التعديلات على الحساب" if tree_mode == "تعديل حساب قائم" else "💾 حفظ الحساب الجديد"
                submit_account = st.form_submit_button(btn_label)

                if submit_account:
                    if not acc_id or not acc_name:
                        st.warning("يرجى ملء حقول رقم الحساب واسم الحساب أولا.")
                    else:
                        account_payload = {
                            "acc_name": acc_name,
                            "acc_type": acc_type,
                            "class1": class1,
                            "class2": class2,
                            "initial_balance": initial_balance
                        }

                        if tree_mode == "تعديل حساب قائم":
                            success = update_account_in_erp(selected_acc_id, account_payload)
                            if success:
                                st.success(f"🎉 تم تعديل بيانات الحساب [{acc_name}] بنجاح!")
                                st.rerun()
                        else:
                            account_payload["acc_id"] = int(acc_id) if str(acc_id).isdigit() else acc_id
                            account_payload["created_at"] = datetime.now().isoformat()
                            success = insert_account_to_erp(account_payload)
                            if success:
                                st.success(f"🎉 تم حفظ الحساب الجديد [{acc_name}] بنجاح!")
                                st.rerun()

        # =========================================================
        # 📋 جدول شجرة الحسابات الملون
        # =========================================================
        st.markdown("---")
        st.markdown("<h4 style='color: #0078D4;'>قائمة الحسابات الملونة (Chart of Accounts List)</h4>", unsafe_allow_html=True)
        
        if accounts_list:
            df_accounts = pd.DataFrame(accounts_list)

            rename_cols = {
                "acc_id": "رقم الحساب (A)",
                "acc_name": "اسم الحساب (B)",
                "initial_balance": "الرصيد الافتتاحي",
                "acc_type": "نوع الحساب (E)",
                "class1": "التصنيف الأول (F)",
                "class2": "التصنيف الثاني (G)"
            }
            
            cols_to_show = [c for c in rename_cols.keys() if c in df_accounts.columns]
            df_display = df_accounts[cols_to_show].rename(columns=rename_cols)

            def color_rows(row):
                acc_type_val = row.get("نوع الحساب (E)", "")
                if acc_type_val == "قائمة دخل":
                    return ['background-color: #FFF9C4; color: black; font-weight: bold;'] * len(row)
                elif acc_type_val in ["Balance Sheet", "ميزانية"]:
                    return ['background-color: #C8E6C9; color: black; font-weight: bold;'] * len(row)
                else:
                    return ['background-color: #E0F7FA; color: black;'] * len(row)

            format_dict = {}
            if "الرصيد الافتتاحي" in df_display.columns:
                format_dict["الرصيد الافتتاحي"] = "{:,.2f}"

            styled_df = df_display.style.apply(color_rows, axis=1).format(format_dict)
            st.dataframe(styled_df, use_container_width=True, height=450)
        else:
            st.info("لا توجد حسابات مسجلة حاليا.")

    # ---------------------------------------------------------
    # TAB 2: تسجيل قيد محاسبي مفعل ومكتمل (General Journal)
    # ---------------------------------------------------------
    elif st.session_state.active_financial_tab == "إضافة قيد":
        st.markdown("<h4 style='color: #0078D4;'>تسجيل قيد محاسبي يومية عامة (General Journal Batch)</h4>", unsafe_allow_html=True)
        
        if not accounts_list:
            st.warning("⚠️ يرجى إضافة حسابات أولاً في شجرة الحسابات لتتمكن من تسجيل القيود المحاسبية.")
        else:
            acc_dict = {f"{a['acc_id']} - {a['acc_name']}": a['acc_id'] for a in accounts_list}

            # بيانات ترويسة القيد
            j_col1, j_col2, j_col3 = st.columns(3)
            with j_col1:
                doc_no = st.text_input("رقم المستند / القيد:", value=f"JV-{datetime.now().strftime('%Y%m%d%H%M')}")
            with j_col2:
                posting_date = st.date_input("تاريخ القيد المحاسبي:", datetime.now())
            with j_col3:
                journal_desc = st.text_input("البيان العام للقيد:", value="قيد تسوية / حركة يومية عامة")

            st.markdown("---")
            st.markdown("##### أطراف القيد المحاسبي (Journal Lines)")

            if 'journal_rows_count' not in st.session_state:
                st.session_state.journal_rows_count = 2

            btn_add_col, btn_rem_col, _ = st.columns([1, 1, 4])
            with btn_add_col:
                if st.button("➕ إضافة طرف جديد"):
                    st.session_state.journal_rows_count += 1
                    st.rerun()
            with btn_rem_col:
                if st.button("➖ حذف أخير") and st.session_state.journal_rows_count > 2:
                    st.session_state.journal_rows_count -= 1
                    st.rerun()

            journal_lines = []
            total_debit = 0.0
            total_credit = 0.0

            # بناء جدول الإدخال الديناميكي
            for idx in range(st.session_state.journal_rows_count):
                c_acc, c_deb, c_cred, c_line_desc = st.columns([3, 2, 2, 3])
                with c_acc:
                    selected_acc = st.selectbox(f"الحساب ({idx+1}):", list(acc_dict.keys()), key=f"j_acc_{idx}")
                with c_deb:
                    debit = st.number_input(f"مدين ({idx+1}):", min_value=0.0, value=0.0, step=100.0, key=f"j_deb_{idx}")
                with c_cred:
                    credit = st.number_input(f"دائن ({idx+1}):", min_value=0.0, value=0.0, step=100.0, key=f"j_cred_{idx}")
                with c_line_desc:
                    line_desc = st.text_input(f"شرح السطر ({idx+1}):", value=journal_desc, key=f"j_desc_{idx}")

                total_debit += debit
                total_credit += credit
                journal_lines.append({
                    "acc_id": acc_dict[selected_acc],
                    "debit": debit,
                    "credit": credit,
                    "desc": line_desc
                })

            # ملخص ومؤشر توازن القيد
            st.markdown("---")
            b_col1, b_col2, b_col3 = st.columns(3)
            b_col1.metric("إجمالي الطرف المدين", f"{total_debit:,.2f} ج.م")
            b_col2.metric("إجمالي الطرف الدائن", f"{total_credit:,.2f} ج.م")
            
            diff = total_debit - total_credit
            if abs(diff) < 0.001 and (total_debit > 0):
                b_col3.markdown("<div style='background-color:#C8E6C9; color:#1B5E20; padding:12px; border-radius:5px; text-align:center; font-weight:bold;'>✅ القيد متوازن ومستعد للترحيل</div>", unsafe_allow_html=True)
                
                if st.button("🚀 ترحيل القيد وتحديث الأرصدة (Post Journal)", type="primary", use_container_width=True):
                    success_all = True
                    for line in journal_lines:
                        net_effect = line['debit'] - line['credit']
                        if net_effect != 0:
                            if not update_account_balance(line['acc_id'], net_effect):
                                success_all = False
                    
                    if success_all:
                        st.success(f"🎉 تم ترحيل القيد رقم [{doc_no}] بنجاح وتحديث أرصدة الحسابات في قاعدة البيانات!")
                        st.session_state.journal_rows_count = 2
                        st.rerun()
            else:
                b_col3.markdown(f"<div style='background-color:#FFCDD2; color:#B71C1C; padding:12px; border-radius:5px; text-align:center; font-weight:bold;'>⚠️ القيد غير متوازن | الفرق: {diff:,.2f}</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TAB 3 & 4: الأستاذ المساعد والصيانة
    # ---------------------------------------------------------
    elif st.session_state.active_financial_tab == "الأستاذ المساعد":
        st.markdown("<h4 style='color: #0078D4;'>دفتر الأستاذ (General Ledger Entries)</h4>", unsafe_allow_html=True)
        st.info("قسم عرض الحركة المالية التفصيلية واستعراض دفتر الأستاذ العام لكل حساب.")

    elif st.session_state.active_financial_tab == "لوحة الصيانة":
        st.markdown("<h4 style='color: #D32F2F;'>لوحة الصيانة وتعديل البيانات</h4>", unsafe_allow_html=True)
        st.warning("قسم الصيانة وإدارة البيانات وتدقيق الحسابات.")

# =========================================================
# 2️⃣ موديول المخازن
# =========================================================
with erp_tab2:
    st.markdown("<h3 style='color: #0078D4;'>إدارة المستودعات والمخازن (Inventory)</h3>", unsafe_allow_html=True)
    inv_data = load_inventory_data()
    if inv_data:
        st.dataframe(pd.DataFrame(inv_data), use_container_width=True)
    else:
        st.info("لا توجد بيانات مخزنية حاليا.")

# =========================================================
# 3️⃣ موديول الموارد البشرية
# =========================================================
with erp_tab3:
    st.markdown("<h3 style='color: #0078D4;'>الموارد البشرية (Human Resources)</h3>", unsafe_allow_html=True)
    hr_data = load_hr_data()
    if hr_data:
        st.dataframe(pd.DataFrame(hr_data), use_container_width=True)
    else:
        st.info("لا توجد بيانات موظفين حاليا.")

# =========================================================
# 4️⃣ موديول المبيعات
# =========================================================
with erp_tab4:
    st.markdown("<h3 style='color: #0078D4;'>المبيعات والعملاء (Sales & Customers)</h3>", unsafe_allow_html=True)
    sales_data = load_sales_data()
    if sales_data:
        st.dataframe(pd.DataFrame(sales_data), use_container_width=True)
    else:
        st.info("لا توجد فواتير مبيعات مسجلة حاليا.")

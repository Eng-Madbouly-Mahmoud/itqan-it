import streamlit as st
from datetime import datetime
from supabase import create_client, Client

# 🔑 إعدادات الاتصال بقاعدة بيانات Supabase السحابية الصحيحة لمشروعك
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0ZWpicm1manJlb2d1dXhvaHNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA2Nzc4ODUsImV4cCI6MjEwNjI1Mzg4NX0.mCmdj3d5ltZca-nGr7XEQPhBBsTFyGTXn2HOqr8l7M8"

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# 📥 دالة جلب البيانات من قاعدة البيانات السحابية Supabase
def load_data():
    try:
        response = supabase.table("tickets").select("*").order("id", desc=False).execute()
        tickets = []
        if response.data:
            for row in response.data:
                ticket = row.copy()
                ticket['ID'] = row.get('id', row.get('ID'))  
                ticket['name'] = row.get('name', 'غير مسجل')
                ticket['dept'] = row.get('dept', 'غير محدد')
                ticket['issue'] = row.get('issue', '-')
                ticket['status'] = row.get('status', 'Pending (قيد الانتظار)')
                ticket['solved_by'] = row.get('solved_by', 'لم تُحل بعد ⏳')
                ticket['created_at'] = row.get('created_at', '-')
                ticket['updated_at'] = row.get('updated_at', '-')
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
        max_id = max([int(t['ID']) for t in st.session_state.tickets if t.get('ID') is not None])
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
                
                if insert_ticket(new_ticket):
                    st.session_state.tickets = load_data()  
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
        
        st.session_state.tickets = load_data()
        
        if st.session_state.tickets and len(st.session_state.tickets) > 0:
            import pandas as pd
            df_report = pd.DataFrame(st.session_state.tickets)
            
            st.markdown("### 📊 استخراج التقارير وقائمة البلاغات التاريخية")
            st.dataframe(df_report[["ID", "name", "dept", "issue", "status", "solved_by", "created_at", "updated_at"]], use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🛠️ تحديث حالة تذكرة وإسنادها للمهندس في Supabase:")
            
            ticket_ids = [int(t['ID']) for t in st.session_state.tickets if t.get('ID') is not None]
            selected_id = st.selectbox("اختر رقم التذكرة للتعديل:", ticket_ids)
            
            current_ticket = next(t for t in st.session_state.tickets if int(t['ID']) == selected_id)
            
            current_engineer = current_ticket.get('solved_by', '')
            if current_engineer == "لم تُحل بعد ⏳":
                current_engineer = ""
                
            current_status = current_ticket.get('status', 'Pending (قيد الانتظار)')
            status_options = ["Pending (قيد الانتظار)", "In Progress (جاري العمل)", "Solved (تم حل المشكلة)"]
            
            it_engineer = st.text_input("👨‍💻 اسم المهندس القائم بالحل:", value=current_engineer)
            new_status = st.selectbox(
                "الحالة الجديدة للتذكرة:", 
                options=status_options, 
                index=status_options.index(current_status) if current_status in status_options else 0
            )
            
            save_changes = st.button("💾 حفظ التعديلات وتحديث السيرفر")
            
            if save_changes:
                if it_engineer.strip() == "":
                    engineer_name = "لم تُحل بعد ⏳"
                else:
                    engineer_name = it_engineer
                
                updated_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                
                updated_fields = {
                    "status": new_status,
                    "solved_by": engineer_name,
                    "updated_at": updated_time
                }
                
                if update_ticket_in_db(selected_id, updated_fields):

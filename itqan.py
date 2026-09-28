import streamlit as st
from datetime import datetime
import pandas as pd
import os

# اسم الملف الخارجي لحفظ البيانات
DATA_FILE = "tickets.csv"

# دالة لتحميل البيانات من ملف CSV
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            return df.to_dict(orient="records")
        except:
            return []
    return []

# دالة لحفظ البيانات إلى ملف CSV
def save_data(tickets_list):
    if tickets_list:
        df = pd.DataFrame(tickets_list)
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    else:
        if os.path.exists(DATA_FILE):
            pd.DataFrame(columns=["ID", "name", "dept", "issue", "status", "solved_by", "created_at", "updated_at"]).to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# تهيئة مخزن البيانات وقراءة الملف الخارجي
if 'tickets' not in st.session_state:
    st.session_state.tickets = load_data()

if 'next_id' not in st.session_state:
    if st.session_state.tickets:
        max_id = max([int(t['ID']) for t in st.session_state.tickets])
        st.session_state.next_id = max_id + 1
    else:
        st.session_state.next_id = 101

# إعدادات الصفحة والأيقونة الرئيسية للموقع
st.set_page_config(page_title="مركز الدعم الفني - IT", page_icon="🛠️", layout="wide")

# =========================================================
# 💻 محتوى النظام الأصلي
# =========================================================

# تصميم الهيدر مع الشريط الترحيبي المتحرك لشركة الهدى
st.markdown("""
    <div style='background-color: #1E3A8A; padding: 20px; border-radius: 10px; margin-bottom: 5px;'>
        <h1 style='text-align: center; color: white; margin: 0;'>لوحة تكنولوجيا المعلومات والشبكات ⚙️</h1>
    </div>
    <div style='background-color: #0F172A; padding: 8px; border-radius: 5px; margin-bottom: 20px;'>
        <marquee direction='right' style='color: #38BDF8; font-weight: bold; font-size: 16px; margin: 0;'>
            🏢 شركة الهدى للمقاولات ترحب بكم في المركز الذكي للدعم الفني .. الرجاء تسجيل بلاغات الأعطال بدقة لسرعة توجيه مهندس الـ IT إليكم فوراً 🛠️
        </marquee>
    </div>
""", unsafe_allow_html=True)

# إنشاء التبويبات العلوية للموقع
tab1, tab2 = st.tabs(["📝 بوابة الموظفين (تسجيل بلاغ عطل)", "🖥️ لوحة تحكم الـ IT (إدارة التذاكر)"])

# 📝 بوابة الموظفين
with tab1:
    st.markdown("<h3 style='text-align: right; color: #1E3A8A;'>📥 تسجيل بلاغ عطل جديد في النظام</h3>", unsafe_allow_html=True)
    st.write("برجاء ملء الخانات التالية بدقة ليتم توجيه الدعم الفني إليك فوراً:")
    
    with st.form("ticket_form", clear_on_submit=True):
        name = st.text_input("👤 اسم الموظف بالكامل (Employee Name):")
        dept = st.selectbox("🏢 القسم التابع له (Department):", ["الحسابات", "الموارد البشرية", "الهندسة المدنية", "المشتريات", "إدارة عامة", "المكتب الفني", "أخرى"])
        issue = st.text_area("⚠️ وصف العطل أو المشكلة التقنية بالتفصيل (Issue Description):")
        
        submit = st.form_submit_button("🚀 إرسال التذكرة إلى قسم الدعم الفني")
        
        if submit:
            if name.strip() and issue.strip():
                current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                
                new_ticket = {
                    "ID": st.session_state.next_id,
                    "name": name,
                    "dept": dept,
                    "issue": issue,
                    "status": "Pending (قيد الانتظار)",
                    "solved_by": "لم تُحل بعد ⏳",
                    "created_at": current_time,
                    "updated_at": "لم تُحدث بعد"
                }
                st.session_state.tickets.append(new_ticket)
                save_data(st.session_state.tickets)
                st.success(f"🎉 تم تسجيل بلاغك بنجاح يا هندسة! رقم التذكرة الخاص بك هو: #{st.session_state.next_id}")
                st.session_state.next_id += 1
                st.rerun()
            else:
                st.error("❌ الرجاء كتابة اسم الموظف ووصف العطل أولاً قبل الإرسال!")

# 🖥️ لوحة تحكم الـ IT
with tab2:
    st.markdown("<h3 style='text-align: right; color: #16A34A;'>🖥️ شاشة مراقبة وحل الأعطال الحالية</h3>", unsafe_allow_html=True)
    
    password = st.text_input("🔑 أدخل كلمة مرور الإدارة لتحديث التذاكر:", type="password")
    
    if password == "1234": 
        st.success("🔓 تم تفعيل صلاحيات المهندس المسؤول.")
        
        # 📊 قسم استخراج التقارير (يظهر فقط عند وجود تذاكر)
        if st.session_state.tickets:
            st.markdown("### 📊 استخراج التقارير")
            # تحويل التذاكر الحالية إلى DataFrame وتجهيزها للتحميل
            df_report = pd.DataFrame(st.session_state.tickets)
            csv_data = df_report.to_csv(index=False, encoding="utf-8-sig")
            
            # زر التحميل المباشر
            st.download_button(
                label="📥 تحميل تقرير الأعطال الشامل (ملف Excel / CSV)",
                data=csv_data,
                file_name=f"IT_Support_Report_{datetime.now().strftime('%Y-%m-%d')}.csv",
                mime="text/csv"
            )
            st.markdown("---")
        
        if st.session_state.tickets:
            st.markdown("### 🛠️ تحديث حالة تذكرة وإسنادها للمهندس:")
            ticket_ids = [int(t['ID']) for t in st.session_state.tickets]
            selected_id = st.selectbox("اختر رقم التذكرة للتعديل:", ticket_ids)
            
            it_engineer = st.text_input("👨‍💻 اسم المهندس القائم بالحل:")
            new_status = st.selectbox("الحالة الجديدة للتذكرة:", ["Pending (قيد الانتظار)", "In Progress (جاري العمل)", "Solved (تم حل المشكلة بنجاح ✅)"])
            
            if st.button("💾 حفظ تحديث التذكرة"):
                if it_engineer.strip():
                    for t in st.session_state.tickets:
                        if int(t['ID']) == selected_id:
                            t['updated_at'] = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                            t['status'] = new_status
                            t['solved_by'] = it_engineer if "Solved" in new_status else f"جاري المتابعة بواسطة {it_engineer}"
                            save_data(st.session_state.tickets)
                            st.success(f"✅ تم تحديث التذكرة #{selected_id} بنجاح!")
                            st.rerun()
                else:
                    st.error("⚠️ الرجاء كتابة اسم المهندس الذي قام بحل المشكلة أولاً!")
            st.markdown("---")
            
    elif password != "":
        st.error("❌ كلمة المرور غير صحيحة! لا تملك صلاحية تعديل التذاكر.")

    # عرض التذاكر المتاحة بشكل منظم
    if not st.session_state.tickets:
        st.info("💡 لا توجد تذاكر أو أعطال مسجلة حالياً في النظام. كل الأجهزة تعمل بكفاءة!")
    else:
        st.write(f"إجمالي الأعطال المسجلة حالياً: **{len(st.session_state.tickets)}** تذكرة.")
        st.markdown("---")
        
        for t in st.session_state.tickets:
            status_str = str(t['status'])
            bg_color = "#FEF2F2" if "Pending" in status_str else ("#FEF3C7" if "In Progress" in status_str else "#F0FDF4")
            border_color = "#DC2626" if "Pending" in status_str else ("#D97706" if "In Progress" in status_str else "#16A34A")
            
            t_created = t.get('created_at', 'تاريخ قديم')
            t_updated = t.get('updated_at', 'لم تُحدث')
            
            st.markdown(f"""
                <div style='background-color: {bg_color}; padding: 15px; border-radius: 8px; border-right: 5px solid {border_color}; margin-bottom: 15px;'>
                    <h4 style='margin: 0; color: #1E3A8A;'>📍 تذكرة رقم #{int(t['ID'])} <span style='float: left; font-size: 12px; color: #6B7280;'>📅 تاريخ الإرسال: {t_created}</span></h4>
                    <p style='margin: 5px 0;'><b>👤 الموظف:</b> {t['name']} | <b>🏢 القسم:</b> {t['dept']}</p>
                    <p style='margin: 5px 0;'><b>📋 وصف المشكلة:</b> {t['issue']}</p>
                    <p style='margin: 5px 0; color: {border_color};'><b>⚡ الحالة الحالية:</b> {t['status']}</p>
                    <p style='margin: 0; color: #4B5563;'><b>👨‍💻 القائم بالحل:</b> {t['solved_by']} <span style='float: left; font-size: 12px; color: #9CA3AF;'>⏱️ آخر تحديث: {t_updated}</span></p>
                </div>
            """, unsafe_allow_html=True)
import streamlit as st

# 1. إعدادات الصفحة (تظهر في تبويب المتصفح)
st.set_page_config(
    page_title="أتقان للمحاماه والاستشارات القانونيه والتحكيم",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. حقن الألوان الجديدة (البني الفاتح والأبيض) في كامل التطبيق لتغيير الثيم الافتراضي
st.markdown(
    """
    <style>
    /* تغيير خلفية التطبيق الأساسية إلى الأبيض والنصوص إلى البني الداكن */
    .stApp {
        background-color: #FFFFFF;
        color: #3E2723;
    }
    
    /* تنسيق القائمة الجانبية (Sidebar) باللون البني الفاتح جداً */
    [data-testid="stSidebar"] {
        background-color: #F5EFEB;
    }
    
    /* تنسيق الأزرار لتصبح باللون البني الفاتح والكتابة باللون الأبيض */
    div.stButton > button:first-child {
        background-color: #A47551;
        color: white;
        border-radius: 8px;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #8C5E3C;
        color: white;
    }
    
    /* توحيد نوع الخط ودعم النصوص العربية */
    html, body, [class*="css"]  {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    </style>
    """,
    unsafe_allow_html=True)

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
st.set_page_config(
    page_title="الدكتور صلاح حسب الله - مركز الدعم الفني - شركة إتقان",
    page_icon="⚖️",
    layout="wide"
)

# =========================================================
# 💻 محتوى نظام شركة إتقان للمحاماة (التصميم البني الجديد)
# =========================================================

# تصميم الهيدر مع اللوجو المدمج والشريط الترحيبي باللون البني والبيج الفخم
st.markdown("""
    <div style='background-color: #8C6239; padding: 25px; border-radius: 12px; margin-bottom: 5px; display: flex; align-items: center; justify-content: center; gap: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <!-- لوجو ميزان العدالة مدمج برمجياً بصيغة SVG -->
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

# تخصيص ألوان التبويبات (Tabs) لتتناسب مع الطابع البني من خلال CSS
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

# إنشاء التبويبات العلوية للموقع
tab1, tab2 = st.tabs(["📝 بوابة الموظفين والمستشارين (تسجيل عطل)", "🖥️ لوحة تحكم الـ IT (إدارة التذاكر)"])

# 📝 بوابة الموظفين
with tab1:
    st.markdown("<h3 style='text-align: right; color: #8C6239;'>📥 تسجيل بلاغ عطل تقني جديد في النظام</h3>", unsafe_allow_html=True)
    st.write("برجاء ملء الخانات التالية بدقة ليتم توجيه الدعم الفني إليك فوراً لتجنب تعطيل العمل القانوني:")
    
    with st.form("ticket_form", clear_on_submit=True):
        name = st.text_input("👤 اسم الموظف / المستشار بالكامل:")
        dept = st.selectbox("🏢 القسم / الإدارة التابع لها:", [
            "قسم الاداره العليا", 
            "بنك مصر", 
            "بنك الاهلي", 
            "التجاري الدولي", 
            "الادمن", 
            "إدارة عامة", 
            "أخرى"
        ])
        issue = st.text_area("⚠️ وصف العطل أو المشكلة التقنية بالتفصيل (مثل: مشكلة بالطابعة، انقطاع شبكة، عطل ببرامج الأرشيف):")
        
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
                st.success(f"🎉 تم تسجيل بلاغك بنجاح! رقم التذكرة الخاص بك هو: #{st.session_state.next_id}")
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
        
        # 📊 قسم استخراج التقارير (يظهر فقط عند وجود تذاكر)
        if st.session_state.tickets:
            st.markdown("### 📊 استخراج التقارير")
            df_report = pd.DataFrame(st.session_state.tickets)
            csv_data = df_report.to_csv(index=False, encoding="utf-8-sig")
            
            st.download_button(
                label="📥 تحميل تقرير الأعطال الشامل (ملف CSV)",
                data=csv_data,
                file_name=f"Etqan_Law_IT_Report_{datetime.now().strftime('%Y-%m-%d')}.csv",
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
                    st.error("⚠️ الرجاء كتابة اسم المهندس أولاً!")
            st.markdown("---")
            
    elif password != "":
        st.error("❌ كلمة المرور غير صحيحة! لا تملك صلاحية تعديل التذاكر.")

    # عرض التذاكر المتاحة بشكل منظم
    st.markdown("### 📋 قائمة البلاغات الحالية في النظام")
    if not st.session_state.tickets:
        st.info("💡 لا توجد تذاكر أو بلاغات مسجلة حالياً.")
    else:
        df_display = pd.DataFrame(st.session_state.tickets)
        # إعادة ترتيب الأعمدة لتظهر للمهندس بشكل منظم ومفهوم
        df_display.columns = ["رقم التذكرة", "اسم الموظف", "القسم", "وصف المشكلة", "الحالة", "المسؤول عن الحل", "تاريخ الإنشاء", "آخر تحديث"]
        st.dataframe(df_display, use_container_width=True)

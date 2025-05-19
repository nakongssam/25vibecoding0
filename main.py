import streamlit as st
import sqlite3
from datetime import datetime

# 데이터베이스 연결
conn = sqlite3.connect('gratitude_journal.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        student TEXT,
        entry_number INTEGER,
        target TEXT,
        content TEXT,
        shared INTEGER DEFAULT 0
    )
''')
conn.commit()

# 날짜 및 사용자 이름
st.set_page_config(page_title="감사일기 앱", page_icon="📘", layout="centered")
st.markdown("<h1 style='text-align: center;'>💙 오늘의 감사일기 💙</h1>", unsafe_allow_html=True)
today = datetime.now().strftime("%Y-%m-%d")

with st.form("gratitude_form"):
    student_name = st.text_input("닉네임을 입력하세요:", "")

    entries = []
    for i in range(1, 4):
        col1, col2 = st.columns([1, 3])
        with col1:
            target = st.text_input(f"감사 대상 {i}", key=f"target_{i}")
        with col2:
            content = st.text_input(f"감사 내용 {i}", key=f"content_{i}")
        entries.append((target, content))

    share_option = st.checkbox("작성한 일기를 익명으로 공유합니다.")
    submitted = st.form_submit_button("🌸 저장하기 🌸")

    if submitted:
        if student_name.strip() == "":
            st.warning("닉네임을 입력해주세요.")
        else:
            st.success("감사일기가 저장되었습니다!")
            for idx, (target, content) in enumerate(entries, start=1):
                if target.strip() or content.strip():
                    c.execute('''
                        INSERT INTO journal (date, student, entry_number, target, content, shared)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (today, student_name, idx, target, content, 1 if share_option else 0))
            conn.commit()

st.markdown("---")

# 사용자별 일기 보기
st.subheader("🔍 내 일기 히스토리")
search_name = st.text_input("닉네임으로 검색:")
if st.button("📅 내 일기 보기"):
    c.execute("SELECT date, target, content FROM journal WHERE student = ? ORDER BY date DESC", (search_name,))
    results = c.fetchall()
    if results:
        for date, target, content in results:
            with st.container():
                st.markdown(f"**[{date}]** 대상: {target}  ")
                st.markdown(f"내용: {content}")
                st.markdown("---")
    else:
        st.info("해당 닉네임의 감사일기가 없습니다.")

# 공유된 일기 보기
st.subheader("🌼 다른 학생들의 감사일기")
if st.checkbox("공유된 감사일기 보기"):
    c.execute("SELECT date, target, content FROM journal WHERE shared = 1 ORDER BY date DESC")
    shared_entries = c.fetchall()
    for date, target, content in shared_entries:
        st.markdown(f"📅 **{date}**")
        st.markdown(f"- 감사 대상: {target}")
        st.markdown(f"- 내용: {content}")
        st.markdown("---")

conn.close()

import streamlit as st
import sqlite3
from datetime import datetime

# 데이터베이스 초기화
conn = sqlite3.connect('gratitude_journal.db')
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

# 오늘 날짜
today = datetime.now().strftime("%Y-%m-%d")

# 제목
st.title("📘 오늘의 감사일기")

# 사용자 이름 입력
student_name = st.text_input("이름 또는 닉네임을 입력하세요", "")

# 감사일기 입력 (3개)
entries = []
for i in range(1, 4):
    st.subheader(f"{i}️⃣ 감사 대상 및 내용")
    target = st.text_input(f"{i}. 감사 대상", key=f"target_{i}")
    content = st.text_area(f"{i}. 감사 내용", key=f"content_{i}")
    entries.append((target, content))

# 저장 버튼
if st.button("✅ 저장하기"):
    if student_name.strip() == "":
        st.warning("이름 또는 닉네임을 입력해주세요.")
    else:
        for idx, (target, content) in enumerate(entries, start=1):
            if target.strip() or content.strip():
                c.execute('''
                    INSERT INTO journal (date, student, entry_number, target, content)
                    VALUES (?, ?, ?, ?, ?)
                ''', (today, student_name, idx, target, content))
        conn.commit()
        st.success("감사일기가 저장되었습니다!")

# 공유 일기 목록 보기
st.markdown("---")
st.subheader("📖 공유된 감사일기 모아보기")

if st.checkbox("공유된 일기 보기"):
    c.execute("SELECT date, student, target, content FROM journal WHERE shared = 1 ORDER BY date DESC")
    shared_entries = c.fetchall()
    for date, student, target, content in shared_entries:
        st.markdown(f"**[{date}] {student}**")
        st.markdown(f"- 감사 대상: {target}")
        st.markdown(f"- 내용: {content}")
        st.markdown("---")

conn.close()

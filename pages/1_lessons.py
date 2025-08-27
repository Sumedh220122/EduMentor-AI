import streamlit as st
from main import EduMentor

st.title("📚 Your Lessons")

student_name = st.session_state.get("student_name", "")

if not student_name:
    st.info("Please create your personalized roadmap on the main page first.")

else:
    edumentor = EduMentor()
    student_records = edumentor.get_student_lessons(student_name)
    lessons = student_records["lessons"]
    if not lessons:
        st.warning("No lessons found for this student.")
    else:
        from collections import defaultdict
        import re

        def week_sort_key(week_str):
            match = re.search(r'\d+', week_str)
            return int(match.group()) if match else float('inf')

        week_topic_map = defaultdict(lambda: defaultdict(list))
        for lesson in lessons:
            for sub_topic in lesson["sub_topic_data"]:
                week = sub_topic["week"]
                topic = sub_topic["sub_topic"]
                content = sub_topic["content"]
                week_topic_map[week][topic].append(content)

        for week in sorted(week_topic_map.keys(), key=week_sort_key):
            st.header(week)
            for topic in week_topic_map[week]:
                st.subheader(topic)
                for idx, content in enumerate(week_topic_map[week][topic], 1):
                    with st.expander(f"Lesson {idx}"):
                        st.markdown(content)
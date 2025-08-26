import streamlit as st
from main import EduMentor

st.title("🎓 Student Info Form")

fields = {
    "name": "Full Name",
    "age": "Age",
    "what_are_your_interests": "What are your interests?",
    "what_you_like_to_do": "What do you like to do?",
    "how_good_are_you?": "How would you rate your current skill level?",
    "how_long_are_you_willing_to_commit_to_learning": "How much time can you commit to learning each week?",
}

with st.form("student_info_form"):
    name = st.text_input(fields["name"])
    age = st.number_input(fields["age"], min_value=0, max_value=100, step=1)
    interests = st.text_area(fields["what_are_your_interests"], height=100)
    hobbies = st.text_area(fields["what_you_like_to_do"], height=150)
    skill_level = st.text_area(fields["how_good_are_you?"], height=100)
    commitment = st.text_area(fields["how_long_are_you_willing_to_commit_to_learning"], height=100)

    submit = st.form_submit_button("Submit")

if submit:
    with st.spinner("🛠️ Creating personalized plan for you... hang on a bit..."):
        student_info = {
            "name": name,
            "age": age,
            "interests": interests,
            "hobbies": hobbies,
            "skill_level": skill_level,
            "learning_commitment": commitment,
        }
        edumentor = EduMentor()
        resources = edumentor.create_lessons(student_info)

    st.success("✅ Personalized roadmap created!")
    st.title("📘 Learning Roadmap")
    st.dataframe(resources, use_container_width=True)


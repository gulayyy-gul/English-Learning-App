import streamlit as st
import json
import os


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="English Learning App",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# DATA
# --------------------------------------------------

DATA_FILE = "english_student_data.json"

default_student = {
    "name": "",
    "level": "Beginner",
    "time": "15 minutes",
    "completed": 0,
    "quiz_scores": [],
    "vocabulary": [],
    "mistakes": [],
    "streak": 1
}


def load_data():
    student = default_student.copy()

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                saved_data = json.load(f)
                student.update(saved_data)
        except:
            pass

    return student


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.student, f, indent=2)


if "student" not in st.session_state:
    st.session_state.student = load_data()


student = st.session_state.student


# --------------------------------------------------
# LESSONS
# --------------------------------------------------

lessons = [
    {
        "title": "Greetings",
        "topic": "Vocabulary",
        "content": """
# 👋 Lesson 1: Greetings

Learn these common English greetings:

- **Hello** = a greeting
- **Hi** = an informal greeting
- **Good morning** = greeting used in the morning
- **Good evening** = greeting used in the evening
- **Goodbye** = used when leaving

### Examples

**Hello! How are you?**

**Hi! My name is Ali.**

**Good morning, teacher.**
"""
    },

    {
        "title": "Pronouns",
        "topic": "Grammar",
        "content": """
# 📚 Lesson 2: Pronouns

Pronouns are words we use instead of names.

**I • You • He • She • It • We • They**

### Examples

**I am a student.**

**She is my sister.**

**They are friends.**
"""
    },

    {
        "title": "Simple Sentences",
        "topic": "Sentence Building",
        "content": """
# ✏️ Lesson 3: Simple Sentences

A simple English sentence usually has:

**Subject + Verb + Object**

### Examples

I eat food.

She reads a book.

They play football.

### Remember

Start a sentence with a capital letter and finish it with punctuation.
"""
    },

    {
        "title": "Present Simple",
        "topic": "Grammar",
        "content": """
# 📖 Lesson 4: Present Simple

We use the present simple for habits and things that happen regularly.

### Examples

I go to school.

You play football.

She goes to school.

He likes tea.

### Remember

With **he / she / it**, the verb often gets **s** or **es**.
"""
    }
]


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def create_profile(name, level, time):
    if not name.strip():
        return False

    student["name"] = name.strip()
    student["level"] = level
    student["time"] = time

    save_data()

    return True


def get_current_lesson():
    index = min(
        student["completed"],
        len(lessons) - 1
    )

    return lessons[index]


def complete_lesson():
    if student["completed"] < len(lessons):
        student["completed"] += 1
        save_data()


def check_quiz(answer):
    correct = answer == "goes"

    if correct:
        student["quiz_scores"].append(1)
        save_data()

        return True

    else:
        student["quiz_scores"].append(0)

        if "Present simple: he/she/it" not in student["mistakes"]:
            student["mistakes"].append(
                "Present simple: he/she/it"
            )

        save_data()

        return False


def check_reading(answer):
    return answer.lower().strip() == "ali"


def check_writing(text):
    if not text.strip():
        return "Please write a sentence first."

    text_lower = text.lower().strip()

    if "she go" in text_lower and "she goes" not in text_lower:

        if "She + goes" not in student["mistakes"]:
            student["mistakes"].append("She + goes")

        save_data()

        return """
### Almost correct! 👍

You wrote:

**She go...**

Use **goes** with "she".

✅ Correct:

**She goes to school.**
"""

    return """
### Good effort! 🌟

Your sentence has been received.

Keep practicing English every day!
"""


def ask_ai(question):

    if not question.strip():
        return "Please ask me an English question."

    q = question.lower()

    if "hello" in q or "hi" in q:
        return """
👋 Hello!

You can ask me things like:

- What does "happy" mean?
- Explain present tense.
- Correct my sentence.
- Give me 5 English sentences.
"""

    if "present" in q:
        return """
### Present Simple

We use the present simple for habits and regular actions.

Examples:

**I play football.**

**She plays football.**

Remember: with **he, she, it**, we usually add **s** or **es**.
"""

    if "correct" in q or "sentence" in q:
        return """
Sure! 😊

Write your English sentence and I will help you correct it.

Example:

❌ She go to school.

✅ She goes to school.
"""

    if "word" in q or "meaning" in q:
        return """
Tell me the English word you want to understand.

I can give you:

- Simple meaning
- Example sentence
- Easy explanation
"""

    return f"""
🤖 **English Teacher**

You asked:

> {question}

For this beginner version, I can help with basic vocabulary, grammar, sentences, reading and writing.

Try asking:

**"Explain present simple."**
"""


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("📚 English Learning")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "👤 Profile",
        "📚 Learn",
        "🎯 Practice",
        "📖 Reading",
        "✍️ Writing",
        "🤖 Ask AI",
        "📊 Progress"
    ]
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🌟 English Learning App")

st.caption(
    "Learn English step by step — simple, short and friendly."
)

st.divider()


# ==================================================
# HOME
# ==================================================

if page == "🏠 Home":

    name = student["name"] or "Student"

    total = len(lessons)
    completed = min(student["completed"], total)

    progress = int(
        (completed / total) * 100
    )

    if completed < total:
        recommended = lessons[completed]["title"]
    else:
        recommended = "Revision"

    st.header(f"Welcome, {name}! 👋")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Progress",
            f"{progress}%"
        )

    with col2:
        st.metric(
            "Lessons",
            f"{completed}/{total}"
        )

    with col3:
        st.metric(
            "🔥 Streak",
            f"{student['streak']} days"
        )

    st.divider()

    st.subheader("📅 Today's Learning")

    st.info(
        f"Your recommended lesson is **{recommended}**."
    )

    st.write(
        f"Daily study time: **{student['time']}**"
    )

    if st.button(
        "▶️ Start Today's Lesson",
        type="primary"
    ):
        st.session_state.page = "📚 Learn"
        st.rerun()

    st.subheader("🎯 Recommended Practice")

    st.write(
        "Practice vocabulary and review your recent mistakes."
    )


# ==================================================
# PROFILE
# ==================================================

elif page == "👤 Profile":

    st.header("👤 Student Profile")

    name = st.text_input(
        "Your Name",
        value=student["name"],
        placeholder="Enter your name"
    )

    level = st.selectbox(
        "English Level",
        ["Beginner", "Elementary"],
        index=(
            0
            if student["level"] == "Beginner"
            else 1
        )
    )

    time = st.radio(
        "Daily Learning Time",
        [
            "15 minutes",
            "30 minutes",
            "45 minutes",
            "60 minutes"
        ],
        index=[
            "15 minutes",
            "30 minutes",
            "45 minutes",
            "60 minutes"
        ].index(student["time"])
    )

    if st.button(
        "💾 Save Profile",
        type="primary"
    ):

        if create_profile(name, level, time):

            st.success(
                f"Welcome, {student['name']}! 👋"
            )

            st.write(
                f"**Level:** {student['level']}"
            )

            st.write(
                f"**Daily study time:** {student['time']}"
            )

        else:
            st.warning(
                "Please enter your name."
            )


# ==================================================
# LEARN
# ==================================================

elif page == "📚 Learn":

    st.header("📚 Learn English")

    lesson = get_current_lesson()

    st.subheader(
        f"Lesson {student['completed'] + 1}: "
        f"{lesson['title']}"
    )

    st.caption(
        f"Topic: {lesson['topic']}"
    )

    st.markdown(
        lesson["content"]
    )

    st.divider()

    st.subheader("🎯 Your Task")

    st.write(
        "Read the lesson carefully, then go to Practice and test yourself."
    )

    if st.button(
        "✅ Complete Lesson",
        type="primary"
    ):

        complete_lesson()

        st.success(
            "Lesson completed! 🎉"
        )

        if student["completed"] < len(lessons):
            st.info(
                f"Next lesson: "
                f"**{lessons[student['completed']]['title']}**"
            )
        else:
            st.success(
                "You completed all available lessons! 🌟"
            )


# ==================================================
# PRACTICE
# ==================================================

elif page == "🎯 Practice":

    st.header("🎯 Quick Practice")

    st.write(
        "Complete the sentence:"
    )

    st.markdown(
        "### She ___ to school every day."
    )

    answer = st.radio(
        "Choose the correct answer",
        ["go", "goes", "going", "gone"],
        key="quiz_answer"
    )

    if st.button(
        "Check Answer",
        type="primary"
    ):

        if check_quiz(answer):

            st.success(
                "✅ Correct! Great job!"
            )

        else:

            st.error(
                "❌ Not quite."
            )

            st.markdown(
                """
The correct answer is **goes**.

We say:

**She goes to school.**

With **she**, we use **goes**.
"""
            )


# ==================================================
# READING
# ==================================================

elif page == "📖 Reading":

    st.header("📖 Reading Practice")

    st.markdown(
        """
### Read the passage:

**Ali is a student. He lives in Lahore.  
He goes to school every morning.  
He likes English.**
"""
    )

    st.subheader(
        "Question"
    )

    st.write(
        "What is the student's name?"
    )

    answer = st.text_input(
        "Your Answer"
    )

    if st.button(
        "Check Answer",
        type="primary"
    ):

        if check_reading(answer):

            st.success(
                "✅ Correct! Ali is the student in the passage."
            )

        else:

            st.error(
                "❌ Try again. Read the passage once more."
            )


# ==================================================
# WRITING
# ==================================================

elif page == "✍️ Writing":

    st.header("✍️ Writing Practice")

    st.write(
        "Write one simple English sentence."
    )

    st.markdown(
        "**Example:** I like apples."
    )

    text = st.text_area(
        "Write your sentence",
        height=120
    )

    if st.button(
        "Check My Writing",
        type="primary"
    ):

        result = check_writing(text)

        st.markdown(result)


# ==================================================
# AI ASSISTANT
# ==================================================

elif page == "🤖 Ask AI":

    st.header("🤖 AI English Assistant")

    st.write(
        "Ask your English teacher anything."
    )

    st.markdown(
        """
### Examples

- What does "beautiful" mean?
- Explain present tense.
- Correct my sentence.
- Give me 5 English sentences.
"""
    )

    question = st.text_area(
        "Ask your question",
        height=120
    )

    if st.button(
        "🤖 Ask AI",
        type="primary"
    ):

        response = ask_ai(question)

        st.markdown(response)


# ==================================================
# PROGRESS
# ==================================================

elif page == "📊 Progress":

    st.header("📊 Your Progress")

    total = len(lessons)

    completed = min(
        student["completed"],
        total
    )

    percent = int(
        (completed / total) * 100
    )

    scores = student["quiz_scores"]

    if scores:
        quiz_percent = int(
            (sum(scores) / len(scores)) * 100
        )
    else:
        quiz_percent = 0

    mistakes = (
        ", ".join(student["mistakes"])
        if student["mistakes"]
        else "None yet"
    )

    st.subheader("Overall Progress")

    st.progress(
        percent / 100
    )

    st.write(
        f"**{percent}% complete**"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Lessons",
            f"{completed}/{total}"
        )

    with col2:
        st.metric(
            "Quiz Score",
            f"{quiz_percent}%"
        )

    with col3:
        st.metric(
            "Vocabulary",
            f"{len(student['vocabulary'])} words"
        )

    st.subheader("🔥 Learning Streak")

    st.write(
        f"{student['streak']} days"
    )

    st.subheader("⚠️ Common Mistakes")

    st.write(
        mistakes
    )

    st.success(
        "Keep practicing! 🌟"
    )

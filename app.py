import streamlit as st
from database import add_task, mark_task_done, delete_task, get_progress
from logic import get_processed_tasks, get_completed_tasks, get_todays_summary

# ─────────────────────────────────
# APP TITLE
# ─────────────────────────────────

st.title("📚 Smart Study Planner")
st.write("Plan smart. Study smart. Win! 🏆")

# ─────────────────────────────────
# SIDEBAR MENU
# ─────────────────────────────────

menu = st.sidebar.selectbox(
    "📌 Menu",
    ["➕ Add Task", "📅 My Timetable", "✅ Progress"]
)


# ─────────────────────────────────
# PAGE 1 — ADD TASK
# ─────────────────────────────────

if menu == "➕ Add Task":
    st.header("➕ Add New Task")

    task_name  = st.text_input("📝 Task Name")
    deadline   = st.date_input("📅 Deadline")
    difficulty = st.slider(
                    "⚡ Difficulty (1 = Easy, 10 = Hard)",
                    min_value = 1,
                    max_value = 10,
                    value     = 5
                )

    if st.button("Add Task ➕"):
        if task_name == "":
            st.warning("⚠️ Please enter a task name!")
        else:
            add_task(task_name, str(deadline), difficulty)
            st.success(f"✅ '{task_name}' added successfully!")


# ─────────────────────────────────
# PAGE 2 — MY TIMETABLE
# ─────────────────────────────────

elif menu == "📅 My Timetable":
    st.header("📅 Your Study Timetable")

    tasks = get_processed_tasks()

    if len(tasks) == 0:
        st.info("📭 No pending tasks! Add some tasks first.")

    else:
        summary = get_todays_summary()
        st.write(f"📊 Total tasks: **{summary['total_tasks']}**")
        st.write(f"⏰ Total study hours today: **{summary['total_hours']} hours**")
        st.write("---")

        for task in tasks:
            st.subheader(f"{task['urgency']}  {task['task_name']}")
            st.write(f"📅 Deadline   : {task['deadline']}")
            st.write(f"📆 Days Left  : {task['days_left']} days")
            st.write(f"⚡ Difficulty : {task['difficulty']} / 10")
            st.write(f"⏰ Study Today: {task['study_hours']} hours")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"✅ Done", key=f"done_{task['id']}"):
                    mark_task_done(task['id'])
                    st.success("Marked as done!")
                    st.rerun()

            with col2:
                if st.button(f"🗑️ Delete", key=f"delete_{task['id']}"):
                    delete_task(task['id'])
                    st.success("Task deleted!")
                    st.rerun()

            st.write("---")


# ─────────────────────────────────
# PAGE 3 — PROGRESS
# ─────────────────────────────────

elif menu == "✅ Progress":
    st.header("✅ Your Progress")

    progress = get_progress()

    st.metric("Overall Progress", f"{progress}%")
    st.progress(progress / 100)

    if progress == 100:
        st.balloons()
        st.success("🎉 Amazing! All tasks completed!")
    elif progress >= 50:
        st.info("💪 Great going! More than halfway done!")
    else:
        st.warning("📚 Keep studying! You got this!")

    completed = get_completed_tasks()

    if len(completed) > 0:
        st.write("### ✅ Completed Tasks")
        for task in completed:
            st.write(f"✅ {task['task_name']} — {task['deadline']}")
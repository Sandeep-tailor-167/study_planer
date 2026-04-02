from groq import Groq
from datetime import date


# ─────────────────────────────────
# CONNECT TO AI
# ─────────────────────────────────

import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# ─────────────────────────────────
# GENERATE AI TIMETABLE
# ─────────────────────────────────

def generate_ai_timetable(tasks):
    today = date.today()

    # Build task list for AI to read
    task_list = ""
    for task in tasks:
        task_list += f"""
- Task      : {task['task_name']}
  Deadline  : {task['deadline']}
  Difficulty: {task['difficulty']} out of 10
  Days Left : {task['days_left']} days
  Urgency   : {task['urgency']}
"""

    # If no tasks pending
    if task_list == "":
        return "✅ No pending tasks! You are all caught up!"

    # Send to AI
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
Today is {today}.

Here are my pending study tasks:
{task_list}

You are a smart study planner assistant.
Think about TWO things for each task:
1. Deadline   → how many days are left
2. Difficulty → how hard the task is (1 easy, 10 very hard)

A task with HIGH difficulty and CLOSE deadline 
needs the most attention!

Please give me:
1. A smart study timetable for TODAY
   showing exact hours for each task
2. One powerful study tip for the hardest task
3. One short motivational line at the end

Keep it simple, clear and friendly!
"""
            }
        ]
    )

    return response.choices[0].message.content


# ─────────────────────────────────
# GENERATE STUDY TIPS FOR ONE TASK
# ─────────────────────────────────

def get_study_tips(task_name, difficulty, days_left):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
I have a task called "{task_name}".
Difficulty level : {difficulty} out of 10
Days left        : {days_left} days

Give me:
1. 3 specific study tips for this task
2. Best time of day to study this
3. One thing to do RIGHT NOW to start

Keep it short, practical and motivating!
"""
            }
        ]
    )

    return response.choices[0].message.content


# ─────────────────────────────────
# MOTIVATIONAL MESSAGE
# ─────────────────────────────────

def get_motivation(progress_percent):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
A student has completed {progress_percent}% of their study tasks.

Write ONE short motivational message for them.
Maximum 3 sentences.
Be friendly, energetic and encouraging!
"""
            }
        ]
    )

    return response.choices[0].message.content

from database import get_all_tasks
from datetime import date


# ─────────────────────────────────
# CALCULATE DAYS LEFT
# ─────────────────────────────────

def get_days_left(deadline):
    today     = date.today()
    deadline  = date.fromisoformat(deadline)
    days_left = (deadline - today).days
    return days_left


# ─────────────────────────────────
# CALCULATE PRIORITY SCORE
# ─────────────────────────────────

def get_priority_score(days_left, difficulty_rating):

    # Deadline already passed!
    if days_left < 0:
        return 999

    # Deadline is today!
    if days_left == 0:
        return 998

    # Normal formula: difficulty ÷ days left
    score = difficulty_rating / days_left
    return round(score, 2)


# ─────────────────────────────────
# LABEL TASK BY URGENCY
# ─────────────────────────────────

def get_urgency_label(score):
    if score >= 999:
        return "💀 OVERDUE"
    elif score >= 2:
        return "🔴 Critical"
    elif score >= 1:
        return "🟡 Important"
    else:
        return "🟢 Comfortable"


# ─────────────────────────────────
# CALCULATE STUDY HOURS PER DAY
# ─────────────────────────────────

def get_study_hours(days_left, difficulty_rating):

    # Deadline passed
    if days_left < 0:
        return 8

    # Due today
    if days_left == 0:
        return 6

    # Formula: harder task = more hours
    # difficulty 1-3  = 1 hour
    # difficulty 4-6  = 2 hours
    # difficulty 7-10 = 3 hours
    if difficulty_rating <= 3:
        hours = 1
    elif difficulty_rating <= 6:
        hours = 2
    else:
        hours = 3

    # If deadline is very close → add extra hour
    if days_left <= 3:
        hours += 1

    return hours


# ─────────────────────────────────
# PROCESS ALL TASKS
# ─────────────────────────────────

def get_processed_tasks():
    raw_tasks = get_all_tasks()
    processed = []

    for task in raw_tasks:
        task_id           = task[0]
        task_name         = task[1]
        deadline          = task[2]
        difficulty_rating = task[3]
        is_done           = task[4]

        # Skip completed tasks
        if is_done == 1:
            continue

        # Calculate everything
        days_left     = get_days_left(deadline)
        score         = get_priority_score(days_left, difficulty_rating)
        urgency_label = get_urgency_label(score)
        study_hours   = get_study_hours(days_left, difficulty_rating)

        processed.append({
            "id"          : task_id,
            "task_name"   : task_name,
            "deadline"    : deadline,
            "difficulty"  : difficulty_rating,
            "days_left"   : days_left,
            "score"       : score,
            "urgency"     : urgency_label,
            "study_hours" : study_hours
        })

    # Sort by score — highest priority first
    processed.sort(key=lambda x: x["score"], reverse=True)

    return processed


# ─────────────────────────────────
# GET COMPLETED TASKS
# ─────────────────────────────────

def get_completed_tasks():
    raw_tasks = get_all_tasks()
    completed = []

    for task in raw_tasks:
        task_id   = task[0]
        task_name = task[1]
        deadline  = task[2]
        is_done   = task[4]

        if is_done == 1:
            completed.append({
                "id"        : task_id,
                "task_name" : task_name,
                "deadline"  : deadline
            })

    return completed


# ─────────────────────────────────
# GET SUMMARY FOR TODAY
# ─────────────────────────────────

def get_todays_summary():
    tasks       = get_processed_tasks()
    total_hours = sum(task["study_hours"] for task in tasks)

    overdue     = [t for t in tasks if t["urgency"] == "💀 OVERDUE"]
    critical    = [t for t in tasks if t["urgency"] == "🔴 Critical"]
    important   = [t for t in tasks if t["urgency"] == "🟡 Important"]
    comfortable = [t for t in tasks if t["urgency"] == "🟢 Comfortable"]

    summary = {
        "total_tasks"   : len(tasks),
        "total_hours"   : total_hours,
        "overdue"       : overdue,
        "critical"      : critical,
        "important"     : important,
        "comfortable"   : comfortable
    }

    return summary

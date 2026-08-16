import os
import streamlit as st
import little_steps
from datetime import date, timedelta
import pandas as pd
import uuid
import copy

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Little Steps 🌱",
    page_icon="🌱",
    layout="wide"
)


# ============================================================
# LITTLE STEPS VISUAL DESIGN
# ============================================================

st.markdown("""
<style>
/* Overall app */
.stApp {
    background: linear-gradient(180deg, #f7fbf7 0%, #ffffff 45%, #f5faf6 100%);
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Typography */
h1, h2, h3 {
    letter-spacing: -0.02em;
}

/* Hero */
.ls-hero {
    padding: 2.2rem 2.4rem;
    border-radius: 28px;
    background: linear-gradient(135deg, #e8f5e9 0%, #f5fbf6 55%, #ffffff 100%);
    border: 1px solid #d7ead9;
    box-shadow: 0 10px 30px rgba(44, 95, 52, 0.08);
    margin-bottom: 1.5rem;
}

.ls-hero h1 {
    margin: 0 0 .35rem 0;
    font-size: clamp(2rem, 5vw, 3.25rem);
}

.ls-hero p {
    margin: .25rem 0;
    color: #4f6653;
    font-size: 1.05rem;
}

/* Cards */
.ls-card {
    background: rgba(255,255,255,.92);
    border: 1px solid #e0eae1;
    border-radius: 20px;
    padding: 1.25rem;
    box-shadow: 0 8px 24px rgba(34, 68, 40, .06);
    height: 100%;
}

.ls-goal {
    background: linear-gradient(135deg, #f0f9f1, #ffffff);
    border: 2px solid #cfe6d1;
    border-radius: 24px;
    padding: 1.6rem;
    margin: .5rem 0 1rem 0;
    text-align: center;
}

.ls-goal-label {
    text-transform: uppercase;
    letter-spacing: .12em;
    font-size: .76rem;
    font-weight: 800;
    color: #5d7962;
}

.ls-goal-text {
    font-size: 1.45rem;
    font-weight: 750;
    margin-top: .5rem;
    color: #254c2a;
}

/* Quote / encouragement */
.ls-quote {
    border-left: 5px solid #72a878;
    background: #f3f9f3;
    border-radius: 0 16px 16px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    color: #36563b;
    font-size: 1.02rem;
}

/* Badge */
.ls-badge {
    background: linear-gradient(180deg, #fffdf4, #ffffff);
    border: 1px solid #eee3b5;
    border-radius: 18px;
    padding: 1rem;
    text-align: center;
    min-height: 120px;
    box-shadow: 0 5px 18px rgba(100, 85, 20, .05);
}

/* CTA buttons */
div.stButton > button {
    border-radius: 14px;
    min-height: 2.8rem;
    font-weight: 700;
    transition: transform .15s ease, box-shadow .15s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(45, 90, 50, .12);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #f2f8f3;
    border-right: 1px solid #dce9de;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

/* Progress bar */
div[data-testid="stProgressBar"] > div > div {
    border-radius: 999px;
}

/* Mobile */
@media (max-width: 700px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
    }

    .ls-hero {
        padding: 1.5rem;
        border-radius: 20px;
    }

    .ls-goal {
        padding: 1.25rem;
        border-radius: 18px;
    }

    .ls-goal-text {
        font-size: 1.2rem;
    }
}

/* Subtle entrance animation */
@keyframes ls-fade-up {
    from { opacity: 0; transform: translateY(7px); }
    to { opacity: 1; transform: translateY(0); }
}

.ls-card, .ls-goal, .ls-hero, .ls-quote, .ls-badge {
    animation: ls-fade-up .45s ease-out both;
}
</style>
""", unsafe_allow_html=True)



# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f8faf8;
    }

    .hero {
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #e8f5e9,
            #f1f8e9
        );
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 18px;
        color: #4f5d50;
    }

    .goal-card {
        padding: 25px;
        border-radius: 20px;
        background-color: white;
        border: 2px solid #dcebdd;
        margin-bottom: 20px;
    }

    .goal-title {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6b756c;
    }

    .goal-text {
        font-size: 25px;
        font-weight: 600;
        margin-top: 8px;
    }

    .quote {
        padding: 20px;
        border-radius: 15px;
        background-color: #eef7ee;
        font-size: 18px;
        font-style: italic;
        text-align: center;
        margin: 20px 0;
    }

    .badge {
        padding: 15px;
        border-radius: 15px;
        background-color: #fffdf0;
        border: 1px solid #f0e5a5;
        text-align: center;
        margin-bottom: 10px;
    }

    .small-text {
        color: #6b756c;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

data = little_steps.load_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_encouragement(data):

    completed = data["weekly_completed"]
    target = data["weekly_target"]

    if completed == 0:

        return (
            "You don't need to do everything today. "
            "You just need to take the first step. 🌱"
        )

    if completed < target:

        remaining = target - completed

        return (
            f"You're making progress! "
            f"Just {remaining} more "
            f"activity day(s) to reach your target. 💪🏾"
        )

    return (
        "🎉 You reached your weekly target! "
        "Take a moment to celebrate how far you've come."
    )


def get_week_dates():

    today = date.today()

    monday = today - timedelta(
        days=today.weekday()
    )

    return [
        monday + timedelta(days=i)
        for i in range(7)
    ]


def activity_completed_on(data, day):

    day_string = day.isoformat()

    for entry in data["history"]:

        if entry["date"] == day_string:

            return True

    return False


def get_today_activity(data):

    """
    Choose today's activity.

    We rotate through the available activities
    so the user gets some variety.
    """

    activity_index = (
        len(data["history"])
        % len(data["activities"])
    )

    return data["activities"][activity_index]
def get_journey_stage(data):
    """
    Determine the user's current Little Steps journey stage
    based on the number of activities they've completed.
    """

    total = len(data["history"])

    if total == 0:
        return {
            "emoji": "🌱",
            "title": "Starting Out",
            "message": "Every journey starts with one little step."
        }

    elif total < 3:
        return {
            "emoji": "🌿",
            "title": "Taking Root",
            "message": "You're starting to build your routine."
        }

    elif total < 7:
        return {
            "emoji": "🌳",
            "title": "Growing Strong",
            "message": "Your little steps are becoming a habit."
        }

    elif total < 15:
        return {
            "emoji": "🌸",
            "title": "Building Momentum",
            "message": "You're showing real consistency."
        }

    else:
        return {
            "emoji": "🏆",
            "title": "Thriving",
            "message": "Look how far your little steps have taken you!"
        }


def get_next_milestone(data):

    total = len(data["history"])

    milestones = [
        1,
        3,
        7,
        15,
        25,
        50
    ]

    for milestone in milestones:

        if total < milestone:

            return milestone

    return None

# ============================================================
# ADAPTIVE COACHING
# ============================================================

def calculate_adaptive_target(current_target, available_days, completed, feedback):
    """Single source of truth for Little Steps target adaptation.

    Rules:
    - A completed target + manageable feedback increases the target by 1.
    - Too-easy feedback also allows a 1-day increase.
    - Missing the target + difficult feedback reduces the target by 1.
    - Otherwise the target stays the same.
    - The target always stays between 1 and the user's available days.
    """
    current_target = int(current_target)
    available_days = max(1, min(int(available_days), 7))
    completed = int(completed)

    if feedback == "too_difficult":
        new_target = current_target - 1
    elif feedback == "too_easy":
        new_target = current_target + 1
    elif completed >= current_target:
        new_target = current_target + 1
    else:
        new_target = current_target

    return max(1, min(new_target, available_days))


def get_demo_result(data, scenario):
    """Presentation-only simulation using the same adaptive logic as the app."""
    current_target = int(
        data.get("weekly_target", data.get("days_per_week", 1))
    )
    available_days = int(data.get("days_per_week", 1))

    if scenario == "strong":
        completed = current_target
        feedback = "just_right"
        feedback_label = "🙂 Just right"
        headline = "🔥 You're ready to progress!"
        message = (
            f"You completed {completed}/{current_target} activities "
            "and found the routine manageable."
        )
    else:
        completed = max(1, current_target - 2)
        feedback = "too_difficult"
        feedback_label = "😫 Too difficult"
        headline = "🌱 Let's make the goal smaller."
        message = (
            f"You completed {completed}/{current_target} activities "
            "and found the routine challenging."
        )

    new_target = calculate_adaptive_target(
        current_target,
        available_days,
        completed,
        feedback
    )

    return {
        "old_target": current_target,
        "completed": completed,
        "feedback": feedback_label,
        "new_target": new_target,
        "headline": headline,
        "message": message,
    }


def start_of_current_week():
    today = date.today()
    return today - timedelta(days=today.weekday())


def handle_week_transition(data):
    """Apply the same adaptive logic when a real week has finished."""
    if not data.get("week_start"):
        data["week_start"] = start_of_current_week().isoformat()
        return False

    current_week_start = start_of_current_week()
    stored_start = date.fromisoformat(data["week_start"])

    if stored_start >= current_week_start:
        return False

    previous_target = int(data.get("weekly_target", data.get("days_per_week", 1)))
    available_days = int(data.get("days_per_week", 1))

    # Use the saved weekly count and the difficulty feedback recorded
    # during the previous week.
    completed = int(data.get("weekly_completed", 0))

    week_entries = [
        entry for entry in data.get("history", [])
        if stored_start.isoformat() <= entry["date"] < current_week_start.isoformat()
    ]

    difficulties = [
        entry.get("difficulty")
        for entry in week_entries
        if entry.get("difficulty")
    ]

    if "too_difficult" in difficulties:
        feedback = "too_difficult"
    elif "too_easy" in difficulties:
        feedback = "too_easy"
    else:
        feedback = "just_right"

    new_target = calculate_adaptive_target(
        previous_target,
        available_days,
        completed,
        feedback
    )

    data["last_week"] = {
        "target": previous_target,
        "completed": completed,
        "feedback": feedback,
    }

    data["weekly_target"] = new_target
    data["weekly_completed"] = 0
    data["week_start"] = current_week_start.isoformat()

    little_steps.save_data(data)
    return True


# ============================================================
# WEEKLY ADAPTATION
# ============================================================

if data is not None:
    handle_week_transition(data)



# ============================================================
# RESET USER JOURNEY
# ============================================================

def reset_user_data():
    """Delete the saved journey so the next run starts as a new user."""
    save_file = getattr(
        little_steps,
        "SAVE_FILE",
        "little_steps_data.json"
    )

    if os.path.exists(save_file):
        os.remove(save_file)

# ============================================================
# MULTIPLE FITNESS GOALS
# ============================================================

GOAL_TEMPLATES = {
    "Walking / cardio": [
        "Walk for 20 minutes",
        "Take a 10 minute brisk walk",
        "Do a 25 minute light jog or walk"
    ],
    "Strength": [
        "Do 2 sets of 10 bodyweight squats",
        "Do a 10 minute bodyweight workout",
        "Complete 2 sets of 8 wall or incline push-ups"
    ],
    "Mobility / flexibility": [
        "Stretch for 10 minutes",
        "Do a 5 minute mobility routine",
        "Complete a gentle full-body stretch"
    ],
    "General fitness": [
        "Complete a 20 minute workout",
        "Move for 15 minutes",
        "Do a short full-body workout"
    ]
}


def make_goal(name, step, category="General fitness"):
    return {
        "id": str(uuid.uuid4())[:8],
        "name": name.strip(),
        "step": step.strip(),
        "category": category
    }


def migrate_goals(data):
    """Give existing users a goals list without losing saved progress."""
    if data.get("goals"):
        return

    activities = data.get("activities", [])
    if not activities:
        activities = ["Complete a small fitness activity"]

    data["goals"] = [
        make_goal(
            f"Goal {i + 1}",
            activity,
            "General fitness"
        )
        for i, activity in enumerate(activities[:3])
    ]


def get_active_goals(data):
    return [
        goal for goal in data.get("goals", [])
        if goal.get("active", True)
    ]


def goal_completed_today(data, goal_id):
    today = date.today().isoformat()

    for entry in data.get("history", []):
        if entry.get("date") == today:
            if goal_id in entry.get("goals_done", []):
                return True

    return False


# ============================================================
# ONBOARDING
# ============================================================

if data is None:

    st.markdown(
        """
        <div class="ls-hero">

        <h1>🌱 Little Steps</h1>

        <p>
        Build your fitness journey one small,
        achievable step at a time.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader(
        "Let's get started 👋🏾"
    )

    st.write(
        """
        You don't need an intense fitness programme.

        Little Steps helps you turn a bigger fitness goal
        into small actions that fit into your life.
        """
    )

    st.divider()

    name = st.text_input(
        "What's your name?"
    )

    activity_level = st.selectbox(
        "How active are you currently?",
        [
            "Beginner",
            "Getting Active",
            "Active"
        ]
    )

    days = st.number_input(
        "How many days per week can you exercise?",
        min_value=1,
        max_value=7,
        value=3,
        step=1
    )

    st.caption(
        "Choose the number of days that realistically "
        "fit into your life."
    )

    if st.button(
        "Create my journey 🌱",
        type="primary"
    ):

        if not name.strip():

            st.error(
                "Please enter your name."
            )

        else:

            weekly_target = days

            activities = (
                little_steps.build_activities(
                    activity_level
                )
            )

            data = {

                "name": name,

                "activity_level":
                    activity_level,

                "days_per_week":
                    days,

                "activities":
                    activities,

                "goals": [
                    make_goal(
                        "My fitness goal",
                        activities[0] if activities else "Complete a small fitness activity",
                        "General fitness"
                    )
                ],

                "weekly_target":
                    weekly_target,

                "weekly_completed":
                    0,

                "week_start":
                    date.today().isoformat(),

                "points":
                    0,

                "streak":
                    0,

                "longest_streak":
                    0,

                "last_checkin":
                    None,

                "history":
                    [],

                "badges":
                    []
            }

            little_steps.save_data(
                data
            )

            st.success(
                "Your Little Steps journey has begun! 🌱"
            )

            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

else:

    name = data["name"]

    # ========================================================
    # NAVIGATION
    # ========================================================

    with st.sidebar:

        st.title("🌱 Little Steps")
        st.caption("Small steps. Real progress.")
        st.divider()

        page = st.radio(
            "Navigate",
            [
                "🏠 Home",
                "🌱 My Journey",
                "💡 How It Works"
            ]
        )

        st.divider()

        # ----------------------------------------------------
        # DEMO MODE
        # ----------------------------------------------------
        demo_mode = st.toggle(
            "🧪 Demo Mode",
            value=False,
            help="Presentation-only simulation. It does not change your saved progress."
        )

        if demo_mode:
            st.caption("Presentation-only simulation using the same adaptive target logic as the real app. Your saved data is not changed.")

        st.divider()

        # ========================================================
        # MY GOALS
        # ========================================================

        st.subheader("🎯 My Goals")

        active_goals = get_active_goals(data)

        st.caption(
            f"{len(active_goals)} active goal(s)"
        )

        for goal in active_goals:
            st.write(
                f"• **{goal['name']}** — {goal['step']}"
            )

        with st.expander("➕ Add a fitness goal"):

            goal_name = st.text_input(
                "Goal name",
                placeholder="e.g. Build strength",
                key="new_goal_name"
            )

            goal_category = st.selectbox(
                "Goal type",
                list(GOAL_TEMPLATES.keys()),
                key="new_goal_category"
            )

            goal_step = st.selectbox(
                "Choose a little step",
                GOAL_TEMPLATES[goal_category],
                key="new_goal_step"
            )

            custom_step = st.text_input(
                "Or write your own little step",
                placeholder="e.g. Cycle for 15 minutes",
                key="custom_goal_step"
            )

            if st.button(
                "Add goal 🌱",
                type="primary",
                use_container_width=True
            ):

                if not goal_name.strip():
                    st.error("Give your goal a name first.")
                else:

                    final_step = (
                        custom_step.strip()
                        if custom_step.strip()
                        else goal_step
                    )

                    data.setdefault("goals", []).append(
                        make_goal(
                            goal_name,
                            final_step,
                            goal_category
                        )
                    )

                    little_steps.save_data(data)

                    st.success(
                        f"Added **{goal_name}**!"
                    )

                    st.rerun()

        st.divider()

        # ========================================================
        # SETTINGS
        # ========================================================

        with st.expander("⚙️ Settings"):

            st.caption(
                "Resetting your journey permanently removes your "
                "saved goals, points, streaks and history."
            )

            if st.button(
                "🔄 Reset My Journey",
                use_container_width=True
            ):
                st.session_state["confirm_reset"] = True

            if st.session_state.get("confirm_reset", False):

                st.warning(
                    "Are you sure? This will erase your current journey "
                    "and start Little Steps as a new user."
                )

                confirm_col, cancel_col = st.columns(2)

                with confirm_col:
                    if st.button(
                        "Yes, start again",
                        type="primary",
                        use_container_width=True
                    ):
                        reset_user_data()
                        st.session_state.clear()
                        st.rerun()

                with cancel_col:
                    if st.button(
                        "Cancel",
                        use_container_width=True
                    ):
                        st.session_state["confirm_reset"] = False
                        st.rerun()

        st.divider()
        st.subheader("Your Profile")
        st.write(f"**Level:** {data['activity_level']}")
        st.write(f"**Available days:** {data['days_per_week']}")

        st.divider()
        st.subheader("Your Stats")
        st.write(f"🔥 Streak: {data['streak']}")
        st.write(f"🏆 Points: {data['points']}")
        st.write(f"🌱 Activities: {len(data['history'])}")

    # ========================================================
    # HOME
    # ========================================================

    if page == "🏠 Home":

        # ====================================================
        # DEMO MODE PANEL
        # ====================================================

        if demo_mode:
            st.markdown(
                """
                <div class="ls-hero">
                <h1>🧪 Adaptive Coaching Demo</h1>
                <p>Show judges how Little Steps responds to progress and feedback.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.info(
                "This is a presentation simulation. Your real progress, streak and saved data are not changed."
            )

            demo_col1, demo_col2 = st.columns(2)

            with demo_col1:
                if st.button(
                    "🔥 Simulate a strong week",
                    use_container_width=True
                ):
                    st.session_state["demo_scenario"] = "strong"

            with demo_col2:
                if st.button(
                    "🌱 Simulate a difficult week",
                    use_container_width=True
                ):
                    st.session_state["demo_scenario"] = "difficult"

            scenario = st.session_state.get("demo_scenario")

            if scenario:
                demo = get_demo_result(data, scenario)

                st.divider()
                st.subheader("Step 1 → What happened?")

                c1, c2, c3 = st.columns(3)
                c1.metric("Target", f"{demo['old_target']} days")
                c2.metric("Completed", f"{demo['completed']}/{demo['old_target']}")
                c3.metric("Feedback", demo["feedback"])

                st.subheader("Step 2 → Little Steps adapts")

                if demo["new_target"] > demo["old_target"]:
                    st.success(
                        f"{demo['headline']}\n\n"
                        f"{demo['message']}\n\n"
                        f"**Next target: {demo['new_target']} days** 🌱"
                    )
                elif demo["new_target"] < demo["old_target"]:
                    st.warning(
                        f"{demo['headline']}\n\n"
                        f"{demo['message']}\n\n"
                        f"**Next target: {demo['new_target']} days** 💚"
                    )
                else:
                    st.info(
                        f"{demo['headline']}\n\n"
                        f"{demo['message']}\n\n"
                        f"**Next target: {demo['new_target']} days**"
                    )

                st.caption(
                    "The demo uses the same target-adaptation function as real weekly transitions, while keeping your saved data untouched."
                )

                if st.button("↺ Reset demo", use_container_width=True):
                    st.session_state.pop("demo_scenario", None)
                    st.rerun()

            st.divider()

        st.markdown(
            f"""
            <div class="ls-hero">
            <h1>🌱 Little Steps</h1>
            <p>Welcome back, {name} 👋🏾</p>
            <p>Let's focus on one small step today.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        completed = data["weekly_completed"]
        target = data["weekly_target"]
        progress = min(completed / target, 1) if target else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎯 Weekly goal", f"{completed}/{target}")
        with col2:
            st.metric("🔥 Streak", f"{data['streak']} days")
        with col3:
            st.metric("🏆 Points", data["points"])
        with col4:
            st.metric("🌱 Activities", len(data["history"]))

        st.divider()

        left, right = st.columns([1.5, 1])

        with left:

            st.subheader("🌱 Today's Little Step")

            today = date.today().isoformat()
            already_checked_in = data["last_checkin"] == today

            if already_checked_in:
                st.success(
                    """✅ You've already completed today's step!

Come back tomorrow for your next little step."""
                )
            else:

                active_goals = get_active_goals(data)

                st.write(
                    "Choose one or more goals to work on today."
                )

                selected_goal_ids = []

                for goal in active_goals:

                    already_done = goal_completed_today(
                        data,
                        goal["id"]
                    )

                    checked = st.checkbox(
                        f"**{goal['name']}** — {goal['step']}",
                        value=already_done,
                        disabled=already_done,
                        key=f"today_goal_{goal['id']}"
                    )

                    if checked:
                        selected_goal_ids.append(
                            goal["id"]
                        )

                st.caption(
                    "You can work on multiple goals in one day. "
                    "Completing at least one goal counts as one activity day."
                )

                if st.button(
                    "✓ Save today's goals 🌱",
                    type="primary",
                    use_container_width=True
                ):

                    if not selected_goal_ids:

                        st.warning(
                            "Select at least one goal you've completed."
                        )

                    else:

                        today = date.today().isoformat()

                        completed_goals = [
                            goal for goal in active_goals
                            if goal["id"] in selected_goal_ids
                        ]

                        data["history"].append(
                            {
                                "date": today,
                                "goals_done": selected_goal_ids,
                                "activities": [
                                    goal["step"]
                                    for goal in completed_goals
                                ],
                                "activity": completed_goals[0]["step"],
                                "difficulty": "just_right"
                            }
                        )

                        data["last_checkin"] = today
                        data["weekly_completed"] += 1

                        # Reward each completed goal.
                        data["points"] += (
                            10 * len(completed_goals)
                        )

                        if data["streak"] == 0:
                            data["streak"] = 1
                        else:
                            data["streak"] += 1

                        data["longest_streak"] = max(
                            data["longest_streak"],
                            data["streak"]
                        )

                        data["_weekly_target_reached"] = (
                            data["weekly_completed"]
                            >= data["weekly_target"]
                        )

                        little_steps.check_new_badges(
                            data
                        )

                        data.pop(
                            "_weekly_target_reached",
                            None
                        )

                        little_steps.save_data(
                            data
                        )

                        st.success(
                            f"🌱 Amazing! You completed "
                            f"{len(completed_goals)} goal(s) today."
                        )

                        st.balloons()
                        st.rerun()

            st.subheader("🎯 This Week")
            st.progress(progress)

            if completed < target:
                st.write(f"**{completed} of {target} activity days completed.**")
            else:
                st.success(f"🎉 You've completed your {target}-day target!")

            st.markdown(
                f"""
                <div class="ls-quote">"{get_encouragement(data)}"</div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.subheader("🗓️ Your Week")
            week_dates = get_week_dates()

            for day in week_dates:
                completed_day = activity_completed_on(data, day)
                day_name = day.strftime("%a")
                label = f"{day_name} {day.strftime('%d %b')}"

                if completed_day:
                    st.success(f"✓ {label}")
                elif day == date.today():
                    st.info(f"• {label} ← Today")
                else:
                    st.write(f"○ {label}")

            st.subheader("🏆 Badges")
            earned = data.get("badges", [])

            if not earned:
                st.caption("Complete activities to unlock your first badge 🌱")
            else:
                for badge in little_steps.BADGES:
                    if badge["id"] in earned:
                        st.markdown(
                            f"""
                            <div class="ls-badge">
                            <strong>{badge['name']}</strong><br>
                            <span class="small-text">{badge['desc']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

        st.divider()

        # ====================================================
        # ADAPTIVE PLAN
        # ====================================================

        st.subheader("🧠 Your Adaptive Plan")
        last_week = data.get("last_week")

        if last_week:
            old_target = last_week["target"]
            old_completed = last_week["completed"]
            current_target = data["weekly_target"]

            if current_target > old_target:
                st.success(
                    f"🔥 **You're ready to progress!**\n\n"
                    f"Last week you completed **{old_completed}/{old_target}** activities.\n\n"
                    f"Your new target is **{current_target} activities**. 🌱"
                )
            elif current_target < old_target:
                st.info(
                    f"🌱 **We're making the goal smaller.**\n\n"
                    f"Last week the target felt challenging.\n\n"
                    f"Your new target is **{current_target} activities**.\n\n"
                    f"Sustainable progress is still progress. 💚"
                )
            else:
                st.info(
                    f"🙂 **Let's build consistency.**\n\n"
                    f"We'll keep your target at **{current_target} activities**."
                )
        else:
            st.info(
                "🧠 **Your plan adapts with you.**\n\n"
                "At the end of your first week, Little Steps will look at your completed activities, difficulty feedback and available days to help decide your next little step."
            )

    # ========================================================
    # MY JOURNEY
    # ========================================================

    elif page == "🌱 My Journey":

        st.markdown(
            """
            <div class="ls-hero">
            <h1>🌱 My Journey</h1>
            <p>Every little step is part of the journey.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # MY FITNESS GOALS
        # ----------------------------------------------------

        st.subheader("🎯 My Fitness Goals")

        active_goals = get_active_goals(data)

        if active_goals:

            for goal in active_goals:

                col1, col2, col3 = st.columns([4, 1, 1])

                with col1:
                    st.markdown(
                        f"""
                        <div class="ls-card">
                            <strong>{goal['name']}</strong><br>
                            <span class="small-text">
                            {goal['category']} · {goal['step']}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # EDIT BUTTON
                with col2:
                    if st.button(
                        "✏️ Edit",
                        key=f"edit_goal_{goal['id']}"
                    ):
                        st.session_state[
                            f"editing_goal_{goal['id']}"
                        ] = True

                # REMOVE BUTTON
                with col3:
                    if st.button(
                        "🗑️ Remove",
                        key=f"remove_goal_{goal['id']}"
                    ):
                        data["goals"] = [
                            g for g in data["goals"]
                            if g["id"] != goal["id"]
                        ]

                        little_steps.save_data(data)
                        st.rerun()

                # EDIT FORM
                if st.session_state.get(
                    f"editing_goal_{goal['id']}",
                    False
                ):

                    with st.form(
                        f"edit_form_{goal['id']}"
                    ):

                        st.markdown("### ✏️ Edit your goal")

                        edited_name = st.text_input(
                            "Goal name",
                            value=goal["name"],
                            key=f"edit_name_{goal['id']}"
                        )

                        categories = list(
                            GOAL_TEMPLATES.keys()
                        )

                        current_category = goal.get(
                            "category",
                            "General fitness"
                        )

                        if current_category not in categories:
                            current_category = "General fitness"

                        edited_category = st.selectbox(
                            "Goal type",
                            categories,
                            index=categories.index(
                                current_category
                            ),
                            key=f"edit_category_{goal['id']}"
                        )

                        suggested_steps = GOAL_TEMPLATES[
                            edited_category
                        ]

                        edited_step = st.text_input(
                            "Little step",
                            value=goal["step"],
                            key=f"edit_step_{goal['id']}"
                        )

                        save_col, cancel_col = st.columns(2)

                        with save_col:
                            save_edit = st.form_submit_button(
                                "💾 Save changes",
                                type="primary",
                                use_container_width=True
                            )

                        with cancel_col:
                            cancel_edit = st.form_submit_button(
                                "Cancel",
                                use_container_width=True
                            )

                        if save_edit:

                            if not edited_name.strip():
                                st.error(
                                    "Please give your goal a name."
                                )

                            elif not edited_step.strip():
                                st.error(
                                    "Please add a little step."
                                )

                            else:

                                for saved_goal in data["goals"]:

                                    if saved_goal["id"] == goal["id"]:

                                        saved_goal["name"] = (
                                            edited_name.strip()
                                        )

                                        saved_goal["category"] = (
                                            edited_category
                                        )

                                        saved_goal["step"] = (
                                            edited_step.strip()
                                        )

                                little_steps.save_data(data)

                                st.session_state[
                                    f"editing_goal_{goal['id']}"
                                ] = False

                                st.success(
                                    "Your goal has been updated! 🌱"
                                )

                                st.rerun()

                        if cancel_edit:

                            st.session_state[
                                f"editing_goal_{goal['id']}"
                            ] = False

                            st.rerun()

        else:

            st.info(
                "No active goals yet. Add your first one from the sidebar."
            )
        stage = get_journey_stage(data)
        next_milestone = get_next_milestone(data)
        total = len(data["history"])

        st.markdown(
            f"""
            <div class="ls-goal">
            <div style="text-align:center;">
            <div style="font-size:70px;">{stage['emoji']}</div>
            <h2>{stage['title']}</h2>
            <p>{stage['message']}</p>
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("🎯 Your Next Milestone")

        if next_milestone:
            st.write(
                f"You've completed **{total} activities**. "
                f"Your next milestone is **{next_milestone} activities**."
            )

            previous = 0
            for milestone in [1, 3, 7, 15, 25, 50]:
                if total >= milestone:
                    previous = milestone
                else:
                    break

            milestone_progress = (
                (total - previous) /
                (next_milestone - previous)
            )
            milestone_progress = max(0, min(milestone_progress, 1))
            st.progress(milestone_progress)
            st.caption(f"{next_milestone - total} little step(s) to go 🌱")
        else:
            st.success("🏆 You've reached every current milestone!")

        st.divider()
        st.subheader("📈 Your Activity")

        if data["history"]:
            history_df = pd.DataFrame(data["history"])
            history_df["date"] = pd.to_datetime(history_df["date"])
            daily_activity = (
                history_df.groupby("date")
                .size()
                .reset_index(name="Activities")
                .set_index("date")
            )
            st.line_chart(daily_activity["Activities"])
        else:
            st.info("Complete your first activity and your progress will appear here. 🌱")

        st.subheader("🏆 Your Badges")
        earned = data.get("badges", [])

        if not earned:
            st.info("Your first badge is waiting for you 🌱")
        else:
            badge_columns = st.columns(3)
            badge_number = 0
            for badge in little_steps.BADGES:
                if badge["id"] in earned:
                    with badge_columns[badge_number % 3]:
                        st.markdown(
                            f"""
                            <div class="ls-badge">
                            <div style="font-size:35px;">🏆</div>
                            <strong>{badge['name']}</strong><br>
                            <span class="small-text">{badge['desc']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    badge_number += 1

    # ========================================================
    # HOW IT WORKS
    # ========================================================

    elif page == "💡 How It Works":

        st.markdown(
            """
            <div class="ls-hero">
            <h1>💡 How Little Steps Works</h1>
            <p>Big goals become easier when you break them into little steps.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("The idea 🌱")
        st.write(
            """Fitness can feel overwhelming.

Instead of asking you to completely change your lifestyle, Little Steps starts with something much simpler:

**What's one thing you can realistically do today?**"""
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """### 1️⃣ Start small

Tell us how many days you can realistically exercise.

We create achievable steps based on your starting point."""
            )

        with col2:
            st.markdown(
                """### 2️⃣ Give feedback

After each activity, tell us:

😫 Too difficult

🙂 Just right

🔥 Too easy

Your experience matters."""
            )

        with col3:
            st.markdown(
                """### 3️⃣ Keep growing

Little Steps uses your progress and feedback to help decide what your next target should be.

No perfection required."""
            )

        st.divider()
        st.subheader("🌱 The Little Steps philosophy")
        st.markdown(
            """
            <div class="ls-quote"><strong>Progress, not perfection.</strong></div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            """Missing a day doesn't erase your progress.

Finding something difficult doesn't mean you've failed.

Taking a smaller step is still moving forward.

Little Steps is designed to encourage consistency rather than perfection."""
        )

        st.divider()
        st.subheader("🔒 Designed for wellness")
        st.write(
            """Little Steps focuses on general fitness and wellness rather than medical diagnosis or treatment.

It doesn't require medical records, wearable data, or sensitive health information to work."""
        )

        st.success(
            """🌱 Your goal isn't to become perfect.

Your goal is simply to take the **next little step.**"""
        )

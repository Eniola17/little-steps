import json
import os
from datetime import date, datetime, timedelta


SAVE_FILE = "little_steps_data.json"


# ============================================================
# PERSISTENCE
# ============================================================

def load_data():
    """Load saved user data from the JSON file."""

    if os.path.exists(SAVE_FILE):

        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)

            # Make sure older versions of the program
            # don't break when new features are added.
            data.setdefault("badges", [])
            data.setdefault("weekly_target", 1)
            data.setdefault("weekly_completed", 0)
            data.setdefault("week_start", date.today().isoformat())
            data.setdefault("history", [])
            data.setdefault("points", 0)
            data.setdefault("streak", 0)
            data.setdefault("longest_streak", 0)
            data.setdefault("last_checkin", None)

            return data

        except (json.JSONDecodeError, KeyError):
            print("Your saved data couldn't be read.")
            print("We'll start a fresh profile.")

    return None


def save_data(data):
    """Save user data to JSON."""

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ============================================================
# INPUT VALIDATION
# ============================================================

def get_number(prompt, minimum, maximum):
    """Ask the user for a number within a specific range."""

    while True:

        try:
            value = int(input(prompt))

            if minimum <= value <= maximum:
                return value

            print(
                f"Please enter a number between "
                f"{minimum} and {maximum}."
            )

        except ValueError:

            print("Please enter a valid number.")


# ============================================================
# ONBOARDING
# ============================================================

def onboarding():

    print("================================")
    print("          LITTLE STEPS 🌱")
    print("================================")
    print()

    print(
        "Let's build your fitness journey "
        "one small step at a time."
    )

    print()

    name = input("What's your name? ").strip()

    while not name:
        print("Please enter your name.")
        name = input("> ").strip()

    print()

    print(f"Nice to meet you, {name}! 👋🏾")

    # --------------------------------------------------------
    # ACTIVITY LEVEL
    # --------------------------------------------------------

    print()
    print("How active are you currently?")
    print()

    print("1. I rarely exercise")
    print("2. I exercise occasionally")
    print("3. I exercise regularly")

    activity_choice = get_number(
        "> ",
        1,
        3
    )

    if activity_choice == 1:
        activity_level = "Beginner"

    elif activity_choice == 2:
        activity_level = "Getting Active"

    else:
        activity_level = "Active"

    print()
    print(
        f"Your starting level: {activity_level}"
    )

    # --------------------------------------------------------
    # AVAILABLE DAYS
    # --------------------------------------------------------

    print()

    days = get_number(
        "How many days per week can you exercise?\n> ",
        1,
        7
    )

    # --------------------------------------------------------
    # WEEKLY TARGET
    # --------------------------------------------------------

    weekly_target = calculate_weekly_target(
        activity_level,
        days
    )

    print()

    print(
        f"You have {days} day(s) available per week."
    )

    print(
        f"We'll start with {weekly_target} "
        f"activity day(s) this week."
    )

    # --------------------------------------------------------
    # ACTIVITIES
    # --------------------------------------------------------

    activities = build_activities(
        activity_level
    )

    print()
    print("Here are some activities you can choose from:")

    for i, activity in enumerate(
        activities,
        start=1
    ):
        print(f"  {i}. {activity}")

    # --------------------------------------------------------
    # CREATE USER DATA
    # --------------------------------------------------------

    today = date.today()

    data = {

        "name": name,

        "activity_level": activity_level,

        "days_per_week": days,

        "activities": activities,

        "weekly_target": weekly_target,

        "weekly_completed": 0,

        "week_start": today.isoformat(),

        "points": 0,

        "streak": 0,

        "longest_streak": 0,

        "last_checkin": None,

        "history": [],

        "badges": []
    }

    save_data(data)

    print()

    print("================================")
    print("       YOUR FIRST TARGET 🌱")
    print("================================")

    print()

    print(
        f"Complete {weekly_target} "
        f"activity day(s) this week."
    )

    print()

    print(
        "Remember: progress matters more "
        "than perfection."
    )

    return data


# ============================================================
# WEEKLY TARGET CALCULATION
# ============================================================

def calculate_weekly_target(
    activity_level,
    days
):
    """
    Determine a realistic starting target.

    Available days are not automatically the target.
    """

    if activity_level == "Beginner":

        if days <= 2:
            return 1

        elif days <= 4:
            return 2

        else:
            return 3

    elif activity_level == "Getting Active":

        if days <= 2:
            return 2

        elif days <= 4:
            return 3

        else:
            return 4

    else:

        if days <= 2:
            return 2

        elif days <= 4:
            return 3

        else:
            return 5


# ============================================================
# ACTIVITIES
# ============================================================

def build_activities(activity_level):

    if activity_level == "Beginner":

        return [
            "Go for a 10-minute walk",
            "Stretch for 5 minutes",
            "Do 10 bodyweight squats",
            "Take a short walk outside",
            "Do a 10-minute beginner workout"
        ]

    elif activity_level == "Getting Active":

        return [
            "Go for a 20-minute walk",
            "Do a 15-minute home workout",
            "Stretch for 10 minutes",
            "Go for a light jog",
            "Do a bodyweight strength session"
        ]

    else:

        return [
            "Complete a 30-minute workout",
            "Go for a 30-minute run or brisk walk",
            "Complete a strength session",
            "Do a mobility/stretch session",
            "Complete a cardio workout"
        ]


# ============================================================
# BADGES
# ============================================================

BADGES = [

    {
        "id": "first_step",
        "name": "🌱 First Step",
        "desc": "Complete your first activity",
        "check": lambda d:
            len(d["history"]) >= 1
    },

    {
        "id": "streak_3",
        "name": "🔥 3-Day Streak",
        "desc": "Check in 3 days in a row",
        "check": lambda d:
            d["streak"] >= 3
    },

    {
        "id": "streak_7",
        "name": "⭐ One Week Strong",
        "desc": "Check in 7 days in a row",
        "check": lambda d:
            d["streak"] >= 7
    },

    {
        "id": "streak_30",
        "name": "🏅 30-Day Streak",
        "desc": "Check in 30 days in a row",
        "check": lambda d:
            d["streak"] >= 30
    },

    {
        "id": "points_100",
        "name": "💯 Century Club",
        "desc": "Earn 100 points",
        "check": lambda d:
            d["points"] >= 100
    },

    {
        "id": "points_500",
        "name": "🏆 500 Points",
        "desc": "Earn 500 points",
        "check": lambda d:
            d["points"] >= 500
    },

    {
        "id": "comeback",
        "name": "🌤️ Comeback",
        "desc": "Check in again after a break",
        "check": lambda d:
            d.get("_just_came_back", False)
    },

    {
        "id": "weekly_win",
        "name": "🎯 Target Achieved",
        "desc": "Reach your weekly target",
        "check": lambda d:
            d.get("_weekly_target_reached", False)
    }
]


def check_new_badges(data):

    if "badges" not in data:
        data["badges"] = []

    newly_earned = []

    for badge in BADGES:

        if (
            badge["id"] not in data["badges"]
            and badge["check"](data)
        ):

            data["badges"].append(
                badge["id"]
            )

            newly_earned.append(badge)

    if newly_earned:

        print()
        print("🎉 NEW BADGE UNLOCKED!")

        for badge in newly_earned:

            print(
                f"  {badge['name']}"
            )

            print(
                f"  {badge['desc']}"
            )


# ============================================================
# POINTS
# ============================================================

def points_for_activity():

    return 10


# ============================================================
# DATE HELPERS
# ============================================================

def days_since(last_checkin_str):

    if last_checkin_str is None:
        return None

    last = datetime.strptime(
        last_checkin_str,
        "%Y-%m-%d"
    ).date()

    return (
        date.today() - last
    ).days


def get_week_start(data):

    return datetime.strptime(
        data["week_start"],
        "%Y-%m-%d"
    ).date()


def days_into_current_week(data):

    return (
        date.today()
        - get_week_start(data)
    ).days


# ============================================================
# INACTIVITY
# ============================================================

def inactivity_check(data):

    gap = days_since(
        data["last_checkin"]
    )

    if gap is None:
        return

    if gap == 1:

        return

    elif gap == 2:

        print()

        print(
            f"Hey {data['name']}, "
            "we missed you yesterday!"
        )

        print(
            "No worries — let's get back to it today 💪🏾"
        )

    elif gap >= 3:

        print()

        print(
            f"It's been {gap} days since your "
            "last check-in."
        )

        print(
            "Life happens — that's okay."
        )

        print(
            "Your streak reset, but your "
            "progress still counts."
        )

        print(
            "Ready to take one small step today? 🌱"
        )

        if data["streak"] > 0:

            data["longest_streak"] = max(
                data["longest_streak"],
                data["streak"]
            )

        data["streak"] = 0

        data["_just_came_back"] = True


# ============================================================
# DAILY CHECK-IN
# ============================================================

def daily_checkin(data):

    today_str = date.today().isoformat()

    # Prevent multiple check-ins in one day
    if data["last_checkin"] == today_str:

        print()

        print(
            "You've already checked in today. "
            "Nice work! ✅"
        )

        print(
            "Come back tomorrow for your next step."
        )

        return

    print()

    print(
        f"Today's activity, "
        f"{data['name']}:"
    )

    print()

    for i, activity in enumerate(
        data["activities"],
        start=1
    ):

        print(
            f"{i}. {activity}"
        )

    print()

    choice = get_number(
        "Which activity did you complete today?\n> ",
        1,
        len(data["activities"])
    )

    activity = data["activities"][
        choice - 1
    ]

    # --------------------------------------------------------
    # DIFFICULTY
    # --------------------------------------------------------

    print()

    print(
        "How did that activity feel?"
    )

    print()

    print("1. 😫 Too difficult")
    print("2. 🙂 Just right")
    print("3. 🔥 Too easy")

    difficulty_choice = get_number(
        "> ",
        1,
        3
    )

    if difficulty_choice == 1:

        difficulty = "too_difficult"

    elif difficulty_choice == 2:

        difficulty = "just_right"

    else:

        difficulty = "too_easy"

    # --------------------------------------------------------
    # POINTS
    # --------------------------------------------------------

    earned = points_for_activity()

    data["points"] += earned

    # --------------------------------------------------------
    # WEEKLY PROGRESS
    # --------------------------------------------------------

    data["weekly_completed"] += 1

    # --------------------------------------------------------
    # STREAK
    # --------------------------------------------------------

    if data["streak"] == 0:

        data["streak"] = 1

    else:

        data["streak"] += 1

    data["longest_streak"] = max(
        data["longest_streak"],
        data["streak"]
    )

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    data["last_checkin"] = today_str

    data["history"].append(
        {
            "date": today_str,
            "activity": activity,
            "difficulty": difficulty
        }
    )

    # --------------------------------------------------------
    # FEEDBACK
    # --------------------------------------------------------

    print()

    print(
        f"🌱 You completed: {activity}"
    )

    print(
        f"+{earned} points!"
    )

    print(
        f"Total points: "
        f"{data['points']} 🏆"
    )

    print(
        f"Current streak: "
        f"{data['streak']} day(s) 🔥"
    )

    if difficulty == "too_difficult":

        print()

        print(
            "That's okay — you listened to yourself."
        )

        print(
            "We'll keep the next steps manageable. 💚"
        )

    elif difficulty == "just_right":

        print()

        print(
            "Nice! You're building consistency."
        )

        print(
            "Progress, not perfection. 🌱"
        )

    else:

        print()

        print(
            "🔥 You found that manageable!"
        )

        print(
            "You might be ready for a slightly "
            "bigger challenge."
        )

    # --------------------------------------------------------
    # WEEKLY TARGET
    # --------------------------------------------------------

    print()

    print(
        f"Weekly progress: "
        f"{data['weekly_completed']}/"
        f"{data['weekly_target']}"
    )

    if (
        data["weekly_completed"]
        >= data["weekly_target"]
    ):

        data["_weekly_target_reached"] = True

        print()

        print(
            "🎉 WEEKLY TARGET ACHIEVED!"
        )

        print(
            "You've taken another step forward."
        )

        check_new_badges(data)

        data.pop(
            "_weekly_target_reached",
            None
        )

    else:

        check_new_badges(data)

    data.pop(
        "_just_came_back",
        None
    )


# ============================================================
# WEEKLY REVIEW
# ============================================================

def weekly_review(data):

    target = data["weekly_target"]

    completed = data["weekly_completed"]

    print()

    print("================================")
    print("        WEEKLY REVIEW 🌱")
    print("================================")

    print()

    print(
        f"You completed "
        f"{completed}/{target} "
        f"activity days."
    )

    # --------------------------------------------------------
    # COMPLETION RATE
    # --------------------------------------------------------

    if target > 0:

        completion_rate = (
            completed / target
        )

    else:

        completion_rate = 0

    print()

    print(
        f"Completion: "
        f"{int(completion_rate * 100)}%"
    )

    # --------------------------------------------------------
    # ASK HOW THE WEEK FELT
    # --------------------------------------------------------

    print()

    print(
        "Overall, how did this week's "
        "target feel?"
    )

    print()

    print("1. 😫 Too difficult")
    print("2. 🙂 Just right")
    print("3. 🔥 Too easy")

    difficulty_choice = get_number(
        "> ",
        1,
        3
    )

    # --------------------------------------------------------
    # ADAPT TARGET
    # --------------------------------------------------------

    old_target = target

    new_target = adapt_weekly_target(
        data,
        completion_rate,
        difficulty_choice
    )

    # --------------------------------------------------------
    # WEEKLY FEEDBACK
    # --------------------------------------------------------

    print()

    if completion_rate >= 1:

        print(
            "🔥 You reached your target!"
        )

        print(
            "That's a fantastic week."
        )

    elif completion_rate >= 0.5:

        print(
            "🌱 You made meaningful progress "
            "this week."
        )

        print(
            "Remember: consistency doesn't "
            "require perfection."
        )

    else:

        print(
            "💚 This week didn't go exactly "
            "as planned."
        )

        print(
            "That's okay. We can make the "
            "next step smaller."
        )

    # --------------------------------------------------------
    # TARGET CHANGE
    # --------------------------------------------------------

    print()

    if new_target > old_target:

        print(
            f"🔥 You're ready to progress!"
        )

        print(
            f"Next week's target: "
            f"{new_target} activities"
        )

    elif new_target < old_target:

        print(
            "🌱 Let's make next week "
            "a little more manageable."
        )

        print(
            f"Next week's target: "
            f"{new_target} activities"
        )

    else:

        print(
            "🙂 We'll keep the same target "
            "for another week."
        )

        print(
            f"Next week's target: "
            f"{new_target} activities"
        )

    # --------------------------------------------------------
    # RESET WEEK
    # --------------------------------------------------------

    data["weekly_target"] = new_target

    data["weekly_completed"] = 0

    data["week_start"] = date.today().isoformat()

    data["last_week"] = {
        "target": old_target,
        "completed": completed,
        "completion_rate": completion_rate,
        "difficulty": difficulty_choice
    }

    save_data(data)

    print()

    print(
        "New week unlocked! 🚀"
    )


# ============================================================
# ADAPTIVE ALGORITHM
# ============================================================

def adapt_weekly_target(
    data,
    completion_rate,
    difficulty
):
    def get_week_feedback(data):
        """
    Look at the difficulty feedback from the
    current week's completed activities.

    Returns the overall difficulty:
    too_difficult, just_right, or too_easy.
    """

    week_start = datetime.strptime(
        data["week_start"],
        "%Y-%m-%d"
    ).date()

    feedback = []

    for entry in data["history"]:

        entry_date = datetime.strptime(
            entry["date"],
            "%Y-%m-%d"
        ).date()

        if entry_date >= week_start:

            feedback.append(
                entry.get(
                    "difficulty",
                    "just_right"
                )
            )

    if not feedback:

        return "just_right"

    difficult = feedback.count(
        "too_difficult"
    )

    easy = feedback.count(
        "too_easy"
    )

    if difficult > easy and difficult >= len(feedback) / 2:

        return "too_difficult"

    elif easy > difficult and easy >= len(feedback) / 2:

        return "too_easy"

    else:

        return "just_right"
    """
    Adapt the next week's target.

    difficulty:
        1 = too difficult
        2 = just right
        3 = too easy
    """

    current_target = data["weekly_target"]

    maximum = data["days_per_week"]

    # --------------------------------------------------------
    # TOO DIFFICULT
    # --------------------------------------------------------

    if difficulty == 1:

        # Reduce the target by one,
        # but never below 1.
        return max(
            1,
            current_target - 1
        )

    # --------------------------------------------------------
    # JUST RIGHT
    # --------------------------------------------------------

    elif difficulty == 2:

        # If they completed the target,
        # increase slightly.
        if completion_rate >= 1:

            return min(
                current_target + 1,
                maximum
            )

        # If they completed at least half,
        # keep the target the same.
        else:

            return current_target

    # --------------------------------------------------------
    # TOO EASY
    # --------------------------------------------------------

    else:

        # If the target was too easy and
        # they completed most/all of it,
        # increase by one.
        if completion_rate >= 0.75:

            return min(
                current_target + 1,
                maximum
            )

        else:

            return current_target


# ============================================================
# CHECK WHETHER WEEK IS FINISHED
# ============================================================

def check_week_status(data):

    days_elapsed = days_into_current_week(data)

    # Week is considered complete after 7 days.
    return days_elapsed >= 7


# ============================================================
# PROGRESS DASHBOARD
# ============================================================

def show_progress(data):

    print()

    print(
        f"--- {data['name']}'s Progress ---"
    )

    print()

    print(
        f"Level: "
        f"{data['activity_level']}"
    )

    print(
        f"Available days: "
        f"{data['days_per_week']}"
    )

    print(
        f"Weekly target: "
        f"{data['weekly_target']} activities"
    )

    print(
        f"Completed this week: "
        f"{data['weekly_completed']}"
    )

    print(
        f"Points: "
        f"{data['points']}"
    )

    print(
        f"Current streak: "
        f"{data['streak']} day(s)"
    )

    print(
        f"Longest streak: "
        f"{data['longest_streak']} day(s)"
    )

    print(
        f"Total activities: "
        f"{len(data['history'])}"
    )

    # --------------------------------------------------------
    # PROGRESS BAR
    # --------------------------------------------------------

    target = data["weekly_target"]

    completed = data["weekly_completed"]

    if target > 0:

        percentage = min(
            completed / target,
            1
        )

        bar_length = 10

        filled = int(
            percentage * bar_length
        )

        bar = (
            "█" * filled
            + "░" * (
                bar_length - filled
            )
        )

        print()

        print(
            f"Weekly progress: "
            f"{bar} "
            f"{int(percentage * 100)}%"
        )

    # --------------------------------------------------------
    # LAST WEEK
    # --------------------------------------------------------

    if "last_week" in data:

        last_week = data["last_week"]

        print()

        print("--- Last Week ---")

        print(
            f"Target: "
            f"{last_week['target']}"
        )

        print(
            f"Completed: "
            f"{last_week['completed']}"
        )

        print(
            f"Completion: "
            f"{int(last_week['completion_rate'] * 100)}%"
        )

    # --------------------------------------------------------
    # BADGES
    # --------------------------------------------------------

    earned = data.get(
        "badges",
        []
    )

    print()

    print(
        f"Badges earned: "
        f"{len(earned)}/{len(BADGES)}"
    )

    if earned:

        for badge in BADGES:

            if badge["id"] in earned:

                print(
                    f"  {badge['name']} — "
                    f"{badge['desc']}"
                )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    data = load_data()

    # --------------------------------------------------------
    # NEW USER
    # --------------------------------------------------------

    if data is None:

        data = onboarding()

    # --------------------------------------------------------
    # RETURNING USER
    # --------------------------------------------------------

    else:

        print()

        print(
            f"Welcome back, "
            f"{data['name']} 🌱"
        )

        # Check inactivity
        inactivity_check(data)

        # Check whether a full week has passed
        if check_week_status(data):

            print()

            print(
                "Your week is complete! 🎉"
            )

            print(
                "Let's review how things went."
            )

            weekly_review(data)

        save_data(data)

    # --------------------------------------------------------
    # MAIN MENU
    # --------------------------------------------------------

    while True:

        print()

        print("================================")

        print(
            "What would you like to do?"
        )

        print()

        print(
            "1. Check in for today"
        )

        print(
            "2. View progress"
        )

        print(
            "3. Review current week"
        )

        print(
            "4. Exit"
        )

        print(
            "================================"
        )

        choice = input("> ").strip()

        # ----------------------------------------------------
        # CHECK IN
        # ----------------------------------------------------

        if choice == "1":

            daily_checkin(data)

            save_data(data)

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        elif choice == "2":

            show_progress(data)

        # ----------------------------------------------------
        # WEEKLY REVIEW
        # ----------------------------------------------------

        elif choice == "3":

            weekly_review(data)

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "4":

            print()

            print(
                f"See you next time, "
                f"{data['name']}! 🌱"
            )

            print(
                "Keep taking little steps."
            )

            break

        else:

            print()

            print(
                "Please choose 1, 2, 3, or 4."
            )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()
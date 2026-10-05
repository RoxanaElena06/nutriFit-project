import csv
import json
import os
import random
from asyncio.windows_events import NULL
from datetime import datetime, timedelta
from faker import Faker

# Faker initialization for synthetic data
fake = Faker()

# Set the number of users and the number of days for which we generate data
NUM_USERS = 100
NUM_DAYS = 50
START_DATE = datetime.now() - timedelta(days=NUM_DAYS)

# The directory where we will save the generated files
OUTPUT_DIR = "nutrifit_raw_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_users():
    """1. Generate users (dim_users)"""
    users = []
    for i in range(NUM_USERS):
        user_id = 101 + i

        name = fake.name()

        # 3% from users to have null at name
        if random.random() < 0.03:
            name = None  # Mistake that I will cath in data cleansing phase

        users.append(
            {
                "user_id": user_id,
                "name": name,
                "age": random.randint(18, 50),
                "weight_kg": round(random.uniform(55.0, 95.0), 1),
                "height_cm": random.randint(155, 195),
                "daily_step_goal": random.choice([5000, 8000, 10000, 12000, 15000, 20000]),
                "daily_calorie_goal": random.choice([1300, 1500, 1800, 2000, 2500]),
            }
        )


    # Save in JSON format
    with open(
        f"{OUTPUT_DIR}/users_profiles.json", "w", encoding="utf-8"
    ) as f:
        json.dump(users, f, indent=4)

    print("Generate file: users_profiles.json")
    return users


def generate_daily_activity(users):
    """2. Generates daily activity files (Fitbit Schema)"""
    activity_rows = []

    for user in users:
        user_id = user["user_id"]
        for day in range(NUM_DAYS):
            activity_date = (START_DATE + timedelta(days=day)).strftime(
                "%Y-%m-%d"
            )

            # Generate activ steps and minutes
            total_steps = random.randint(1000, 20000)
            very_active_min = random.randint(0, 60)
            fairly_active_min = random.randint(0, 45)
            lightly_active_min = random.randint(60, 250)
            sedentary_min = 1440 - (
                very_active_min + fairly_active_min + lightly_active_min
            )

            # Proportional distance calculation
            total_dist = round(total_steps * 0.00075, 2)  #0.00075 is the average stride length in km
            very_active_dist = round(total_dist * 0.3, 2)  #30%
            mod_active_dist = round(total_dist * 0.2, 2)  #20%
            light_active_dist = round(total_dist * 0.5, 2)  #50%

            calories = random.randint(1000, 3200)

            # I intentionally add 1% chance of outlier value to test data cleansing in Silver Layer
            if random.random() < 0.01:
                calories = -100

            row = (
                {
                    "id": user_id,
                    "ActivityDate": activity_date,
                    "TotalSteps": total_steps,
                    "TotalDistance": total_dist,
                    "TrackerDistance": total_dist,
                    "LoggedActivitiesDistance": 0.0,
                    "VeryActiveDistance": very_active_dist,
                    "ModeratelyActiveDistance": mod_active_dist,
                    "LightActiveDistance": light_active_dist,
                    "SedentaryActiveDistance": 0.0,
                    "VeryActiveMinutes": very_active_min,
                    "FairlyActiveMinutes": fairly_active_min,
                    "LightlyActiveMinutes": lightly_active_min,
                    "SedentaryMinutes": sedentary_min,
                    "Calories": calories,
                }
            )

            activity_rows.append(row)

            if random.random() < 0.02:
                activity_rows.append(row)

    # Save in CSV format
    fieldnames = list(activity_rows[0].keys())
    with open(
        f"{OUTPUT_DIR}/daily_activity.csv", "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(activity_rows)

    print("Generate file: daily_activity.csv")


def generate_nutrition_logs(users):
    """3. Generate nutrition/meal file(NutriFit Schema)"""
    # Breakfast & Snacks
    breakfast_snack_meals = [
        ("Oatmeal with Berries", 320, 12.0, 55.0, 5.0),
        ("Greek Yogurt with Honey", 180, 16.0, 20.0, 2.5),
        ("Avocado Toast with Egg", 350, 14.0, 32.0, 18.0),
        ("Protein Shake (Banana & Peanut Butter)", 380, 32.0, 42.0, 10.0),
        ("Chia Pudding with Mango", 220, 6.0, 34.0, 8.0),
        ("Omelette with Spinach and Feta", 310, 22.0, 4.0, 23.0),
        ("Pancakes with Maple Syrup", 420, 8.0, 68.0, 12.0),
        ("Fruit Salad & Almonds", 210, 5.0, 36.0, 7.0),
        ("Cottage Cheese with Apples", 190, 18.0, 22.0, 3.0),
        ("Rice Cakes with Peanut Butter", 240, 8.0, 28.0, 11.0)]

    # Lunch & Dinner
    main_meals =[
        ("Chicken & Rice Bowl", 550, 45.0, 60.0, 10.0),
        ("Salmon with Asparagus & Quinoa", 520, 40.0, 35.0, 22.0),
        ("Turkey Sandwich on Whole Wheat", 410, 32.0, 44.0, 11.0),
        ("Beef Steak with Baked Potato", 650, 48.0, 42.0, 28.0),
        ("Tuna Pasta Salad", 480, 36.0, 52.0, 12.0),
        ("Lentil Soup with Bread", 340, 18.0, 56.0, 4.0),
        ("Grilled Tofu Buddha Bowl", 430, 22.0, 48.0, 16.0),
        ("Chicken Caesar Salad", 460, 38.0, 12.0, 29.0),
        ("Shrimp Stir-Fry with Vegetables", 390, 34.0, 38.0, 9.0),
        ("Burrito Bowl with Black Beans", 580, 26.0, 78.0, 18.0),
        ("Cod Fish with Sweet Potato", 370, 30.0, 40.0, 5.0),
        ("Turkey Meatballs with Pasta", 530, 42.0, 58.0, 14.0),
        ("Veggie Pizza Slice", 290, 11.0, 36.0, 12.0),
        ("Chickpea Curry with Basmati Rice", 470, 16.0, 72.0, 11.0),
        ("Beef Wrap with Hummus", 510, 35.0, 46.0, 20.0)
    ]

    meals_by_type  = {
        "breakfast": breakfast_snack_meals,
        "snack": breakfast_snack_meals,
        "lunch": main_meals,
        "dinner": main_meals,
    }
    meal_types = ["breakfast", "lunch", "dinner", "snack"]
    nutrition_rows = []
    log_id = 1000001

    for user in users:
        user_id = user["user_id"]
        for day in range(NUM_DAYS):
            date_str = (START_DATE + timedelta(days=day)).strftime("%Y-%m-%d")

            day_meal_types = random.sample(meal_types, random.randint(2,4))

            # Each user has 2-4 meals per day
            for meal_type in day_meal_types:
                options = meals_by_type[meal_type]
                meal_name, cals, prot, carbs, fat = random.choice(options)
                row = {
                        "log_id": log_id,
                        "user_id": user_id,
                        "date": date_str,
                        "meal_type": meal_type,
                        "food_name": meal_name,
                        "calories": cals,
                        "protein_g": prot,
                        "carbs_g": carbs,
                        "fat_g": fat,
                    }

                nutrition_rows.append(row)

                if random.random() < 0.02:
                    nutrition_rows.append(row)

                log_id += 1

    # Save in CSV format
    fieldnames = list(nutrition_rows[0].keys())
    with open(
        f"{OUTPUT_DIR}/daily_nutrition.csv", "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(nutrition_rows)

    print("Generate file: daily_nutrition.csv")


if __name__ == "__main__":
    print("Start to generate data...")
    generated_users = generate_users()
    generate_daily_activity(generated_users)
    generate_nutrition_logs(generated_users)
    print("\nGeneration completed successfully!")
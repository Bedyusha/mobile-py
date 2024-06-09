from datetime import datetime

def calculate_calories_and_food(weight_in_grams, birthdate, food_calories_per_100g):
    weight_in_kg = weight_in_grams / 1000
    age_in_months = (datetime.now() - datetime.strptime(birthdate, "%Y.%m.%d")).days // 30

    resting_calorie = weight_in_kg * 40 # Калорийность в состоянии покоя

    if age_in_months <= 4:
        daily_calories = resting_calorie * 3 # Умножаем на коэффициент 3 для щенков до 4 месяцев
    elif age_in_months <= 6:
        daily_calories = resting_calorie * 2 # Умножаем на коэффициент 2 для щенков до полугода
    elif age_in_months <= 8:
        daily_calories = resting_calorie * 1.2 # Умножаем на коэффициент 1.2 для щенков до 8 месяцев
    else:
        daily_calories = resting_calorie # Для взрослых собак и щенков старше 8 месяцев

    daily_food_in_grams = daily_calories / (food_calories_per_100g / 100)

    return daily_calories, daily_food_in_grams

# Пример использования функции
weight_in_grams = 7000
birthdate = "2024.01.01" # Дата рождения в формате гг.мм.дд
food_calories_per_100g = 370 # Калорийность корма на 100 грамм
daily_calories, daily_food_in_grams = calculate_calories_and_food(weight_in_grams, birthdate, food_calories_per_100g)
print(f"Ежедневное количество калорий: {daily_calories} ккал")
print(f"Ежедневное количество корма: {daily_food_in_grams} г")

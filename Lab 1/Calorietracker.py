# Project Title: Daily Calorie Tracker CLI
# Author: Vinayak [2501730150]


import datetime # Required for Task 6 to get the timestamp

def run_calorie_tracker():
    print("==================================================")
    print("           Daily Calorie Tracker CLI              ")
    print("==================================================")
    
    meal_names = [] 
    calorie_amounts = [] 
    
    # Get the daily calorie limit
    while True:
        try:
            daily_limit = float(input("\nEnter your daily calorie limit (e.g., 2000): ")) #
            if daily_limit > 0:
                break
            else:
                print("Limit must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number for the limit.")

    # Ask the user how many meals to enter
    while True:
        try:
            num_meals = int(input(f"How many meals will you log today (1 or more)? "))
            if num_meals >= 1:
                break
            else:
                print("You must enter at least 1 meal.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Collect meal data
    for i in range(num_meals):
        print(f"\n--- Entering Meal {i + 1} of {num_meals} ---")
        meal_name = input("Enter meal name (e.g., Breakfast, Lunch): ")
        meal_names.append(meal_name)

        # Calorie Amount Input and Conversion
        while True:
            try:
                # Use input() and convert to float for calorie amount
                calorie_input = input("Enter calorie amount for this meal: ")
                calorie_amount = float(calorie_input)
                calorie_amounts.append(calorie_amount)
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for calories.")
    
    
    total_calories = sum(calorie_amounts)
    average_calories = total_calories / len(calorie_amounts) if calorie_amounts else 0.0

    # Determine limit status
    limit_status = ""
    
    if total_calories > daily_limit:
        limit_status = " WARNING: You have EXCEEDED your daily calorie limit!"
    else:
        limit_status = " Success: You are WITHIN your daily calorie limit."
    
   

    # Build the report string for printing and saving
    report_lines = []
    report_lines.append("\n==================================================")
    report_lines.append("              DAILY CALORIE REPORT                ")
    report_lines.append(f"Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") # For Task 6
    report_lines.append(f"Daily Limit: {daily_limit} Calories")
    report_lines.append("==================================================")
    
    # Header of the summary table
    report_lines.append(f"{'Meal Name':<20}\t{'Calories':>10}")
    report_lines.append("-" * 35)

    for meal, calories in zip(meal_names, calorie_amounts):
        report_lines.append(f"{meal:<20}\t{calories:>10.2f}") 

    report_lines.append("-" * 35)

    # Summary calculations
    report_lines.append(f"{'Total:':<20}\t{total_calories:>10.2f}")
    report_lines.append(f"{'Average:':<20}\t{average_calories:>10.2f}")
    report_lines.append("-" * 35)
    report_lines.append(f"Limit Status: {limit_status}")
    report_lines.append("==================================================")

    # Print the report to the CLI
    for line in report_lines:
        print(line)

    # Task 6 (Bonus): Save Session Log to File 
    
    save_log = input("\nDo you want to save this session log to a file? (yes/no): ").lower()
    
    if save_log == 'yes':
        filename = "calorie_log.txt"
        try:
            with open(filename, "a") as file:
                file.write("\n" + "\n".join(report_lines))
                file.write("\n\n")
            print(f"\nReport successfully saved to {filename}")
        except Exception as e:
            print(f"\nError saving file: {e}")

if __name__ == "__main__":
    run_calorie_tracker()
# -*- coding: utf-8 -*-

def main():
    annual_salary = askUserForNumber("Enter your annual salary: ")
    portion_saved = askUserForDecimal("Enter the percent of your salary to save, as a decimal: ")  
    total_cost = askUserForNumber("Enter the cost of your dream home: ")
    semi_annual_rise = askUserForDecimal("Enter the semi-annual raise, as a decimal: ")

    # 25% of the total_cost
    portion_down_payment = total_cost * .25
    monthly_salary = annual_salary / 12

    qMonths = 0
    current_savings = 0
    while current_savings < portion_down_payment:

        # One month has passed
        qMonths += 1

        # Profit from the investment (4% annual)
        current_savings += current_savings * 0.04 / 12

        # Saved from the salary
        current_savings += monthly_salary * portion_saved

        # Increase the salary every 6 months
        if qMonths % 6 == 0:
            monthly_salary += monthly_salary * semi_annual_rise
        
    print("Number of months: " + str(qMonths))

# Promp the user for a number
def askUserForNumber(text):
    
    while True:
        number = input(text)
        try:
            number = int(number)
            if number > 0:
                return number
            else:
                continue
        except:
            # continue asking until the user enters a number
            continue

# Promp the user for a decimal number
def askUserForDecimal(text):
    
    while True:
        number = input(text)
        try:
            number = float(number)
            if number > 0 and number <= 1:
                return number
            else:
                continue
        except:
            # continue asking until the user enters a number
            continue

# Init program
main()

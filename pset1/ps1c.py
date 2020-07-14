# -*- coding: utf-8 -*-

def main():
    annual_salary = askUserForNumber("Enter the starting salary: ")
    portion_down_payment = 250000

    found = False
    numberOfGuesses = 0

    high = 10000 # 100%
    low = 0      # 0%
    guess = int((low + high) / 2)
    while abs(high - low) > 1:

        numberOfGuesses += 1
        portion_saved = guess / 10000
        # Reset for each iteration
        monthly_salary = annual_salary / 12
        current_savings = 0

        for i in range(1, 37):
    
            # Profit from the investment (4% annual)
            current_savings += current_savings * .04 / 12

            # Saved from the salary
            current_savings += monthly_salary * portion_saved

            # Increase the salary every 6 months by 7%
            if i % 6 == 0:
                monthly_salary += monthly_salary * .07

        # To be 100 near to the result is OK
        if abs(portion_down_payment - current_savings) < 100:
            found = True
            break
        elif current_savings > portion_down_payment:
            high = guess
        else:
            low = guess
        guess = int((low + high) / 2)

    if found:
        print("Best savings rate: " + str(guess / 10000))
        print("Steps in bisection search: " + str(numberOfGuesses))
    else:
        print("It is not possible to pay the down payment in three years.")

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

# Init program
main()

print("We're going to count BMI.")

weight = float(input("What is your weight in kg? "))
height = float(input("What is your height in cm? "))

bmi = round(weight / ((height / 100) ** 2), 2)

if bmi < 18.5:
    print("Your BMI is", bmi, "which means you are underweight.")

elif 18.5 <= bmi < 25:
    print("Your BMI is", bmi, "which means you are normal weight.")
    
else:
    print("Your BMI is", bmi, "which means you are overweight.")

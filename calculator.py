num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

# choose operation
print("Select operation:")
print("1. Add")
print("2. Subtract")
print("3. Multiply")
print("4. Divide")

choice = input("Enter choice (1/2/3/4): ")

# perform operation
if choice == '1':
    print(num1, "+", num2, "=", num1 + num2)

elif choice == '2':
    print(num1, "-", num2, "=", num1 - num2)

elif choice == '3':
    print(num1, "*", num2, "=", num1 * num2)

elif choice == '4':
    if num2 != 0:
        print("Result:", num1 / num2)
    else:
        print("Error: Division by zero is not allowed.")

else:
    print("Invalid input")

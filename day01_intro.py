
# OWASPShield - Interactive Menu

print("===== WELCOME TO OWASPSHIELD =====")

while True:
    print("\n1. About OWASPShield")
    print("2. Sample Cybersecurity Questions")
    print("3. Security Rule Check")
    print("0. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        print("\nOWASPShield is a cybersecurity learning assistant.")
        print("It helps beginners understand web application security.")

    elif choice == "2":
        print("\nSample Questions:")
        print("1. What is SQL Injection?")
        print("2. What is Cross-Site Scripting (XSS)?")
        print("3. What is OWASP Top 10?")

    elif choice == "3":
        print("\nBasic Password Security Check")
        password = input("Enter a sample password: ")

        if len(password) >= 8:
            print("Password length is acceptable.")
        else:
            print("Password is too short. Use at least 8 characters.")

    elif choice == "0":
        print("\nThank you for using OWASPShield. Goodbye!")
        break

    else:
        print("\nInvalid choice! Please enter 0, 1, 2, or 3.")


from app.records import load_records, search, count_by, get_by_id


def main():

    while True:

        print("\n===== OWASPSHIELD =====")
        print("1. View all records")
        print("2. Search cheat sheets")
        print("3. Count by OWASP category")
        print("4. Find record by ID")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            records = load_records()

            for i, record in enumerate(records, start=1):
                print(f"\nID: {i}")
                print("Cheat Sheet:", record["cheat_sheet"])
                print("Vulnerability:", record["vulnerability"])
                print("Recommended Control:", record["recommended_control"])
                print("Exact Parameter:", record["exact_parameter"])
                print("OWASP Category:", record["owasp_top10_category"])
                print("Source URL:", record["source_url"])

        elif choice == "2":

            keyword = input("Enter search keyword: ")
            results = search(keyword)

            if results:
                for record in results:
                    print("\nCheat Sheet:", record["cheat_sheet"])
                    print("Vulnerability:", record["vulnerability"])
                    print("OWASP Category:", record["owasp_top10_category"])
                    print("Source:", record["source_url"])
            else:
                print("No matching records found.")

        elif choice == "3":

            category = input("Enter OWASP category: ")
            result = count_by(category)

            print("Total records in this category:", result)

        elif choice == "4":

            try:
                record_id = int(input("Enter record ID: "))
                record = get_by_id(record_id)

                if record:
                    print("\nRecord found:")
                    print(record)
                else:
                    print("Record ID not found.")

            except ValueError:
                print("Please enter a valid numeric ID.")

        elif choice == "5":

            print("Thank you for using OWASPShield!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

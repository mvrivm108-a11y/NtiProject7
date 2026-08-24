from datetime import datetime
import difflib


class LostItem:
    def __init__(self, type, brand, colour, description):
        self.type = type
        self.brand = brand
        self.colour = colour
        self.description = description
        self.date_found = datetime.now()

    def show_info(self):
        return (
            f"Type: {self.type}, "
            f"Brand: {self.brand}, "
            f"Colour: {self.colour}, "
            f"Description: {self.description}"
        )


class System:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def search_item(self, search_description):
        matches = []

        for item in self.items:
            similarity = difflib.SequenceMatcher(
                None,
                search_description.lower(),
                item.description.lower()
            ).ratio()

            if similarity > 0.6:
                matches.append((item, similarity))

        return matches

    def show_items(self):
        if not self.items:
            print("❌ No found items available.")
            return

        for item in self.items:
            print(item.show_info())

    def remove_item(self, item, status):
        days = (datetime.now() - item.date_found).days

        if days >= 30 or status.lower() == "found":
            if item in self.items:
                self.items.remove(item)

    def filter_by_date_range(self, days_ago):
        filtered = []

        for item in self.items:
            age = (datetime.now() - item.date_found).days

            if age <= days_ago:
                filtered.append(item)

        return filtered

    def show_filtered_by_date(self, days_ago):
        results = self.filter_by_date_range(days_ago)

        if not results:
            print(f"❌ No items found in the last {days_ago} days.")
            return

        print(f"\n✅ Items added in the last {days_ago} days:\n")

        for item in results:
            age = (datetime.now() - item.date_found).days
            print(f"{item.show_info()} - Added {age} days ago")

        print()


# Create the system
system1 = System()


while True:

    welcome = input(
        """Welcome to the Lost and Found Program.

Enter 'lost' if you lost an object and need to search for it.
Enter 'found' if you found a lost item and want to register it.

Your choice: """
    )

    print("\n=====================================================\n")

    # ================= FOUND =================

    if welcome.lower() == "found":

        type1 = input(
            "Enter the type of object that you found "
            "(bag-passport-book-clothes): "
        )

        brand = input(
            "Enter the brand or the name of this object: "
        )

        colour = input(
            "Enter the color of the object: "
        )

        description = input(
            "Enter the object's description: "
        )

        lostitem1 = LostItem(
            type1,
            brand,
            colour,
            description
        )

        system1.add_item(lostitem1)

        print("\n✅ Item added successfully!\n")

        continuation = input(
            "Enter 1 to return to the first menu\n"
            "Enter 2 to Exit: "
        )

        if continuation == "1":
            continue

        elif continuation == "2":
            break

        else:
            print("Wrong choice, Exiting.")
            break

    # ================= LOST =================

    elif welcome.lower() == "lost":

        print("Type 1 to show information of the found objects.")
        print("Type 2 to search for a lost object.")
        print("Type 3 to filter by date range.")
        print("Type 4 to exit.")

        choice = input("Enter your choice: ")

        # Show all items
        if choice == "1":

            print("\n=== All Found Items ===\n")

            system1.show_items()

            print()

        # Search for an item
        elif choice == "2":

            search_term = input(
                "Enter description of the object you're looking for: "
            )

            results = system1.search_item(search_term)

            if results:

                print("\n✅ Found similar items:\n")

                for item, similarity in results:
                    print(
                        f"{item.show_info()} "
                        f"- Similarity: {similarity * 100:.1f}%\n"
                    )

            else:
                print("❌ No similar items found.\n")

        # Filter by date
        elif choice == "3":

            try:
                days = int(
                    input(
                        "Enter number of days "
                        "(e.g., 7 for last week): "
                    )
                )

                if days < 0:
                    print("❌ Number of days cannot be negative.")

                else:
                    system1.show_filtered_by_date(days)

            except ValueError:
                print("❌ Please enter a valid number.")

        # Exit
        elif choice == "4":

            break

        else:
            print("❌ Wrong choice.")

    # ================= INVALID =================

    else:

        print("❌ Invalid choice. Please enter 'lost' or 'found'.")
        

print("\nThank you for using Lost and Found System! 👋")
        print("Invalid choice")
        break

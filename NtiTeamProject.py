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
        return(f'type : {self.type} ,brand : {self.brand} , colour : {self.colour} , description : {self.description} ')


class System:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)

    def search_item(self, search_description):
        matches = []
        for item in self.items:
            similarity = difflib.SequenceMatcher(None, search_description.lower(), item.description.lower()).ratio()
            if similarity > 0.6:
                matches.append((item, similarity))
        return matches

    def show_items(self):
        for item in self.items:
            print(item.show_info())
    
    def remove_item(self, item, status):
        self.status = status
        days = (datetime.now() - item.date_found).days
        if days >= 30:
            self.items.remove(item)
        if self.status == "found":
            self.items.remove(item)
    
    # ✅ ميثود 5: الفلترة حسب العمر
    def filter_by_date_range(self, days_ago):
        """البحث عن الأشياء المضافة في آخر X يوم"""
        filtered = []
        
        for item in self.items:
            age = (datetime.now() - item.date_found).days
            if age <= days_ago:
                filtered.append(item)
        
        return filtered
    
    def show_filtered_by_date(self, days_ago):
        """عرض الأشياء المضافة في آخر X يوم"""
        results = self.filter_by_date_range(days_ago)
        
        if not results:
            print(f"❌ No items found in the last {days_ago} days")
            return
        
        print(f"\n✅ Items added in the last {days_ago} days:\n")
        for item in results:
            age = (datetime.now() - item.date_found).days
            print(f"{item.show_info()} - Added {age} days ago")
        print()


system1 = System()

while True:
    welcome = input('''Welcome to the lost and found program, Enter lost, If you lost an object and need to search for it
           Enter found, If you found a lost item and want to register it, 
           ''')
    print("\n=====================================================\n")
    
    if welcome.lower() == 'found':
        type1 = input("Enter the type of object that you found(bag-passport-book-clothes): ")
        brand = input("Enter the brand or the name of this object: ")
        colour = input("Enter the color of the object: ")
        description = input("Enter the object's description: ")
        lostitem1 = LostItem(type1, brand, colour, description)
        
        system1.add_item(lostitem1)
        print("✅ Item added successfully!\n")
        
        continuation = int(input('Enter 1 to return to the first menu\nEnter 2 to Exit: '))
        if continuation == 1:
            continue
        elif continuation == 2:
            break
        else:
            print("Wrong choice, Exiting")
            break
    
    elif welcome.lower() == 'lost':
        print("Type 1 to show info of the found objects:")
        print("Type 2 to search for a lost object: ")
        print("Type 3 to filter by date range:")
        print("Type 4 to exit:") 
        choice = int(input())
        
        if choice == 1:
            print("\n=== All Found Items ===\n")
            system1.show_items()
            print()
        
        elif choice == 2:
            search_term = input("Enter description of the object you're looking for: ")
            results = system1.search_item(search_term)
            
            if results:
                print("\n✅ Found similar items:\n")
                for item, similarity in results:
                    print(f"{item.show_info()} - Similarity: {similarity*100:.1f}%\n")
            else:
                print("❌ No similar items found\n")
        
        elif choice == 3:
            days = int(input("Enter number of days (e.g., 7 for last week): "))
            system1.show_filtered_by_date(days)
        
        elif choice == 4:
            break
        else:
            print("Wrong choice")
    
    else:
        print("Invalid choice")
        break

print("\nThank you for using Lost and Found System! 👋")
    
    else:
        print("Invalid choice")
        break

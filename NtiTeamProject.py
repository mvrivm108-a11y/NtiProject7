from datetime import datetime
import difflib

class LostItem:
    def __init__(self, type, brand, colour, description):
        self.type = type
        self.brand = brand
        self.colour = colour
        self.description = description
        self.date_found = datetime.now()
        self.status = "found"  # default status when registered

    def show_info(self):
        return (f"Type: {self.type}, Brand: {self.brand}, "
                f"Colour: {self.colour}, Description: {self.description}, "
                f"Status: {self.status}")






class System:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def search_item(self, search_description):
        matches = []
        for item in self.items:
            similarity = difflib.SequenceMatcher(
                None, search_description.lower(), item.description.lower()
            ).ratio()
            if similarity > 0.6:  # 60% similarity means its the same
                item.status = "claimed"  # mark as claimed when matched
                matches.append((item, similarity))
        return matches

    def show_items(self):
        for item in self.items:
            print(item.show_info())

    def remove_item(self, item):
        days = (datetime.now() - item.date_found).days
        if days >= 30 or item.status == "claimed":
            self.items.remove(item)

        

        
system1=System()

while True:
    welcome=input('''Welcome to the lost and found program, Enter lost if you lost an object and need to search for it
Enter found if you found a lost item and want to register it :''')
    print("\n=====================================================\n")
    if welcome.lower() =='found':
        type1=input("Enter the type of object that you found(bag-passport-book-clothes): ")
        brand1=input("Enter the brand or the name of this object: ")
        colour1=input("Enter the color of the object: ")
        description1=input("Enter the object's description: ")
        lostitem1=LostItem(type1,brand1,colour1,description1)
        continuation=int(input('Enter 1 to return to the first menu\nEnter 2 to Exit: '))
        if continuation==1:
            continue
        elif continuation==2:
            break
        else:
            print("Wrong choice, Exiting")
            break
    elif welcome.lower() == 'lost':
        print("Type 1 to show info of the found objects:")
        print("Type 2 to search for a lost object: ")
        print("Type 3 to exit: ") 
        choice = int(input())
        if choice == 1:
            system1.show_items()   # ✅ show all items in the system
        elif choice == 2:
            search_desc = input("Enter description of your lost item: ")
            matches = system1.search_item(search_desc)  # ✅ pass description
            if matches:
                for item, sim in matches:
                    print(f"Match found: {item.show_info()} (Similarity: {sim:.2f})")
            else:
                print("No matching items found.")
        else:
            print("Invalid choice")
            break
    else:
        print("Invalid choice, Exiting")
        break
    
     
        

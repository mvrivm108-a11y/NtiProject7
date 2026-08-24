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
#lets say no. of found object in the excel file is 30 object
number_of_obj=30
#thats when searching |
#loop not very correct

while True:
    welcome=input('''Welcome to the lost and found program, Enter lost, If you lost an object and need to search for it
           Enter found, If you found a lost item and want to register it, 
           ''')
    print("\n=====================================================\n")
    if welcome.lower() =='found':
        type1=input("Enter the type of object that you found(bag-passport-book-clothes): ")
        brand=input("Enter the brand or the name of this object: ")
        colour=input("Enter the color of the object: ")
        description=input("Enter the object's description: ")
        lostitem1=LostItem(type1,brand,colour,description)
        continuation=int(input('Enter 1 to return to the first menu\nEnter 2 to Exit: '))
        if continuation==1:
            continue
        elif continuation==2:
            break
        else:
            print("Wrong choice, Exiting")
            break
    elif welcome.lower()=='lost':
        print("Type 1 to show info of the found objects:")
        print("Type 2 to search for an lost object: ")
        print("Type 3 to exit:") 
        choice=int(input())
        if choice==1:
            lostitem1.show_info()
        elif choice==2:
            system1.search_item()
        else:
            break
    else:
        break
        print("Invalid choice")
        break

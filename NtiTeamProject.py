from datetime import datetime
import difflib
import json
import os

class LostItem:
    def __init__(self, id, category, brand, colour, description, date_found=None, status="found"):
        self.id = id
        self.category = category
        self.brand = brand
        self.colour = colour
        self.description = description
        if date_found:
            self.date_found = datetime.fromisoformat(date_found)
        else:
            self.date_found = datetime.now()
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "brand": self.brand,
            "colour": self.colour,
            "description": self.description,
            "date_found": self.date_found.isoformat(),
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            category=data["category"],
            brand=data["brand"],
            colour=data["colour"],
            description=data["description"],
            date_found=data["date_found"],
            status=data["status"]
        )

    def show_info(self):
        return (f"ID: {self.id}, Category: {self.category}, "
                f"Brand: {self.brand}, Colour: {self.colour}, "
                f"Description: {self.description}, Status: {self.status}")

class LostRequest:
    def __init__(self, id, category, brand, colour, description, date_request=None):
        self.id = id
        self.category = category
        self.brand = brand
        self.colour = colour
        self.description = description

        if date_request:
            self.date_request = datetime.fromisoformat(date_request)
        else:
            self.date_request = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "brand": self.brand,
            "colour": self.colour,
            "description": self.description,
            "date_request": self.date_request.isoformat()}

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            category=data["category"],
            brand=data["brand"],
            colour=data["colour"],
            description=data["description"],
            date_request=data["date_request"])

    def show_info(self):
        return (
            f"Request ID: {self.id}, "
            f"Category: {self.category}, "
            f"Brand: {self.brand}, "
            f"Colour: {self.colour}, "
            f"Description: {self.description}")

class System:
    def __init__(self):
        self.items = []
        self.data_file = "lost_items_data.json"
        self.load_data()
        self.requests= []
        self.requests_file= "lost_requests_data.json"
        self.load_requests()

    def save_data(self):
        """Save all items to JSON file"""
        try:
            data = [item.to_dict() for item in self.items]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
            """Load items from JSON file"""
            try:
                if os.path.exists(self.data_file):
                    with open(self.data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.items = [LostItem.from_dict(item) for item in data]
                    print(f"Loaded {len(self.items)} items from database.")
                else:
                    print("No existing data file found. Starting with empty database.")
            except Exception as e:
                print(f"Error loading data: {e}")
                self.items = []

    def save_requests(self):
        try:
            data = [request.to_dict() for request in self.requests]
            with open(self.requests_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Requests saved successfully!")
        except Exception as e:
            print(f"Error saving requests: {e}")

    def load_requests(self):
        try:
            if os.path.exists(self.requests_file):
                with open(self.requests_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.requests = [LostRequest.from_dict(request)
                    for request in data]
                print(f"Loaded {len(self.requests)} lost requests.")
            else:
                print("No existing requests file found.")
        except Exception as e:
            print(f"Error loading requests: {e}")
            self.requests = []

    def create_request(self, category, brand, colour, description):
        if self.requests:
            request_id = max(request.id for request in self.requests) + 1
        else:
            request_id = 1
        request = LostRequest(request_id, category, brand, colour, description)
        self.add_request(request)
        return request

    def add_request(self, request):
        self.requests.append(request)
        self.save_requests()

    def add_item(self, item):
        self.items.append(item)
        self.save_data()  # Save immediately after adding

    def search_item(self, category, brand, colour, description):
        matches = []
        for item in self.items:
            item_text = (item.category + " " + item.brand + " " + item.colour + " " + item.description).lower()
            search_text = (category + " " + brand + " " + colour + " " + description).lower()

            similarity = difflib.SequenceMatcher(
                None, search_text, item_text).ratio()
            if similarity > 0.5:
                print(f"Possible match: {item.show_info()} (Similarity: {similarity})")
                confirm = input("Is this your item? (yes/no): ")
                if confirm.lower() == "yes":
                    item.status = "claimed"
                    matches.append((item, similarity))
        if matches:
            self.save_data()
        return matches

    def search_requests(self, item):
        matches = []
        for request in self.requests:
            item_text = (item.category + " " + item.brand + " " + item.colour + " " + item.description).lower()
            request_text = (request.category + " " + request.brand + " " + request.colour + " " + request.description).lower()
            similarity = difflib.SequenceMatcher(None, item_text, request_text).ratio()
            if similarity > 0.5:
                matches.append((request, similarity))
        return matches
    
    def search_by_category(self, category):
        matches = []
        for item in self.items:
            if item.category.lower() == category.lower():
                matches.append(item)
        if not matches:
            print("No items found in this category.")
        else:
            for item in matches:
                print(item.show_info())
        return matches
    def show_items(self):
        if not self.items:
            print("No items registered yet.")
            return
        for item in self.items:
            print(item.show_info())

    def remove_item(self, item):
        days = (datetime.now() - item.date_found).days
        if days >= 30 or item.status == "claimed":
            self.items.remove(item)
            self.save_data()
            return True
        return False
    
    def find_item(self, item_id):
        for item in self.items:
            if item.id == item_id:
                return item
        return None

system1 = System()

fixed_password = 'admin123'
while True:
    welcome = input('''Welcome to the lost and found program, Enter lost if you lost an object and need to search for it
                    Enter found if you found a lost item and want to register it :''')
    print("\n=====================================================\n")
    
    if welcome.lower() == 'found':
        state = input('Enter as local or management? (write l or m): ')
        if state.lower() == 'm':
            password = input('Enter password for verification: ')
            if password == fixed_password:
                print('Verification completed successfully!')
                while True:
                    print("===== MANAGEMENT MENU =====")
                    print('1. Add found item')
                    print('2. Show found items')
                    print('3. Delete found item')
                    print('4. Exit')
                    management_choice = int(input("Enter your choice: "))
                    
                    if management_choice == 1:
                        print("""===== Categories =====
                                                1. Bag
                                                2. Watch
                                                3. Ring
                                                4. Phone
                                                5. Passport
                                                6. Book
                                                7. Clothes
                                                8. Keys
                                                9. Other""")
                        category_choice = int(input("Enter the category number: "))
                        if category_choice == 1:
                            category1 = "Bag"
                        elif category_choice == 2:
                            category1 = "Watch"
                        elif category_choice == 3:
                            category1 = "Ring"
                        elif category_choice == 4:
                            category1 = "Phone"
                        elif category_choice == 5:
                            category1 = "Passport"
                        elif category_choice == 6:
                            category1 = "Book"
                        elif category_choice == 7:
                            category1 = "Clothes"
                        elif category_choice == 8:
                            category1 = "Keys"
                        elif category_choice == 9:
                            category1 = "Other"
                        else:
                            print("Invalid category.")
                            continue
                        
                        brand1 = input("Enter the brand or the name of this object: ")
                        colour1 = input("Enter the color of the object: ")
                        description1 = input("Enter the object's description: ")
                        
                        if system1.items:
                            item_id = max(item.id for item in system1.items) + 1
                        else:
                            item_id = 1
                        
                        found_item = LostItem(item_id, category1, brand1, colour1, description1)
                        system1.add_item(found_item)
                        print('Item added successfully!')
                        request_matches = system1.search_requests(found_item)
                        if request_matches:
                            print("\n===== POSSIBLE LOST REQUESTS =====")
                            for request, similarity in request_matches:
                                print(f"{request.show_info()} (Similarity: {similarity})")
                            else:
                                print("No matching lost requests found.")
                        
                    elif management_choice == 2:
                        system1.show_items()
                        
                    elif management_choice == 3:
                        item_id = int(input("Enter the ID of the item to delete: "))
                        item = system1.find_item(item_id)
                        if item is None:
                            print("Item not found.")
                        else:
                            deleted = system1.remove_item(item)
                            if deleted:
                                print('Item deleted successfully!')
                            else:
                                print("This item cannot be deleted yet.")
                                print("It must be older than 30 days or claimed.")
                                
                    elif management_choice == 4:
                        print("Returning to main menu...")
                        break
                    else:
                        print("Invalid choice.")
                
                continuation = int(input('Enter 1 to return to the first menu\nEnter 2 to Exit: '))
                if continuation == 1:
                    continue
                elif continuation == 2:
                    break
                else:
                    print("Wrong choice, Exiting")
                    break
                    
            else:
                print("Wrong password! Access denied.")
                
        elif state.lower() == 'l':
            print('Sorry! Access Not Allowed')
            print('Please hand the item to the nearest security point')
        else:
            print('Error! Check your choice again.')
            continue

    elif welcome.lower() == 'lost':
        print("===== USER MENU =====")
        print("1. Show all found items")
        print("2. Search by category")
        print("3. Search for a lost item")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            system1.show_items()
        elif choice == 2:
            print("""===== Categories =====
                    1. Bag
                    2. Watch
                    3. Ring
                    4. Phone
                    5. Passport
                    6. Book
                    7. Clothes
                    8. Keys
                    9. Other""")
            category_choice = int(input("Enter the category number: "))
            if category_choice == 1:
                category1 = "Bag"
            elif category_choice == 2:
                category1 = "Watch"
            elif category_choice == 3:
                category1 = "Ring"
            elif category_choice == 4:
                category1 = "Phone"
            elif category_choice == 5:
                category1 = "Passport"
            elif category_choice == 6:
                category1 = "Book"
            elif category_choice == 7:
                category1 = "Clothes"
            elif category_choice == 8:
                category1 = "Keys"
            elif category_choice == 9:
                category1 = "Other"
            else:
                print("Invalid category.")
                continue
            system1.search_by_category(category1)
        elif choice == 3:
            print("Enter the information about your lost item.")
            category = input("Enter category: ")
            brand = input("Enter brand or name: ")
            colour = input("Enter colour: ")
            description = input("Enter description: ")

            matches = system1.search_item(category, brand, colour, description)
            if matches:
                for item, sim in matches:
                    print(f"Match found: {item.show_info()} "f"(Similarity: {sim:.2f})")
                    system1.remove_item(item)
            else:
                print("No matching items found.")
                create = input("Would you like to create a lost request? (y or n): ")
                if create.lower() == "y":
                    request = system1.create_request(category, brand, colour, description)
                    print("Lost request created successfully!")
                    print(request.show_info())
        elif choice == 4:
            print("Exiting")
            break
            
    else:
        print("Invalid choice, Exiting")
        break
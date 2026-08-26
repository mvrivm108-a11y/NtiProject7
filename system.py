from datetime import datetime
import difflib
import json
import os
from lost_item import LostItem
from request_item import LostRequest
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

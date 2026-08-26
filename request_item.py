from datetime import datetime
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
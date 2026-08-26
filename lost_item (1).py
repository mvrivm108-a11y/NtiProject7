from datetime import datetime
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
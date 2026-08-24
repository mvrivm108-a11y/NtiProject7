from datetime import datetime
class LostItem :
    def __init__(self,type,brand,colour,description):
        self.type=type
        self.brand=brand
        self.colour=colour
        self.description=description
        self.date_found=datetime.now()
    def show_info(self):
        return(f'type : {self.type} ,brand : {self.brand} , colour : {self.colour} , description : {self.description} ')
class System :
    def __init__(self):
        self.items=[]
    def add_item (self , item ):
        self.items.append(item)

    def search_item (self , item):
    
        if item in self.items:
            return 'found item'
        else :
            return 'not found'
    def show_items (self):
        for item in self.items :
            print(item.show_info())
    def remove_item(self,item):
        days=(datetime.now()-item.date_found).days
        if days >=30:
            self.items.remove(item)
        
system1=System()
#lets say no. of found object in the excel file is 30 object
number_of_obj=30
#thats when searching |
#loop not very correct

for i in range(number_of_obj):
    welcome=input('''Welcome to the lost and found program, \nIf you lost an object and need to search for it, Enter lost
           \nIf you found a lost item and want to register it, Enter found
           Please answer the following requests!''')
    print("\n=====================================================\n")
    if welcome =='found':
        type1=input("Enter the type of object that you found(bag-passport-book-clothes): ")
        brand=input("Enter the brand or the name of this object: ")
        colour=input("Enter the color of the object: ")
        description=input("Enter the object's description: ")
        lostitem1=LostItem(type1,brand,colour,description)
    elif welcome=='lost':
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
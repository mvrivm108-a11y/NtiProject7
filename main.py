from system import System
from lost_item import LostItem

system1 = System()
fixed_password = 'admin123'
while True:                                                    ##### EDITED
    welcome = input('''===Welcome to the lost and found program===\nEnter lost if you lost an object and need to search for it.\nEnter found if you found a lost item and want to register it :''')
    print("\n=====================================================\n")
    
    if welcome.lower() == 'found':
        state = input('Enter as local or management? (write l or m): ')
        if state.lower() == 'm':
            password = input('Enter password for verification: ')
            if password == fixed_password:
                print('Verification completed successfully!\n')
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
                elif continuation == 2:                      #print('Thanks for using our system!')
                    break
                else:
                    print("Wrong choice, Exiting")
                    break
                    
            else:
                print("Wrong password! Access denied.")
                
        elif state.lower() == 'l':
            print('Sorry! Access Not Allowed')
            print('Please hand the item to the nearest security point\n')
            #print('Thanks for using our system!')
            #break
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
            category = input("Enter category: ")                 # category like above?
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
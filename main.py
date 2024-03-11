class menu:
    def __init__(self):
        self.items = []
    
    def __repr__(self):
        return self
    
    def __str__(self):
        menu_list = "\nMenu:\n"
        for i in range(len(self.items)):
            menu_list += f'{i+1}. {self.items[i].name}, {self.items[i].price}, {self.items[i].qnt}; \n'
        return menu_list
    
    def add(self, item):
        self.items.append(item)
    
    def find(self, other):
        for i in range(len(self.items)):
            if self.items[i] == other:
                return True
        return False
    
    def simple_rem(self, item_r):
        self.items.remove(item_r)
        
class item:
    def __init__(self, name, price, qnt):
        self.name = name
        self.price = price
        self.qnt = qnt

    def __repr__(self):
        return self
    
    def __str__(self):
        return f'Name: {self.name}, Price: {self.price}, Qnt: {self.qnt}.'
    
    def __eq__(self, other):
        if isinstance(other, item):
            if self.name == other.name and self.price == other.price and self.qnt == other.qnt:
                return True
            else:
                return False
        else:
            return False
    
    def change_name(self, name):
        self.name = name
    def change_price(self, price):
        self.price = price
    def change_qnt(self, qnt):
        self.qnt = qnt

def filtered(menu_obj, filtered_value, oper_1, oper_2):
    if oper_1 == 1:
        if oper_2 == 1:
            filtered_menu = [d for d in menu_obj.items if d.name != filtered_value]
        elif oper_2 == 2:
            filtered_menu = [d for d in menu_obj.items if d.price != filtered_value]
        else:
            filtered_menu = [d for d in menu_obj.items if d.qnt != filtered_value]
    else:
        if oper_2 == 1:
            filtered_menu = [d for d in menu_obj.items if d.name == filtered_value]
        elif oper_2 == 2:
            filtered_menu = [d for d in menu_obj.items if d.price == filtered_value]
        else:
            filtered_menu = [d for d in menu_obj.items if d.qnt == filtered_value]
    return filtered_menu

menu_1 = menu()
print("Empty menu was created. \n")

def show_menu():
    print("""1. Create item 
2. Show current item 
3. Change name of current item 
4. Change price of current item 
5. Change qnt of current item 
6. Add current item to the menu 
7. Show full menu 
8. Simple remove form menu 
9. Filter menu 
10. Exit \n""")

item_1 = item("name", 0, 0)

while True:
    show_menu()
    choice = input("Enter your choice (1-10): ")
    
    if choice == "1":
        print("Name:")
        d1_name = input()

        while True:
            print("Price:")
            d1_price_str = input()
            try:
                d1_price = float(d1_price_str)
                if d1_price >= 0:
                    break
                else:
                    print("\nprice can't be negative\n")
            except ValueError:
                print("\nInvalid input: qnt not a valid float\n")
        while True:
            print("Qnt:")
            d1_qnt_str = input()
            try:
                d1_qnt = int(d1_qnt_str)
                if d1_qnt >= 0:
                    break
                else:
                    print("\nqnt can't be negative\n")
            except ValueError:
                print("\nInvalid input: qnt not a valid int\n")

        try:
            item_1 = item(d1_name, d1_price, d1_qnt)
            print("\nCreated successfully\n")
        except:
            print("\nSomething went wrong while trying to create item...\n")

    elif choice == "2":
        print(f"\nCurrent item: \n{item_1}\n")

    elif choice == "3":
        print(f"\nCurrent name: {item_1.name} \nProvide new name:")
        name = input()
        item_1.change_name(name)
        
    elif choice == "4":
        while True:
            print(f"\nCurrent price: {item_1.price} \nProvide new price:")
            try:
                price = float(input())
                if price >= 0:
                    break
                else:
                    print("\nprice can't be negative\n")
            except:
                print("\nIncorrect value\n")
        item_1.change_price(price)

    elif choice == "5":
        while True:
            print(f"\nCurrent qnt: {item_1.qnt} \nProvide new qnt:")
            try:
                qnt = int(input())
                if qnt >= 0:
                    break
                else:
                    print("\nqnt can't be negative\n")
            except:
                print("\nIncorrect value\n")
        item_1.change_qnt(qnt)
    
    elif choice == "6":
        try:
            menu_1.add(item_1)
            print("\nItem was added successfully\n")
        except:
            print("\nSomething went wrong while trying to add an item\n")

    elif choice == "7":
        print(menu_1)
    
    elif choice == "8":
        print("Name:")
        dr_name = input()

        while True:
            print("Price:")
            dr_price_str = input()
            try:
                dr_price = float(dr_price_str)
                if dr_price >= 0:
                    break
                else:
                    print("\nprice can't be negative\n")
            except ValueError:
                print("\nInvalid input: price not a valid float\n")

        while True:
            print("Qnt:")
            dr_qnt_str = input()
            try:
                dr_qnt = int(dr_qnt_str)
                if dr_qnt >= 0:
                    break
                else:
                    print("\nqnt can't be negative\n")
            except ValueError:
                print("\nInvalid input: qnt not a valid int\n")

        item_r = item(dr_name, dr_price, dr_qnt)

        print("\nItem to remove: ", item_r)

        if menu_1.find(item_r):
            print("\nItem found\n")
        else:
            print("\nItem not found\n")

        try:
            menu_1.simple_rem(item_r)
            print("item deleted\n")
        except:
            print("unable to delete\n")
            
    elif choice == "9":
        print("\n1. Blackilst \n2. Whitelist")
        while True:
            try:
                oper_1 = int(input())
                if 0 < oper_1 < 3:
                    break
                else:
                    print("\nIncorrect operation number\n")
            except:
                print("\nIncorrect operation value type\n")
        print("\n1. Name \n2. Price \n3. Qnt")
        while True:
            try:
                oper_2 = int(input())
                if 0 < oper_2 < 4:
                    break
                else:
                    print("\nIncorrect operation number\n")
            except:
                print("\nIncorrect operation value type\n")
        print("Provide filtered value: ")
        filtered_value = input()
        filtered_menu = filtered(menu_1, filtered_value, oper_1, oper_2)
        for i in range(len(filtered_menu)):
            print(filtered_menu[i])


    elif choice == "10":
        print("\nExiting the program. Goodbye!\n")
        break
    else:
        print("\nInvalid choice. Please enter a number between 1 and 10.\n")
    

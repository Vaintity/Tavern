class menu:
    def __init__(self):
        self.items = []
    
    def __repr__(self):
        return self
    
    def __str__(self):
        for i in range(len(self.items)):
            return f'{i+1}. {self.items[i].name}, {self.items[i].price}, {self.items[i].qnt};'
    
    def add(self, item):
        self.items.append(item)
    
    def simple_rem(self, item_r):
        if isinstance(item_r, item):
            self.remove(item_r)
        else:
            raise TypeError('Not supported variable type')
        
class item:
    def __init__(self, name, price, qnt):
        self.name = name
        self.price = price
        self.qnt = qnt

    def __repr__(self):
        return self
    
    def __str__(self):
        return f'Name: {self.name}, Price: {self.price}, Qnt: {self.qnt}.'
    
    def change_name(self, name):
        self.name = name
    def change_price(self, price):
        self.price = price
    def change_qnt(self, qnt):
        self.qnt = qnt

#filtering: oper_1 - black-/whitelist, oper_2 - by Name/Price/Qnt
def filtered(menu_obj, filtered_value, oper_1, oper_2):
    if isinstance(menu_obj, menu) and 0 < oper_2 < 4:
        if oper_1 == 1:
            filtered_menu = [d for d in menu_obj if d[oper_2] != filtered_value]
        elif oper_1 == 2:
            filtered_menu = [d for d in menu_obj if d[oper_2] == filtered_value]
        else:
            raise ValueError('Incorrect operation_1 value')
    else:
        raise Exception('Not supported menu variable type or Incorrect operation_2 value')
    return filtered_menu

menu_1 = menu()
print("Empty menu was created.")

def show_menu():
    print("\n1. Create item")
    print("2. Show current item")
    print("3. Change name of current item")
    print("4. Change price of current item")
    print("5. Change qnt of current item")
    print("6. Add current item to the menu")
    print("7. Show full menu")
    print("8. Simple remove form menu")
    print("9. Filter menu")
    print("10. Exit \n")

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
                break
            except ValueError:
                print("Invalid input: qnt not a valid float \n")
        while True:
            print("Qnt:")
            d1_qnt_str = input()
            try:
                d1_qnt = int(d1_qnt_str)
                break
            except ValueError:
                print("Invalid input: qnt not a valid int \n")

        try:
            item_1 = item(d1_name, d1_price, d1_qnt)
            print("Created successfully")
        except:
            print("Something went wrong while trying to create item...")

    elif choice == "2":
        print(item_1)

    elif choice == "3":
        print("Provide new name:")
        name = input()
        item_1.change_name(name)
        
    elif choice == "4":
        while True:
            print("Provide new price:")
            try:
                price = float(input())
                break
            except:
                print("Incorrect value")
        item_1.change_price(price)

    elif choice == "5":
        while True:
            print("Provide new qnt:")
            try:
                qnt = int(input())
                break
            except:
                print("Incorrect value")
        item_1.change_qnt(qnt)
    
    elif choice == "6":
        try:
            menu_1.add(item_1)
            print("\nItem was added successfully")
        except:
            print("\nSomething went wrong while trying to add an item")

    elif choice == "7":
        print("\n", menu_1)
    
    elif choice == "8":
        print("Name:")
        dr_name = input()

        while True:
            print("Price:")
            dr_price_str = input()
            try:
                dr_price = float(dr_price_str)
                break
            except ValueError:
                print("Invalid input: qnt not a valid float")

        while True:
            print("Qnt:")
            dr_qnt_str = input()
            try:
                dr_qnt = int(dr_qnt_str)
                break
            except ValueError:
                print("Invalid input: qnt not a valid int")

        item_r = item(dr_name, dr_price, dr_qnt)
        try:
            menu_1.simple_rem(item_r)
        except:
            print("No such item")

    elif choice == "9":
        print("1. Blackilst \n2. Whitelist")
        oper_1 = input()
        print("1. Name \n2. Price \n3. Qnt")
        oper_2 = input()
        print("Provide filtered value: ")
        filtered_value = input()
        filtered(menu_1, filtered_value, oper_1, oper_2)


    elif choice == "10":
        print("\nExiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 10.")
    

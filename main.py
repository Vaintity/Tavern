class menu:
    def __init__(self):
        self.drinks = []
    
    def __repr__(self):
        return self
    
    def __str__(self):
        for i in self:
            return f'{i+1}. {self[i].name}, {self[i].price}, {self[i].qnt};'
    
    def add(self, drink):
        self.drinks.append(drink)
    
    def simple_rem(self, drink_r):
        if isinstance(drink_r, drink):
            self.remove(drink_r)
        else:
            raise TypeError('Not supported variable type')
        
class drink:
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
    print("1. Create drink")
    print("2. Show current drink")
    print("3. Change name of current drink")
    print("4. Change price of current drink")
    print("5. Change qnt of current drink")
    print("6. Add current drink to the menu")
    print("7. Show full menu")
    print("8. Simple remove form menu")
    print("9. Filter menu")
    print("10. Exit")

cntr = 0

while True:
    show_menu()
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        print("Name:")
        d1_name = input()

        print("Price:")
        d1_price_str = input()
        try:
            d1_price = float(d1_price_str)
        except ValueError:
            print("Invalid input: qnt not a valid float")

        print("Qnt:")
        d1_qnt_str = input()
        try:
            d1_qnt = int(d1_qnt_str)
        except ValueError:
            print("Invalid input: qnt not a valid int")

        drink_1 = drink(d1_name, d1_price, d1_qnt)

    elif choice == "2":
        drink_1.__str__

    elif choice == "3":
        drink_1.change_name
    elif choice == "4":
        drink_1.change_price
    elif choice == "5":
        drink_1.change_qnt
    
    elif choice == "6":
        menu_1.add(drink_1)

    elif choice == "7":
        menu_1.__str__
    
    elif choice == "8":
        print("Name:")
        dr_name = input()

        print("Price:")
        dr_price_str = input()
        try:
            dr_price = float(dr_price_str)
        except ValueError:
            print("Invalid input: qnt not a valid float")

        print("Qnt:")
        dr_qnt_str = input()
        try:
            dr_qnt = int(dr_qnt_str)
        except ValueError:
            print("Invalid input: qnt not a valid int")

        drink_r = drink(dr_name, dr_price, dr_qnt)
        menu_1.simple_rem(drink_r)

    elif choice == "9":
        print("1. Blackilst \n2. Whitelist")
        oper_1 = input()
        print("1. Name \n2. Price \n3. Qnt")
        oper_2 = input()
        print("Provide filtered value: ")
        filtered_value = input()
        filtered(menu_1, filtered_value, oper_1, oper_2)


    elif choice == "10":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 10.")
    

from datetime import datetime


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

    def find_index(self, other):
        for i in range(len(self.items)):
            if self.items[i] == other:
                return i

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


class customer:
    def __init__(self, username):
        self.username = username
        self.date = datetime.now()
        self.bin = []

    def __repr__(self):
        return self

    def __str__(self):
        return f'Username: {self.username} \nRegistration date: {self.date.strftime("%d.%m.%Y %H:%M")}'

    def show_bin(self, menu_used):
        if not self.bin:
            return "Bin is empty..."
        else:
            if not menu_1.items:
                return "Menu is empty..."
            else:
                bin = ""
                for i in range(len(self.bin)):
                    bin += f"{i+1}. {menu_used.items[self.bin[i][0]].name}, price: {menu_used.items[self.bin[i][0]].price}, quantity: {self.bin[i][1]} \n"
                return bin

    def change_name(self, name):
        self.username = name


class customer_list:
    def __init__(self):
        self.customers = []

    def __repr__(self):
        return self

    def __str__(self):
        customer_list_show = "customer_list:\n"
        for i in range(len(self.customers)):
            customer_list_show += f'{i+1}. {self.customers[i].username}; \n'
        return customer_list_show

    def add(self, customer):
        self.customers.append(customer)

    def find(self, other):
        for i in range(len(self.customers)):
            if self.customers[i].username == other.username:
                return True
        return False

    def find_index(self, username):
        for i in range(len(self.customers)):
            if self.customers[i].username == username:
                return i

    def check_username(self, username):
        for i in range(len(self.customers)):
            if self.customers[i].username == username:
                return True
        return False

    def simple_rem(self, cr_username):
        del self.customers[self.find_index(cr_username)]


def filtered(menu_obj, filtered_value, oper_1, oper_2):
    if oper_1 == 1:
        if oper_2 == 1:
            filtered_menu = [
                d for d in menu_obj.items if d.name != filtered_value]
        elif oper_2 == 2:
            filtered_menu = [
                d for d in menu_obj.items if d.price != filtered_value]
        else:
            filtered_menu = [
                d for d in menu_obj.items if d.qnt != filtered_value]
    else:
        if oper_2 == 1:
            filtered_menu = [
                d for d in menu_obj.items if d.name == filtered_value]
        elif oper_2 == 2:
            filtered_menu = [
                d for d in menu_obj.items if d.price == filtered_value]
        else:
            filtered_menu = [
                d for d in menu_obj.items if d.qnt == filtered_value]
    return filtered_menu


def change_item(item_to_change):
    while True:
        print("1. Change name \n2. Change price \n3. Change qnt \n4. Back")
        choice_it_chan = input()

        if choice_it_chan == "1":
            print(f"\nCurrent name: {item_to_change.name} \nProvide new name:")
            name = input()
            item_to_change.change_name(name)

        elif choice_it_chan == "2":
            while True:
                print(
                    f"\nCurrent price: {item_to_change.price} \nProvide new price:")
                try:
                    price = float(input())
                    if price >= 0:
                        break
                    else:
                        print("\nprice can't be negative\n")
                except:
                    print("\nIncorrect value\n")
            item_to_change.change_price(price)

        elif choice_it_chan == "3":
            while True:
                print(
                    f"\nCurrent qnt: {item_to_change.qnt} \nProvide new qnt:")
                try:
                    qnt = int(input())
                    if qnt >= 0:
                        break
                    else:
                        print("\nqnt can't be negative\n")
                except:
                    print("\nIncorrect value\n")
            item_to_change.change_qnt(qnt)

        elif choice_it_chan == "4":
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.\n")


def change_bin(customer_to_change, menu_used):
    while True:
        print("1. Add new item to the bin \n2. Change qnt of an item in the bin \n3. Delete item from the bin \n4. Back")
        choice_chan_bin = input()

        if choice_chan_bin == "1":
            if not menu_used.items:
                print("Menu is empty...")
            else:
                print("Choose item from the menu: ", menu_used)
                choice_it_add = input()
                try:
                    choice_it_add = int(choice_it_add)
                    if 0 < choice_it_add <= len(menu_used.items):
                        print(
                            "Selected item numer: ", menu_used.items[choice_it_add - 1], "\nProvide quantity: ")
                        it_add_qnt = input()
                        try:
                            it_add_qnt = int(it_add_qnt)
                            if 0 < it_add_qnt <= menu_used.items[choice_it_add - 1].qnt:
                                customer_to_change.bin.append(
                                    [choice_it_add - 1, it_add_qnt])
                                menu_used.items[choice_it_add -
                                                1].qnt -= it_add_qnt
                            elif 0 < it_add_qnt > menu_used.items[choice_it_add - 1].qnt:
                                print(
                                    "Quantity provided is larger then quantity of items in stock")
                            elif it_add_qnt == 0:
                                print("No items will be added to the bin")
                            else:
                                print("\nqnt can't be negative\n")
                        except ValueError:
                            print("\nInvalid input: qnt not a valid int\n")
                    else:
                        print("Incorrect item number")
                except:
                    print("Item number must be a number and must be on the menu")

        elif choice_chan_bin == "2":
            if not customer_to_change.bin:
                print("Bin is empty...")
            else:
                print(
                    f"Items currently in the bin: \n{customer_to_change.show_bin(menu_used)} \n")
                print("Quantity of what item to change? (provide item number): ")
                choice_it_bin_chan = input()
                try:
                    choice_it_bin_chan = int(choice_it_bin_chan)
                    if 0 < choice_it_bin_chan <= len(customer_to_change.bin):
                        print("Enter new quantity: ")
                        new_qnt = input()
                        try:
                            new_qnt = int(new_qnt)

                            max_qnt = menu_used.items[customer_to_change.bin[choice_it_bin_chan - 1]
                                                      [0]].qnt + customer_to_change.bin[choice_it_bin_chan - 1][1]

                            if 0 < new_qnt <= max_qnt:
                                menu_used.items[customer_to_change.bin[choice_it_bin_chan - 1][0]
                                                ].qnt += customer_to_change.bin[choice_it_bin_chan - 1][1]
                                customer_to_change.bin[choice_it_bin_chan -
                                                       1][1] = new_qnt
                                menu_used.items[customer_to_change.bin[choice_it_bin_chan - 1]
                                                [0]].qnt -= new_qnt

                            elif 0 < new_qnt > max_qnt:
                                print(
                                    "Quantity provided is larger then quantity of items in stock")

                            elif new_qnt == 0:
                                menu_used.items[customer_to_change.bin[choice_it_bin_chan - 1][0]
                                                ].qnt += customer_to_change.bin[choice_it_bin_chan - 1][1]
                                del customer_to_change.bin[choice_it_bin_chan - 1]
                                print("Item has been removed from the bin")

                            else:
                                print("\nqnt can't be negative\n")

                        except ValueError:
                            print("\nInvalid input: qnt not a valid int\n")
                    else:
                        print("There is no item under that number")
                except:
                    print("Item number must be a number and must be in the bin")

        elif choice_chan_bin == "3":
            if not customer_to_change.bin:
                print("Bin is empty...")
            else:
                print(
                    f"Items currently in the bin: \n{customer_to_change.show_bin(menu_used)} \n")
                print("What item to delete? (provide item number): ")
                choice_it_bin_del = input()
                try:
                    choice_it_bin_del = int(choice_it_bin_del)
                    if 0 < choice_it_bin_del <= len(customer_to_change.bin):
                        menu_used.items[customer_to_change.bin[choice_it_bin_del - 1][0]
                                        ].qnt += customer_to_change.bin[choice_it_bin_del - 1][1]
                        del customer_to_change.bin[choice_it_bin_del - 1]
                        print("Item has been removed from the bin")
                    else:
                        print("There is no item under that number")
                except:
                    print("Item number must be a number and must be in the bin")

        elif choice_chan_bin == "4":
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.\n")


menu_1 = menu()
print("Empty menu was created. \n")
list_1 = customer_list()
print("Empty customer list was created. \n")


def show_menu():
    print("""1. Create item 
2. Show current item 
3. Change current item 
4. Add current item to the menu 

5. Show full menu
6. Change item details on the menu 
7. Simple remove from menu 
8. Filter menu 
9. Clear menu 

10. Create customer 
11. Change current customer's username 
12. Edit current customer's bin 
13. Show current customer's details 
14. Add current customer to the list 

15. Show customer list 
16. Delete customer from the list 
17. Change customer's username on the list 
18. Edit customer's bin on the list 
19. Show customer's details on the list 
20. Clear customer list 

x. Exit \n""")


while True:
    show_menu()
    choice = input("Enter your choice (1-20 or x): ")

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
                print("\nInvalid input: price not a valid float\n")
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
        try:
            item_1
            print(f"\nCurrent item: \n{item_1}\n")
        except:
            print("There are no items created yet")

    elif choice == "3":
        try:
            item_1
            change_item(item_1)
        except:
            print("There are no items created yet")

    elif choice == "4":
        try:
            item_1
            if menu_1.find(item_1):
                print("Same exact item is already on menu")
            else:
                try:
                    menu_1.add(item_1)
                    print("\nItem was added successfully\n")
                except:
                    print("\nSomething went wrong while trying to add an item\n")
        except:
            print("There are no items created yet")

    elif choice == "5":
        if not menu_1.items:
            print("Menu is empty...")
        else:
            print(menu_1)

    elif choice == "6":
        if not menu_1.items:
            print("Menu is empty...")
        else:
            print("Name:")
            dch_name = input()

            while True:
                print("Price:")
                dch_price_str = input()
                try:
                    dch_price = float(dch_price_str)
                    if dch_price >= 0:
                        break
                    else:
                        print("\nprice can't be negative\n")
                except ValueError:
                    print("\nInvalid input: price not a valid float\n")

            while True:
                print("Qnt:")
                dch_qnt_str = input()
                try:
                    dch_qnt = int(dch_qnt_str)
                    if dch_qnt >= 0:
                        break
                    else:
                        print("\nqnt can't be negative\n")
                except ValueError:
                    print("\nInvalid input: qnt not a valid int\n")

            item_ch = item(dch_name, dch_price, dch_qnt)

            print("\nItem to change: ", item_ch)

            if menu_1.find(item_ch):
                print("\nItem found\n")
                item_ch_index = menu_1.find_index(item_ch)
                change_item(menu_1.items[item_ch_index])
            else:
                print("\nItem not found\n")

    elif choice == "7":
        if not menu_1.items:
            print("Menu is empty...")
        else:
            print("Name:")
            ir_name = input()

            while True:
                print("Price:")
                ir_price_str = input()
                try:
                    ir_price = float(ir_price_str)
                    if ir_price >= 0:
                        break
                    else:
                        print("\nprice can't be negative\n")
                except ValueError:
                    print("\nInvalid input: price not a valid float\n")

            while True:
                print("Qnt:")
                ir_qnt_str = input()
                try:
                    ir_qnt = int(ir_qnt_str)
                    if ir_qnt >= 0:
                        break
                    else:
                        print("\nqnt can't be negative\n")
                except ValueError:
                    print("\nInvalid input: qnt not a valid int\n")

            item_r = item(ir_name, ir_price, ir_qnt)

            print("\nItem to remove: ", item_r)

            if menu_1.find(item_r):
                print("\nItem found\n")
                try:
                    menu_1.simple_rem(item_r)
                    print("item deleted\n")
                except:
                    print("unable to delete\n")
            else:
                print("\nItem not found\n")

    elif choice == "8":
        if not menu_1.items:
            print("Menu is empty...")
        else:
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

    elif choice == "9":
        if not menu_1.items:
            print("Menu is empty...")
        else:
            print("\nAre you sure you want to delete all items from the menu? (y/n)")
            choice_clear = input()
            if choice_clear == "y":
                menu_1.items.clear()
                print("\nMenu was cleared")
            elif choice_clear == "n":
                print("\nMenu remains the same")
            else:
                print("\nInvalid input. Returning to main menu...\n")

    elif choice == "10":
        print("Enter username: ")
        username = input()
        try:
            customer_1 = customer(username)
            print("New customer was created.")
        except:
            print("Something went wrong while creating new customer...")

    elif choice == "11":
        try:
            customer_1
            print(
                f"Current customer's username: {customer_1.username} \nProvide new username:")
            username = input()
            customer_1.change_name(username)
        except:
            print("There are no customers created yet")

    elif choice == "12":
        try:
            customer_1
            change_bin(customer_1, menu_1)
        except:
            print("There are no customers created yet")

    elif choice == "13":
        try:
            customer_1
            print(f"\nCurrent customer: \n{customer_1}")
            print(
                f"Items currently in the bin: \n{customer_1.show_bin(menu_1)} \n")
        except:
            print("There are no customers created yet")

    elif choice == "14":
        try:
            customer_1
            if list_1.find(customer_1):
                print("Customer with this username is already on the list")
            else:
                try:
                    list_1.add(customer_1)
                    print("\nCustomer was added successfully\n")
                except:
                    print("\nSomething went wrong while trying to add an customer\n")
        except:
            print("There are no customers created yet")

    elif choice == "15":
        if not list_1.customers:
            print("List is empty...")
        else:
            print(list_1)

    elif choice == "16":
        if not list_1.customers:
            print("List is empty...")
        else:
            print("Username:")
            cr_username = input()

            print("\nCustomer to remove: ", cr_username)

            if list_1.check_username(cr_username):
                print("\nCustomer found\n")
                try:
                    list_1.simple_rem(cr_username)
                    print("Customer deleted\n")
                except:
                    print("unable to delete\n")
            else:
                print("\nCustomer not found\n")

    elif choice == "17":
        if not list_1.customers:
            print("List is empty...")
        else:
            print("Username:")
            find_chan_cus_username = input()
            if list_1.check_username(find_chan_cus_username):
                print("\nCustomer found\n")
                print("Provide new username:")
                chan_username = input()
                list_1.customers[list_1.find_index(
                    find_chan_cus_username)].change_name(chan_username)
            else:
                print("\nCustomer not found\n")

    elif choice == "18":
        if not list_1.customers:
            print("List is empty...")
        else:
            print("Username:")
            chan_bin_cus_username = input()
            if list_1.check_username(chan_bin_cus_username):
                print("\nCustomer found\n")
                change_bin(list_1.customers[list_1.find_index(
                    chan_bin_cus_username)], menu_1)
            else:
                print("\nCustomer not found\n")

    elif choice == "19":
        if not list_1.customers:
            print("List is empty...")
        else:
            print("Username:")
            show_cus_username = input()
            if list_1.check_username(show_cus_username):
                print("\nCustomer found\n")
                print(
                    list_1.customers[list_1.find_index(show_cus_username)])
                print(
                    f"Items currently in the bin: \n{list_1.customers[list_1.find_index(show_cus_username)].show_bin(menu_1)} \n")
            else:
                print("\nCustomer not found\n")

    elif choice == "20":
        if not list_1.customers:
            print("List is empty...")
        else:
            print("\nAre you sure you want to delete all customers from the list? (y/n)")
            choice_clear = input()
            if choice_clear == "y":
                list_1.customers.clear()
                print("\nList was cleared")
            elif choice_clear == "n":
                print("\nList remains the same")
            else:
                print("\nInvalid input. Returning to main menu...\n")

    elif choice == "x":
        print("\nExiting the program. Goodbye!\n")
        break
    else:
        print("\nInvalid choice. Please enter a number between 1 and 20 or x.\n")

from datetime import datetime
import sqlite3

conn = sqlite3.connect('tavern.db')
cursor = conn.cursor()

ctq_menu = '''
CREATE TABLE IF NOT EXISTS menu (
    item_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL,
    qnt INTEGER
);
'''
cursor.execute(ctq_menu)

ctq_customer_list = '''
CREATE TABLE IF NOT EXISTS customer_list (
    customer_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    date REAL
);
'''
cursor.execute(ctq_customer_list)

ctq_bin = '''
CREATE TABLE IF NOT EXISTS bin (
    bin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    qnt INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer_list(customer_id),
    FOREIGN KEY (item_id) REFERENCES menu(item_id)
);
'''
cursor.execute(ctq_bin)

conn.commit()


class db:
    @staticmethod
    def isEmpty(table_name):
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        if count == 0:
            print(f"The table '{table_name}' is empty.")
            return True
        else:
            print(
                f"The table '{table_name}' is not empty. It contains {count} record(s).")
            return False

    @staticmethod
    def deleteAllRecords(table_name):
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()


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

    @staticmethod
    def fetch_menu():
        fetch_menu_query = "SELECT * FROM menu;"
        cursor.execute(fetch_menu_query)
        fetched = cursor.fetchall()
        menu_fetched = menu()
        for i in range(len(fetched)):
            menu_fetched.add(item(fetched[i][1], fetched[i][2], fetched[i][3]))
        return menu_fetched

    @staticmethod
    def addItem(name, price, qnt):
        insert_item_query = "INSERT INTO menu (name, price, qnt) VALUES (?, ?, ?);"
        item_data = (name, price, qnt)
        cursor.execute(insert_item_query, item_data)
        conn.commit()

    @staticmethod
    def updateItem(item_id, name, price, qnt):
        update_item_query = "UPDATE menu SET name = ?, price = ?, qnt = ? WHERE item_id = ?;"
        item_data = (name, price, qnt, item_id)
        cursor.execute(update_item_query, item_data)
        conn.commit()

    @staticmethod
    def removeItem(item_id):
        delete_item_query = "DELETE FROM menu WHERE item_id = ?;"
        item_data = (item_id,)
        cursor.execute(delete_item_query, item_data)
        conn.commit()

    def add(self, item):
        self.items.append(item)

    @staticmethod
    def findItemName(name):
        find_item_query = "SELECT * FROM menu WHERE name = ?;"
        item_data = (name,)
        cursor.execute(find_item_query, item_data)
        found = cursor.fetchall()
        return found

    @staticmethod
    def findItemId(item_id):
        find_item_query = "SELECT * FROM menu WHERE item_id = ?;"
        item_data = (item_id,)
        cursor.execute(find_item_query, item_data)
        found = cursor.fetchall()
        return found


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
    def __init__(self, username, date):
        self.username = username
        self.date = date
        self.bin = []

    def __repr__(self):
        return self

    def __str__(self):
        return f'Username: {self.username} \nRegistration date: {datetime.fromtimestamp(self.date).strftime("%d.%m.%Y %H:%M")}'

    @staticmethod
    def addBin(customer_id, item_id, qnt):
        insert_bin_query = "INSERT INTO bin (customer_id, item_id, qnt) VALUES (?, ?, ?);"
        bin_data = (customer_id, item_id, qnt)
        cursor.execute(insert_bin_query, bin_data)
        conn.commit()

    @staticmethod
    def checkBin(customer_id):
        find_customer_query = "SELECT * FROM bin WHERE customer_id = ?;"
        customer_data = (customer_id,)
        cursor.execute(find_customer_query, customer_data)
        found = cursor.fetchall()
        return found

    @staticmethod
    def show_bin_db(customer_id):
        customer_bin = customer.checkBin(customer_id)
        if not customer_bin:
            return "Bin is empty..."
        else:
            cus_bin_text = ""
            menu_used = menu.fetch_menu()
            if not menu_used.items:
                return "Menu is empty..."
            else:
                for i in range(len(customer_bin)):
                    cus_bin_text += f"{i+1}. {menu_used.items[customer_bin[i][2] - 1].name}, price: {menu_used.items[customer_bin[i][2] - 1].price}, quantity: {customer_bin[i][3]} \n"
                return cus_bin_text

    def change_name(self, name):
        self.username = name


class customer_list:
    def __init__(self):
        self.customers = []

    def __repr__(self):
        return self

    def __str__(self):
        customer_list_show = "Customer list:\n"
        for i in range(len(self.customers)):
            customer_list_show += f'{i+1}. {self.customers[i].username}; \n'
        return customer_list_show

    @staticmethod
    def fetch_customer_list():
        fetch_customer_list_query = "SELECT * FROM customer_list;"
        cursor.execute(fetch_customer_list_query)
        fetched = cursor.fetchall()
        list_fetched = customer_list()
        for i in range(len(fetched)):
            list_fetched.add(customer(fetched[i][1], fetched[i][2]))
        return list_fetched

    @staticmethod
    def addCustomer(username, date):
        insert_customer_query = "INSERT INTO customer_list (username, date) VALUES (?, ?);"
        customer_data = (username, date)
        cursor.execute(insert_customer_query, customer_data)
        conn.commit()

    def add(self, customer):
        self.customers.append(customer)

    @staticmethod
    def findCustomerName(username):
        find_customer_query = "SELECT * FROM customer_list WHERE username = ?;"
        customer_data = (username,)
        cursor.execute(find_customer_query, customer_data)
        found = cursor.fetchall()
        return found


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


def change_bin_db(customer_id):
    while True:
        print("1. Add new item to the bin \n2. Change qnt of an item in the bin \n3. Delete item from the bin \n4. Back")
        choice_chan_bin = input()

        if choice_chan_bin == "1":

            print("Choose item from the menu: ")
            menu_used = menu.fetch_menu()
            print(menu_used)
            choice_it_add = input()

            try:
                choice_it_add = int(choice_it_add)
                item_add = menu.findItemId(choice_it_add)

                if item_add:
                    print("Provide quantity: ")
                    it_add_qnt = input()

                    try:
                        it_add_qnt = int(it_add_qnt)
                        if 0 < it_add_qnt <= item_add[0][3]:

                            customer.addBin(
                                customer_id, item_add[0][0], it_add_qnt)

                            cursor.execute(
                                f"UPDATE menu SET qnt = qnt - {it_add_qnt} WHERE item_id = {item_add[0][0]}")
                            conn.commit()

                        elif 0 < it_add_qnt > item_add[0][3]:
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

            customer_bin = customer.checkBin(customer_id)
            if not customer_bin:
                print("Bin is empty...")
            else:

                print(
                    f"Items currently in the bin: \n{customer.show_bin_db(customer_id)} \n")
                print("Quantity of what item to change? (provide item number): ")
                choice_it_bin_chan = input()
                choice_it_bin_chan = int(choice_it_bin_chan)
                choice_it_bin_chan -= 1

                try:
                    if 0 <= choice_it_bin_chan <= len(customer_bin):

                        print("Enter new quantity: ")
                        new_qnt = input()
                        try:
                            new_qnt = int(new_qnt)

                            menu_used = menu.fetch_menu()
                            max_qnt = menu_used.items[customer_bin[choice_it_bin_chan]
                                                      [2]].qnt + customer_bin[choice_it_bin_chan][3]

                            if 0 < new_qnt <= max_qnt:

                                update_qnt_add_query = "UPDATE menu SET qnt = qnt + ? WHERE item_id = ?"
                                update_qnt_add_data = (
                                    customer_bin[choice_it_bin_chan][3], customer_bin[choice_it_bin_chan][2])
                                cursor.execute(
                                    update_qnt_add_query, update_qnt_add_data)
                                conn.commit()

                                update_qnt_bin_query = "UPDATE bin SET qnt = ? WHERE bin_id = ?"
                                update_qnt_bin_data = (
                                    new_qnt, customer_bin[choice_it_bin_chan][0])
                                cursor.execute(
                                    update_qnt_bin_query, update_qnt_bin_data)
                                conn.commit()

                                update_qnt_subtract_query = "UPDATE menu SET qnt = qnt - ? WHERE item_id = ?"
                                update_qnt_subtract_data = (
                                    new_qnt, customer_bin[choice_it_bin_chan][2])
                                cursor.execute(
                                    update_qnt_subtract_query, update_qnt_subtract_data)
                                conn.commit()
                                conn.commit()

                            elif 0 < new_qnt > max_qnt:
                                print(
                                    "Quantity provided is larger then quantity of items in stock")

                            elif new_qnt == 0:

                                update_qnt_add_query = "UPDATE menu SET qnt = qnt + ? WHERE item_id = ?"
                                update_qnt_add_data = (
                                    customer_bin[choice_it_bin_chan][3], customer_bin[choice_it_bin_chan][2])
                                cursor.execute(
                                    update_qnt_add_query, update_qnt_add_data)
                                conn.commit()

                                delete_from_bin_query = "DELETE FROM bin WHERE bin_id = ?"
                                delete_from_bin_data = (
                                    customer_bin[choice_it_bin_chan][0],)
                                cursor.execute(
                                    delete_from_bin_query, delete_from_bin_data)
                                conn.commit()

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

            customer_bin = customer.checkBin(customer_id)
            if not customer_bin:
                print("Bin is empty...")
            else:

                print(
                    f"Items currently in the bin: \n{customer.show_bin_db(customer_id)} \n")
                print("What item to delete? (provide item number): ")
                choice_it_bin_del = input()

                try:
                    choice_it_bin_del = int(choice_it_bin_del)
                    choice_it_bin_del -= 1

                    if 0 <= choice_it_bin_del <= len(customer_bin):

                        update_qnt_add_query = "UPDATE menu SET qnt = qnt + ? WHERE item_id = ?"
                        update_qnt_add_data = (
                            customer_bin[choice_it_bin_del][3], customer_bin[choice_it_bin_del][2])
                        cursor.execute(update_qnt_add_query,
                                       update_qnt_add_data)
                        conn.commit()

                        delete_from_bin_query = "DELETE FROM bin WHERE bin_id = ?"
                        delete_from_bin_data = (
                            customer_bin[choice_it_bin_del][0],)
                        cursor.execute(delete_from_bin_query,
                                       delete_from_bin_data)
                        conn.commit()

                        print("Item has been removed from the bin")

                    else:
                        print("There is no item under that number")
                except:
                    print("Item number must be a number and must be in the bin")

        elif choice_chan_bin == "4":
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.\n")


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
12. Show current customer's details 
13. Add current customer to the list 

14. Show customer list 
15. Delete customer from the list 
16. Change customer's username on the list 
17. Edit customer's bin on the list 
18. Show customer's details on the list 
19. Clear customer list 

x. Exit \n""")


while True:
    show_menu()
    choice = input("Enter your choice (1-19 or x): ")

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
            if menu.findItemName(item_1.name):
                print("Item with the same name is already on the menu")
            else:
                try:
                    menu.addItem(item_1.name, item_1.price, item_1.qnt)
                    print("\nItem was added successfully\n")
                except:
                    print("\nSomething went wrong while trying to add an item\n")
        except NameError:
            print("There are no items created yet")

    elif choice == "5":
        try:
            menu_1 = menu.fetch_menu()
            print("Menu was loaded.")
        except:
            print("Unable to load the menu.")
        if not menu_1.items:
            print("Menu is empty...")
        else:
            print(menu_1)

    elif choice == "6":
        if db.isEmpty("menu"):
            print("Menu is empty...")
        else:
            print("Name:")
            ich_name = input()

            item_f = menu.findItemName(ich_name)
            if item_f:
                print("\nItem found\n")
                item_2 = item(item_f[0][1], item_f[0][2], item_f[0][3])
                change_item(item_2)
                try:
                    menu.updateItem(
                        item_f[0][0], item_2.name, item_2.price, item_2.qnt)
                    print("\nItem was updated successfully\n")
                except:
                    print("\nSomething went wrong while trying to update an item\n")
            else:
                print("\nItem not found\n")

    elif choice == "7":
        if db.isEmpty("menu"):
            print("Menu is empty...")
        else:
            print("Name:")
            ir_name = input()

            item_f = menu.findItemName(ir_name)
            if item_f:
                print("\nItem found\n")
                try:
                    menu.removeItem(item_f[0][0])
                    print("\nItem was removed successfully\n")

                    try:
                        cursor.execute(
                            f"DELETE FROM bin WHERE item_id = {item_f[0][0]};")
                        conn.commit()
                        print("\nCorresponding records were removed form the bin.\n")
                    except:
                        print("\nNo items were removed from the bin.")

                except:
                    print("\nSomething went wrong while trying to remove an item\n")
            else:
                print("\nItem not found\n")

    elif choice == "8":
        try:
            menu_1 = menu.fetch_menu()
            print("Menu was loaded.")
        except:
            print("Unable to load the menu.")

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

            if oper_2 == 1:
                print("Provide filtered value (Name): ")
                filtered_value = input()

            elif oper_2 == 2:
                while True:
                    print("Provide filtered value (Price): ")
                    filtered_value = input()
                    try:
                        filtered_value = float(filtered_value)
                        if filtered_value >= 0:
                            break
                        else:
                            print("\nprice can't be negative\n")
                    except ValueError:
                        print("\nInvalid input: price not a valid float\n")

            elif oper_2 == 3:
                while True:
                    print("Provide filtered value (Qnt): ")
                    filtered_value = input()
                    try:
                        filtered_value = int(filtered_value)
                        if filtered_value >= 0:
                            break
                        else:
                            print("\nqnt can't be negative\n")
                    except ValueError:
                        print("\nInvalid input: qnt not a valid int\n")

            else:
                print("\nIncorrect operation 2 value\n")

            filtered_menu = filtered(menu_1, filtered_value, oper_1, oper_2)
            for i in range(len(filtered_menu)):
                print(filtered_menu[i])

    elif choice == "9":
        if db.isEmpty("menu"):
            print("Menu is empty...")
        else:
            print("\nAre you sure you want to delete all items from the menu? (y/n)")
            choice_clear = input()
            if choice_clear == "y":
                db.deleteAllRecords("bin")
                print("\nBin was cleared")
                db.deleteAllRecords("menu")
                print("\nMenu was cleared")
            elif choice_clear == "n":
                print("\nMenu remains the same")
            else:
                print("\nInvalid input. Returning to main menu...\n")

    elif choice == "10":
        print("Enter username: ")
        username = input()
        try:
            customer_1 = customer(username, datetime.now().timestamp())
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
            print(f"\nCurrent customer: \n{customer_1}")

        except:
            print("There are no customers created yet")

    elif choice == "13":
        try:
            if customer_list.findCustomerName(customer_1.username):
                print("Customer with this username is already on the list")
            else:
                try:
                    customer_list.addCustomer(
                        customer_1.username, customer_1.date)

                    print("\nCustomer was added successfully\n")
                except:
                    print("\nSomething went wrong while trying to add an customer\n")
        except NameError:
            print("There are no customers created yet")

    elif choice == "14":
        try:
            list_1 = customer_list.fetch_customer_list()
            print("Customer list was loaded.")
        except:
            print("Unable to load load customer list.")
        if not list_1.customers:
            print("List is empty...")
        else:
            print(list_1)

    elif choice == "15":
        if db.isEmpty("customer_list"):
            print("List is empty...")
        else:
            print("Username:")
            cr_username = input()
            try:
                cr = customer_list.findCustomerName(cr_username)
                print("Customer found.")
                try:
                    cursor.execute(
                        f"DELETE FROM bin WHERE customer_id = {cr[0][0]};")
                    conn.commit()
                    print("Customer's bin deleted")
                except:
                    print("Customer's bin is empty")
                try:
                    cursor.execute(
                        f"DELETE FROM customer_list WHERE customer_id = {cr[0][0]};")
                    conn.commit()
                    print("Customer deleted\n")
                except:
                    print("Error: can't delete\n")
            except:
                print("Customer not found\n")

    elif choice == "16":
        if db.isEmpty("customer_list"):
            print("List is empty...")
        else:
            print("Username:")
            find_chan_cus_username = input()
            print("Provide new username:")
            chan_username = input()
            try:
                find_chan_cus = customer_list.findCustomerName(
                    find_chan_cus_username)
                print("Customer found.")
                try:
                    chan_cus_query = "UPDATE customer_list SET username = ? WHERE customer_id = ?"
                    chan_cus_data = (chan_username, find_chan_cus[0][0])
                    cursor.execute(chan_cus_query, chan_cus_data)
                    conn.commit()
                except:
                    print("\nError: unable to update.\n")
            except:
                print("Customer not found\n")

    elif choice == "17":
        if db.isEmpty("customer_list"):
            print("List is empty...")
        else:
            print("Username:")
            chan_bin_cus_username = input()
            chan_bin_cus = customer_list.findCustomerName(
                chan_bin_cus_username)
            if chan_bin_cus:
                print("\nCustomer found\n")
                change_bin_db(chan_bin_cus[0][0])
            else:
                print("\nCustomer not found\n")

    elif choice == "18":
        if db.isEmpty("customer_list"):
            print("List is empty...")
        else:
            print("Username:")
            show_cus_username = input()
            try:
                show_cus = customer_list.findCustomerName(show_cus_username)
                print(
                    f'Username: {show_cus[0][1]} \nRegistration date: {datetime.fromtimestamp(show_cus[0][2]).strftime("%d.%m.%Y %H:%M")}')
                print(
                    f"Items currently in the bin: \n{customer.show_bin_db(show_cus[0][0])} \n")
            except:
                print("\nCustomer not found\n")

    elif choice == "19":
        if db.isEmpty("customer_list"):
            print("List is empty...")
        else:
            print("\nAre you sure you want to delete all customers from the list? (y/n)")
            choice_clear = input()
            if choice_clear == "y":

                fetch_bin_query = "SELECT * FROM bin;"
                cursor.execute(fetch_bin_query)
                fetched_bin = cursor.fetchall()
                for i in range(len(fetched_bin)):
                    update_qnt_add_query = "UPDATE menu SET qnt = qnt + ? WHERE item_id = ?"
                    update_qnt_add_data = (
                        fetched_bin[i][3], fetched_bin[i][2])
                    cursor.execute(update_qnt_add_query, update_qnt_add_data)
                    conn.commit()

                db.deleteAllRecords("bin")
                print("\nBin was cleared")
                db.deleteAllRecords("customer_list")
                print("\nCustomer list was cleared")
            elif choice_clear == "n":
                print("\nList remains the same")
            else:
                print("\nInvalid input. Returning to main menu...\n")

    elif choice == "x":
        print("\nExiting the program. Goodbye!\n")
        break
    else:
        print("\nInvalid choice. Please enter a number between 1 and 19 or x.\n")

try:
    cursor.close()
    conn.close()
    print("Connection to database closed successfully.")
except:
    print("Closing connection to database failed.")

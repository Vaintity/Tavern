
class menu:
    @staticmethod
    def findItemId(item_id):
        find_item_query = "SELECT * FROM menu WHERE item_id = ?;"
        item_data = (item_id,)
        cursor.execute(find_item_query, item_data)
        found = cursor.fetchall()
        return found


class customer:
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
                    cus_bin_text += f"{i+1}. {menu_used.items[customer_bin[i][2]].name}, price: {menu_used.items[customer_bin[i][2]].price}, quantity: {customer_bin[i][3]} \n"
                return cus_bin_text


def change_bin(customer_id):
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
                choice_it_add -= 1
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

                try:
                    choice_it_bin_chan = int(choice_it_bin_chan)
                    choice_it_bin_chan -= 1
                    if 0 < choice_it_bin_chan <= len(customer_bin):

                        print("Enter new quantity: ")
                        new_qnt = input()
                        try:
                            new_qnt = int(new_qnt)

                            menu_used = menu.fetch_menu()
                            max_qnt = menu_used.items[customer_id.bin[choice_it_bin_chan]
                                                      [2]].qnt + customer_bin[choice_it_bin_chan][3]

                            if 0 < new_qnt <= max_qnt:

                                cursor.execute(
                                    f"UPDATE menu SET qnt = qnt + {customer_bin[choice_it_bin_chan][3]} WHERE item_id = {customer_bin[choice_it_bin_chan][2]}")

                                cursor.execute(
                                    f"UPDATE bin SET qnt = {new_qnt} WHERE bin_id = {customer_bin[choice_it_bin_chan][0]}")

                                cursor.execute(
                                    f"UPDATE menu SET qnt = qnt - {new_qnt} WHERE item_id = {customer_bin[choice_it_bin_chan][2]}")

                                conn.commit()

                            elif 0 < new_qnt > max_qnt:
                                print(
                                    "Quantity provided is larger then quantity of items in stock")

                            elif new_qnt == 0:

                                cursor.execute(
                                    f"UPDATE menu SET qnt = qnt + {customer_bin[choice_it_bin_chan][3]} WHERE item_id = {customer_bin[choice_it_bin_chan][2]}")

                                cursor.execute(
                                    f"DELETE FROM bin WHERE bin_id = {customer_bin[choice_it_bin_chan][0]}")

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

                    if 0 < choice_it_bin_del <= len(customer_bin):

                        cursor.execute(
                            f"UPDATE menu SET qnt = qnt + {customer_bin[choice_it_bin_del][3]} WHERE item_id = {customer_bin[choice_it_bin_del][2]}")

                        cursor.execute(
                            f"DELETE FROM bin WHERE bin_id = {customer_bin[choice_it_bin_del][0]}")

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



'''
    elif choice == "17":
        if db.isEmpty("customer_list"):
            print("List is empty...")
        else:
            print("Username:")
            find_chan_cus_username = input()
            find_chan_cus = customer_list.findCustomerName(find_chan_cus_username)
            if find_chan_cus:
                print("\nCustomer found\n")
                print("Provide new username:")
                chan_username = input()
                cursor.execute(f"UPDATE customer_list SET username = {chan_username} WHERE customer_id = {find_chan_cus[0][0]}")

                list_1.customers[list_1.find_index(
                    find_chan_cus_username)].change_name(chan_username)
            else:
                print("\nCustomer not found\n")
    '''

'''

def change_bin(customer_to_change):
    menu_used = menu.fetch_menu()
    if not menu_used.items:
        return "Menu is empty..."
    else:
        while True:
            print("1. Add new item to the bin \n2. Change qnt of an item in the bin \n3. Delete item from the bin \n4. Back")
            choice_chan_bin = input()

            if choice_chan_bin == "1":
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
                        f"Items currently in the bin: \n{customer_to_change.show_bin()} \n")
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
                        f"Items currently in the bin: \n{customer_to_change.show_bin()} \n")
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
'''


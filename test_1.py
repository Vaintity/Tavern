choice = 0
customer_1 = 0
list_1 = []
menu_1 = []
def change_bin():
    return 0
if False:
    pass


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
            if not menu_1.items:
                print("Menu is empty...")
            else:
                change_bin(list_1.customers[list_1.find_index(chan_bin_cus_username)], menu_1)
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
            if not menu_1.items:
                print("Menu is empty...")
            else:
                print(f"\nCurrent customer: \n{show_cus_username}")
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

else:
    pass

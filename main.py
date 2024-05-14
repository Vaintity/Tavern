from datetime import datetime
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStatusBar, QTextEdit, QFileDialog,
                             QLabel, QWidget, QHBoxLayout, QPushButton, QLineEdit,
                             QRadioButton, QGridLayout, QFormLayout, QAction, QDialog,
                             QMenuBar, QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QMessageBox, QListWidget, QComboBox, QCheckBox)
from PyQt5.QtCore import Qt
import sys
import sqlite3
import requests
import re

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

ctq_bin_external = '''
CREATE TABLE IF NOT EXISTS bin_external (
    bin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    qnt INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer_list(customer_id)
);
'''
cursor.execute(ctq_bin_external)

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


class api(ABC):
    @abstractmethod
    def get_game(param, value):
        link_game = "https://www.cheapshark.com/api/1.0/games"

        if param == 1:
            response = requests.get(link_game, params={"title": value})
        elif param == 2:
            response = requests.get(link_game, params={"steamAppID": value})
        else:
            print("Incorrect param")

        if response.status_code == 200:
            games = response.json()
            for game in games:
                game_title = game.get('external', 'No title provided')
                game_id = game.get('gameID', 'No ID provided')
                steamApp_id = game.get('steamAppID', 'No ID provided')
                print(
                    f"Title: {game_title}, Game ID: {game_id}, SteamAppID: {steamApp_id}")
        else:
            print(f"Failed to fetch data: {response.status_code}, 'N/A'")

    @abstractmethod
    def game_id_check(value):
        link_game = "https://www.cheapshark.com/api/1.0/games"
        response = requests.get(link_game, params={"id": value})
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return False

    @abstractmethod
    def game_id_show(value):
        link_game = "https://www.cheapshark.com/api/1.0/games"
        response = requests.get(link_game, params={"id": value})
        if response.status_code == 200:
            data = response.json()
            title = data['info']['title']
            steamAppID = data['info']['steamAppID']
            cheapest_price = data['cheapestPriceEver']['price']
            cheapest_date = data['cheapestPriceEver']['date']
            print("Game Title:", title)
            print("Steam App ID:", steamAppID)
            print("Cheapest Price Ever:", cheapest_price)
            print("Date of Cheapest Price:", cheapest_date)
            print("\nDeals:")
            for deal in data['deals']:
                print(
                    f"Store: {api.get_store(deal['storeID'])[0]}, Price: {deal['price']}, Savings: {deal['savings']}")
        else:
            print(f"Failed to fetch data: {response.status_code}, 'N/A'")

    @abstractmethod
    def get_store(store_id=None):
        if store_id != None:
            link_store = "https://www.cheapshark.com/api/1.0/stores"
            response_store = requests.get(
                link_store, params={"storeID": store_id})
            if response_store.status_code == 200:
                stores = response_store.json()
                for store in stores:
                    if str(store.get('storeID')) == str(store_id):
                        store_name = store.get('storeName', 'No name provided')
                        store_active = store.get(
                            'isActive', 'No status provided')
                        return [store_name, store_active]
                return ['Store not found', 'N/A']
            else:
                return [f"Failed to fetch data: {response_store.status_code}", 'N/A']
        else:
            link_store = "https://www.cheapshark.com/api/1.0/stores"
            response_store = requests.get(link_store)
            if response_store.status_code == 200:
                stores = response_store.json()
                store_list = []
                for store in stores:
                    store_name = store.get('storeName', 'No name provided')
                    store_active = store.get('isActive', 'No status provided')
                    store_list.append([store_name, store_active])
                return store_list
            else:
                return [f"Failed to fetch data: {response_store.status_code}", 'N/A']

    @abstractmethod
    def get_deal(param, sale_check, value):
        link_deal = "https://www.cheapshark.com/api/1.0/deals"

        if param == 1:
            if sale_check == 1:
                response = requests.get(link_deal, params={"title": value, "onSale": "1"})
            else:
                response = requests.get(link_deal, params={"title": value})
        elif param == 2:
            if sale_check == 1:
                response = requests.get(link_deal, params={"upperPrice": value, "onSale": "1"})
            else:
                response = requests.get(link_deal, params={"upperPrice": value})
        elif param == 3:
            if sale_check == 1:
                response = requests.get(link_deal, params={"lowerPrice": value, "onSale": "1"})
            else:
                response = requests.get(link_deal, params={"lowerPrice": value})
        elif param == 4:
            if sale_check == 1:
                response = requests.get(link_deal, params={"onSale": "1"})
            else:
                response = requests.get(link_deal)
        else:
            print("Incorrect param")

        if response.status_code == 200:
            deals = response.json()
            return deals
        else:
            print(f"Failed to fetch data: {response.status_code}, 'N/A'")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tavern Management System")
        self.setGeometry(100, 100, 800, 600)

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.menu_management_tab = MenuManagement()
        self.customer_management_tab = CustomerManagement()
        self.api_interaction_tab = APIInteraction()

        self.tab_widget.addTab(self.menu_management_tab, "Menu Management")
        self.tab_widget.addTab(
            self.customer_management_tab, "Customer Management")
        self.tab_widget.addTab(self.api_interaction_tab, "API Interactions")

        self.tab_widget.currentChanged.connect(self.onTabChange)

    def onTabChange(self, index):
        if index == 0:
            self.menu_management_tab.load_menu_items()
        elif index == 1:
            self.customer_management_tab.load_customers()
        elif index == 2:
            self.api_interaction_tab.update_store_list()

    def closeEvent(self, event):
        try:
            cursor.close()
            conn.close()
            print("Cursor and connection closed successfully")
        except:
            print("Something went wrong while closing cursor and connection")
        event.accept()


class MenuManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Item ID", "Name", "Price", "Quantity"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.load_menu_items()

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Enter item name to find")
        self.search_field.textChanged.connect(self.find_item)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_field)

        self.add_button = QPushButton("Add Item")
        self.edit_button = QPushButton("Edit Item")
        self.delete_button = QPushButton("Delete Item")

        self.add_button.clicked.connect(self.add_item)
        self.edit_button.clicked.connect(self.edit_item)
        self.delete_button.clicked.connect(self.delete_item)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_menu_items(self):
        cursor.execute("SELECT * FROM menu;")
        fetched = cursor.fetchall()
        self.populate_table_data(fetched)

    def find_item(self):
        search_term = self.search_field.text().strip().lower()
        if not search_term:
            cursor.execute("SELECT * FROM menu;")
        else:
            cursor.execute("SELECT * FROM menu WHERE LOWER(name) LIKE ?", ('%' + search_term + '%',))

        fetched = cursor.fetchall()
        self.populate_table_data(fetched)

    def populate_table_data(self, data):
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j in range(len(row)):
                self.table.setItem(i, j, QTableWidgetItem(str(row[j])))

    def add_item(self):
        dialog = ItemDialog()
        if dialog.exec() == QDialog.Accepted:
            item_data = dialog.get_data()
            name = item_data['name']
            price = item_data['price']
            quantity = item_data['quantity']
            if name and price and quantity:
                try:
                    price = float(price)
                    quantity = int(quantity)
                    if price >= 0 and quantity >= 0:
                        if menu.findItemName(name):
                            QMessageBox.warning(
                                self, "Invalid Input", "Item with the same name is already on the menu.")
                        else:
                            menu.addItem(name, price, quantity)
                            self.load_menu_items()
                    else:
                        QMessageBox.warning(
                            self, "Invalid Input", "Price and quantity must be non-negative.")
                except ValueError as e:
                    QMessageBox.warning(
                        self, "Invalid Input", "Price and quantity need to be numeric.")
            else:
                QMessageBox.warning(self, "Invalid Input",
                                    "All fields are required.")

    def edit_item(self):
        row = self.table.currentRow()
        if row != -1:
            item_id = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            price = self.table.item(row, 2).text()
            quantity = self.table.item(row, 3).text()

            dialog = ItemDialog(item_id, name, price, quantity)
            if dialog.exec() == QDialog.Accepted:
                item_data = dialog.get_data()
                name = item_data['name']
                price = item_data['price']
                quantity = item_data['quantity']
                if name and price and quantity:
                    try:
                        price = float(price)
                        quantity = int(quantity)
                        if price >= 0 and quantity >= 0:
                            menu.updateItem(item_id, name, price, quantity)
                            self.load_menu_items()
                        else:
                            QMessageBox.warning(
                                self, "Invalid Input", "Price and quantity must be non-negative.")
                    except ValueError as e:
                        QMessageBox.warning(
                            self, "Invalid Input", "Price and quantity need to be numeric.")
                else:
                    QMessageBox.warning(
                        self, "Invalid Input", "All fields are required.")
        else:
            QMessageBox.warning(self, "Selection Required",
                                "Please select an item to edit.")

    def delete_item(self):
        row = self.table.currentRow()
        if row != -1:
            item_id = self.table.item(row, 0).text()
            response = QMessageBox.question(self, 'Confirm Deletion',
                                            "Are you sure you want to delete this item?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if response == QMessageBox.Yes:
                try:
                    menu.removeItem(item_id)
                    self.load_menu_items()
                    QMessageBox.information(
                        self, "Success", "Item has been deleted successfully.")
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"Failed to delete item: {str(e)}")
            else:
                QMessageBox.information(
                    self, "Cancelled", "Item deletion cancelled.")
        else:
            QMessageBox.warning(self, "Selection Required",
                                "Please select an item to delete.")


class ItemDialog(QDialog):
    def __init__(self, item_id=None, name="", price="", qnt="", parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Item Details")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(name)
        self.price_edit = QLineEdit(price)
        self.qnt_edit = QLineEdit(qnt)

        self.layout.addRow(QLabel("Name:"), self.name_edit)
        self.layout.addRow(QLabel("Price:"), self.price_edit)
        self.layout.addRow(QLabel("Quantity:"), self.qnt_edit)

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        self.layout.addRow(button_layout)

    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "price": self.price_edit.text(),
            "quantity": self.qnt_edit.text()
        }


class CustomerManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Customer ID", "Username", "Registration Date", "Edit Bin"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.load_customers()

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Enter customer username to find")
        self.search_field.textChanged.connect(self.find_customer)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_field)

        self.add_button = QPushButton("Add Customer")
        self.edit_button = QPushButton("Edit Customer")
        self.delete_button = QPushButton("Delete Customer")

        self.add_button.clicked.connect(self.add_customer)
        self.edit_button.clicked.connect(self.edit_customer)
        self.delete_button.clicked.connect(self.delete_customer)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_customers(self):
        cursor.execute("SELECT * FROM customer_list;")
        fetched = cursor.fetchall()
        self.populate_customer_table_data(fetched)

    def find_customer(self):
        search_term = self.search_field.text().strip().lower()
        if not search_term:
            cursor.execute("SELECT * FROM customer_list;")
        else:
            cursor.execute("SELECT * FROM customer_list WHERE LOWER(username) LIKE ?", ('%' + search_term + '%',))

        fetched = cursor.fetchall()
        self.populate_customer_table_data(fetched)

    def populate_customer_table_data(self, data):
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(row[1]))
            self.table.setItem(i, 2, QTableWidgetItem(
                str(datetime.fromtimestamp(row[2]).strftime("%d.%m.%Y %H:%M"))))
            cell_widget = ButtonCell()
            cell_widget.edit_bin_button.clicked.connect(
                lambda _, cid=row[0]: self.open_bin_editor(cid))
            self.table.setCellWidget(i, 3, cell_widget)

    def open_bin_editor(self, customer_id):
        bin_window = BinEditWindow(customer_id)
        bin_window.exec()

    def add_customer(self):
        dialog = CustomerDialog()
        if dialog.exec() == QDialog.Accepted:
            customer_data = dialog.get_data()
            username = customer_data["username"].replace(" ", "")
            registration_date = datetime.now().timestamp()
            if username:
                if customer_list.find_customer_by_username(username):
                    QMessageBox.warning(
                        self, "Invalid Input", "Customer with the same username is already on the list.")
                else:
                    customer_list.addCustomer(username, registration_date)
                    self.load_customers()

    def edit_customer(self):
        row = self.table.currentRow()
        if row != -1:
            customer_id = self.table.item(row, 0).text()
            username = self.table.item(row, 1).text()
            registration_date = self.table.item(row, 2).text()

            dialog = CustomerDialog(customer_id, username, registration_date)
            if dialog.exec() == QDialog.Accepted:
                customer_data = dialog.get_data()
                username = customer_data['username']
                if username:
                    customer_list.updateCustomer(customer_id, username)
                    self.load_customers()
                else:
                    QMessageBox.warning(
                        self, "Invalid Input", "All fields are required.")
        else:
            QMessageBox.warning(self, "Selection Required",
                                "Please select an item to edit.")

    def delete_customer(self):
        row = self.table.currentRow()
        if row != -1:
            customer_id = self.table.item(row, 0).text()
            response = QMessageBox.question(self, 'Confirm Deletion',
                                            "Are you sure you want to delete this customer?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if response == QMessageBox.Yes:
                try:
                    customer_list.deleteCustomer(customer_id)
                    self.load_customers()
                    QMessageBox.information(
                        self, "Success", "Customer has been deleted successfully.")
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"Failed to delete customer: {str(e)}")
            else:
                QMessageBox.information(
                    self, "Cancelled", "Customer deletion cancelled.")
        else:
            QMessageBox.warning(self, "Selection Required",
                                "Please select a customer to delete.")


class CustomerDialog(QDialog):
    def __init__(self, customer_id=None, username="", registration_date="", parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Customer Details")
        self.layout = QFormLayout(self)

        self.username_edit = QLineEdit(username)
        self.layout.addRow(QLabel("Username:"), self.username_edit)

        if customer_id:
            registration_date_label = QLabel(registration_date)
            self.layout.addRow("Registration Date:", registration_date_label)

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        self.layout.addRow(button_layout)

    def get_data(self):
        return {
            "username": self.username_edit.text()
        }


class ButtonCell(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.edit_bin_button = QPushButton("Edit Bin")
        self.edit_bin_button.setFixedSize(80, 25)
        layout.addWidget(self.edit_bin_button, alignment=Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)


class BinEditWindow(QDialog):
    def __init__(self, customer_id):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)
        self.customer_id = customer_id
        self.setWindowTitle("Edit Customer Bin")
        self.setGeometry(100, 100, 800, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.local_bin_tab = QWidget()
        self.external_bin_tab = QWidget()
        self.local_bin_table = QTableWidget()
        self.exteranl_bin_table = QTableWidget()

        self.setup_bin_tab(0, self.local_bin_tab, self.load_local_bin, self.add_item_local,
                           self.edit_item_localbin, self.delete_item_local, self.local_bin_table)
        self.setup_bin_tab(1, self.external_bin_tab, self.load_external_bin, self.add_item_external,
                           self.edit_item_external, self.delete_item_external, self.exteranl_bin_table)

        self.tabs.addTab(self.local_bin_tab, "Local Bin")
        self.tabs.addTab(self.external_bin_tab, "External Bin")

        layout.addWidget(self.tabs)

    def setup_bin_tab(self, tab_id, tab, load_data_func, add_func, edit_func, delete_func, table=None):
        layout = QVBoxLayout()

        if table is None:
            table = QTableWidget()
        if tab_id == 0:
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels(
                ["Bin ID", "Customer ID", "Username", "Item Id", "Item name", "Quantity"])
        else:
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(
                ["Bin ID", "Customer ID", "Username", "Deal Id", "Item name", "Store name", "Quantity"])

        load_data_func(table)

        btn_layout = QHBoxLayout()
        if tab_id == 0:
            add_button = QPushButton("Add Item")
            add_button.clicked.connect(add_func)
            btn_layout.addWidget(add_button)
        else:
            pass
        edit_button = QPushButton("Edit Item")
        edit_button.clicked.connect(lambda: edit_func(table))
        btn_layout.addWidget(edit_button)
        
        delete_button = QPushButton("Delete Item")
        delete_button.clicked.connect(lambda: delete_func(table))
        btn_layout.addWidget(delete_button)

        layout.addWidget(table)
        layout.addLayout(btn_layout)

        tab.setLayout(layout)

    def load_local_bin(self, table):
        fetch_bin_query = "SELECT * FROM bin WHERE customer_id = ?;"
        cursor.execute(fetch_bin_query, (self.customer_id,))
        fetched = cursor.fetchall()
        table.setRowCount(len(fetched))
        for i in range(len(fetched)):
            table.setItem(i, 0, QTableWidgetItem(str(fetched[i][0])))
            table.setItem(i, 1, QTableWidgetItem(str(fetched[i][1])))
            cursor.execute(
                "SELECT username FROM customer_list WHERE customer_id = ?;", (fetched[i][1],))
            fetched_username = cursor.fetchall()
            table.setItem(i, 2, QTableWidgetItem(fetched_username[0][0]))
            table.setItem(i, 3, QTableWidgetItem(str(fetched[i][2])))
            cursor.execute(
                "SELECT name FROM menu WHERE item_id = ?;", (fetched[i][2],))
            fetched_itemname = cursor.fetchall()
            table.setItem(i, 4, QTableWidgetItem(fetched_itemname[0][0]))
            table.setItem(i, 5, QTableWidgetItem(str(fetched[i][3])))

    def load_external_bin(self, table):
        fetch_bin_query = "SELECT * FROM bin_external WHERE customer_id = ?;"
        cursor.execute(fetch_bin_query, (self.customer_id,))
        fetched = cursor.fetchall()
        table.setRowCount(len(fetched))
        for i in range(len(fetched)):
            table.setItem(i, 0, QTableWidgetItem(str(fetched[i][0])))
            table.setItem(i, 1, QTableWidgetItem(str(fetched[i][1])))
            cursor.execute(
                "SELECT username FROM customer_list WHERE customer_id = ?;", (fetched[i][1],))
            fetched_username = cursor.fetchall()
            table.setItem(i, 2, QTableWidgetItem(fetched_username[0][0]))
            table.setItem(i, 3, QTableWidgetItem(fetched[i][2]))
            link_deal = "https://www.cheapshark.com/api/1.0/deals?id=" + fetched[i][2]
            response = requests.get(link_deal)
            if response.status_code == 200:
                deal_data = response.json()
                game_name = deal_data['gameInfo']['name']
            else:
                print(f"Failed to fetch data: {response.status_code}, 'N/A'")
            table.setItem(i, 4, QTableWidgetItem(game_name))
            store_name = api.get_store(fetched[i][3])[0]
            table.setItem(i, 5, QTableWidgetItem(store_name))
            table.setItem(i, 6, QTableWidgetItem(str(fetched[i][4])))

    def add_item_local(self):
        dialog = AddItemDialog(self.customer_id, self)
        if dialog.exec_():
            self.load_local_bin(self.local_bin_table)

    def edit_item_localbin(self, table):
        try:
            row = table.currentRow()
            if row != -1:
                itemname = table.item(row, 4).text()
                qnt = table.item(row, 5).text()
                bin_id = int(table.item(row, 0).text())
                item_id = int(table.item(row, 3).text())
                old_qnt_bin = int(table.item(row, 5).text())

                dialog = EditItemDialog(self, itemname, qnt, table)
                
                if dialog.exec() == QDialog.Accepted:
                    new_bin_data = dialog.get_data()
                    new_qnt = int(new_bin_data["Qnt"])

                    if new_qnt >= 0:
                        self.update_bin_and_menu_quantities(item_id, new_qnt, old_qnt_bin, bin_id)
                        self.load_local_bin(self.local_bin_table)
                    else:
                        QMessageBox.warning(self, "Invalid Input", "Quantity must be a non-negative integer.")
                else:
                    print("Dialog canceled or closed")
            else:
                QMessageBox.warning(self, "Selection Required", "Please select an item to edit.")
        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.warning(self, "Error", "An error occurred while editing item.")

    def update_bin_and_menu_quantities(self, item_id, new_qnt, old_qnt_bin, bin_id):
        cursor.execute("SELECT qnt FROM menu WHERE item_id = ?;", (item_id,))
        old_qnt_menu_fetched = cursor.fetchall()
        if old_qnt_menu_fetched:
            old_qnt_menu = old_qnt_menu_fetched[0][0]
        else:
            QMessageBox.warning(self, "Invalid Item ID",
                                "There is no item under that ID.")
        max_qnt = old_qnt_bin + old_qnt_menu

        if new_qnt <= max_qnt:
            cursor.execute(
                "UPDATE menu SET qnt = qnt + ? WHERE item_id = ?;", (old_qnt_bin, item_id))
            conn.commit()
            cursor.execute(
                "UPDATE bin SET qnt = ? WHERE bin_id = ?;", (new_qnt, bin_id))
            conn.commit()
            cursor.execute(
                "UPDATE menu SET qnt = qnt - ? WHERE item_id = ?;", (new_qnt, item_id))
            conn.commit()
        elif new_qnt == 0:
            cursor.execute(
                "UPDATE menu SET qnt = qnt + ? WHERE item_id = ?;", (old_qnt_bin, item_id))
            conn.commit()
            cursor.execute("DELETE FROM bin WHERE bin_id = ?;", (bin_id,))
            conn.commit()
        elif new_qnt > max_qnt:
            QMessageBox.warning(self, "Invalid Quantity",
                                "Quantity provided is invalid or too large.")
        else:
            QMessageBox.warning(
                self, "Invalid Input", "Please enter a valid integer for quantity higher than 0.")

    def delete_item_local(self, table):
        row = table.currentRow()
        if row != -1:
            bin_id = int(table.item(row, 0).text())
            item_id = int(table.item(row, 3).text())
            old_qnt_bin = int(table.item(row, 5).text())
            response = QMessageBox.question(self, 'Confirm Deletion',
                                            "Are you sure you want to delete this item?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if response == QMessageBox.Yes:
                try:
                    cursor.execute("SELECT qnt FROM menu WHERE item_id = ?;", (item_id,))
                    old_qnt_menu_fetched = cursor.fetchall()
                    if old_qnt_menu_fetched:
                        old_qnt_menu = old_qnt_menu_fetched[0][0]
                    else:
                        QMessageBox.warning(self, "Invalid Item ID",
                                            "There is no item under that ID.")
                    cursor.execute(
                        "UPDATE menu SET qnt = qnt + ? WHERE item_id = ?;", (old_qnt_bin, item_id))
                    conn.commit()
                    cursor.execute("DELETE FROM bin WHERE bin_id = ?;", (bin_id,))
                    conn.commit()
                    self.load_local_bin(self.local_bin_table)
                    QMessageBox.information(
                        self, "Success", "Item has been deleted successfully.")
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"Failed to delete the item: {str(e)}")
            else:
                QMessageBox.information(
                    self, "Cancelled", "Item deletion cancelled.")
        else:
            QMessageBox.warning(self, "Selection Required",
                                "Please select an item to delete.")

    def add_item_external(self):
        print("Adding item to external bin")

    def edit_item_external(self, table):
        try:
            row = table.currentRow()
            if row != -1:
                itemname = table.item(row, 4).text()
                qnt = table.item(row, 6).text()
                bin_id = int(table.item(row, 0).text())

                dialog = EditItemDialog(self, itemname, qnt, table)
                
                if dialog.exec() == QDialog.Accepted:
                    new_bin_data = dialog.get_data()
                    new_qnt = int(new_bin_data["Qnt"])

                    if new_qnt >= 0:
                        self.update_external_bin_quantities(new_qnt, bin_id)
                        self.load_external_bin(self.exteranl_bin_table)
                    else:
                        QMessageBox.warning(self, "Invalid Input", "Quantity must be a non-negative integer.")
                else:
                    print("Dialog canceled or closed")
            else:
                QMessageBox.warning(self, "Selection Required", "Please select an item to edit.")
        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.warning(self, "Error", "An error occurred while editing item.")

    def update_external_bin_quantities(self, new_qnt, bin_id):
        if new_qnt == 0:
            cursor.execute(
                "DELETE FROM bin_external WHERE bin_id = ?", (bin_id,))
            conn.commit()
        else:
            cursor.execute(
                "UPDATE bin_external SET qnt = ? WHERE bin_id = ?;", (new_qnt, bin_id))
            conn.commit()

    def delete_item_external(self, table):
        row = table.currentRow()
        if row != -1:
            bin_id = int(table.item(row, 0).text())
            response = QMessageBox.question(self, 'Confirm Deletion',
                                            "Are you sure you want to delete this item?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if response == QMessageBox.Yes:
                try:
                    cursor.execute(
                        "DELETE FROM bin_external WHERE bin_id = ?", (bin_id,))
                    conn.commit()
                    self.load_external_bin(self.exteranl_bin_table)
                    QMessageBox.information(
                        self, "Success", "Item has been deleted successfully.")
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"Failed to delete the item: {str(e)}")
            else:
                QMessageBox.information(
                    self, "Cancelled", "Item deletion cancelled.")
        else:
            QMessageBox.warning(self, "Selection Required",
                                "Please select an item to delete.")


class AddItemDialog(QDialog):
    def __init__(self, customer_id, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)
        self.customer_id = customer_id
        self.setWindowTitle("Add Items to Bin")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Item ID", "Name", "Price", "Quantity"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.load_menu_items()

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        add_button = QPushButton("Add to Bin")
        add_button.clicked.connect(self.add_to_bin)

        layout.addWidget(self.table)
        layout.addWidget(self.quantity_input)
        layout.addWidget(add_button)
        self.setLayout(layout)

    def load_menu_items(self):
        fetch_menu_query = "SELECT * FROM menu;"
        cursor.execute(fetch_menu_query)
        fetched = cursor.fetchall()
        self.table.setRowCount(len(fetched))
        for i in range(len(fetched)):
            self.table.setItem(i, 0, QTableWidgetItem(str(fetched[i][0])))
            self.table.setItem(i, 1, QTableWidgetItem(fetched[i][1]))
            self.table.setItem(i, 2, QTableWidgetItem(str(fetched[i][2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(fetched[i][3])))

    def add_to_bin(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Selection Required",
                                "Please select an item to add.")
            return

        item_id = int(self.table.item(row, 0).text())
        max_quantity = int(self.table.item(row, 3).text())
        try:
            quantity_to_add = int(self.quantity_input.text())
            if 0 < quantity_to_add <= max_quantity:
                customer.addBin(self.customer_id, item_id, quantity_to_add)
                update_query = "UPDATE menu SET qnt = qnt - ? WHERE item_id = ?"
                cursor.execute(update_query, (quantity_to_add, item_id))
                conn.commit()
                print(
                    f"Added {quantity_to_add} of item ID {item_id} to customer ID {self.customer_id}'s bin")
                self.accept()
            else:
                QMessageBox.warning(self, "Invalid Quantity",
                                    "Quantity provided is invalid or too large.")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                                "Please enter a valid integer for quantity.")


class EditItemDialog(QDialog):
    def __init__(self, bin_window, itemname, qnt, table, parent=None):
        super().__init__(parent)
        self.bin_window = bin_window
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Edit item quantity")

        self.layout = QFormLayout(self)

        itemname_label = QLabel(itemname)
        self.layout.addRow("Item name:", itemname_label)

        self.qnt_edit = QLineEdit(qnt)
        self.layout.addRow(QLabel("Quantity:"), self.qnt_edit)

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        self.layout.addRow(button_layout)

    def get_data(self):
        return {
            "Qnt": self.qnt_edit.text()
        }

class APIInteraction(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.store_list_widget = QListWidget()
        self.update_store_list()

        self.find_deal_button = QPushButton("Find Deal")
        self.find_deal_button.clicked.connect(self.find_deal)

        layout.addWidget(QLabel("Active Stores:"))
        layout.addWidget(self.store_list_widget)
        layout.addWidget(self.find_deal_button)

        self.setLayout(layout)

    def update_store_list(self):
        self.store_list_widget.clear()
        store_list = self.get_store()
        for store in store_list:
            if store[1] == 1:
                self.store_list_widget.addItem(f"{store[0]} - Active")

    def get_store(self):
        link_store = "https://www.cheapshark.com/api/1.0/stores"
        response_store = requests.get(link_store)
        if response_store.status_code == 200:
            stores = response_store.json()
            store_list = []
            for store in stores:
                store_name = store.get('storeName', 'No name provided')
                store_active = store.get('isActive', 'No status provided')
                store_list.append([store_name, store_active])
            return store_list
        else:
            return [[f"Failed to fetch data: {response_store.status_code}", 'N/A']]

    def find_deal(self):
        dialog = DealFinderWindow()
        if dialog.exec_():
            self.load_local_bin(self.local_bin_table)

class DealFinderWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Find Deals")
        self.setGeometry(100, 100, 1000, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems(["Title", "Upper Price", "Lower Price"])
        self.sale_check_box = QCheckBox("Is On Sale")
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("If empty - shows first 60 deals on sale")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)

        self.deals_table = QTableWidget()
        self.deals_table.setColumnCount(8)
        self.deals_table.setHorizontalHeaderLabels(
            ["Title", "Game ID", "Store ID", "Store", "On Sale", "Sale Price, usd", "Normal Price, usd", "Deal ID"])
        default_width = self.deals_table.horizontalHeader().defaultSectionSize()
        self.deals_table.setColumnWidth(0, 2 * default_width)
        self.deals_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.no_deals_label = QLabel("No deals found")
        self.no_deals_label.setVisible(False)
        self.no_deals_label.setAlignment(Qt.AlignCenter)

        self.add_to_customer_button = QPushButton("Add Deal to Customer's External Bin")
        self.add_to_customer_button.clicked.connect(self.open_customer_selection_window)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_type_combo)
        search_layout.addWidget(self.sale_check_box)
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)
        layout.addWidget(self.deals_table)
        layout.addWidget(self.no_deals_label)
        layout.addWidget(self.add_to_customer_button)

        self.setLayout(layout)

    def perform_search(self):
        param = self.search_type_combo.currentIndex() + 1
        sale_check = 1 if self.sale_check_box.isChecked() else 0
        field_text = self.search_field.text()
        value = re.sub(r'[^a-zA-Z0-9]', '', field_text)

        deals = api.get_deal(param, sale_check, value)
        self.update_deals_table(deals)

    def update_deals_table(self, deals):
        self.deals_table.setRowCount(0)
        if len(deals) == 0:
            self.no_deals_label.setVisible(True)
        else:
            self.no_deals_label.setVisible(False)
            self.deals_table.setRowCount(len(deals))
            for i, deal in enumerate(deals):
                self.deals_table.setItem(i, 0, QTableWidgetItem(deal['title']))
                self.deals_table.setItem(i, 1, QTableWidgetItem(deal['gameID']))
                store_id = deal['storeID']
                self.deals_table.setItem(i, 2, QTableWidgetItem(store_id))
                store_name = api.get_store(store_id)
                self.deals_table.setItem(i, 3, QTableWidgetItem(store_name[0]))
                self.deals_table.setItem(i, 4, QTableWidgetItem("Yes" if deal['isOnSale'] == "1" else "No"))
                self.deals_table.setItem(i, 5, QTableWidgetItem(deal['salePrice']))
                self.deals_table.setItem(i, 6, QTableWidgetItem(deal['normalPrice']))
                self.deals_table.setItem(i, 7, QTableWidgetItem(deal['dealID']))

    def open_customer_selection_window(self):
        selected_row = self.deals_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Required", "Please select a deal first.")
            return
        selected_deal = self.deals_table.item(selected_row, 6).text()
        selected_deal = {
        'storeID': self.deals_table.item(selected_row, 2).text(),
        'dealID': self.deals_table.item(selected_row, 7).text()
        }
        dialog = CustomerSelectionWindow(selected_deal)
        dialog.exec_()

class CustomerSelectionWindow(QDialog):
    def __init__(self, selected_deal, parent=None):
        super().__init__(parent)
        self.selected_deal = selected_deal
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Select Customer and Quantity")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Enter customer username to find")
        self.search_field.textChanged.connect(self.find_customer)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_field)

        self.customer_list = QListWidget()
        self.load_customers()

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_deal_to_customer_bin)

        layout.addLayout(search_layout)
        layout.addWidget(self.customer_list)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.add_button)
        self.setLayout(layout)

    def load_customers(self):
        cursor.execute("SELECT username FROM customer_list;")
        fetched = cursor.fetchall()
        self.populate_customer_list(fetched)

    def populate_customer_list(self, data):
        self.customer_list.clear()
        for i in range(len(data)):
            self.customer_list.addItem(data[i][0])

    def find_customer(self):
        search_term = self.search_field.text().strip().lower()
        if not search_term:
            cursor.execute("SELECT username FROM customer_list;")
        else:
            cursor.execute("SELECT username FROM customer_list WHERE LOWER(username) LIKE ?", ('%' + search_term + '%',))

        fetched = cursor.fetchall()
        self.populate_customer_list(fetched)

    def add_deal_to_customer_bin(self):
        selected_customer_name = self.customer_list.currentItem().text()
        cursor.execute("SELECT customer_id FROM customer_list WHERE username LIKE ?", (selected_customer_name,))
        fetched = cursor.fetchall()
        selected_customer = fetched[0][0]
        quantity = self.quantity_input.text()
        if selected_customer and quantity.isdigit():
            customer.addBin_external(selected_customer, self.selected_deal['dealID'], self.selected_deal['storeID'], quantity)
            print(f"Adding {self.selected_deal} to {selected_customer}'s bin with quantity {quantity}")
            QMessageBox.information(self, "Success", "Deal has been added successfully.")
            self.accept()
        else:
            QMessageBox.warning(self, "Input Error", "Please select a customer and enter a valid quantity.")


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
    def addItem(name, price, qnt):
        insert_item_query = "INSERT INTO menu (name, price, qnt) VALUES (?, ?, ?);"
        item_data = (name, price, qnt)
        cursor.execute(insert_item_query, item_data)
        conn.commit()

    @staticmethod
    def updateItem(item_id, name, price, qnt):
        try:
            update_item_query = "UPDATE menu SET name = ?, price = ?, qnt = ? WHERE item_id = ?;"
            item_data = (name, price, qnt, item_id)
            cursor.execute(update_item_query, item_data)
            conn.commit()
            print("Database updated successfully")
        except Exception as e:
            print(f"Error updating database: {e}")

    @staticmethod
    def removeItem(item_id):
        try:
            delete_item_query = "DELETE FROM menu WHERE item_id = ?"
            cursor.execute(delete_item_query, (item_id,))
            conn.commit()
            print("Item removed successfully from the database")
        except Exception as e:
            print(f"Error removing item from database: {e}")

        try:
            delete_records_query = "DELETE FROM bin WHERE item_id = ?"
            cursor.execute(delete_records_query, (item_id,))
            conn.commit()
            print("\nCorresponding records were removed form the bin.")
        except:
            print("\nNo items were removed from the bin.")

    @staticmethod
    def findItemName(name):
        find_item_query = "SELECT * FROM menu WHERE name = ?;"
        item_data = (name,)
        cursor.execute(find_item_query, item_data)
        found = cursor.fetchall()
        return found

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
        check_records_query = "SELECT * FROM bin WHERE customer_id = ? AND item_id = ?;"
        cursor.execute(check_records_query, (customer_id, item_id))
        found = cursor.fetchall()
        if not found:
            insert_bin_query = "INSERT INTO bin (customer_id, item_id, qnt) VALUES (?, ?, ?);"
            bin_data = (customer_id, item_id, qnt)
            cursor.execute(insert_bin_query, bin_data)
            conn.commit()
        else:
            update_bin_query = "UPDATE bin SET qnt = qnt + ? WHERE customer_id = ? AND item_id = ?;"
            cursor.execute(update_bin_query, (qnt, customer_id, item_id))
            conn.commit()

    @staticmethod
    def addBin_external(customer_id, item_id, store_id, qnt):
        insert_bin_query = "INSERT INTO bin_external (customer_id, item_id, store_id, qnt) VALUES (?, ?, ?, ?);"
        bin_data = (customer_id, item_id, store_id, qnt)
        cursor.execute(insert_bin_query, bin_data)
        conn.commit()

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
    def addCustomer(username, date):
        insert_customer_query = "INSERT INTO customer_list (username, date) VALUES (?, ?);"
        customer_data = (username, date)
        cursor.execute(insert_customer_query, customer_data)
        conn.commit()

    @staticmethod
    def updateCustomer(customer_id, username):
        try:
            chan_cus_query = "UPDATE customer_list SET username = ? WHERE customer_id = ?"
            chan_cus_data = (username, customer_id)
            cursor.execute(chan_cus_query, chan_cus_data)
            conn.commit()
            print("Database updated successfully")
        except Exception as e:
            print(f"Error updating database: {e}")

    @staticmethod
    def deleteCustomer(customer_id):
        try:
            del_cus_query = "DELETE FROM customer_list WHERE customer_id = ?"
            cursor.execute(del_cus_query, (customer_id,))
            conn.commit()
            print("Customer deleted")
        except Exception as e:
            print(f"Error updating database: {e}")

        try:
            delete_records_query = "DELETE FROM bin WHERE customer_id = ?"
            cursor.execute(delete_records_query, (customer_id,))
            conn.commit()
            print("Customer's bin deleted")
        except:
            print("Customer's bin is empty")

    @staticmethod
    def find_customer_by_username(username):
        find_customer_query = "SELECT * FROM customer_list WHERE username = ?"
        cursor.execute(find_customer_query, (username,))
        found = cursor.fetchall()
        return found


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

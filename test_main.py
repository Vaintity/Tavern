import pytest
import sqlite3
import os
from PyQt5.QtWidgets import QApplication
from unittest.mock import patch, MagicMock
from main import get_db_connection, db, menu, customer, customer_list, api, MainWindow, MenuManagement, CustomerManagement, APIInteraction

TEST_DB = 'test_tavern.db'


@pytest.fixture(scope='module')
def db_conn():
    conn, cursor = get_db_connection(TEST_DB)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu (
        item_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL,
        qnt INTEGER
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_list (
        customer_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        date REAL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bin (
        bin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        qnt INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customer_list(customer_id),
        FOREIGN KEY (item_id) REFERENCES menu(item_id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bin_external (
        bin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        store_id INTEGER NOT NULL,
        qnt INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customer_list(customer_id)
    );
    ''')

    conn.commit()

    yield conn, cursor

    cursor.close()
    conn.close()
    os.remove(TEST_DB)


@pytest.fixture(scope='function', autouse=True)
def clear_db(db_conn):
    conn, cursor = db_conn
    cursor.execute("DELETE FROM menu;")
    cursor.execute("DELETE FROM customer_list;")
    cursor.execute("DELETE FROM bin;")
    cursor.execute("DELETE FROM bin_external;")
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'menu';")
    cursor.execute(
        "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'customer_list';")
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'bin';")
    cursor.execute(
        "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'bin_external';")
    conn.commit()


def set_cursor_conn(instance, db_conn):
    instance.conn, instance.cursor = db_conn


class TestDB:
    @pytest.fixture(autouse=True)
    def setup_method(self, db_conn):
        set_cursor_conn(self, db_conn)

    def test_isEmpty(self):
        assert db.isEmpty('menu', self.cursor) == True
        assert db.isEmpty('customer_list', self.cursor) == True

    def test_deleteAllRecords(self):
        menu.addItem("Test Item", 10.0, 5, self.cursor, self.conn)
        assert db.isEmpty('menu', self.cursor) == False
        db.deleteAllRecords('menu', self.cursor, self.conn)
        assert db.isEmpty('menu', self.cursor) == True


class TestMenu:
    @pytest.fixture(autouse=True)
    def setup_method(self, db_conn):
        set_cursor_conn(self, db_conn)

    def test_addItem(self):
        menu.addItem("Test Item", 10.0, 5, self.cursor, self.conn)
        self.cursor.execute("SELECT * FROM menu WHERE name = 'Test Item'")
        item = self.cursor.fetchone()
        assert item is not None
        assert item[1] == "Test Item"
        assert item[2] == 10.0
        assert item[3] == 5

    def test_updateItem(self):
        menu.addItem("Test Item", 10.0, 5, self.cursor, self.conn)
        self.cursor.execute(
            "SELECT item_id FROM menu WHERE name = 'Test Item'")
        item_id = self.cursor.fetchone()[0]
        menu.updateItem(item_id, "Updated Item", 15.0,
                        10, self.cursor, self.conn)
        self.cursor.execute("SELECT * FROM menu WHERE item_id = ?", (item_id,))
        item = self.cursor.fetchone()
        assert item[1] == "Updated Item"
        assert item[2] == 15.0
        assert item[3] == 10

    def test_removeItem(self):
        menu.addItem("Test Item", 10.0, 5, self.cursor, self.conn)
        self.cursor.execute(
            "SELECT item_id FROM menu WHERE name = 'Test Item'")
        item_id = self.cursor.fetchone()[0]
        menu.removeItem(item_id, self.cursor, self.conn)
        self.cursor.execute("SELECT * FROM menu WHERE item_id = ?", (item_id,))
        item = self.cursor.fetchone()
        assert item is None

    @pytest.mark.parametrize("name, expected", [
        ("Nonexistent Item", []),
        ("Test Item", [(1, "Test Item", 10.0, 5)])
    ])
    def test_findItemName(self, name, expected):
        if name == "Test Item":
            menu.addItem(name, 10.0, 5, self.cursor, self.conn)
        result = menu.findItemName(name, self.cursor)
        result_formatted = [(row[0], row[1], row[2], row[3]) for row in result]
        assert result_formatted == expected


class TestCustomer:
    @pytest.fixture(autouse=True)
    def setup_method(self, db_conn):
        set_cursor_conn(self, db_conn)

    def test_addCustomer(self):
        customer_list.addCustomer(
            "Test User", 1625151600.0, self.cursor, self.conn)
        self.cursor.execute(
            "SELECT * FROM customer_list WHERE username = 'Test User'")
        customer = self.cursor.fetchone()
        assert customer is not None
        assert customer[1] == "Test User"
        assert customer[2] == 1625151600.0

    def test_updateCustomer(self):
        customer_list.addCustomer(
            "Test User", 1625151600.0, self.cursor, self.conn)
        self.cursor.execute(
            "SELECT customer_id FROM customer_list WHERE username = 'Test User'")
        customer_id = self.cursor.fetchone()[0]
        customer_list.updateCustomer(
            customer_id, "Updated User", self.cursor, self.conn)
        self.cursor.execute(
            "SELECT * FROM customer_list WHERE customer_id = ?", (customer_id,))
        customer = self.cursor.fetchone()
        assert customer[1] == "Updated User"

    def test_deleteCustomer(self):
        customer_list.addCustomer(
            "Test User", 1625151600.0, self.cursor, self.conn)
        self.cursor.execute(
            "SELECT customer_id FROM customer_list WHERE username = 'Test User'")
        customer_id = self.cursor.fetchone()[0]
        customer_list.deleteCustomer(customer_id, self.cursor, self.conn)
        self.cursor.execute(
            "SELECT * FROM customer_list WHERE customer_id = ?", (customer_id,))
        customer = self.cursor.fetchone()
        assert customer is None

    @pytest.mark.parametrize("username, expected", [
        ("Nonexistent User", []),
        ("Test User", [(1, "Test User", 1625151600.0)])
    ])
    def test_find_customer_by_username(self, username, expected):
        if username == "Test User":
            customer_list.addCustomer(
                username, 1625151600.0, self.cursor, self.conn)
        result = customer_list.find_customer_by_username(username, self.cursor)
        result_formatted = [(row[0], row[1], row[2]) for row in result]
        assert result_formatted == expected

    def test_addCustomer_duplicate(self):
        customer_list.addCustomer(
            "Test User", 1625151600.0, self.cursor, self.conn)
        with pytest.raises(sqlite3.IntegrityError):
            customer_list.addCustomer(
                "Test User", 1625151600.0, self.cursor, self.conn)


class TestCustomerBin:
    @pytest.fixture(autouse=True)
    def setup_method(self, db_conn):
        set_cursor_conn(self, db_conn)

    def test_addBin(self):
        customer_list.addCustomer(
            "Test User", 1625151600.0, self.cursor, self.conn)
        menu.addItem("Test Item", 10.0, 5, self.cursor, self.conn)
        customer.addBin(1, 1, 5, self.cursor, self.conn)
        self.cursor.execute(
            "SELECT * FROM bin WHERE customer_id = 1 AND item_id = 1")
        bin_entry = self.cursor.fetchone()
        assert bin_entry is not None
        assert bin_entry[3] == 5

    def test_addBin_existing(self):
        customer_list.addCustomer(
            "Test User", 1625151600.0, self.cursor, self.conn)
        menu.addItem("Test Item", 10.0, 5, self.cursor, self.conn)
        customer.addBin(1, 1, 5, self.cursor, self.conn)
        customer.addBin(1, 1, 5, self.cursor, self.conn)
        self.cursor.execute(
            "SELECT qnt FROM bin WHERE customer_id = 1 AND item_id = 1")
        quantity = self.cursor.fetchone()[0]
        assert quantity == 10

    def test_addBin_external(self):
        customer_list.addCustomer(
            "Test User", 1625151600.0, self.cursor, self.conn)
        customer.addBin_external(1, 1, 1, 5, self.cursor, self.conn)
        self.cursor.execute(
            "SELECT * FROM bin_external WHERE customer_id = 1 AND item_id = 1 AND store_id = 1")
        bin_entry = self.cursor.fetchone()
        assert bin_entry is not None
        assert bin_entry[4] == 5


@pytest.fixture(scope='module')
def app():
    return QApplication([])


class TestMainWindow:
    def test_init(self, app):
        main_window = MainWindow()
        assert main_window is not None

    @patch('main.MenuManagement.load_menu_items')
    def test_menu_management_tab(self, mock_load_menu_items, app):
        main_window = MainWindow()
        main_window.tab_widget.setCurrentIndex(0)
        mock_load_menu_items.assert_called_once()

    @patch('main.CustomerManagement.load_customers')
    def test_customer_management_tab(self, mock_load_customers, app):
        main_window = MainWindow()
        main_window.tab_widget.setCurrentIndex(1)

        initial_call_count = mock_load_customers.call_count
        assert initial_call_count >= 1

        main_window.tab_widget.setCurrentIndex(0)
        main_window.tab_widget.setCurrentIndex(1)

        assert mock_load_customers.call_count == initial_call_count + 1


class TestAPIInteraction:
    @patch('main.requests.get')
    def test_get_store(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'storeID': 1, 'storeName': 'Steam', 'isActive': 1}]
        mock_get.return_value = mock_response

        store_list = APIInteraction().get_store()
        assert store_list == [['Steam', 1]]

    @patch('main.requests.get')
    def test_get_deal(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'title': 'Game', 'gameID': '123', 'storeID': '1', 'salePrice': '10.0', 'normalPrice': '20.0', 'dealID': '1'}]
        mock_get.return_value = mock_response

        deals = api.get_deal(1, 1, 'Game')
        assert len(deals) == 1
        assert deals[0]['title'] == 'Game'

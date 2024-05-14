'''
Why is it always shows deals both on sale and not on sale regardless if box is checked or if it is not
'''
class DealFinderWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Find Deals")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Search options
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems(["Title", "Upper Price", "Lower Price"])
        self.sale_check_box = QCheckBox("Is On Sale")
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("If empty - shows first 60 deals on sale")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)

        # Table to display deals
        self.deals_table = QTableWidget()
        self.deals_table.setColumnCount(6)  # Title, Game ID, Store, On Sale, Sale Price, Normal Price
        self.deals_table.setHorizontalHeaderLabels(
            ["Title", "Game ID", "Store", "On Sale", "Sale Price, usd", "Normal Price, usd"])
        default_width = self.deals_table.horizontalHeader().defaultSectionSize()
        self.deals_table.setColumnWidth(0, 2 * default_width)
        self.deals_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Layout configuration
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_type_combo)
        search_layout.addWidget(self.sale_check_box)
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)
        layout.addWidget(self.deals_table)

        self.setLayout(layout)

    def perform_search(self):
        param = self.search_type_combo.currentIndex() + 1  # 1-Title, 2-Upper Price, 3-Lower Price
        sale_check = 1 if self.sale_check_box.isChecked() else 0
        field_text = self.search_field.text()
        value = re.sub(r'[^a-zA-Z0-9]', '', field_text)

        # Assuming get_deal function returns list of deals or error message
        deals = api.get_deal(param, sale_check, value)
        self.update_deals_table(deals)

    def update_deals_table(self, deals):
        self.deals_table.setRowCount(len(deals))
        for i, deal in enumerate(deals):
            self.deals_table.setItem(i, 0, QTableWidgetItem(deal['title']))
            self.deals_table.setItem(i, 1, QTableWidgetItem(deal['gameID']))
            store_id = deal.get('storeID', 'No ID provided')
            store_name = api.get_store(store_id)
            self.deals_table.setItem(i, 2, QTableWidgetItem(store_name[0]))
            self.deals_table.setItem(i, 3, QTableWidgetItem("Yes" if deal['isOnSale'] == "1" else "No"))
            self.deals_table.setItem(i, 4, QTableWidgetItem(deal['salePrice']))
            self.deals_table.setItem(i, 5, QTableWidgetItem(deal['normalPrice']))

@abstractmethod
    def get_deal(param, sale_check, value):
        link_deal = "https://www.cheapshark.com/api/1.0/deals"

        if param == 1:
            if sale_check == 1:
                response = requests.get(link_deal, params={"title": value, "isOnSale": "1"})
            else:
                response = requests.get(link_deal, params={"title": value})
        elif param == 2:
            if sale_check == 1:
                response = requests.get(link_deal, params={"upperPrice": value, "isOnSale": "1"})
            else:
                response = requests.get(link_deal, params={"upperPrice": value})
        elif param == 3:
            if sale_check == 1:
                response = requests.get(link_deal, params={"lowerPrice": value, "isOnSale": "1"})
            else:
                response = requests.get(link_deal, params={"lowerPrice": value})
        elif param == 4:
            if sale_check == 1:
                response = requests.get(link_deal, params={"isOnSale": "1"})
            else:
                response = requests.get(link_deal)
        else:
            print("Incorrect param")

        if response.status_code == 200:
            deals = response.json()
            return deals
        else:
            print(f"Failed to fetch data: {response.status_code}, 'N/A'")
import requests
import re

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

link_deal = "https://www.cheapshark.com/api/1.0/deals"

value = "Baldur's Gate 3"
value = re.sub(r'[^a-zA-Z0-9]', '', value)
#response = requests.get(link_deal, params={"title": value, "isOnSale": "1"})
payload = {"title": value, "onSale": "1"}
response = requests.get(link_deal, params=payload)
print(response.url)

#value = 10
#response = requests.get(link_deal, params={"upperPrice": value, "isOnSale": "1"})

if response.status_code == 200:
    deals = response.json()
    for game in deals:
        game_title = game.get('title', 'No title provided')
        game_id = game.get('gameID', 'No ID provided')
        store_id = game.get('storeID', 'No ID provided')
        store_name = get_store(store_id)
        on_sale = game.get('isOnSale', 'No status provided')
        if on_sale == "1":
            on_sale_status = "yes"
        else: 
            on_sale_status = "no"
        sale_price = game.get('salePrice', 'No price provided')
        normal_price = game.get('normalPrice', 'No price provided')
        print(f"\nTitle: {game_title} \nGame ID: {game_id} \nStore: {store_name[0]} \nOn sale: {on_sale_status} \nSale price: {sale_price} \nNormal price: {normal_price}")
else:
    print(f"Failed to fetch data: {response.status_code}, 'N/A'")


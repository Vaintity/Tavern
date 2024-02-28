class menu:
    def __init__(self):
        self.drinks = []
    
    def add(self, drink):
        self.drinks.append(drink)
    
    def simple_rem(self, drink):
        if isinstance(drink, int):
            self.drinks.pop(drink-1)
        elif isinstance(drink, list) and len(drink) == 3:
            self.drinks.remove(drink)
        else:
            raise TypeError('Not supported variable type')
        
class drink:
    def __init__(self, name, price, qnt):
        self.name = name
        self.price = price
        self.qnt = qnt
    
    def change_name(self, name):
        self.name = name
    def change_price(self, price):
        self.price = price
    def change_qnt(self, qnt):
        self.qnt = qnt

#filtering: oper_1 - black-/whitelist, oper_2 - by Name/Price/Qnt
def filter(menu_obj, drink_obj, oper_1, oper_2):
    if isinstance(menu_obj, menu) and 0 < oper_2 < 4:
        if oper_1 == 1:
            filtered_menu = [d for d in menu_obj if d[oper_2] != drink_obj]
        elif oper_1 == 2:
            filtered_menu = [d for d in menu_obj if d[oper_2] == drink_obj]
        else:
            raise ValueError('Incorrect operation number')
    else:
        raise Exception('Not supported menu variable type or Incorrect operation number')
    return filtered_menu

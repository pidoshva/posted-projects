from datetime import date
import random

class Customer:
    def __init__(self,cust_id,name,address,phone,email):
        self.cust_id = cust_id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
    def append_to_file(self,fname):
        with open(fname,'a') as customers_file:
            customers_file.write(self.__str__())
    def __str__(self):
        return f"{self.cust_id},{self.name},{self.address},{self.phone},{self.email}\n"

class Place_Order:
    def __init__(self,cust_id=None,order_id=None,date=None,line_items=None):
        self.cust_id = cust_id
        self.order_id = order_id
        self.date = date
        self.line_items = line_items

    def count_orders(self):
        count = 1
        with open('orders.txt','r') as items_file:
            temp = [[i.strip()] for i in items_file]
            for i in temp:
                if count % 2 == 1:
                    count += 1
        return count

    def append_to_file(self,fname):
        with open(fname,'a') as orders_file:
            orders_file.write(self.__str__())
    def __str__(self):
        return f"{self.cust_id},{self.order_id},{self.date}{self.line_items}\n"

class Item:
    def __init__(self,item_id=None,description=None,price=None,qty=None):
        self.item_id = item_id
        self.description = description
        self.price = price
        self.qty = qty

    def sub_total(self):
        return float(self.price * float(self.qty))

    def total(self):
        self.total_price = 0
        self.total_price += self.sub_total()
        return self.total_price

    def read_items(self,fname):
        with open(fname,'r') as items_file:
            temp = [[i.strip()] for i in items_file]
            items_data = [i.split(",") for j in temp for i in j]
        return items_data

    def __str__(self):
        return f'\nItem {self.item_id}: "{self.description}", {self.qty} @ {self.price:.2f}, Subtotal: ${round(self.sub_total(),2):.2f}\n'

class Payment:
    def __init__(self,pay=None,data1=None,data2=None):
        self.pay = pay #payment type
        self.data1 = data1
        self.data2 = data2
    def __str__(self):
        if self.pay == '1':
            return str(Credit(self.data1,self.data2).append_data())
        elif self.pay == '2':
            return str(PayPal(self.data1).append_data())
        elif self.pay == '3':
            return str(WireTransfer(self.data1,self.data2).append_data())

class Credit:
    def __init__(self,card_number,exp_date):
        self.card_number = card_number
        self.exp_date = exp_date
    def append_data(self):
        with open('orders.txt','a') as orders_file:
            orders_file.write(self.__str__())
    def __str__(self):
        return f"{1},{self.card_number},{self.exp_date}\n"

class PayPal:
    def __init__(self,paypal_id):
        self.paypal_id = paypal_id

    def append_data(self):
        with open('orders.txt','a') as orders_file:
            orders_file.write(self.__str__())
    def __str__(self):
        return f"{2},{self.paypal_id}\n"

class WireTransfer:
    def __init__(self,bank_id,account_id):
        self.bank_id = bank_id
        self.account_id = account_id
    def append_data(self):
        with open('orders.txt','a') as orders_file:
            orders_file.write(self.__str__())
    def __str__(self):
        return f"{3},{self.bank_id},{self.account_id}\n"

def main():
    with open('orders.txt','r') as order_file:
        rand_int = random.randint(1000,9999)
        if rand_int not in order_file:
            ask_customer_id = rand_int
    line_items = str()
    ordered_items = str()
    total = float()
    with open('items.txt','r') as items_file:
            temp = [[i.strip()] for i in items_file]
            items_data = [i.split(",") for j in temp for i in j]
    while True:
        ask_item_id = input("Enter Item ID You'd Like to Purchase: ")
        if ask_item_id == 'q':
            quit()
        else:
            for i in items_data:
                if ask_item_id in i:
                    ask_qty = input("Qty: ")
                    current_date = date.today()
                    for item in Item().read_items('items.txt'):
                        if item[0] == ask_item_id:
                            item_id = item[0]
                            description = item[1]
                            price = float(item[2])
                            qty = ask_qty
                            item_obj = Item(item_id,description,price,qty)
                            line_items += f",{item_obj.item_id}-{item_obj.qty}"
                            ordered_items += Item(item_id,description,price,qty).__str__()
                            print(ordered_items)
                            total += Item(item_id,description,price,qty).total()
                            print(f"Total: ${total:.2f}")
                            # message asking if user wants to continue shopping
                            keep_shopping = input("Keep Shopping?(y/n/q) ")
                            if keep_shopping == 'y':
                                continue
                            elif keep_shopping == 'n':
                                print("\n======Complete Order======\n")
                                f_name = input("Enter your first name: ")
                                l_name = input("Enter your last name: ")
                                street = input("Enter your address (street): ")
                                city = input("Enter your city: ")
                                state = input("Enter your state: ")
                                zip_code = input("Enter your zip code: ")
                                name = f"{f_name} {l_name}" #full name
                                address = f"{street},{city},{state},{zip_code}" #full address
                                ph_number = input("Enter your phone number: ")
                                email = input("Enter your email: ")
                                print("===Choose Your Payment Method===")
                                print("Credit Card (1), PayPal (2), Wire Transfer (3)")
                                pay = input("Choose your payment method: ")
                                Place_Order(ask_customer_id,Place_Order().count_orders(),current_date,line_items).append_to_file('orders.txt')
                                if pay == '1':
                                    card_number = input("Enter card number: ")
                                    exp_date = input("Enter exp_date: ")
                                    Payment(pay,card_number,exp_date).__str__()
                                elif pay == '2':
                                    paypal_id = input("Enter PayPay ID: ")
                                    Payment(pay,paypal_id).__str__()
                                elif pay == '3':
                                    account_number = input("Enter account number: ")
                                    routing_number = input("Enter routing number: ")
                                    Payment(pay,account_number,routing_number).__str__()
                                else:
                                    print("Error!")
                                Customer(ask_customer_id,name,address,ph_number,email).append_to_file('customers.txt')
                                print(f"==============\nThank You For Your Purchase, {name}\nAmount Paid: ${round(total,2)}\n")
                                quit()
                            elif keep_shopping == 'q':
                                quit()
            else:
                print("Item NOT Found!")

if __name__ == "__main__":
    main()

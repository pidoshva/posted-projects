"""
Vadym Pidoshva
CS3270
ProjectD: Online Groceries
Date Compleated: Mar 17, 2022
"""
class Customer:
    """implementing customer class"""
    def __init__(self,cust_id=None,name=None,street=None,city=None,state=None,postal_code=None,phone=None,email=None):
        """initialization of customer class"""
        self.cust_id = cust_id
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.phone = phone
        self.email = email

    def read_customers(self,fname):
        """reading customers.txt file"""
        with open(fname,'r') as customers_file:
            temp = [[i.strip()] for i in customers_file]
            customer_data = [i.split(",") for j in temp for i in j]
        return customer_data

    def __str__(self):
        """customer info string"""
        return f"\nCustomer ID #{self.cust_id}\n{self.name}, ph. {self.phone}, email: {self.email}\n{self.street}\n{self.city}, {self.state} {self.postal_code}\n"

class Order:
    """implementing order class"""
    def __init__(self,cust_id=None,order_id=None,order_date=None,line_items=None,payment=None):
        """initialization of order class"""
        self.order_id = order_id
        self.order_date = order_date
        self.cust_id = cust_id
        self.line_items = line_items #list[0] - item_id; list[1] - qty.
        self.payment = payment
        #accessing Customer class
        for i in Customer().read_customers('customers.txt'):
            if self.cust_id == i[0]:
                self.customers = Customer(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        self.payment_obj = Payment(self.payment)
        #order details in a sorted list
        self.order_details = list()
        if self.line_items:
            for i in self.line_items:
                self.order_details.append(LineItem(i[0],i[1]).order_details())
                self.order_details.sort()

    def total(self):
        """calculating total amount paid"""
        self.total_price = 0
        if self.line_items:
            for i in self.line_items:
                self.total_price += LineItem(i[0],i[1]).sub_total()
        return float(self.total_price)

    def read_orders(self,fname):
        """reading data from the order.txt file"""
        with open(fname,'r') as orders_file:
            temp = [[i.strip()] for i in orders_file]
            orders_data = [i.split(",") for j in temp for i in j]
        return orders_data

    def __str__(self):
        """order output string"""
        self.final_order_details = str()
        for i in self.order_details:
            self.final_order_details += i
        return f"Order #{self.order_id}, Date: {self.order_date}\nAmount: ${round(self.total(),2):.2f}, {self.payment_obj}\n{self.customers}\nOrder Details:\n{self.final_order_details}\n===========================\n"

class LineItem:
    """implementing lineitem class"""
    def __init__(self,item_id,qty):
        """initialization of lineitem class"""
        self.item_id = item_id
        self.qty = qty
        items = Item().read_items('items.txt')
        for item in items:
            if item[0] == item_id:
                item_id = item[0]
                description = item[1]
                price = float(item[2])
                self.item_obj = Item(item_id,description,price)

    def sub_total(self):
        """calculating subtotal for each product"""
        return float(self.item_obj.price * float(self.qty)) #item price times amount purchased(qty)

    def order_details(self):
        """implementing order_details fucntion"""
        order_details = str()
        if self.item_id in self.item_obj.item_id:
            order_details += f'\tItem {self.item_obj.item_id}: "{self.item_obj.description}", {self.qty} @ {self.item_obj.price:.2f}\n'
            return order_details #returning a string of all the items purchased by a customer

class Item:
    """implementing an item class"""
    def __init__(self,item_id=None,description=None,price=None):
        """initializing an item class"""
        self.item_id = item_id
        self.description = description
        self.price = price

    def read_items(self,fname):
        """reading data from items.txt file"""
        with open(fname,'r') as items_file:
            temp = [[i.strip()] for i in items_file]
            items_data = [i.split(",") for j in temp for i in j]
        return items_data

class Payment:
    """implementing a payment class"""
    def __init__(self,pay):
        """initializing a payment class"""
        self.pay = pay #payment type

    def __str__(self):
        """determining the payment method"""
        if self.pay[0] == '1': #if payment method is '1' then credit card was used
            return str(Credit(self.pay[1],self.pay[2]))
        elif self.pay[0] == '2': #if payment method is '2' then paid through PayPal account
            return str(PayPal(self.pay[1]))
        elif self.pay[0] == '3': #if payment method is '3' then payed through accound number and routing number
            return str(WireTransfer(self.pay[1],self.pay[2]))

class Credit:
    """implementing credit card class (payment method)"""
    def __init__(self,card_number,exp_date):
        """initializing a credit class"""
        self.card_number = card_number
        self.exp_date = exp_date
    def __str__(self):
        """returning an output string"""
        return f"Paid by Credit card {self.card_number}, exp. {self.exp_date}"

class PayPal:
    """implementing paypal class (payment method)"""
    def __init__(self,paypal_id):
        """initializing a paypal class"""
        self.paypal_id = paypal_id
    def __str__(self):
        """returning an output string"""
        return f"Paid by PayPal ID: {self.paypal_id}"

class WireTransfer:
    """implementing wiretransfer class (payment method)"""
    def __init__(self,bank_id,account_id):
        """initializing a wiretransfer class"""
        self.bank_id = bank_id
        self.account_id = account_id
    def __str__(self):
        """returning an output string"""
        return f"Paid by Wire transfer from Bank ID {self.bank_id}, Account# {self.account_id}"

def main():
    """implementing main function"""
    orders = Order().read_orders('orders.txt')
    count = 1 #line at (number)
    #looping through lines of order.txt data
    for order in orders:
        if count%2 == 1: #if the line is odd
            cust_id = order[0] #assigning data to Order class as customer id
            order_id = order[1] #assigning data to Order class as order id
            date = order[2] #assigning data to Order class as date purchased
            line_items = order[3:] #assigning data to Order class as items purchased and their amount (list)
            line_items = [i.split('-') for i in line_items] #organizing line_items (removing '-')
        else:
            payment = order #if the line is even then it is assigned as a payment method for a line above
            order_obj = Order(cust_id,order_id,date,line_items,payment) #creating an order object and passing assigned data to a class itself
            print(str(order_obj)) #printing output in a console
            #appending output to a file "order_report.txt"
            with open('order_report.txt','a') as order_report:
                order_report.write(str(order_obj))
        count += 1 #line count

if __name__ == "__main__":
    main()

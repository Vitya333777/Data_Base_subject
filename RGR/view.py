class View:

    # Goods
    def show_goods(self, Goods):
        if Goods:
            print("Goods:")
            for goods in Goods:
                print(f"goods_id: {goods[0]}, goods_name: {goods[1]}, goods_description: {goods[2]}, goods_price: {goods[3]}")
        else:
            print("Good was not found.")

    def get_goods_name(self):
        goods_name = input("Enter goods name: ")
        return goods_name

    def get_goods_id(self):
        goods_id = input("Enter goods id: ")
        return goods_id

    def get_goods_description(self):
        goods_description = input("Enter goods description: ")
        return goods_description

    def get_goods_price(self):
        goods_price = input("Enter goods price: ")
        return goods_price

    # Order
    def show_order(self, Order):
        if Order:
            print("Orders:")
            for order in Order:
                print(f"order_id: {order[0]}, order_date: {order[1]}, order_price: {order[2]}, client_id: {order[3]}")
        else:
            print("Order was not found.")

    def get_order_date(self):
        order_date = input("Enter order date: ")
        return order_date

    def get_order_id(self):
        order_id = input("Enter order id: ")
        return order_id

    def get_order_price(self):
        order_price = input("Enter order price: ")
        return order_price

    def get_numb_of_pos(self):
        pos_numb = input("Enter number of positions in this order: ")
        return pos_numb

    # Client
    def show_client(self, Client):
        if Client:
            print("Clients:")
            for client in Client:
                print(f"Client id: {client[0]}, client name: {client[1]}, client phone number: {client[2]}, client sex: {client[3]}")
        else:
            print("Client was not found.")

    def get_client_id(self):
        client_id = input("Enter client id: ")
        return client_id

    def get_client_name(self):
        client_name = input("Enter client name: ")
        return client_name

    def get_client_ph_number(self):
        client_ph_number = input("Enter client phone number: ")
        return client_ph_number

    def get_client_sex(self):
        client_sex = input("Enter client sex: ")
        return client_sex

    # Loyalty program
    def show_loyalty_program(self, Loyalty_program):
        if Loyalty_program:
            print("Loyalty programs:")
            for program in Loyalty_program:
                print(f"Loyalty program id: {program[0]}, client_id: {program[1]}, loyalty_program_sum: {program[2]}, discount level: {program[3]}")
        else:
            print("Loyalty program was not found.")

    def get_rand_number(self):
        rand_number = input("Enter number of random generated clients: ")
        return rand_number

    def show_message(self, message):
        print(message)
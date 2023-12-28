from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice = self.show_menu()
            if choice == '1':
                self.run_add()
            elif choice == '2':
                self.run_view()
            elif choice == '3':
                self.run_edit()
            elif choice == '4':
                self.run_delete()
            elif choice == '5':
                self.run_generate()
            elif choice == '6':
                break

    def show_menu(self):
        self.view.show_message("\n====== MENU ======")
        self.view.show_message("(1) ADD")
        self.view.show_message("(2) VIEW")
        self.view.show_message("(3) EDIT")
        self.view.show_message("(4) DELETE")
        self.view.show_message("(5) GENERATE CLIENTS")
        self.view.show_message("(6) QUIT")
        return input("Enter your choice: ")

    def menu(self):
        self.view.show_message("(1) GOODS")
        self.view.show_message("(2) LOYALTY PROGRAM")
        self.view.show_message("(3) CLIENT")
        self.view.show_message("(4) ORDER")
        self.view.show_message("(5) QUIT")
        return input("Enter your choice: ")

    def run_add(self):
        self.view.show_message("\n===== ADD =====")
        while True:
            choice_1 = self.menu()
            if choice_1 == '1':
                self.add_goods()
            elif choice_1 == '2':
                self.add_loyalty_program()
            elif choice_1 == '3':
                self.add_client()
            elif choice_1 == '4':
                self.add_order()
            elif choice_1 == '5':
                break

    def run_view(self):
        self.view.show_message("\n===== VIEW =====")
        while True:
            choice_2 = self.menu()
            if choice_2 == '1':
                self.view_goods()
            elif choice_2 == '2':
                self.view_loyalty_program()
            elif choice_2 == '3':
                self.view_client()
            elif choice_2 == '4':
                self.view_order()
            elif choice_2 == '5':
                break

    def run_edit(self):
        self.view.show_message("\n===== EDIT =====")
        while True:
            choice_3 = self.menu()
            if choice_3 == '1':
                self.edit_goods()
            elif choice_3 == '2':
                self.edit_loyalty_program()
            elif choice_3 == '3':
                self.edit_client()
            elif choice_3 == '4':
                self.edit_order()
            elif choice_3 == '5':
                break

    def run_delete(self):
        self.view.show_message("\n===== DELETE =====")
        while True:
            choice_4 = self.menu()
            if choice_4 == '1':
                self.delete_goods()
            elif choice_4 == '2':
                self.delete_loyalty_program()
            elif choice_4 == '3':
                self.delete_client()
            elif choice_4 == '4':
                self.delete_order()
            elif choice_4 == '5':
                break

    def run_generate(self):
        number = self.view.get_rand_number()
        if number.isdigit():
            self.model.generate_random_client(number)
        else:
            print("Error. You entered an incorrect type of data.")

    # Goods
    def add_goods(self):
        goods_name = self.view.get_goods_name()
        goods_description = self.view.get_goods_description()
        goods_price = self.view.get_goods_price()
        self.model.add_goods(goods_name, goods_description, goods_price)

    def view_goods(self):
        goods = self.model.get_all_goods()
        self.view.show_goods(goods)

    def edit_goods(self):
        goods_id_1 = self.view.get_goods_id()
        goods_name = self.view.get_goods_name()
        goods_description = self.view.get_goods_description()
        goods_price = self.view.get_goods_price()
        goods_id = goods_id_1
        if goods_price.isdigit() and goods_id.isdigit():
            self.model.edit_goods(goods_name, goods_description, goods_price, goods_id)
        else:
            print("Error. You entered an incorrect type.")

    def delete_goods(self):
        goods_id = self.view.get_goods_id()
        if goods_id.isdigit():
            self.model.delete_goods(goods_id)
        else:
            print("Error. Entered id is incorrect.")

    # Loyalty_program
    def add_loyalty_program(self):
        print("You can't manual add Loyalty program, because it automaticaly generates for each new client.")

    def view_loyalty_program(self):
        loyalty_program = self.model.get_all_loyalty_programs()
        self.view.show_loyalty_program(loyalty_program)

    def edit_loyalty_program(self):
        print("You can't manual edit Loyalty program, because it automaticaly generates for each new client.")

    def delete_loyalty_program(self):
        print("Loyalty program can be deleted only together with the client-owner of this program.")

    # Order
    def add_order(self):
        order_date = self.view.get_order_date()
        client_id = self.view.get_client_id()
        tmp = self.view.get_numb_of_pos()
        if tmp.isdigit() and client_id.isdigit() and tmp.isdigit:
            self.model.add_order(order_date, tmp, client_id)
        else:
            print("Error. You entered an incorrect type of data.")

    def view_order(self):
        order = self.model.get_all_order()
        self.view.show_order(order)

    def edit_order(self):
        order_id_1 = self.view.get_order_id()
        order_date = self.view.get_order_date()
        client_id = self.view.get_client_id()
        tmp = self.view.get_numb_of_pos()
        order_id = order_id_1
        if order_id.isdigit() and client_id.isdigit() and tmp.isdigit():
            self.model.edit_order(order_date, tmp, client_id, order_id)
        else:
            print("Error. You entered an incorrect type of data.")

    def delete_order(self):
        order_id = self.view.get_order_id()
        if order_id.isdigit():
            self.model.delete_order(order_id)
        else:
            print("Error. You entered an incorrect type of data.")

    # Client
    def add_client(self):
        client_name= self.view.get_client_name()
        client_ph_number = self.view.get_client_ph_number()
        client_sex = self.view.get_client_sex()
        if client_name.isalpha() and client_ph_number.isdigit() and client_sex.isalpha():
            self.model.add_client(client_name, client_ph_number, client_sex)
        else:
            print("Error. You entered an incorrect type of data.")

    def view_client(self):
        clients = self.model.get_all_clients()
        self.view.show_client(clients)

    def edit_client(self):
        client_id = self.view.get_client_id()
        client_name = self.view.get_client_name()
        client_ph_number = self.view.get_client_ph_number()
        client_sex = self.view.get_client_sex()
        if client_id.isdigit() and client_name.isalpha() and client_ph_number.isdigit() and client_sex.isalpha():
            self.model.edit_client(client_id, client_name, client_ph_number, client_sex)
        else:
            print("Error. You entered an incorrect type of data.")

    def delete_client(self):
        client_id = self.view.get_client_id()
        if client_id.isdigit():
            self.model.delete_client(client_id)
        else:
            print("Error. You entered an incorrect type of data.")


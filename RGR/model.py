import psycopg2
class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='Database_1',
            user='postgres',
            password='K201298k?',
            host='localhost',
            port=5432
        )

    # Goods
    def add_goods(self, name, description, price):
        c = self.conn.cursor()
        c.execute('INSERT INTO "Goods" ("goods_name", "goods_description", "goods_price") VALUES (%s, %s, %s)', (name, description, price))
        self.conn.commit()
        print("Good was added successfully!")

    def edit_goods(self, goods_name, goods_description, goods_price, goods_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Goods" WHERE "goods_id" = %s', (goods_id,))
        check_1 = c.fetchall()
        if check_1:
            c.execute('UPDATE "Goods" SET "goods_name"=%s, "goods_description"=%s, "goods_price"=%s WHERE "goods_id"=%s', (goods_name, goods_description, goods_price, goods_id))
            self.conn.commit()
            print("Good was edited successfully!")
        else:
            print("Error. This good doesn't exist.")

    def delete_goods(self, goods_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Goods" WHERE "goods_id" = %s', (goods_id,))
        check_1 = c.fetchall()
        c.execute('SELECT * FROM "Order_goods" WHERE "goods_id" = %s', (goods_id,))
        check_2 = c.fetchall()
        if check_1 and check_2:
            c.execute('DELETE FROM "Order_goods" WHERE "goods_id"=%s', (goods_id,))
            self.conn.commit()
            c.execute('DELETE FROM "Goods" WHERE "goods_id"=%s', (goods_id,))
            self.conn.commit()
            print("Good was deleted successfully!")
        else:
            print("Error. This good doesn't exist.")

    def get_all_goods(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Goods"')
        return c.fetchall()

    # Order
    def add_order(self, order_date, tmp, client_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Client" WHERE "client_id" = %s', (client_id,))
        check = c.fetchall()
        if not check:
            print("Error. No such client id.")
        else:
            sum = 0
            id_array = []
            for i in range(int(tmp)):
                tmp_1 = self.get_goods_id_for_order(i)
                id_array.append(tmp_1)
                c.execute('SELECT "goods_price" FROM "Goods" WHERE "goods_id" = %s', (tmp_1,))
                result = c.fetchone()
                sum = sum + result[0]
            c.execute('SELECT "loyalty_program_sum" FROM "Loyalty_program" WHERE "client_id" = %s', (client_id,))
            buf_1 = c.fetchone()[0]
            sum_1 = int(buf_1) + sum
            discount_level, sum_2 = self.count_discount_level(sum_1, sum)
            final_sum = int(buf_1) + sum_2
            c.execute('UPDATE "Loyalty_program" SET "loyalty_program_sum"=%s, "discount_level"=%s WHERE "client_id"=%s', (final_sum, discount_level, client_id))
            self.conn.commit()
            c.execute('INSERT INTO "Order" ("order_date", "order_price", client_id) VALUES (%s, %s, %s) RETURNING "order_id"', (order_date, sum_2, client_id))
            buf = c.fetchone()[0]
            self.conn.commit()
            for i in range(int(tmp)):
                c.execute('INSERT INTO "Order_goods" ("goods_id", "order_id") VALUES (%s, %s)', (id_array[i], buf))
            self.conn.commit()
            print("Order was added successfully!")

    def get_goods_id_for_order(self, buf):
        goods_id_for_order = input("Enter id of the {} position (good): ".format(buf + 1))
        return goods_id_for_order

    def count_discount_level(self, sum_1, sum):
        if int(sum_1) < 1500:
            return 0, int(sum)*1
        elif 1500 < int(sum_1) < 5000:
            return 1, int(sum)*0.95
        elif 5000 < int(sum_1) < 10000:
            return 2, int(sum)*0.9
        elif int(sum_1) > 10000:
            return 3, int(sum)*0.85

    def get_all_order(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Order"')
        return c.fetchall()

    def edit_order(self, order_date, tmp, client_id, order_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Order" WHERE "order_id" = %s', (order_id,))
        check_1 = c.fetchall()
        if check_1:
            sum = 0
            id_array = []
            for i in range(int(tmp)):
                tmp_1 = self.get_goods_id_for_order(i)
                id_array.append(tmp_1)
                c.execute('SELECT "goods_price" FROM "Goods" WHERE "goods_id" = %s', (tmp_1,))
                result = c.fetchone()
                sum = sum + result[0]
            c.execute('SELECT "client_id" FROM "Order" WHERE "order_id" = %s', (order_id,))
            tmp_2 = c.fetchone()[0]
            c.execute('SELECT "loyalty_program_sum" FROM "Loyalty_program" WHERE "client_id" = %s', (tmp_2,))
            buf_1 = c.fetchone()[0]
            c.execute('SELECT "order_price" FROM "Order" WHERE "order_id" = %s', (order_id,))
            buf_2 = c.fetchone()[0]
            sum_2 = int(buf_1) - int(buf_2)
            c.execute('UPDATE "Loyalty_program" SET "loyalty_program_sum"=%s WHERE "client_id"=%s',(sum_2, tmp_2))
            self.conn.commit()
            c.execute('SELECT "loyalty_program_sum" FROM "Loyalty_program" WHERE "client_id" = %s', (client_id,))
            tmp_3 = c.fetchone()[0]
            sum_3 = int(tmp_3) + int(sum)
            discount_level_1, sum_4 = self.count_discount_level(sum_3, sum)
            final_sum = int(tmp_3) + int(sum_4)
            c.execute('UPDATE "Loyalty_program" SET "loyalty_program_sum"=%s, "discount_level"=%s WHERE "client_id"=%s',(final_sum, discount_level_1, client_id))
            self.conn.commit()
            c.execute('UPDATE "Order" SET "order_date"=%s, "order_price"=%s, "client_id"=%s WHERE "order_id"=%s',(order_date, int(sum_4), client_id, order_id))
            self.conn.commit()
            c.execute('DELETE FROM "Order_goods" WHERE "order_id"=%s', (order_id,))
            self.conn.commit()
            for i in range(int(tmp)):
                c.execute('INSERT INTO "Order_goods" ("goods_id", "order_id") VALUES (%s, %s)', (id_array[i], order_id))
                self.conn.commit()
            print("Order was edited successfully!")
        else:
            print("Error. No such order id.")

    def delete_order(self, order_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Order" WHERE "order_id" = %s', (order_id,))
        check_1 = c.fetchall()
        c.execute('SELECT * FROM "Order_goods" WHERE "order_id" = %s', (order_id,))
        check_2 = c.fetchall()
        if check_1 and check_2:
            c.execute('SELECT "client_id" FROM "Order" WHERE "order_id" = %s', (order_id,))
            tmp_2 = c.fetchone()[0]
            c.execute('SELECT "loyalty_program_sum" FROM "Loyalty_program" WHERE "client_id" = %s', (tmp_2,))
            buf_1 = c.fetchone()[0]
            c.execute('SELECT "order_price" FROM "Order" WHERE "order_id" = %s', (order_id,))
            buf_2 = c.fetchone()[0]
            sum_2 = int(buf_1) - int(buf_2)
            discount_level, non_active = self.count_discount_level(sum_2, buf_2)
            c.execute('UPDATE "Loyalty_program" SET "loyalty_program_sum"=%s, "discount_level"=%s WHERE "client_id"=%s', (sum_2, discount_level, tmp_2))
            self.conn.commit()
            c.execute('DELETE FROM "Order_goods" WHERE "order_id"=%s', (order_id,))
            self.conn.commit()
            c.execute('DELETE FROM "Order" WHERE "order_id"=%s', (order_id,))
            self.conn.commit()
            print("Order was deleted successfully!")
        else:
            print("Error. This order doesn't exist.")


    # Client

    def add_client(self, client_name, client_ph_number, client_sex):
        c = self.conn.cursor()
        c.execute('INSERT INTO "Client" ("client_name", "client_ph_number", "client_sex") VALUES (%s, %s, %s) RETURNING "client_id"',(client_name, client_ph_number, client_sex))
        result = c.fetchone()[0]
        tmp = 0
        c.execute('INSERT INTO "Loyalty_program" ("client_id", "loyalty_program_sum", "discount_level") VALUES (%s, %s, %s)',(result, tmp, tmp))
        self.conn.commit()
        print("Client was added successfully!")

    def get_all_clients(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Client"')
        return c.fetchall()

    def edit_client(self, client_id, client_name, client_ph_number, client_sex):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Client" WHERE "client_id" = %s', (client_id,))
        check = c.fetchall()
        if check:
            c.execute('UPDATE "Client" SET "client_name"=%s, "client_ph_number"=%s, "client_sex"=%s WHERE "client_id"=%s', (client_name, client_ph_number, client_sex, client_id))
            self.conn.commit()
            print("Client was edited successfully!")
        else:
            print("Error. This client doesn't exist.")

    def delete_client(self, client_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Client" WHERE "client_id" = %s', (client_id,))
        check_1 = c.fetchall()
        c.execute('SELECT * FROM "Order" WHERE "client_id" = %s', (client_id,))
        check_2 = c.fetchall()
        c.execute('SELECT * FROM "Loyalty_program" WHERE "client_id" = %s', (client_id,))
        check_3 = c.fetchall()
        if check_1 and check_2 and check_3:
            c.execute('DELETE FROM "Loyalty_program" WHERE "client_id"= %s', (client_id,))
            self.conn.commit()
            c.execute('SELECT "order_id" FROM "Order" WHERE "client_id" = %s', (client_id,))
            tmp = c.fetchall()
            for tmp_1 in tmp:
                c.execute('DELETE FROM "Order_goods" WHERE "order_id"=%s', (tmp_1[0],))
                self.conn.commit()
            c.execute('DELETE FROM "Order" WHERE "client_id"=%s', (client_id,))
            self.conn.commit()
            c.execute('DELETE FROM "Client" WHERE "client_id"=%s', (client_id,))
            self.conn.commit()
            print("Client was deleted successfully!")
        elif check_1 and not check_2 and check_3:
            c.execute('DELETE FROM "Loyalty_program" WHERE "client_id"=%s', (client_id,))
            self.conn.commit()
            c.execute('DELETE FROM "Client" WHERE "client_id"=%s', (client_id,))
            self.conn.commit()
            print("Client was deleted successfully!")
        else:
            print("Error. This client doesn't exist.")

    # Loyalty_program

    def get_all_loyalty_programs(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Loyalty_program"')
        return c.fetchall()

    # Auto random generating clients

    def generate_random_client(self, number):
        c = self.conn.cursor()
        for i in range(int(number)):
            c.execute('INSERT INTO "Client" ("client_name", "client_ph_number", "client_sex") SELECT SUBSTRING(MD5(random()::text), 1, 10) AS client_name, CAST(LPAD(FLOOR(random() * 1000000000)::text, 9, \'0\') AS integer) AS client_ph_number, CASE WHEN random() > 0.5 THEN \'male\' ELSE \'female\' END AS client_sex RETURNING "client_id"')
            result = c.fetchone()[0]
            tmp = 0
            c.execute('INSERT INTO "Loyalty_program" ("client_id", "loyalty_program_sum", "discount_level") VALUES (%s, %s, %s)', (result, tmp, tmp))
            self.conn.commit()
        print("{} new random clients was generated successfully!".format(int(number)))


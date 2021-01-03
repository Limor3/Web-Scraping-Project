import pymysql.cursors
import configuration as cfg


class Sql_insert_products:
    @staticmethod
    def insert_data(cur, con, col_dict, query, col_list):
        """
        This function commit SQL query, and by that inserting data to table.
        :param cur: connection to cursor
        :param con: creating connection to sqlite
        :param col_dict: dict of product
        :param query: sql query
        :param col_list: list of columns names
        """
        values = [col_dict[val] if val in col_dict else UNKNOWN for val in col_list]
        values = tuple(values)
        cur.execute(query, values)
        con.commit()

    @staticmethod
    def update_fk(cur, con, query, item_id):
        """
        This function commit SQL query, and by that updating the foreign key (fk) in the tables by the products table.
        :param cur: connection to cursor
        :param con: creating connection to sqlite
        :param query: sql query
        :param item_id: item ID of the product in the products table
        """
        cur.execute(query, item_id)
        con.commit()

    @staticmethod
    def sql_insert(data_list_products, section):
        """
        The function insert the info of the products into the database, using the insert_data function.
        :param data_list_products: get list of dictionaries of all the info for each product.
               Every item in the list is for different product.
        :param section: the chosen section (dresses\tops\swimwear)
        """
        con = pymysql.connect(host=cfg.CONNECT_DB_HOST,
                              user=cfg.CONNECT_DB_USER,
                              password='Ab123456',
                              db=cfg.CONNECT_DB_DB,
                              charset=cfg.CONNECT_DB_CHARSET,
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        with cur:

            for dict in data_list_products:
                Sql_insert_products.insert_data(cur, con, dict, cfg.SQL_INSERT_TO_PRODUCTS, cfg.PRODUCT_COL_LIST)

            for dict in data_list_products:
                cur.execute(cfg.SQL_ITEM_ID_QUERY, dict[cfg.GET_WEB_ID])
                item_id = cur.fetchone()[cfg.GET_ITEM_ID]

                if section == cfg.SQL_DRESSES_SEC:
                    # adding more fields related to t-shirts and dresses to more_desc table:
                    Sql_insert_products.insert_data(cur, con, dict, cfg.SQL_INSERT_TO_COMMON_DESC, cfg.MORE_DESC_COL_LIST)
                    Sql_insert_products.update_fk(cur, con, cfg.SQL_UPDATE_FK_COMMON_DESC, item_id)

                    Sql_insert_products.insert_data(cur, con, dict, cfg.SQL_INSERT_TO_DRESSES, cfg.DRESSES_COL_LIST)
                    Sql_insert_products.update_fk(cur, con, cfg.SQL_UPDATE_FK_DRESSES, item_id)

                elif section == cfg.SQL_T_SHIRTS_SEC:
                    # adding more fields related to t-shirts and dresses to more_desc table:
                    Sql_insert_products.insert_data(cur, con, dict, cfg.SQL_INSERT_TO_COMMON_DESC, cfg.MORE_DESC_COL_LIST)
                    Sql_insert_products.update_fk(cur, con, cfg.SQL_UPDATE_FK_COMMON_DESC, item_id)

                    Sql_insert_products.insert_data(cur, con, dict, cfg.SQL_INSERT_TO_T_SHIRTS, cfg.TSHIRTS_COL_LIST)
                    Sql_insert_products.update_fk(cur, con, cfg.SQL_UPDATE_FK_T_SHIRTS, item_id)

                elif section == cfg.SQL_SWIMWEAR_SEC:
                    Sql_insert_products.insert_data(cur, con, dict, cfg.SQL_INSERT_TO_SWIMWEAR, cfg.SWIMWEAR_COL_LIST)
                    Sql_insert_products.update_fk(cur, con, cfg.SQL_UPDATE_FK_SWIMWEAR, item_id)



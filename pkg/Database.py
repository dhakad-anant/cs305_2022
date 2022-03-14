from flask_mysqldb import MySQL



class Database():
    def __init__(self,app):

        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'Mysql@12345'
        # app.config['MYSQL_USER'] = 'admin'
        # app.config['MYSQL_PASSWORD'] = 'Mysql@12345'
        app.config['MYSQL_DB'] = 'face'

        # Creating an MySQL object.
        self.mysql = MySQL(app)
        self.app = app

    def query(self, query_stmt, param=(), debug=False):
        """ This function return ALL ROWS from the result of query_stmt """

        rows = None
        print("**************************************query STARTS")
        cur = self.mysql.connection.cursor()
        try:
            print("Database connected successfully!")
            
            numRows = cur.execute(query_stmt, param) 
            print("numRows in result: ", numRows)
            
            rows = cur.fetchall()

            if debug:
                for row in rows:
                    print("#row: ", row)
                print("****rows")
                print(rows)

            # self.mysql.connection.commit() # to be used only when making a transactional query.
            cur.close()
        except Exception as e:
            print("Some Error!!: ", e)
            cur.close()
        print("Database closed successfully!")
        print("**************************************query ENDS")

        return rows 

    def transactional_query(self,query_stmt, param=()):
        """ """

        print("**************************************transactional_query STARTS")
        cur = self.mysql.connection.cursor()
        try:
            print("Database connected successfully!")
            
            numRows = cur.execute(query_stmt, param) 
            print("numRows effected: ", numRows)
            
            self.mysql.connection.commit() # to be used only when making a transactional query.
            cur.close()
        except Exception as e:
            print("Some Error!!: ", e)
            cur.close()
        print("Database closed successfully!")
        print("**************************************transactional_query ENDS")

    def create_table(self):
        query = (
            "DROP TABLE if exists images"
        )
        self.query(query_stmt=query)

        query = (
            """ create table images(
                image_id INT AUTO_INCREMENT PRIMARY KEY,
                person_name VARCHAR(255) NOT NULL,
                version INT NOT NULL,
                date VARCHAR(255),
                location VARCHAR(255),
                image_encoding VARCHAR(3200) NOT NULL
            ); """
        )
        self.query(query_stmt=query)

"""
create table images(
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    person_name VARCHAR(255) NOT NULL,
    version INT NOT NULL,
    date VARCHAR(255),
    location VARCHAR(255),
    image_encoding VARCHAR(3000) NOT NULL
);

self.insert('CREATE TABLE IF NOT EXISTS images(
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    person_name VARCHAR(255) NOT NULL, 
    version_no VARCHAR(255) NOT NULL, 
    location VARCHAR(255) NULL, 
    date_time VARCHAR(255) NULL, 
    image_encoding VARCHAR(5000) NOT NULL)')
"""

########################################################
#
#    CREATE TABLE `stock_research` (
#        `id` int(11) NOT NULL AUTO_INCREMENT,
#        `email` varchar(255) COLLATE utf8_bin NOT NULL,
#        `password` varchar(255) COLLATE utf8_bin NOT NULL,
#        PRIMARY KEY (`id`)
#    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
#    AUTO_INCREMENT=1 ;
#
#########################################################


import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
    user='admin',
    password='',
    db='test',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `stock_research` \
               (`rank`, `symbol`, `company`, `priceChange`, `buyOrder`, `sellOrder`, `newLink`, `timestamp`) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, ('123', '123', '123', '123', '123', '123', '123', '123'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT company FROM `stock_research`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
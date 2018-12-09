import pymysql

host="feeds.cj5cetvpc1ul.ap-northeast-2.rds.amazonaws.com"
port=3306
dbname="feeds"
user="feedAdmin"
password="pw4feedAdmin"

conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)
with conn.cursor() as cursor:
# 	 ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;
	sql1 = """
	CREATE TABLE `users` (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`email` varchar(255) COLLATE utf8_bin NOT NULL,
		`password` varchar(255) COLLATE utf8_bin NOT NULL,
		PRIMARY KEY (`id`)
	)"""
	cursor.execute(sql1)
	sql = "SHOW TABLES;"
	
	cursor.execute(sql)
	result = cursor.fetchone()
	print(result)
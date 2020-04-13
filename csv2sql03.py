import csv
import sqlite3


#def Database():
global conn, cursor
conn = sqlite3.connect("stockman.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS `parts` (REF_NO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
    	                                            PART_NO TEXT, DESCRIPTION TEXT, SUPPLIER TEXT, \
    	                                            ORDER_CODE TEXT, COST_PRICE TEXT, DELIVERED_PRICE TEXT, \
    	                                            STOCK TEXT, UNIT TEXT, LEADTIME TEXT, \
    	                                            LOCATION TEXT, REORDER_QTY TEXT, OWNER TEXT, \
    	                                            SUPPLIER2 TEXT, ORDER_CODE2 TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS `bom_items` (BOM_ITEM_NO INTEGER NOT NULL, BOM INTEGER NOT NULL, \
														PART_NO TEXT, DESCRIPTION TEXT, QTY_USED TEXT, CCTLOC TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS `bom_headers` (BOM_NO INTEGER NOT NULL, BOM TEXT, \
														   DESCRIPTION TEXT, CUSTOMER TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS `companys` (COMP_NO INTEGER NOT NULL, COMPANY TEXT, ADD1 TEXT, ADD2 TEXT, \
    	                                            	ADD3 TEXT, ADD4 TEXT, POST_CODE TEXT, PHONE TEXT, FAX TEXT, ACNO TEXT, \
    	                                            	PTERMS TEXT, EMAIL TEXT, WEB TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS `reports` (PART_REF INTEGER NOT NULL, \
    	                                            PART_NO TEXT, DESCRIPTION TEXT, SUPPLIER TEXT, \
    	                                            SUPPLIER_PN TEXT, QTY_REQUIRED INTEGER, QTY_IN_STOCK INTEGER, \
    	                                            QTY_TO_ORDER INTEGER, UNIT_PRICE REAL, D1 INTEGER, \
    	                                            D2 INTEGER, D3 INTEGER, S1 TEXT, \
    	                                            S2 TEXT, S3 TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS `transactions` (TRAN_NO INTEGER NOT NULL, PART INTEGER NOT NULL, QTY REAL, \
															BOM INTEGER NOT NULL, REF TEXT, TRAN_DATE TEXT)")

with open('./data/PARTS.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0

	for row in csv_reader:
		if line_count == 0:
			print('Started')
			line_count += 1
		else:
			while line_count != int(row[0]):
				cursor.execute("INSERT INTO `parts` (PART_NO) VALUES('deleted')")
				line_count += 1

			cursor.execute("INSERT INTO `parts` (PART_NO, DESCRIPTION, SUPPLIER, ORDER_CODE, COST_PRICE, DELIVERED_PRICE, STOCK,\
            									UNIT, LEADTIME, LOCATION, REORDER_QTY, OWNER, SUPPLIER2, ORDER_CODE2)\
												VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(row[1], row[2], row[3], row[4], row[5],\
												 row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]))
#  
			conn.commit()
#			print(row)
			line_count += 1

print(f'Processed parts {line_count} lines.')

with open('./data/BOM_ITEMS.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0

	for row in csv_reader:
		if line_count == 0:
			print('Started')
			line_count += 1
		else:

			cursor.execute("INSERT INTO `bom_items` (BOM_ITEM_NO, BOM, PART_NO, DESCRIPTION, QTY_USED, CCTLOC)\
										VALUES(?,?,?,?,?,?)",(int(row[0]), int(row[1]), row[2], row[3], row[4], row[5]))
  
			conn.commit()
#			print(row)
			line_count += 1

print(f'Processed parts {line_count} lines.')

with open('./data/BOM_HEADERS.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0

	for row in csv_reader:
		if line_count == 0:
			print('Started')
			line_count += 1
		else:

			cursor.execute("INSERT INTO `bom_headers` (BOM_NO, BOM, DESCRIPTION, CUSTOMER)\
										VALUES(?,?,?,?)",(int(row[0]), row[1], row[2], row[3]))
  
			conn.commit()
#			print(row)
			line_count += 1

print(f'Processed parts {line_count} lines.')

with open('./data/COMPANYS.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0

	for row in csv_reader:
		if line_count == 0:
			print('Started')
			line_count += 1
		else:

			cursor.execute("INSERT INTO `companys` (COMP_NO, COMPANY, ADD1, ADD2, ADD3, ADD4,\
										 POST_CODE, PHONE, FAX, ACNO, PTERMS, EMAIL, WEB)\
										VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(int(row[0]), row[1], row[2], row[3],\
												row[4], row[5],row[6], row[7], row[8], row[9], row[10], row[11], row[12]))
  
			conn.commit()
#			print(row)
			line_count += 1

print(f'Processed parts {line_count} lines.')

with open('./data/REPORTS.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0

	for row in csv_reader:
		if line_count == 0:
			print('Started')
			line_count += 1
		else:

			cursor.execute("INSERT INTO `reports` (PART_REF, PART_NO, DESCRIPTION, SUPPLIER, SUPPLIER_PN, QTY_REQUIRED,\
							 QTY_IN_STOCK, QTY_TO_ORDER, UNIT_PRICE, D1, D2, D3, S1, S2, S3)\
										VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(int(row[0]), row[1], row[2], row[3],row[4], int(row[5]),int(row[6]), \
												int(row[7]), float(row[8]), int(row[9]), int(row[10]), int(row[11]), row[12], row[13], row[14]))
  
			conn.commit()
#			print(row)
			line_count += 1

print(f'Processed parts {line_count} lines.')

with open('./data/TRANSACTIONS.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0

	for row in csv_reader:
		if line_count == 0:
			print('Started')
			line_count += 1
		else:

			cursor.execute("INSERT INTO `transactions` (TRAN_NO, PART, QTY, BOM, REF, TRAN_DATE)\
										VALUES(?,?,?,?,?,?)",(int(row[0]), int(row[1]), float(row[2]), int(row[3]), row[4], row[5]))
  
			conn.commit()
#			print(row)
			line_count += 1

print(f'Processed parts {line_count} lines.')
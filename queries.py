
			cursor.execute("INSERT INTO `parts` (PART_NO, DESCRIPTION, SUPPLIER, ORDER_CODE, COST_PRICE, DELIVERED_PRICE, STOCK,\
            									UNIT, LEADTIME, LOCATION, REORDER_QTY, OWNER, SUPPLIER2, ORDER_CODE2)\
												VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(row[1], row[2], row[3], row[4], row[5],\
												 row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]))

from xlwt import Workbook
wb = Workbook()
Sheet1 = wb.add_sheet('Sheet1')
Sheet1.write(0,0,'Hello')
wb.save('test.xls')

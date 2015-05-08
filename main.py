# -*- coding: utf-8 -*-
import os
from function import *
from pyunpack import Archive

db = databaseConnect()
cursor = db.cursor()

path = 'C:\\test\\'
zip_dir = os.listdir(path)
xml_dir = os.listdir(path + 'xml\\')
print "Начало обработки файлов из дирректории %s\n" % path
print "=====================================================\n"

for zip in zip_dir:
    zip = path + zip
    print 'Распаковка архива: ', zip
    #Archive(zip).extractall(path + 'xml\\')
    print 'Архив распакован в папку ', path + 'xml\\'
    for file in xml_dir:
        file = path + 'xml\\' + file
        print 'Корректировка и ана6лиз файла: ', file
        file_corrector(file)
        data = iterparse(file, events=('start', 'end'))
        Contracts = []
        for event, elem in data:
            if event == 'start' and elem.tag == 'contract':
                Contracts.append(ContractParse(data, extract_region(zip)))
        print 'Анализ файла завершен'
        print 'Количество контрактов в файле: {0}'.format(len(Contracts))
        # print extractRegion(zip)
        #for i in range(len(Contracts)):
        #   print 'Region: ',Contracts[i].Region, Contracts[i].Supplier.ContactInfo
        # print Contracts[0].Customer.inn, Contracts[0].Customer.RegNum, Contracts[0].Customer.kpp, Contracts[0].Customer.FullName
        # query = "INSERT INTO T_CUSTOMER (inn, reg_num, kpp, full_name) VALUES (%(inn)s,%(reg_num)s,%(kpp)s,'%(full_name)s')" % {'inn':Contracts[0].Customer.inn, 'reg_num':Contracts[0].Customer.RegNum, 'kpp':Contracts[0].Customer.kpp, 'full_name':Contracts[0].Customer.FullName}
        query = 'select id from t_customer;'
        print cursor.execute(query.encode('utf-8'))
        print dir(cursor)
        db.commit()
        print cursor.fetchone()
        #os.remove(file)
        break

    break
        # print "Корректировка файла: %s" % file
        # s1 = time.time()
        # file_corrector(file)
        # f1 = time.time()
        # #print "Файл откорректирован за %.3f сек\n" % (f1 - s1)
        # print ".....................................................\n"
        # data = iterparse(file, events=('start','end'))
        # data = iter(data)
        #
        # event,root = data.next()
        # Contracts = [None]
        # s2 = time.time()
        # for event,elem in data:
        #     if event == 'start' and elem.tag  == "contract":
        #         Contracts.append(ContractParse(data))
        # f2 = time.time()
        # print "Данные успешно извлечены за %.3f сек" % (f2-s2)
        # numOfContract = len(Contracts)-1
        # print "Количество контрактов в файле:", numOfContract
        #
        # print "Начало загрузки данных в графовую базу"
        # print "\nФайл успешно обработан\n"
        # break


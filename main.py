# -*- coding: utf-8 -*-
import os
from function import *
from pyunpack import Archive
import collections

def main():
    # #db = databaseConnect()
    # #cursor = db.cursor()
    # path = 'C:\\test\\'
    # zip_dir = os.listdir(path)
    # print "Начало обработки файлов из дирректории %s\n" % path
    # print "=====================================================\n"
    # len_zip = len(zip_dir)
    # for zip in zip_dir:
    #     len_zip -= 1
    #     print 'Осталось: ', len_zip
    #     zip = path + zip
    #     print 'Распаковка архива: ', zip
    #     Archive(zip).extractall('C:\\xml\\')
    #     print 'Архив распакован в папку ', 'C:\\xml\\'
    #     xml_dir = os.listdir('C:\\xml\\')
    #     for file in xml_dir:
    #         file_name = 'C:\\xml\\' + file
    #         if 'Procedure' in file_name or 'Cancel' in file_name:
    #             os.remove(file_name)
    #             continue
    #         print 'Корректировка и анализ файла: ', file_name
    #         file_corrector(file_name)
    #         data = iterparse(file_name, events=('start', 'end'))
    #         Contracts = []
    #         for event, elem in data:
    #             if event == 'start' and elem.tag == 'contract':
    #                 Contracts.append(ContractParse(data, extract_region(zip), zip, file))
    #         print 'Анализ файла завершен'
    #         print 'Количество контрактов в файле: {0}'.format(len(Contracts))
    #         # print extractRegion(zip)
            # query = "INSERT INTO T_CUSTOMER (inn, reg_num, kpp, full_name) VALUES (%(inn)s,%(reg_num)s,%(kpp)s,'%(full_name)s')" % {'inn':Contracts[0].Customer.inn, 'reg_num':Contracts[0].Customer.RegNum, 'kpp':Contracts[0].Customer.kpp, 'full_name':Contracts[0].Customer.FullName}
            # query = 'select id from t_customer;'
            # print cursor.execute(query.encode('utf-8'))
            # print dir(cursor)
            # db.commit()
            # print cursor.fetchone()[0]
            # os.remove(file_name)

            #break
        #break
    f = open(u'C:\\Проекты\\xml2mysql\\contracts_log.log')
    lines = f.readlines()
    f.close()
    tags = []
    for  i in lines:
        tags.append(i.split('\t')[-1].split('tag: ')[-1])
    c = collections.Counter()
    for i in tags:
        c[i] += 1
    f = open(u'C:\\Проекты\\xml2mysql\\contracts_log.log', 'a')
    f.write('\n\n\n\nИТОГ:\n')
    f.write('Всего отсутствует тегов: ' + str(len(tags)) + '\n')
    f.write('Из них:\n')
    for i in c:
        f.write(i.rstrip() + ': ' + str(c[i]) + '\n')
    f.close()
    # db.close()
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

if __name__ == '__main__':
    main()
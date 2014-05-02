# -*- coding: utf-8 -*-
from lxml.etree import iterparse
import os.path
import time

from classes import *
from function import *


graph_db = databaseConnect('GDB','Clear')


path = 'C:\\test\\'
dir = os.listdir(path)

print "Начало обработки файлов из дирректории %s\n" % path
print "=====================================================\n"

q=0
for file in dir:
    file = path + file
    print "Корректировка файла: %s" % file
    s1 = time.time()
    #fileCorrector(file)
    f1 = time.time()
    #print "Файл откорректирован за %.3f сек\n" % (f1 - s1)
    print ".....................................................\n"
    data = iterparse(file,events=('start','end'))
    data = iter(data)

    event,root = data.next()
    Contracts = [None]
    s2 = time.time()
    for event,elem in data:
        if event == 'start' and elem.tag  == "contract":
            Contracts.append(ContractParse(data))
    f2 = time.time()
    print "Данные успешно извлечены за %.3f сек" % (f2-s2)
    numOfContract = len(Contracts)-1
    print "Количество контрактов в файле:", numOfContract

    print "Начало загрузки данных в графовую базу"
    print "\nФайл успешно обработан\n"

    q = 0
    i = 1
    st = time.time()
    batch = neo4j.WriteBatch(graph_db)
    while i <= numOfContract:
        q1 = "MERGE (n:a {inn:'" + Contracts[i].Customer.inn + "'}) SET n.fullName='" + Contracts[i].Customer.FullName + "'"
        batch.append_cypher(q1.encode('utf-8'))


        q2 = "MERGE (m:a {inn:'" + Contracts[i].Supplier.inn + "'}) SET m.orgName='" + Contracts[i].Supplier.OrgName.replace('"','\\"').replace("'","\\'")+ "'"
        batch.append_cypher(q2.encode('utf-8'))

        q3 = "MERGE (n:a {inn:'"+ Contracts[i].Customer.inn +"'})-[r:contract{regNum:'"+ Contracts[i].RegNum+"'}]->(m:a {inn:'" + Contracts[i].Supplier.inn +\
             "'}) SET r.signDate='" + Contracts[i].SignDate + "', r.executionDate='" +\
             Contracts[i].Execution.Year + "-" + Contracts[i].Execution.Month  +   "', r.region='" + extractRegion(file)+ "', r.price='" + Contracts[i].Price + "'"

        batch.append_cypher(q3.encode('utf-8'))

        i = i + 1
        print "Осталось контрактов:", numOfContract-i
    time1 = time.time()

    batch.run()


    time2 = time.time()
    print "Batch отработал за %.3f секунд" % (time2 - time1)

    q = q + 1
    print "обработано ",q, 'файлов'
    fn = time.time()
    print "Файл обработан за ",fn - st

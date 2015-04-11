# -*- coding: utf-8 -*-
from lxml.etree import iterparse
#from py2neo import neo4j
from classes import *


# def databaseConnect (location,clear):
#     print "Подключение к графовой базе данных"
#     if location == 'GDB':
#         graph_db = neo4j.GraphDatabaseService("http://testmerge:4KmnY6jqwOHVB4lSkAdR@testmerge.sb01.stations.graphenedb.com:24789/db/data/")
#     else:
#         graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
#     if clear == 'Clear':
#         graph_db.clear()
#         print "ВНИМАНИЕ! БАЗА ДАННЫХ ПОЛНОСТЬЮ ОЧИЩЕНА! \n"
#     return graph_db

def file_corrector (filename):
    f = open(filename)
    text = f.read()
    f.close()
    text = text.replace("oos:", "").replace("<contract schemeVersion=\"1.0\">", "<contract>")\
                                    .replace("<contractSign>", "<contract>")\
                                    .replace("</contractSign>","</contract>")

    text = text.replace(text.split("<contract>", 1)[0], "<export>\n")
    f = open(filename, 'w')
    f.write(text)

def extractRegion(filename):
    region = filename.split('_inc_')
    region = region[0]
    if '__' in filename:
        region = region.split('__')
        region = region[1]
    else:
        region = region.split('_',1)
        region = region[1]
    return region

def extractDate(filename):
    date = filename.split('_inc_')
    date = date[1]
    date = date.split('_000000_')
    startDate = date[0]
    finishDate = date[1]
    date = startDate + '-' + finishDate
    return date

def ContractParse(data):
    isPrice = True
    currContract = Contract()
    for event,elem in data:
        # if event == 'end' and elem.tag == 'id':
        #     currContract.id = elem.text

        if event == 'end' and elem.tag == 'regNum':
            currContract.RegNum = elem.text
            continue

        # if event == 'end' and elem.tag == 'number':
        #     currContract.Number = elem.text
        #
        # if event == 'end' and elem.tag == 'publishDate':
        #     currContract.PublishDate = elem.text[:10]
        #
        if event == 'end' and elem.tag == 'signDate':
            currContract.SignDate = elem.text
            continue
        #
        # if event == 'end' and elem.tag == 'notificationNumber':
        #     currContract.NotNumber = elem.text

        if event == 'start' and elem.tag == 'customer':
            currContract.Customer = CustomerParse(data)
            continue

        if event == 'start' and elem.tag == 'execution':
            currContract.Execution = ExecutionParse(data)
            continue


        if event == 'end' and elem.tag == 'price' and isPrice == True:
            currContract.Price = elem.text
            continue

        if (event == 'start' and elem.tag == 'products') or (event == 'start' and elem.tag == 'finances'):
            isPrice = False
            continue

        # if event == 'end' and elem.tag == 'protocolDate':
        #     currContract.ProtocolDate = elem.text
        #

        #
        # if event == 'start' and elem.tag == 'product':
        #     currContract.Product = ProductParse(data)

        if event == 'start' and elem.tag == 'supplier':
            currContract.Supplier = SupplierParse(data)
            continue

        if event == 'end' and elem.tag == 'contract':
            return currContract

def CustomerParse(data):
    currCustomer = Customer()
    for event,elem in data:
        if event == 'start' and elem.tag == 'customer':
            currCustomer = Customer()

        # if event == 'end' and elem.tag == 'regNum':
        #     currCustomer.RegNum = elem.text
        #
        if event == 'end' and elem.tag == 'fullName':
            currCustomer.FullName = elem.text
            continue

        if event == 'end' and elem.tag == 'inn':
            currCustomer.inn = elem.text
            continue


        # if event == 'end' and elem.tag == 'kpp':
        #     currCustomer.kpp = elem.text

        if event == 'end' and elem.tag == 'customer':
            if currCustomer.inn == 'NoCustomerINN':
                currCustomer.inn = currCustomer.inn + "_" + str(CustomerParse.NoINNCustomerIndex)
                CustomerParse.NoINNCustomerIndex += 1
            return currCustomer
CustomerParse.NoINNCustomerIndex = 1

def SupplierParse(data):
    currSupplier = Supplier()
    for event,elem in data:
        if event == 'start' and elem.tag == 'supplier':
            currSupplier = Supplier()
            continue

        if event == 'end' and elem.tag == 'inn':
            currSupplier.inn = elem.text
            continue

        #
        # if event == 'end' and elem.tag == 'kpp':
        #     currSupplier.kpp = elem.text
        #
        if event == 'end' and elem.tag == 'organizationName':
            currSupplier.OrgName = elem.text
            continue
        #
        # if event == 'end' and elem.tag == 'countryFullName':
        #     currSupplier.CountryName = elem.text
        #
        # if event == 'end' and elem.tag == 'factualAddress':
        #     currSupplier.FactAddress = elem.text.replace("\\","\\\\")
        #
        # if event == 'end' and elem.tag == 'lastName':
        #     currSupplier.ContactInfo = elem.text + " "
        #
        # if event == 'end' and elem.tag == 'firstName':
        #     currSupplier.ContactInfo = currSupplier.ContactInfo + elem.text + " "
        #
        # if event == 'end' and elem.tag == 'middleName':
        #     currSupplier.ContactInfo = currSupplier.ContactInfo + elem.text
        #
        # if event == 'end' and elem.tag == 'contactPhone':
        #     currSupplier.ContactPhone = elem.text

        if event == 'end' and elem.tag == 'supplier':
            if currSupplier.inn == 'NoSupplierINN':
                currSupplier.inn = currSupplier.inn + "_" + str(SupplierParse.NoINNSupplierIndex)
                SupplierParse.NoINNSupplierIndex += 1
            return  currSupplier
SupplierParse.NoINNSupplierIndex = 1

def ProductParse(data):
    currProduct = Product()
    for event,elem in data:
        if event == 'start' and elem.tag == 'product':
            currProduct = Product()
            continue

        if event == 'end' and elem.tag == 'sid':
            currProduct.Sid = elem.text
            continue

        if event == 'end' and elem.tag == 'name':
            currProduct.Name = elem.text
            continue

        if event == 'end' and elem.tag == 'code':
            currProduct.Code = elem.text
            continue

        if event == 'end' and elem.tag == 'price':
            currProduct.Price = elem.text
            continue

        if event == 'end' and elem.tag == 'product':
            return currProduct

def ExecutionParse(data):
    currExecution = Execution()
    for event,elem in data:
        if event == 'end' and elem.tag == 'month':
            currExecution.Month = elem.text
            continue

        if event == 'end' and elem.tag == 'year':
            currExecution.Year = elem.text
            continue

        if event == 'end' and elem.tag == 'execution':
            return currExecution

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

def fileCorrector (filename):
    f = open(filename)
    text = f.read()
    f.close()

    f = open(filename, 'w')
    f.write(text.replace("oos:", "").replace("<contract schemeVersion=\"1.0\">", "<contract>")\
                                    .replace("<contractSign>", "<contract>")\
                                    .replace("</contractSign>","</contract>"))
    f.close()

    f = open(filename)
    line = f.readlines()
    f.close()

    f = open(filename)
    text3 = f.read()
    f.close()

    f = open(filename, 'w')
    f.write(text3.replace(line[0], '<export>\n'))
    f.close()

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
    data.next()
    for event,elem in data:
        # if event == 'end' and elem.tag == 'id':
        #     currContract.id = elem.text

        if event == 'end' and elem.tag == 'regNum':
            currContract.RegNum = elem.text

        # if event == 'end' and elem.tag == 'number':
        #     currContract.Number = elem.text
        #
        # if event == 'end' and elem.tag == 'publishDate':
        #     currContract.PublishDate = elem.text[:10]
        #
        if event == 'end' and elem.tag == 'signDate':
            currContract.SignDate = elem.text
        #
        # if event == 'end' and elem.tag == 'notificationNumber':
        #     currContract.NotNumber = elem.text

        if event == 'start' and elem.tag == 'customer':

            currContract.Customer = CustomerParse(data)

        if event == 'start' and elem.tag == 'execution':
            currContract.Execution = ExecutionParse(data)



        if event == 'end' and elem.tag == 'price' and isPrice == True:
            currContract.Price = elem.text



        if (event == 'start' and elem.tag == 'products') or (event == 'start' and elem.tag == 'finances'):
            isPrice = False

        # if event == 'end' and elem.tag == 'protocolDate':
        #     currContract.ProtocolDate = elem.text
        #

        #
        # if event == 'start' and elem.tag == 'product':
        #     currContract.Product = ProductParse(data)

        if event == 'start' and elem.tag == 'supplier':
            currContract.Supplier = SupplierParse(data)

        if event == 'end' and elem.tag == 'contract':
            return currContract

def CustomerParse(data):
    currCustomer = Customer()
    data.next()
    for event,elem in data:
        if event == 'start' and elem.tag == 'customer':
            currCustomer = Customer()

        # if event == 'end' and elem.tag == 'regNum':
        #     currCustomer.RegNum = elem.text
        #
        if event == 'end' and elem.tag == 'fullName':
             currCustomer.FullName = elem.text

        if event == 'end' and elem.tag == 'inn':
            currCustomer.inn = elem.text


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
    data.next()
    for event,elem in data:
        if event == 'start' and elem.tag == 'supplier':
            currSupplier = Supplier()

        if event == 'end' and elem.tag == 'inn':
            currSupplier.inn = elem.text

        #
        # if event == 'end' and elem.tag == 'kpp':
        #     currSupplier.kpp = elem.text
        #
        if event == 'end' and elem.tag == 'organizationName':
             currSupplier.OrgName = elem.text
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
    data.next()
    for event,elem in data:
        if event == 'start' and elem.tag == 'product':
            currProduct = Product()

        if event == 'end' and elem.tag == 'sid':
            currProduct.Sid = elem.text

        if event == 'end' and elem.tag == 'name':
            currProduct.Name = elem.text

        if event == 'end' and elem.tag == 'code':
            currProduct.Code = elem.text

        if event == 'end' and elem.tag == 'price':
            currProduct.Price = elem.text

        if event == 'end' and elem.tag == 'product':
            return currProduct

def ExecutionParse(data):
    currExecution = Execution()
    for event,elem in data:
        if event == 'end' and elem.tag == 'month':
            currExecution.Month = elem.text

        if event == 'end' and elem.tag == 'year':
            currExecution.Year = elem.text
        if event == 'end' and elem.tag == 'execution':
            return currExecution


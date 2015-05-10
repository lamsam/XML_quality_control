# -*- coding: utf-8 -*-
from lxml.etree import iterparse
import MySQLdb
from classes import *
import re


def databaseConnect():
    return MySQLdb.connect(charset='utf8',host="127.0.0.1",
            user="root", passwd="root", db="test")

def file_corrector (filename):
    try:
        reg = '<contract schemeVersion="[0-9]\.[0-9]">'
        f = open(filename)
        text = f.read()
        f.close()
        text = text.replace("oos:", "").replace("ns2:", "")\
             .replace("<contractSign>", "<contract>")\
             .replace("</contractSign>","</contract>")
        f = open(filename, 'w')
        f.write(text)
        f.close()
        f = open(filename)
        text = f.read()
        f.close()
        line = re.findall(reg, text)[0]
        text = text.replace(line, "<contract>")
        f = open(filename, 'w')
        f.write(text)
        f.close()
        f = open(filename)
        text = f.read()
        f.close()
        text = text.replace(text.split("<contract>", 1)[0], "<export>\n")
        f = open(filename, 'w')
        f.write(text)
        f.close()
    except IndexError:
        pass


def extract_region(filename):
    region = filename.split('contract_')[1]
    for i in region:
        if i.isdigit():
            region = region[:region.index(i) - 1]
            break
    return region

def extractDate(filename):
    date = filename.split('_inc_')
    date = date[1]
    date = date.split('_000000_')
    startDate = date[0]
    finishDate = date[1]
    date = startDate + '-' + finishDate
    return date

def log_write(str):
    f = open(u'C:\\Проекты\\xml2mysql\\contracts_log.log','a')
    f.write(str + '\n')
    f.close()

def create_log_str(zip, file, region, tag):
    str = region + '\t' + 'zip: ' + zip + '\t' + 'file: ' + file + '\t' + 'tag:' + tag
    return str

def ContractParse(data, region, zip, file):
    isPrice = True
    currContract = Contract()
    currContract.Region = region
    for event,elem in data:
        if event == 'end' and elem.tag == 'id':
            currContract.id = elem.text
            continue

        if event == 'end' and elem.tag == 'regNum':
            currContract.RegNum = elem.text
            continue

        if event == 'end' and elem.tag == 'number':
            currContract.Number = elem.text
            continue

        if event == 'end' and elem.tag == 'publishDate':
            currContract.PublishDate = elem.text[:10]
            continue

        if event == 'end' and elem.tag == 'signDate':
            currContract.SignDate = elem.text
            continue

        if event == 'end' and elem.tag == 'notificationNumber':
            currContract.NotNumber = elem.text
            continue

        if event == 'start' and elem.tag == 'customer':
            currContract.Customer = CustomerParse(data, region)
            continue

        if event == 'start' and elem.tag == 'execution':
            currContract.Execution = ExecutionParse(data, region)
            continue


        if event == 'end' and elem.tag == 'price' and isPrice == True:
            currContract.Price = elem.text
            continue

        if (event == 'start' and elem.tag == 'products') or \
                (event == 'start' and elem.tag == 'finances'):
            isPrice = False
            continue

        # if event == 'end' and elem.tag == 'protocolDate':
        #     currContract.ProtocolDate = elem.text
        #

        #
        # if event == 'start' and elem.tag == 'product':
        #     currContract.Product = ProductParse(data)

        if event == 'start' and elem.tag == 'supplier':
            currContract.Supplier = SupplierParse(data, region)
            continue

        if event == 'end' and elem.tag == 'contract':
            if currContract.id == None or currContract.id == 'None':
                log_write(create_log_str(zip, file, region, ' contract/id'))
            if currContract.RegNum == None or currContract.RegNum == 'None':
                log_write(create_log_str(zip, file, region, ' contract/regNum'))
            if currContract.Number == None or currContract.Number == 'None':
                log_write(create_log_str(zip, file, region, ' contract/number'))
            if currContract.PublishDate == None or currContract.PublishDate == 'None':
                log_write(create_log_str(zip, file, region, ' contract/publishDate'))
            if currContract.SignDate == None or currContract.SignDate == 'None':
                log_write(create_log_str(zip, file, region, ' contract/signDate'))
            if currContract.NotNumber == None or currContract.NotNumber == 'None':
                log_write(create_log_str(zip, file, region, ' contract/notificationNumber'))
            if currContract.Price == None or currContract.Price == 'None':
                log_write(create_log_str(zip, file, region, ' contract/price'))
            #---------------------------------------------------------------
            if currContract.Customer.RegNum == None or currContract.Customer.RegNum == 'None':
                log_write(create_log_str(zip, file, region, ' contract/customer/regNum'))
            if currContract.Customer.FullName == None or currContract.Customer.FullName == 'None':
                log_write(create_log_str(zip, file, region, ' contract/customer/fullName'))
            if currContract.Customer.inn == None or currContract.Customer.inn == 'None':
                log_write(create_log_str(zip, file, region, ' contract/customer/inn'))
            if currContract.Customer.kpp == None or currContract.Customer.kpp == 'None':
                log_write(create_log_str(zip, file, region, ' contract/customer/kpp'))
            #--------------------------------------------------------------
            if currContract.Supplier.inn == None or currContract.Supplier.inn == 'None':
                log_write(create_log_str(zip, file, region, ' contract/supplier/inn'))
            if currContract.Supplier.kpp == None or currContract.Supplier.kpp == 'None':
                log_write(create_log_str(zip, file, region, ' contract/supplier/kpp'))
            if currContract.Supplier.OrgName == None or currContract.Supplier.OrgName == 'None':
                log_write(create_log_str(zip, file, region, ' contract/supplier/organizationName'))
            if currContract.Supplier.CountryName == None or currContract.Supplier.CountryName == 'None':
                log_write(create_log_str(zip, file, region, ' contract/supplier/countryFullName'))
            if currContract.Supplier.FactAddress == None or currContract.Supplier.FactAddress == 'None':
                log_write(create_log_str(zip, file, region, ' contract/supplier/factualAddress'))
            if currContract.Supplier.ContactInfo == None or currContract.Supplier.ContactInfo == 'None':
                log_write(create_log_str(zip, file, region, ' contract/supplier/contactInfo'))
            if currContract.Supplier.ContactPhone == None or currContract.Supplier.ContactPhone == 'None':
                log_write(create_log_str(zip, file, region, ' contract/supplier/contactPhone'))
            return currContract



def CustomerParse(data, region):
    currCustomer = Customer()
    for event,elem in data:
        if event == 'start' and elem.tag == 'customer':
            currCustomer = Customer()
            continue

        if event == 'end' and elem.tag == 'regNum':
            currCustomer.RegNum = elem.text
            continue

        if event == 'end' and elem.tag == 'fullName':
            currCustomer.FullName = elem.text
            continue

        if event == 'end' and elem.tag == 'inn':
            currCustomer.inn = elem.text
            continue


        if event == 'end' and elem.tag == 'kpp':
            currCustomer.kpp = elem.text
            continue

        if event == 'end' and elem.tag == 'customer':
            return currCustomer

def SupplierParse(data, region):
    currSupplier = Supplier()
    for event,elem in data:
        if event == 'start' and elem.tag == 'supplier':
            currSupplier = Supplier()
            continue

        if event == 'end' and elem.tag == 'inn':
            currSupplier.inn = elem.text
            continue

        if event == 'end' and elem.tag == 'kpp':
            currSupplier.kpp = elem.text
            continue

        if event == 'end' and elem.tag == 'organizationName':
            currSupplier.OrgName = elem.text
            continue

        if event == 'end' and elem.tag == 'countryFullName':
            currSupplier.CountryName = elem.text
            continue

        if event == 'end' and elem.tag == 'factualAddress':
            currSupplier.FactAddress = elem.text.replace("\\","\\\\")
            continue

        if event == 'end' and elem.tag == 'lastName':
            currSupplier.ContactInfo = elem.text + ' '
            continue

        if event == 'end' and elem.tag == 'firstName':
            currSupplier.ContactInfo = currSupplier.ContactInfo + elem.text + " "
            continue

        if event == 'end' and elem.tag == 'middleName':
            currSupplier.ContactInfo = currSupplier.ContactInfo + elem.text
            continue

        if event == 'end' and elem.tag == 'contactPhone':
            currSupplier.ContactPhone = elem.text
            continue

        if event == 'end' and elem.tag == 'supplier':
            return currSupplier

def ProductParse(data, region):
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

def ExecutionParse(data, region):
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

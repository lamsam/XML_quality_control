# -*- coding: utf-8 -*-
import MySQLdb
from classes import *
import re

def databaseConnect():
    return MySQLdb.connect(charset='utf8', host="127.0.0.1",
            user="root", passwd="root", db="test")

def file_corrector (filename):
    try:
        reg = '<contract schemeVersion="[0-9]\.[0-9]">'
        with open(filename, 'r') as f:
            text = f.read()
        text = text.replace("oos:", "").replace("ns2:", "")\
             .replace("<contractSign>", "<contract>")\
             .replace("</contractSign>","</contract>")
        line = re.findall(reg, text)[0]
        text = text.replace(line, "<contract>")
        text = text.replace(text.split("<contract>", 1)[0], "<export>\n")
        with open(filename, 'w') as f:
            f.write(text)
    except IndexError:
        pass


def extract_region(filename):
    region = filename.split('contract_')[1]
    for i in region:
        if i.isdigit():
            region = region[:region.index(i) - 1]
            break
    return region

# def extractDate(filename):
#     date = filename.split('_inc_')
#     date = date[1]
#     date = date.split('_000000_')
#     startDate = date[0]
#     finishDate = date[1]
#     date = startDate + '-' + finishDate
#     return date

def log_write(str):
    with open('contracts_log.log','a') as f:
        f.write(str + '\n')

def create_log_str(zip, file, region, tag):
    str = region + '\t' + 'zip: ' + zip + '\t' + 'file: ' + file + '\t' + 'tag:' + tag
    return str

log_no_value = list() #None
log_no_tag = list() #'None'

def ContractParse(data, region, zip, file):
    global log_no_value
    global log_no_tag
    isPrice = True
    isRegNum = True
    isContractID = True
    currContract = Contract()
    currContract.Region = region
    for event,elem in data:
        if event == 'end' and elem.tag.upper() == 'ID' and isContractID == True:
            currContract.id = elem.text
            continue

        if event == 'start' and elem.tag.upper() == 'PLACER':
            isRegNum = False

        if event == 'end' and elem.tag.upper() == 'REGNUM' and isRegNum == True:
            currContract.RegNum = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'NUMBER':
            currContract.Number = elem.text
            isRegNum = True
            continue

        if event == 'end' and elem.tag.upper() == 'PUBLISHDATE':
            currContract.PublishDate = elem.text[:10]
            continue

        if event == 'end' and elem.tag.upper() == 'SIGNDATE':
            currContract.SignDate = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'NOTIFICATIONNUMBER':
            currContract.NotNumber = elem.text
            continue

        if event == 'start' and elem.tag.upper() == 'CUSTOMER':
            currContract.Customer = CustomerParse(data, region)
            continue

        if event == 'start' and elem.tag.upper() == 'EXECUTION':
            currContract.Execution = ExecutionParse(data, region)
            continue

        if event == 'end' and elem.tag.upper() == 'PRICE' and isPrice == True:
            currContract.Price = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'PROTOCOLDATE':
            currContract.ProtocolDate = elem.text
            continue

        if event == 'start' and elem.tag.upper() == 'SINGLECUSTOMERREASON':
            isContractID = False
            continue

        if event == 'start' and elem.tag.upper() == 'CURRENCY':
            currContract.Currency = CurrencyParse(data)
            isPrice = False
            continue

        if event == 'start' and elem.tag.upper() == 'PRODUCTS':
            currContract.Product = ProductParse(data, region)
            isPrice = False
            continue

        if event == 'start' and elem.tag.upper() == 'SUPPLIER':
            currContract.Supplier = SupplierParse(data, region)
            continue

        if event == 'end' and elem.tag.upper() == 'CONTRACT':
            if currContract.id == None:
                log_no_value.append('contract/id')
            elif currContract.id == 'None':
                log_no_tag.append('contract/id')

            if currContract.RegNum == None:
                log_no_value.append('contract/regNum')
            elif currContract.RegNum == 'None':
                log_no_tag.append('contract/regNum')

            if currContract.Number == None:
                log_no_value.append('contract/number')
            elif currContract.Number == 'None':
                log_no_tag.append('contract/number')

            if currContract.PublishDate == None:
                log_no_value.append('contract/publishDate')
            elif currContract.PublishDate == 'None':
                log_no_tag.append('contract/publishDate')

            if currContract.SignDate == None:
                log_no_value.append('contract/signDate')
            elif currContract.SignDate == 'None':
                log_no_tag.append('contract/signDate')

            if currContract.NotNumber == None:
                log_no_value.append('contract/notificationNumber')
            elif currContract.NotNumber == 'None':
                log_no_tag.append('contract/notificationNumber')

            if currContract.Price == None:
                log_no_value.append('contract/price')
            elif currContract.Price == 'None':
                log_no_tag.append('contract/price')
            #---------------------------------------------------------------

            if currContract.Customer.RegNum == None:
                log_no_value.append('contract/customer/regNum')
            elif currContract.Customer.RegNum == 'None':
                log_no_tag.append('contract/customer/regNum')

            if currContract.Customer.FullName == None:
                log_no_value.append('contract/customer/fullName')
            elif currContract.Customer.FullName == 'None':
                log_no_tag('contract/customer/fullName')

            if currContract.Customer.inn == None:
                log_no_value.append('contract/customer/inn')
            elif currContract.Customer.inn == 'None':
                log_no_tag.append('contract/customer/inn')

            if currContract.Customer.kpp == None:
                log_no_value.append('contract/customer/kpp')
            elif currContract.Customer.kpp == 'None':
                log_no_tag.append('contract/customer/kpp')

            #--------------------------------------------------------------

            if currContract.Supplier.inn == None:
                log_no_value.append('contract/supplier/inn')
            elif currContract.Supplier.inn == 'None':
                log_no_tag.append('contract/supplier/inn')

            if currContract.Supplier.kpp == None:
                log_no_value.append('contract/supplier/kpp')
            elif currContract.Supplier.kpp == 'None':
                log_no_tag.append('contract/supplier/kpp')

            if currContract.Supplier.OrgName == None:
                log_no_value.append('contract/supplier/organizationName')
            elif currContract.Supplier.OrgName == 'None':
                log_no_tag.append('contract/supplier/organizationName')

            if currContract.Supplier.CountryName == None:
                log_no_value.append('contract/supplier/countryFullName')
            elif currContract.Supplier.CountryName == 'None':
                log_no_tag.append('contract/supplier/countryFullName')

            if currContract.Supplier.FactAddress == None:
                log_no_value.append('contract/supplier/factualAddress')
            elif currContract.Supplier.FactAddress == 'None':
                log_no_tag.append('contract/supplier/factualAddress')

            if currContract.Supplier.ContactInfo == None:
                log_no_value.append('contract/supplier/contactInfo')
            elif currContract.Supplier.ContactInfo == 'None':
                log_no_tag.append('contract/supplier/contactInfo')

            if currContract.Supplier.ContactPhone == None:
                log_no_value.append('contract/supplier/contactPhone')
            elif currContract.Supplier.ContactPhone == 'None':
                log_no_tag.append('contract/supplier/contactPhone')

            if currContract.Currency.Code == None:
                log_no_value.append('contract/currency/code')
            elif currContract.Currency.Code == 'None':
                log_no_tag.append('contract/currency/code')

            if currContract.Currency.Name == None:
                log_no_value.append('contract/currency/name')
            elif currContract.Currency.Name == 'None':
                log_no_tag.append('contract/currency/name')

            return currContract

ContractParse.log_no_value = list() #None
ContractParse.log_no_tag = list() #'None'



def CustomerParse(data, region):
    currCustomer = Customer()
    for event,elem in data:
        if event == 'start' and elem.tag.upper() == 'CUSTOMER':
            currCustomer = Customer()
            continue

        if event == 'end' and elem.tag.upper() == 'REGNUM':
            currCustomer.RegNum = elem.text
            continue

        if event == 'end' and elem.tag == 'FULLNAME':
            currCustomer.FullName = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'INN':
            currCustomer.inn = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'KPP':
            currCustomer.kpp = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'CUSTOMER':
            return currCustomer

def SupplierParse(data, region):
    currSupplier = Supplier()
    for event,elem in data:
        if event == 'start' and elem.tag.upper() == 'SUPPLIER':
            currSupplier = Supplier()
            continue

        if event == 'end' and elem.tag.upper() == 'INN':
            currSupplier.inn = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'KPP':
            currSupplier.kpp = elem.text
            continue

        if event == 'end' and (elem.tag.upper() == 'ORGANIZATIONNAME' or elem.tag.upper() == 'FULLNAME'):
            currSupplier.OrgName = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'COUNTRYFULLNAME':
            currSupplier.CountryName = elem.text
            continue

        if event == 'end' and (elem.tag.upper() == 'FACTUALADDRESS' or elem.tag.upper() == 'ADDRESS'):
            currSupplier.FactAddress = elem.text.replace("\\","\\\\")
            continue

        if event == 'end' and elem.tag.upper() == 'LASTNAME':
            currSupplier.ContactInfo = elem.text + ' '
            continue

        if event == 'end' and elem.tag.upper() == 'FIRSTNAME':
            currSupplier.ContactInfo = currSupplier.ContactInfo + elem.text + " "
            continue

        if event == 'end' and elem.tag.upper() == 'MIDDLENAME':
            currSupplier.ContactInfo = currSupplier.ContactInfo + elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'CONTACTPHONE':
            currSupplier.ContactPhone = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'SUPPLIER':
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
    for event, elem in data:
        if event == 'end' and elem.tag == 'month':
            currExecution.Month = elem.text
            continue

        if event == 'end' and elem.tag == 'year':
            currExecution.Year = elem.text
            continue

        if event == 'end' and elem.tag == 'execution':
            return currExecution

def CurrencyParse(data):
    currCurrency = Currency()
    for event, elem in data:
        if event == 'end' and elem.tag.upper() == 'CODE':
            currCurrency.Code = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'NAME':
            currCurrency.Name = elem.text
            continue

        if event == 'end' and elem.tag.upper() == 'CURRENCY':
            return currCurrency
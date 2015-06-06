# -*- coding: utf-8 -*-
from classes import *
from re import findall
from collections import Counter
from os import mkdir, listdir
import os
from ftplib import FTP



def ftp_download(region, local_path):
    ftp = FTP('ftp.zakupki.gov.ru', 'free', 'free')
    ftp.cwd('fcs_regions')
    listing = list()
    ftp.cwd(region)
    ftp.cwd('contracts')
    ftp.retrlines("LIST", listing.append)
    for i in listing:
        if 'zip' in i:
            file_name = i.split()[-1]
            local_file_name =  local_path + '\\' + file_name
            lf = open(local_file_name, "wb")
            ftp.retrbinary("RETR " + file_name, lf.write, 8*1024)
            lf.close()

def log_write(str, region):
    with open(region + '_log.txt','a') as f:
        f.write(str + '\n')

def create_log_str(type_error, zip, file, tag):
    str = 'zip: ' + zip + '\t' + 'file: ' + file + '\t' + 'tag:' + tag + '\t' + 'type: ' + type_error
    return str

def file_corrector (filename):
    try:
        reg = '<contract schemeVersion="[0-9]\.[0-9]">'
        with open(filename, 'r') as f:
            text = f.read()
        text = text.replace("oos:", "").replace("ns2:", "")\
             .replace("<contractSign>", "<contract>")\
             .replace("</contractSign>","</contract>")
        line = findall(reg, text)[0]
        text = text.replace(line, "<contract>")
        text = text.replace(text.split("<contract>", 1)[0], "<export>\n")
        with open(filename, 'w') as f:
            f.write(text)
    except IndexError:
        pass

def write_in_log(region,count_contract,log_no_value, log_no_tag, log_error_in_value):
    c_for_no_value = Counter()
    for i in log_no_value:
        c_for_no_value[i] += 1

    c_for_no_tag = Counter()
    for i in log_no_tag:
        c_for_no_tag[i] += 1

    c_for_error_in_value = Counter()
    for i in log_error_in_value:
        c_for_error_in_value[i] +=1

    with open(region + '_log.txt', 'a') as f:
        f.write('\n\n\n==========================================\n\n\n')
        f.write('Проверено контрактов: {0}\n\n'.format(count_contract))
        f.write('Всего ошибок: {0}\n\n'.format(str(len(log_no_tag) + len(log_no_value) + len(log_error_in_value))))
        f.write('Отсутствует тегов: {0}\n'.format(str(len(log_no_tag))))
        for i in dict(c_for_no_tag):
            f.write('\t' + i + ': ' + str(c_for_no_tag[i]) + '\n')
        f.write('\nОтсутствует значений в тегах: {0}\n'.format(str(len(log_no_value))))
        for i in dict(c_for_no_value):
            f.write('\t' + i + ': ' + str(c_for_no_value[i]) + '\n')
        f.write('\nОшибки в имеющихся значениях: {0}\n'.format(str(len(log_error_in_value))))
        for i in dict(c_for_error_in_value):
            f.write('\t' + i + ': ' + str(c_for_error_in_value[i]) + '\n')


def extract_region(filename):
    region = filename.split('contract_')[1]
    for i in region:
        if i.isdigit():
            region = region[:region.index(i) - 1]
            break
    return region

log_no_value = list() #None
log_no_tag = list() #'None'
log_error_in_value = list()

def ContractParse(data, region, zip, file):
    global log_no_value, log_error_in_value, log_no_tag
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
            continue

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
            currContract.Customer = CustomerParse(data)
            continue

        if event == 'start' and elem.tag.upper() == 'EXECUTION':
            currContract.Execution = ExecutionParse(data)
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
            currContract.Product = ProductParse(data)
            isPrice = False
            continue

        if event == 'start' and elem.tag.upper() == 'SUPPLIER':
            currContract.Supplier = SupplierParse(data)
            continue

        if event == 'end' and elem.tag.upper() == 'CONTRACT':
            if currContract.id == None:
                log_write(create_log_str('no_value', zip, file, 'contract/id'), region)
                log_no_value.append('contract/id')
            elif currContract.id == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/id'), region)
                log_no_tag.append('contract/id')

            if currContract.RegNum == None:
                log_write(create_log_str('no_value', zip, file, 'contract/regNum'), region)
                log_no_value.append('contract/regNum')
            elif currContract.RegNum == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/regNum'), region)
                log_no_tag.append('contract/regNum')
            else:
                if not currContract.RegNum.isdigit():
                    log_write(create_log_str('error_in_value', zip, file, 'contract/regNum'), region)
                    log_error_in_value.append('contract/regNum')

            if currContract.Number == None:
                log_write(create_log_str('no_value', zip, file, 'contract/number'), region)
                log_no_value.append('contract/number')
            elif currContract.Number == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/number'), region)
                log_no_tag.append('contract/number')

            if currContract.PublishDate == None:
                log_write(create_log_str('no_value', zip, file, 'contract/publishDate'), region)
                log_no_value.append('contract/publishDate')
            elif currContract.PublishDate == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/publishDate'), region)
                log_no_tag.append('contract/publishDate')

            if currContract.SignDate == None:
                log_write(create_log_str('no_value', zip, file, 'contract/signDate'), region)
                log_no_value.append('contract/signDate')
            elif currContract.SignDate == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/signDate'), region)
                log_no_tag.append('contract/signDate')

            if currContract.NotNumber == None:
                log_write(create_log_str('no_value', zip, file, 'contract/notificationNumber'), region)
                log_no_value.append('contract/notificationNumber')
            elif currContract.NotNumber == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/notificationNumber'), region)
                log_no_tag.append('contract/notificationNumber')

            if currContract.Price == None:
                log_write(create_log_str('no_value', zip, file, 'contract/price'), region)
                log_no_value.append('contract/price')
            elif currContract.Price == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/price'), region)
                log_no_tag.append('contract/price')
            #---------------------------------------------------------------

            if currContract.Customer.RegNum == None:
                log_write(create_log_str('no_value', zip, file, 'contract/customer/regNum'), region)
                log_no_value.append('contract/customer/regNum')
            elif currContract.Customer.RegNum == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/customer/regNum'), region)
                log_no_tag.append('contract/customer/regNum')
            else:
                if not currContract.Customer.RegNum.isdigit():
                    log_write(create_log_str('error_in_value', zip, file, 'contract/customer/regNum'), region)
                    log_error_in_value.append('contract/customer/regMum')

            if currContract.Customer.FullName == None:
                log_write(create_log_str('no_value', zip, file, 'contract/customer/fullName'), region)
                log_no_value.append('contract/customer/fullName')
            elif currContract.Customer.FullName == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/customer/fullName'), region)
                log_no_tag.append('contract/customer/fullName')

            if currContract.Customer.inn == None:
                log_no_value.append('contract/customer/inn')
                log_write(create_log_str('no_value', zip, file, 'contract/customer/inn'), region)
            elif currContract.Customer.inn == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/customer/inn'), region)
                log_no_tag.append('contract/customer/inn')
            else:
                if not currContract.Customer.inn.isdigit():
                    log_write(create_log_str('error_in_value', zip, file, 'contract/customer/inn'), region)
                    log_error_in_value.append('contract/customer/inn')

            if currContract.Customer.kpp == None:
                log_write(create_log_str('no_value', zip, file, 'contract/customer/kpp'), region)
                log_no_value.append('contract/customer/kpp')
            elif currContract.Customer.kpp == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/customer/kpp'), region)
                log_no_tag.append('contract/customer/kpp')
            else:
                if not currContract.Customer.kpp.isdigit():
                    log_write(create_log_str('error_in_value', zip, file, 'contract/customer/kpp'), region)
                    log_error_in_value.append('contract/customer/kpp')

            #--------------------------------------------------------------

            if currContract.Supplier.inn == None:
                log_write(create_log_str('no_value', zip, file, 'contract/supplier/inn'), region)
                log_no_value.append('contract/supplier/inn')
            elif currContract.Supplier.inn == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/supplier/inn'), region)
                log_no_tag.append('contract/supplier/inn')
            else:
                if not currContract.Supplier.inn.isdigit():
                    log_write(create_log_str('error_in_value', zip, file, 'contract/supplier/inn'), region)
                    log_error_in_value.append('contract/supplier/inn')

            if currContract.Supplier.kpp == None:
                log_write(create_log_str('no_value', zip, file, 'contract/supplier/kpp'), region)
                log_no_value.append('contract/supplier/kpp')
            elif currContract.Supplier.kpp == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/supplier/kpp'), region)
                log_no_tag.append('contract/supplier/kpp')
            else:
                if not currContract.Supplier.kpp.isdigit():
                    log_write(create_log_str('error_in_value', zip, file, 'contract/supplier/kpp'), region)
                    log_error_in_value.append('contract/supplier/kpp')

            if currContract.Supplier.OrgName == None:
                log_write(create_log_str('no_value', zip, file, 'contract/supplier/orgName'), region)
                log_no_value.append('contract/supplier/organizationName')
            elif currContract.Supplier.OrgName == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/supplier/orgName'), region)
                log_no_tag.append('contract/supplier/organizationName')

            if currContract.Supplier.CountryName == None:
                log_write(create_log_str('no_value', zip, file, 'contract/supplier/countryFullName'), region)
                log_no_value.append('contract/supplier/countryFullName')
            elif currContract.Supplier.CountryName == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/supplier/countryFullName'), region)
                log_no_tag.append('contract/supplier/countryFullName')

            if currContract.Supplier.FactAddress == None:
                log_write(create_log_str('no_value', zip, file, 'contract/supplier/factualAddress'), region)
                log_no_value.append('contract/supplier/factualAddress')
            elif currContract.Supplier.FactAddress == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/supplier/factualAddress'), region)
                log_no_tag.append('contract/supplier/factualAddress')

            if currContract.Supplier.ContactInfo == None:
                log_write(create_log_str('no_value', zip, file, 'contract/supplier/contactInfo'), region)
                log_no_value.append('contract/supplier/contactInfo')
            elif currContract.Supplier.ContactInfo == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/supplier/contactInfo'), region)
                log_no_tag.append('contract/supplier/contactInfo')

            if currContract.Supplier.ContactPhone == None:
                log_write(create_log_str('no_value', zip, file, 'contract/supplier/contactPhone'), region)
                log_no_value.append('contract/supplier/contactPhone')
            elif currContract.Supplier.ContactPhone == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/supplier/contactPhone'), region)
                log_no_tag.append('contract/supplier/contactPhone')

            if currContract.Currency.Code == None:
                log_write(create_log_str('no_value', zip, file, 'contract/currency/code'), region)
                log_no_value.append('contract/currency/code')
            elif currContract.Currency.Code == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/currency/code'), region)
                log_no_tag.append('contract/currency/code')

            if currContract.Currency.Name == None:
                log_write(create_log_str('no_value', zip, file, 'contract/currency/name'), region)
                log_no_value.append('contract/currency/name')
            elif currContract.Currency.Name == 'None':
                log_write(create_log_str('no_tag', zip, file, 'contract/currency/code'), region)
                log_no_tag.append('contract/currency/name')

            return currContract

def CustomerParse(data):
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

def SupplierParse(data):
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
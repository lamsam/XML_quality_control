# -*- coding: utf-8 -*-
import os
from function import *
from lxml.etree import iterparse
from pyunpack import Archive

count_contract = 0
def main():
    region = 'Moskva'
    global count_contract
    try:
        os.mkdir('zip')
        os.mkdir('xml')
    except:
        pass
    path = 'zip'
    print 'Загрузка данных по региону: ', region
    ftp_download(region, os.path.abspath('zip'))
    zip_dir = os.listdir(path)
    print "Начало обработки файлов из дирректории %s\n" % path
    print "=====================================================\n"
    len_zip = len(zip_dir)
    for zip in zip_dir:
        print 'Осталось: ', len_zip, ' архивов'
        zip = os.path.abspath('zip') + '\\' + zip
        print 'Распаковка архива: ', zip
        Archive(zip).extractall('xml')
        print 'Архив распакован в папку {0}\n'.format('xml')
        xml_dir = os.listdir('xml')
        for file in xml_dir:
            file_name = os.path.abspath('xml')+ '\\' + file
            if 'Procedure' in file_name or 'Cancel' in file_name:
                os.remove(file_name)
                continue
            print 'Корректировка и анализ файла: ', file_name
            file_corrector(file_name)
            data = iterparse(file_name, events=('start', 'end'))
            Contracts = []
            for event, elem in data:
                if event == 'start' and elem.tag == 'contract':
                    Contracts.append(ContractParse(data, extract_region(zip), zip, file))
            count_contract += len(Contracts)
            print 'Анализ файла завершен'
            #os.remove(file_name)
        len_zip -= 1
        #os.remove(zip)
    print "Проверено контрактов: ", count_contract
    write_in_log(region, count_contract, log_no_value, log_no_tag, log_error_in_value)

if __name__ == '__main__':
    main()
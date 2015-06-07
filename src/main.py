# -*- coding: utf-8 -*-
import os
from function import *
from lxml.etree import iterparse
from pyunpack import Archive
import logging
import argparse
import os
import time
import Queue as _queue
from multiprocessing import Process, Queue, Event, cpu_count, Pool


count_contract = 0

def get_args():
    log.debug("Parse command-line arguments...")
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--region', required=True, type=str, dest='region')
    #add more arguments
    return parser.parse_args()


def timer(func):
    def time_inner(*args):
        before = time.time()
        func(*args)
        after = time.time()
        return after - before
    return time_inner

def remove_file(f_name):
    while True:
        try:
            os.remove(f_name)
            return
        except Exception:
            log.error('Cant remove file %s' % f_name)
    
#@timer
def parse(zip_name):
    log.debug('Start to parse [%s]' % zip_name)
    full_zip_name = os.path.join(os.path.abspath('zip'), zip_name)
    log.debug('Upzip archieve: %s' % full_zip_name)
    full_dir_name = os.path.join(os.path.abspath('xml'), zip_name.split('.')[0])
    if not os.path.exists(full_dir_name):
        os.makedirs(full_dir_name)
    Archive(full_zip_name).extractall(full_dir_name)
    log.debug('Archieve unpacked into [%s]' % full_dir_name)
    xml_dir = os.listdir(full_dir_name)
    for cont_file in xml_dir:
        while True:
            flag = 0
            try:
                full_cont_name = os.path.join(os.path.abspath(full_dir_name), cont_file)
                if 'Procedure' in full_cont_name or 'Cancel' in full_cont_name:
                    remove_file(full_cont_name)
                    break
                else:
                    #log.debug('Correction and analysis of file: %s' % full_cont_name)
                    file_corrector(full_cont_name)
                    data = iterparse(full_cont_name, events=('start', 'end'))
                    Contracts = []
                    for event, elem in data:
                        if event == 'start' and elem.tag == 'contract':
                            Contracts.append(ContractParse(data, extract_region(zip_name), zip_name, cont_file))
                    #log.debug('File analysis finished: %s' % full_cont_name)
                    #log.debug('Parsed: %i contracts...' % len(Contracts))
                    remove_file(full_cont_name)
                    break
            except Exception:
                log.error('Catch file error or something %s' % full_cont_name)
                time.sleep(1)
    os.rmdir(full_dir_name)

    #write_in_log(region, count_contract, log_no_value, log_no_tag, log_error_in_value)

def start_parse():
    path = 'zip'
    zip_dir = os.listdir(path)
    #print "Начало обработки файлов из дирректории %s\n" % path
    log.debug("Start processing files from directory %s\n" % path)
    pool = multiprocessing.Pool(cpu_count() * 2)
    pool.map(parse, zip_dir) 
        

def main():
    cmd_args = get_args()
    region = cmd_args.region or None 
    try:
        os.mkdir('zip')
        os.mkdir('xml')
    except:
        pass
    path = 'zip'
    #print 'Загрузка данных по региону: ', region
    log.debug('Start download data for region: %s' % region)
    ftp_download(region, os.path.abspath('zip'))
    start_parse()

log = create_logger("Main")

if __name__ == '__main__':
    main()

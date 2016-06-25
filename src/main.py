#!/usr/bin/env python
# coding: utf-8

"""
    Get historical data from Forexite.

    -referenced program
    http://kasege.net/forex/archives/2006/09/forexitedl_autoforexite.html

    I made the same program with only my necessary function, because
    AutoForexite is too old and stopped maintenance, can not work.
"""

# import urllib
import os
import sys
import urllib.request
import urllib.error
import zipfile

# *** config ***
_SYMBOL = 'USDJPY'
_START_YEAR = 2001
_START_MONTH = 1
_END_YEAR = 2007
_END_MONTH = 12

# output file path
output_filename = _SYMBOL + '_' + str(_START_YEAR) + str(_START_MONTH).zfill(
    2) + '_' + str(_END_YEAR) + str(_END_MONTH).zfill(2) + '.csv'
output_path = '../output/' + output_filename

if os.path.isfile(output_path):
    print('Output file exist. Please try again after delete.')
    sys.exit()


def to_mysql_format(filepath):
    """
    read downloaded file and output data with my format(price table of MySQL)
    :param filepath: downloaded file path after unzip
    :return:
    """
    print('Data converting...')
    f = open(filepath)
    lines = f.readlines()

    for line in lines:
        factor = line.split(',')
        symbol = factor[0]

        # symbol filter
        if symbol != _SYMBOL:
            continue

        # get symbol ID
        symbol_id = 0
        if symbol == 'EURUSD':
            symbol_id = 1
        if symbol == 'USDJPY':
            symbol_id = 2

        # convert datetime format
        year = factor[1][0:4]
        month = factor[1][4:6]
        date = factor[1][6:8]
        hour = factor[2][0:2]
        min = factor[2][2:4]
        datetime = year + '-' + month + '-' + date + ' ' + hour + ':' + min

        # price
        open_price = factor[3]
        high_price = factor[4]
        low_price = factor[5]
        close_price = factor[6]

        # write
        record = str(symbol_id) + ',' + datetime + ',' + open_price + ',' \
                 + high_price + ',' + low_price + ',' + close_price
        with open(output_path, 'a') as f:
            f.write(record)


# start loop of download and write file
cur_year = _START_YEAR
cur_month = _START_MONTH
while cur_year < _END_YEAR or cur_month < _END_MONTH:
    for i in range(1, 32):
        # get filename
        filename = str(i).zfill(2) + str(cur_month).zfill(2) \
                   + str(cur_year)[2:4] + '.zip'
        url = ('https://www.forexite.com/free_forex_quotes/' +
               str(cur_year) + '/' + str(cur_month).zfill(2) + '/' + filename)
        zip_save_path = '../download/' + filename
        unzip_save_path = '../download/' + filename.replace('zip', 'txt')

        # download
        if os.path.exists(unzip_save_path):
            print('{} is already downloaded.'.format(filename))
            # write file
            to_mysql_format(unzip_save_path)
            continue

        print('{} is downloading...'.format(filename))
        r = urllib.request.urlopen(url)

        # check existence zip file or 404 Not Found
        if r.info().get('Content-Type') != 'application/zip':
            # Content-Type is text/html, page is Not Found
            continue
        else:
            # save file
            file = open(zip_save_path, 'wb')
            file.write(r.read())

            # close
            r.close()
            file.close()

            # unzip
            ar = zipfile.ZipFile(zip_save_path)
            ar.extractall('../download/')

            print('{} is downloaded and unzipped.'.format(filename))

            # write file
            to_mysql_format(unzip_save_path)

    # next month
    print('getting file for {}/{} is done'.format(cur_year, cur_month))
    cur_month += 1
    if cur_month > 12:
        cur_month = 1
        cur_year += 1

print('Done!!!')

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# getting files from picofile.com

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import os, time
import subprocess
from timebudget import timebudget
#timebudget.set_quiet()  # don't show measurements as they happen

from rich.progress import track
from rich import print
import seedir as sd
from pathlib import  Path

from parser import *


def getDownloadLink(driver, url):
    driver.get(url)
    elem = driver.find_element_by_id('getDownloadLink')
    elem.click()
    time.sleep(2)
    elem = driver.find_element_by_id('downloadLink')
    return elem.get_attribute("href")


@timebudget
def picofile_dl():
    """
    Main entry point for execution.
    """
    
    args = parse_args()
    driver = Firefox()

    if args.filename:
        with open(args.filename) as fu:
            urls = [item.replace('\n', '') for item in fu.readlines()]
    elif args.url:
        urls = [args.url]
    downloadPath = Path(args.path)

    #for i, url in enumerate(urls, 1):
    if not downloadPath.exists():
        os.mkdir(downloadPath)
    # change directory to download path
    os.chdir(downloadPath)
    try:
        for i, url in enumerate(track(urls, description="Downloading..."), 1):
            showurl = f'{i}/{len(urls)}: {url}'
            try:
                href = getDownloadLink(driver, url)
                if args.verbose: print(f"    {href}")
            except exceptions.NoSuchElementException:
                print(f'{showurl} is expired')
                continue
            except exceptions.WebDriverException as exp:
                print(showurl, exp.msg, sep='\n')
                continue
            
            filename = href[href.rfind('/')+1:]
            #if (downloadPath/f"{filename}").is_file():
            # picofile converts `-` to `_` in the download url
            if list(downloadPath.glob(filename.replace('_', '*'))):
                print(f"{showurl} already exists!")
                continue

            cmd = ['axel', '-Ncvn4', href]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            o, e = proc.communicate()
            print(showurl)
            try:
                print("    Output: " + o.decode('ascii').split('\n')[-2])
            except:
                print("    Output: [err: ascii decode] ", o)
            if e: print(f"    Error: {e.decode('ascii')}")
            if proc.returncode: print(f"    code: {str(proc.returncode)}")

        print(f" DONE! ({args.path}) ".center(70, '='))
        sd.seedir(args.path) # print tree directory
        timebudget.report()
    finally: 
        driver.close()


if __name__ == '__main__':
    picofile_dl()
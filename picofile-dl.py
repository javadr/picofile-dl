#!/usr/bin/env python3
# getting files from picofile.com

import os
import subprocess
import time
import urllib
from pathlib import Path

import seedir as sd
from parsers import parse_args
from rich import print

from rich.progress import track
from selenium.common import exceptions
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from timebudget import timebudget
#timebudget.set_quiet()  # don't show measurements as they happen

def getDownloadLink(driver, url, password):
    driver.get(url)
    try:
        driver.find_element(By.ID, "filePassword").send_keys(password)
    except exceptions.NoSuchElementException:
        pass
    elem = driver.find_element(By.ID, "getDownloadLink")
    elem.click()
    time.sleep(2)
    elem = driver.find_element(By.ID, "downloadLink")
    return elem.get_attribute("href")


@timebudget
def picofile_dl():
    """Main entry point for execution."""  # noqa: D401
    args = parse_args()
    driver = Firefox()

    if args.filename:
        with open(args.filename) as fu:
            urls = [item.replace("\n", "").strip() for item in fu.readlines()]
    elif args.url:
        urls = [args.url]
    downloadPath = Path(args.path).absolute()
    downloadPath.mkdir(parents=True, exist_ok=True)
    # change directory to download path
    os.chdir(downloadPath)
    try:
        for i, url in enumerate(
                track(urls, description="[green]Downloading...[/green]"), 1):
            showurl = urllib.parse.unquote(f"{i}/{len(urls)}: {url}")
            try:
                href = getDownloadLink(driver, url, args.password)
                if not href:
                    print(f"{url} [blink][red]does not fetch![/red][/blink]")
                    continue
            except exceptions.NoSuchElementException:
                print(f"{showurl} [blink][red]is expired![/red][/blink]")
                continue
            except exceptions.WebDriverException as exp:
                print(showurl, exp.msg, sep="\n")
                continue

            filename = urllib.parse.unquote(href[href.rfind("/") + 1:])
            # picofile converts `-` to `_` in the download url
            if list(downloadPath.glob(filename.replace("_", "*"))):
                print(f"{showurl} already exists!")
                continue

            print(showurl)

            #cmd = ['axel', '-Ncvn4', href]
            cmd = ["wget", "-qnd", "--no-check-certificate", href]
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            o, e = proc.communicate()

            try:
                print("    Output: " + o.decode("ascii").split("\n")[-2])
            except:
                print("    Output: [err: ascii decode] ", o)
            if e:
                print(f"    Error: {e.decode('ascii')}")
            if proc.returncode:
                print(f"    code: {str(proc.returncode)}")

        print(f" DONE! ({args.path}) ".center(70, "="))
        sd.seedir(args.path)  # print tree directory
        timebudget.report()
    finally:
        driver.close()


if __name__ == "__main__":
    picofile_dl()

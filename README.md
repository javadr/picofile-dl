# Picofile Downloader

# Introduction

[Picofile](http://picofile.com) is a file server with 20GB free space. This script helps you to batch download.

# Installing dependencies

You can use the `pip` program to install the dependencies on your own.  They are all listed in the `requirements.txt` file.

To use this method, you would proceed as:o 

```python
pip install -r requirements.txt
```

To make Firefox work with Python selenium, you need to install the *geckodriver*. The geckodriver driver will start the real firefox browser and supports Javascript. The script relies on `axel` to download the files. Windows users should download [Axel4Windows](https://sourceforge.net/projects/axel4windows/) and put it in the Windows Path. 

# Running the script
Refer to `picofile-dl --help` for a complete, up-to-date reference on the runtime options supported by this utility.

Run the script to download a single file or a bunch of files:

```python
python picofile-dl.py [-h] [-u URL] [-f FILENAME] [--password PASSWORD] [-p PATH] [-v] [--verbose] 
```
`-u` a url from picofile server to be dowloaded

`-f` a file name including bunch of urls each in a line

`-p` path to save dowloaded files (Default: `/<TEMP>/picofile-dl`)

`--password` password set with the picofile URL

`-h` show help

`-v` output version information and exit

`--verbose` print extra information during the download progress

# Todo
* [X] Download files protected with password 

* [ ] An option do download the files with the browser (useful for windows user to get rid of installing `Axel4Windows`)

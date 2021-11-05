# Picofile Downloader

# Introduction

[Picofile](http://picofile.com) is a file server with 20GB free space. This script helps you to batch download.

# Installing dependencies

You can use the `pip` program to install the dependencies on your own.  They are all listed in the `requirements.txt` file.

To use this method, you would proceed as:o 

```python
pip install -r requirements.txt
```

To make Firefox work with Python selenium, you need to install the *geckodriver*. The geckodriver driver will start the real firefox browser and supports Javascript. The script uses `axel` to download the files. Windows users should download [Axel4Windows](https://sourceforge.net/projects/axel4windows/) and put it in the Windows Path. 

# Running the script
Refer to `picofile-dl --help` for a complete, up-to-date reference on the runtime options supported by this utility.

Run the script to download a single file or a bunch of files:

```python
python picofile-dl.py [-u URL] [-f FILENAME] [-p PATH] [-h] [-v] [--verbose] 
```
`-u` a url from picofile server to be dowloaded

`-f` a file name including bunch of urls each in a line

`-h` show help

`-v` show the current of the script

`--verbose` print extra information during the download progress

# Todo
[ ] Download files protected with password 

[ ] An option do download the files with the browser (useful for windows user to get rid of installing `Axel4Windows`)

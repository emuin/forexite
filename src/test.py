import urllib.request
import os

url = "https://www.forexite.com/free_forex_quotes/2001/03/210301.zip"

r = urllib.request.urlopen(url)
local = open(os.path.basename(url), 'wb')
local.write(r.read())

r.close()
local.close()
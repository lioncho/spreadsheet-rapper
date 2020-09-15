# run properly 
give github id , and google email for permission all access to me.

# lang
python3

# db 
google spread sheet ( new2.sheet )

# library
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from bs4 import BeautifulSoup
import time
import requests
import os
from selenium import webdriver
import warnings
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import gspread
import sqlite3
from sqlite3 import Error
from oauth2client.service_account import ServiceAccountCredentials
warnings.filterwarnings("ignore")

```
pip install bs4
```

# chromedriver
curreunt source is mac os

# run
python manage.py runserver (locally) <br>
python manage.py runserver 0.0.0.1:8000 (on server)


import pymongo
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

client = pymongo.MongoClient("mongodb://localhost:27017/")
DB     = client["Amazon"]
collection = DB["Books"]

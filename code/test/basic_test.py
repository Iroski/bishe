from util.DataSetLoader import DataLoader
import pandas as pd
from service.Crawler import Crawler
# loader=DataLoader('Iroski','bishe')
# loader.get_result()
# clawer=Crawler('alibaba','druid')
# result=clawer.get_issue(4585)
# print(result)

from util.client.DataCleaner import DataCleaner
cleaner=DataCleaner()
print(cleaner.clean_text("i have a pig."))
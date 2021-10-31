from util.ConfigDealer import ConfigDealer
import pandas as pd
import config
import threading
from util.DataLoader import start_getting_info
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
cd=ConfigDealer.get_instance()
data=cd.load_local_repos()

executor = ThreadPoolExecutor(max_workers=2)
all_task = [executor.submit(start_getting_info, (row['owner'],row['repo'])) for _,row in data.iterrows()]
wait(all_task, return_when=ALL_COMPLETED)
print("main finish")
# task1=executor.submit(start_getting_info,(('!','@')))
# print(task1.done())


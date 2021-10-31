from util.ConfigDealer import ConfigDealer
from util.DataLoader import start_getting_info

import argparse
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

if __name__ == '__main__':

    parser=argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--thread-num','-t',type=int,default=4)
    args=parser.parse_args()

    ConfigDealer.init()
    data = ConfigDealer.load_local_repos()
    executor = ThreadPoolExecutor(max_workers=args.thread_num)
    all_task = [executor.submit(start_getting_info, (row['owner'], row['repo'])) for _, row in data.iterrows()]
    wait(all_task, return_when=ALL_COMPLETED)
    print("main finish")
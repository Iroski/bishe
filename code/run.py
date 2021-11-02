from util.ConfigDealer import ConfigDealer
from util.DataLoader import start_getting_info
from util.logUtil import init_logger
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_EXCEPTION

if __name__ == '__main__':

    parser=argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--thread-num','-t',type=int,default=4)
    args=parser.parse_args()

    ConfigDealer.init()
    init_logger()

    data = ConfigDealer.load_local_repos()
    executor = ThreadPoolExecutor(max_workers=args.thread_num)
    all_task = [executor.submit(start_getting_info, (row['owner'], row['repo'])) for _, row in data.iterrows()]

    #增加装饰器后，只有非网络问题会抛出异常
    wait(all_task, return_when=FIRST_EXCEPTION)
    print("main finish")
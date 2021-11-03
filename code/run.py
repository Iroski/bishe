from util.ConfigDealer import ConfigDealer
from util.DataLoader import start_getting_info
from util.RepoLoader import RepoLoader
from util.logUtil import init_logger
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_EXCEPTION, ALL_COMPLETED


def init(args):
    ConfigDealer.init()
    init_logger()
    data = ConfigDealer.load_local_repos()
    if args.hot_repo:
        return RepoLoader.init(data, args.language, args.num,start_page=args.start_page)
    else:
        return data

if __name__ == '__main__':
    #todo 热榜，数据库验证
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--thread-num', '-tn', type=int, default=4)
    parser.add_argument('--hot-repo','-hr',action='store_true',default=False)
    parser.add_argument('--language','-l',type=str,default='java')
    parser.add_argument('--num','-n',type=int,default=0)
    parser.add_argument('--start-page','-sp',type=int,default=0)
    parser.add_argument('--stop-when-error','-sw',action='store_true',default=False)
    args = parser.parse_args()

    repo_data=init(args)

    executor = ThreadPoolExecutor(max_workers=args.thread_num)
    task_list=[]
    for _, row in repo_data.iterrows():
        task=executor.submit(start_getting_info, (row['owner'], row['repo']))
        task_list.append(task)
    # 增加装饰器后，只有非网络问题会抛出异常
    wait(task_list, return_when=FIRST_EXCEPTION)
    if args.stop_when_error:
        for task in reversed(task_list):
            task.cancel()
        wait(task_list, return_when=ALL_COMPLETED)
    print("main finish")

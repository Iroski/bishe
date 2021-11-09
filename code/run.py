from util.ConfigDealer import ConfigDealer
from util.DataLoader import start_getting_info
from util.RepoLoader import RepoLoader
from util.logUtil import get_log_file_name
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_EXCEPTION, ALL_COMPLETED
import multiprocessing


def init(args):
    ConfigDealer.init()

    data = ConfigDealer.load_local_repos()
    if args.hot_repo:
        return RepoLoader.init(data, args.language, args.num, start_page=args.start_page)
    else:
        return data


if __name__ == '__main__':
    # todo 最新验证，增加模式
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--thread-num', '-tn', type=int, default=4)
    parser.add_argument('--hot-repo', '-hr', action='store_true', default=False)
    parser.add_argument('--language', '-l', type=str, default='java')
    parser.add_argument('--num', '-n', type=int, default=60)
    parser.add_argument('--start-page', '-sp', type=int, default=0)
    parser.add_argument('--stop-when-error', '-sw', action='store_true', default=False)
    args = parser.parse_args()

    repo_data = init(args)

    processes: int = args.thread_num
    pool = multiprocessing.Pool(processes=processes)

    configDealer = ConfigDealer.get_instance()
    task_list = []
    for i, row in repo_data.iterrows():
        task_list.append(pool.apply_async(start_getting_info, (
        row['owner'], row['repo'], configDealer.get_token_ptr(), (i % processes), get_log_file_name(),)))

    if args.stop_when_error:
        for result in task_list:
            try:
                print(result.get())
            except Exception as e:
                print(e)
                pool.terminate()
                break
    pool.close()
    pool.join()

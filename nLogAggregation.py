# 標準入力から読み取って出力
import sys
import re
import time
import threading
import schedule

import datetime

logs = dict({})

keyword = re.compile(r"(GET|POST).+")

key_length = 40


def wait_stdin():
    print("wait_stdin")
    for line in sys.stdin:

        key = keyword.search(line)
        if key:
            if not logs.get(key.group()):
                wk_key = key.group()[0:key_length]
                logs[wk_key] = {"log": line, "cnt": 1}
            else:
                logs[key.group()]["cnt"] = logs[key.group()]["cnt"] + 1
        else:
            print("unkown logs")


def summry_logs():
    print("summry_log")
    schedule.every(10).seconds.do(
        lambda:
        # 定期実行処理
        output_logs()
    )
    # イベント監視
    while True:
        # 当該時間にタスクがあれば実行
        schedule.run_pending()
        # 1秒スリープ
        time.sleep(1)


def output_logs():
    print(str(datetime.datetime.now()) + " : count=" + str(len(logs)))

    # print(logs)

    if len(logs) is not 0:
        for line in logs.values():
            print(line["log"].replace("\n", "") + " : count=" + str(line["cnt"]))
        logs.clear()

    print(str(datetime.datetime.now()) + " : count finished .")


print(str(datetime.datetime.now()) + " start")

thread_stdin = threading.Thread(target=wait_stdin)
thread_summarylog = threading.Thread(target=summry_logs)
thread_stdin.start()
thread_summarylog.start()

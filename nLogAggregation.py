# 標準入力から読み取って出力
import sys
import re
import time
import threading
import datetime
import configparser

import schedule

logs = dict({})

config = configparser.SafeConfigParser()
config.read("nLogAggregation.conf")

regex_string = str(config.get("setting", "regex_string"))

key_length = int(config.get("setting", "key_length"))

watch_seconds = int(config.get("setting", "watch_seconds"))

keyword = re.compile(regex_string)


def wait_stdin():
    print("wait_stdin")
    for line in sys.stdin:
        key = keyword.search(line)
        if key:
            wk_key = key.group()[0:key_length]
            if not logs.get(wk_key):
                logs[wk_key] = {"log": line, "cnt": 1}
            else:
                logs[wk_key]["cnt"] = logs[wk_key]["cnt"] + 1
        else:
            print("unkown logs")


def summry_logs():
    print("summry_log")
    schedule.every(watch_seconds).seconds.do(
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

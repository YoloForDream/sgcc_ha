import logging
import logging.config
import sys
import time
import traceback
from datetime import datetime
import argparse
import schedule

from const import *
from data_fetcher import DataFetcher
from sensor_updator import SensorUpdator


def main():
    # 定义首次睡眠时间为10秒
    FIRST_SLEEP_TIME = 10
    try:
        # 获取从run.sh启动main.py脚本时候传入的配置参数信息
        parameters = process_arguments()
        PHONE_NUMBER = parameters[0]
        PASSWORD = parameters[1]
        HASS_URL = parameters[2]
        HASS_TOKEN = parameters[3]
        JOB_START_TIME = parameters[4]
        LOG_LEVEL = parameters[5] 

    except Exception as e:
        logging.error(f"读取配置信息失败，程序将退出，错误信息为{e}")
        sys.exit()

    logger_init(LOG_LEVEL)
    logging.info("程序开始，当前仓库版本为1.3.2，仓库地址为https://github.com/renhaiidea/sgcc_electricity")

    fetcher = DataFetcher(PHONE_NUMBER, PASSWORD)
    updator = SensorUpdator(HASS_URL, HASS_TOKEN)
    logging.info(f"当前登录的用户名为: {PHONE_NUMBER}，homeassistant地址为{HASS_URL},程序将在每天{JOB_START_TIME}执行")
    schedule.every().day.at(JOB_START_TIME).do(run_task, fetcher, updator)

    if datetime.now().time() < datetime.strptime(JOB_START_TIME, "%H:%M").time():
        logging.info(f"此次为首次运行，当前时间早于 JOB_START_TIME: {JOB_START_TIME}，{JOB_START_TIME}再执行！")
        schedule.every().day.at(JOB_START_TIME).do(run_task, fetcher, updator)
    else:
        logging.info(f"此次为首次运行，等待时间(FIRST_SLEEP_TIME)为{FIRST_SLEEP_TIME}秒，可在.env中设置")
        time.sleep(FIRST_SLEEP_TIME)
        run_task(fetcher, updator)

    while True:
        schedule.run_pending()
        time.sleep(1)

def process_arguments():
    # 创建参数解析器
    parser = argparse.ArgumentParser()

    # 添加命令行参数
    parser.add_argument("--PHONE_NUMBER", help="Phone number")
    parser.add_argument("--PASSWORD", help="Password")
    parser.add_argument("--HASS_URL", help="Hass URL")
    parser.add_argument("--HASS_TOKEN", help="Hass token")
    parser.add_argument("--JOB_START_TIME", help="Job start time")
    parser.add_argument("--LOG_LEVEL", help="Log level")

    # 解析命令行参数
    args = parser.parse_args()

    # 使用解析后的参数
    phone_number = args.PHONE_NUMBER
    password = args.PASSWORD
    hass_url = args.HASS_URL
    hass_token = args.HASS_TOKEN
    job_start_time = args.JOB_START_TIME
    log_level = args.LOG_LEVEL


    # 返回解析后的参数列表
    return [phone_number, password, hass_url, hass_token, job_start_time, log_level]

def run_task(data_fetcher: DataFetcher, sensor_updator: SensorUpdator):
    try:
        balance, usage = data_fetcher.fetch()
        sensor_updator.update(BALANCE_SENSOR_NAME, balance, BALANCE_UNIT,)
        sensor_updator.update(USAGE_SENSOR_NAME, usage, USAGE_UNIT)
        logging.info("state-refresh task run successfully!")
    except Exception as e:
        logging.error(f"state-refresh task failed, reason is {e}")
        traceback.print_exc()


def logger_init(level: str):
    logger = logging.getLogger()
    logger.setLevel(level)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    format = logging.Formatter("%(asctime)s  [%(levelname)-8s] ---- %(message)s", "%Y-%m-%d %H:%M:%S")
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(format)
    logger.addHandler(sh)


if __name__ == "__main__":
    main()

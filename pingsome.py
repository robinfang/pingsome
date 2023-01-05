import time
import yaml
from ping3 import ping, verbose_ping
from datetime import datetime, timedelta
import pandas as pd

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    host_list = config["hosts"]
    duration = config["duration_in_minutes"]
    print(host_list)
    # host = 'www.baidu.com'
    src_addr = None
    # src_addr = '192.168.56.1'
    # 简单用法 ping地址即可，超时会返回None 否则返回耗时，单位默认是秒
    start = datetime.now()
    all_result_dict = {}
    while datetime.now() - start < timedelta(minutes=duration):
        nowtime = datetime.now()
        print("ping @ {}".format(nowtime))
        all_result_dict.setdefault("t", []).append(nowtime)
        for host in host_list:
            result = ping(host, unit="ms", src_addr=src_addr)
            if result is None:
                print("ping 失败！")
            else:
                print("ping-{}成功，耗时{}ms".format(host, result))
            all_result_dict.setdefault(host, []).append(result)
        time.sleep(4)
    df = pd.DataFrame(all_result_dict)
    df.to_hdf("result.h5", "pingsome", "w")

import numpy as np
import pandas as pd
import subprocess, time
import scan_wifi_wpa as wpa
import csv
import time
### heatmap initialization
# file_path = './AP_BFS_2.4G.csv'    # file path need to be changed
file_path = './WiFi_2.4G.csv'    # file path need to be changed
data_24G = pd.read_csv(file_path).values
# print(len(data_24G))
# text = "紙巾\n米\n牛奶\n"
# targets = text.split("\n")
# targets.remove('')

# print(text)
# print("target",targets)

map_24G = np.zeros([32, 32, 4], dtype=float)
for i in range(len(data_24G)):
    map_24G[int(data_24G[i, 0]), int(data_24G[i, 1]), 0] = data_24G[i, 2]
    map_24G[int(data_24G[i, 0]), int(data_24G[i, 1]), 1] = data_24G[i, 3]
    map_24G[int(data_24G[i, 0]), int(data_24G[i, 1]), 2] = data_24G[i, 4]
    map_24G[int(data_24G[i, 0]), int(data_24G[i, 1]), 3] = data_24G[i, 5]

# file_path = './AP_BFS_5G.csv'    # file path need to be changed
file_path = './WiFi_5G.csv'    # file path need to be changed
data_5G = pd.read_csv(file_path).values
# print(len(data_5G))
map_5G = np.zeros([32, 32, 4], dtype=float)
for i in range(len(data_5G)):
    map_5G[int(data_5G[i, 0]), int(data_5G[i, 1]), 0] = data_5G[i, 2]
    map_5G[int(data_5G[i, 0]), int(data_5G[i, 1]), 1] = data_5G[i, 3]
    map_5G[int(data_5G[i, 0]), int(data_5G[i, 1]), 2] = data_5G[i, 4]
    map_5G[int(data_5G[i, 0]), int(data_5G[i, 1]), 3] = data_5G[i, 5]

### function part
def WiFi_position(map_24G, map_5G,
        RSSI_24G = np.zeros([4, 1]), RSSI_5G = np.zeros([4, 1])):
    error_map = np.zeros([31, 31], dtype=float)
    for i in range(31):
        for j in range(31):
            for k in range(4):
                if (RSSI_24G[k] != -1):
                    error_map[i, j] += abs(RSSI_24G[k] - map_24G[i, j, k])
                if (RSSI_5G[k] != -1):
                    error_map[i, j] += abs(RSSI_5G[k] - map_5G[i, j, k])
                # print(map_24G[i, j, k])
    temp = np.where(error_map == np.nanmin(error_map))
    # print(np.nanmin(error_map))
    return [temp[0][0], temp[1][0]]

# def scan_wifi():
#     # 使用sudo权限调用wpa_cli工具扫描WiFi
#     scan_output = subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan1', 'scan'], capture_output=True, text=True)
#     if scan_output.returncode != 0:
#         print("Error scanning WiFi networks.")
#         return None

#     # 获取扫描结果
#     scan_results = subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan1', 'scan_results'], capture_output=True, text=True)
#     if scan_results.returncode != 0:
#         print("Error fetching scan results.")
#         return None

#     return scan_results.stdout

# def filter_wifi(scan_output, target_ssids):
#     filtered_results = []
#     lines = scan_output.splitlines()
#     for target_ssid in target_ssids:
#         ssid = target_ssid
#         bssid = ""
#         signal_strength = -1
#         for line in lines:
#             fields = line.split()
#             if len(fields) >= 5 and target_ssid == fields[4]:
#                 ssid = fields[4]
#                 bssid = fields[0]
#                 signal_strength = fields[2]
#         filtered_results.append({'SSID': ssid, 'BSSID': bssid, 'Signal Strength': signal_strength})
#     return filtered_results


def scan_wifi_position(index):
    # data_file = open('data.csv',mode="a")
    # data_writer = csv.DictWriter(data_file,["time","AP1_2.4G", "AP2_2.4G", "AP3_2.4G"
    #                                         , "AP4_2.4G", "AP1_5G", "AP2_5G", "AP3_5G"
    #                                         , "AP4_5G", "pos"])
    #用舊資料
    # inputdata = pd.read_csv('./AP1~4 2.4G 5G.csv').values
    inputdata = pd.read_csv('./Path.csv').values
    if (index > len(inputdata)):
        index = len(inputdata)
    RSSI_24G = [inputdata[index,2],inputdata[index,3],inputdata[index,4],inputdata[index,5]]
    RSSI_5G = [inputdata[index,6],inputdata[index,7],inputdata[index,8],inputdata[index,9]]

    # 把RSSI 傳上去

    # 用掃描的RSSI
    # RSSI_24G = [-1,-1,-1,-1]
    # RSSI_5G = [-1,-1,-1,-1]
    # target_ssids = ["AP1_2.4G", "AP1_5G", "AP2_2.4G", "AP2_5G", "AP3_2.4G", "AP3_5G", "AP4_2.4G", "AP4_5G"]
    # scan_output = wpa.scan_wifi()
    # BIAS = 95
    # if scan_output:
    #     filtered_results = wpa.filter_wifi(scan_output, target_ssids)
    #     if filtered_results:
    #         for idx in range(0,len(target_ssids)-2,2):
    #             if (filtered_results[idx]['Signal Strength'] != -1):
    #                 print(filtered_results[idx]['SSID'],filtered_results[idx]['Signal Strength'])
    #                 RSSI_24G[idx//2] = int(filtered_results[idx]['Signal Strength']) + BIAS
    #             # else:
    #                 # print("\033[31m"+target_ssids[idx]+" NOT FOUND\033[0m")
    #             if (filtered_results[idx+1]['Signal Strength'] != -1):
    #                 print(filtered_results[idx+1]['SSID'],filtered_results[idx+1]['Signal Strength'])
    #                 RSSI_5G[idx//2] = int(filtered_results[idx+1]['Signal Strength']) + BIAS
    #             # else:
    #                 # print("\033[31m"+target_ssids[idx+1]+" NOT FOUND\033[0m")
    #     else:
    #         print(f"No WiFi networks found with SSID '{target_ssids}'.")
    # else:
    #     print("Scan failed.")
    # now = time.time()
    pos = WiFi_position(map_24G, map_5G,RSSI_24G, RSSI_5G)
    # data_writer.writerow({'time':now,"AP1_2.4G":RSSI_24G[0], "AP2_2.4G":RSSI_24G[1]
    #                      , "AP3_2.4G":RSSI_24G[2], "AP4_2.4G":RSSI_24G[3]
    #                      , "AP1_5G":RSSI_5G[0], "AP2_5G":RSSI_5G[1]
    #                      , "AP3_5G":RSSI_5G[2], "AP4_5G":RSSI_5G[3], 'pos':pos})
    print(RSSI_24G)
    print(RSSI_5G)
    # [inputdata[index,0],inputdata[index,1]]
    # return [[inputdata[index,0],inputdata[index,1]],WiFi_position(map_24G, map_5G,RSSI_24G, RSSI_5G)]
    return [pos]

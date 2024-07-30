import subprocess, time, pandas

def scan_wifi():
    # 使用sudo权限调用wpa_cli工具扫描WiFi
    scan_output = subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'scan'], capture_output=True, text=True)
    if scan_output.returncode != 0:
        print("Error scanning WiFi networks.")
        return None

    # 获取扫描结果
    scan_results = subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'scan_results'], capture_output=True, text=True)
    if scan_results.returncode != 0:
        print("Error fetching scan results.")
        return None

    return scan_results.stdout

#def filter_wifi(scan_output, target_ssids):
#    filtered_results = []
#    lines = scan_output.splitlines()
#    for target_ssid in target_ssids:
#        for line in lines:
#            fields = line.split()
#            if len(fields) >= 5 and fields[4] == target_ssid:
#                ssid = fields[4]
#                bssid = fields[0]
#                signal_strength = fields[2]
#                filtered_results.append({'SSID': ssid, 'BSSID': bssid, 'Signal Strength': signal_strength})
#    return filtered_results

def filter_wifi(scan_output, target_ssids):
    filtered_results = []
    lines = scan_output.splitlines()
    for target_ssid in target_ssids:
        ssid = target_ssid
        bssid = ""
        signal_strength = -1
        for line in lines:
            fields = line.split()
            if len(fields) >= 5 and target_ssid == fields[4]:
                ssid = fields[4]
                bssid = fields[0]
                signal_strength = fields[2]
        filtered_results.append({'SSID': ssid, 'BSSID': bssid, 'Signal Strength': signal_strength})
    return filtered_results


def scan_print():
    start = time.time()
    #target_ssid = "Brian0127"
    RSSI_24G = [-1,-1,-1,-1]
    RSSI_5G = [-1,-1,-1,-1]
    BIAS = 95
    target_ssids = ["Brian0127", "IVAN_5G", "IVAN_5G_Guest1", "IVAN"]
    #target_ssids = ["AP1_2.4G", "IVAN_5G", "AP2_2.4G", "AP2_5G", "AP3_2.4G", "AP3_5G", "AP4_2.4G", "AP4_5G"]
    scan_output = scan_wifi()
    if scan_output:
        filtered_results = filter_wifi(scan_output, target_ssids)
        if filtered_results:
            for idx in range(0,len(target_ssids),2):
                if (filtered_results[idx]['Signal Strength'] != -1):
                    print(filtered_results[idx]['SSID'],filtered_results[idx]['Signal Strength'])
                    RSSI_24G[idx//2] = int(filtered_results[idx]['Signal Strength']) + BIAS
                else:
                    print("\033[31m"+target_ssids[idx]+" NOT FOUND\033[0m")
                if (filtered_results[idx+1]['Signal Strength'] != -1):
                    print(filtered_results[idx+1]['SSID'],filtered_results[idx+1]['Signal Strength'])
                    RSSI_5G[idx//2] = int(filtered_results[idx+1]['Signal Strength']) + BIAS
                else:
                    print("\033[31m"+target_ssids[idx+1]+" NOT FOUND\033[0m")
                #if target_ssids[idx] in filtered_results['SSID']:
                #    print("FIND:",target_ssids[idx])
                #else:
                #    print("NOT FOUNT:",target_ssids[idx])
            #for result in filtered_results:
            #    print(result)
        else:
            print(f"No WiFi networks found with SSID '{target_ssids}'.")
    else:
        print("Scan failed.")
    end = time.time()
    print(RSSI_24G)
    print(RSSI_5G)
    print(end - start)

if __name__ == "__main__":
    while(1):
        scan_print()

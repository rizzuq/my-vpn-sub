import os
import re
import socket
import urllib.request
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_FILE = "sub.txt"

# Лучшие мировые базы, обновляемые каждые полчаса
SOURCES = [
    "https://raw.githubusercontent.com/w1770946466/v2ray/main/v2ray",
    "https://raw.githubusercontent.com/freev2ray/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/Borders-Freedom/Sub-Alternative-mirror/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/ToffeeV2ray/Toffee/main/Toffee.txt"
]

def check_single_server_ultra_fast(config_url):
    """Жесткий чекер скорости (0.2 секунды на ответ), отсеивающий n/a."""
    try:
        clean_url = config_url.replace("vless://", "http://").replace("trojan://", "http://").replace("ss://", "http://").replace("vmess://", "http://")
        parsed = urlparse(clean_url)
        netloc = parsed.netloc
        if "@" in netloc:
            netloc = netloc.split("@")[-1]
            
        if ":" in netloc:
            host, port_str = netloc.split(":")
            port = int(port_str)
        else:
            return None
            
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)  # Ультра-порог скорости
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            return config_url
    except:
        pass
    return None

def main():
    raw_content = ""
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                raw_content += response.read().decode('utf-8', errors='ignore') + "\n"
        except:
            continue

    key_pattern = r"(?:vless|trojan|ss|vmess)://[^\s\"']{15,}"
    found_configs = list(set(re.findall(key_pattern, raw_content)))
    
    working_pool = []
    
    # 40 параллельных потоков в облаке Гитхаба
    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = [executor.submit(check_single_server_ultra_fast, cfg) for cfg in found_configs[:500]]
        for future in as_completed(futures):
            res = future.result()
            if res:
                working_pool.append(res)
                if len(working_pool) >= 7:  # Сохраняем топ-7 самых быстрых серверов
                    break

    status_node = "vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_АКТИВНО_И_ПРОВЕРЕНО"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(status_node + "\n")
        for cfg in working_pool:
            f.write(cfg + "\n")

if __name__ == "__main__":
    main()

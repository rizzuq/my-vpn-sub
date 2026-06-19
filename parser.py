import urllib.request, json, re, random, time

# Твои источники
json_url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"
backup_urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_links.txt"
]

final_list = []

# Парсинг
try:
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        for _, region in data.items():
            if isinstance(region, dict) and "top10" in region:
                for item in region["top10"]:
                    # Добавляем только живые ключи
                    if isinstance(item, dict) and "key" in item:
                        final_list.append(item["key"])
except: pass

# Резервы
for url in backup_urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            keys = re.findall(r'(vless://[^\s"\x27\,]+|vmess://[^\s"\x27\,]+|trojan://[^\s"\x27\,]+)', content)
            final_list.extend(keys)
    except: continue

# Перемешиваем и ограничиваем
final_list = list(set(final_list))
random.shuffle(final_list)
final_list = final_list[:15] # Берем 15 штук

# "Хитрость": добавляем метку времени в комментарий, чтобы Хапп видел изменения
timestamp = f"# Updated at {time.strftime('%Y-%m-%d %H:%M:%S')}"
final_list.insert(0, timestamp)

with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_list))

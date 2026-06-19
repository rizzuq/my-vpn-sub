import urllib.request, json, re, random

# База автора (с пингом) + Резервы (агрегаторы)
json_url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"
backup_urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_links.txt"
]

final_list = []
print("Запуск умного фильтра быстрых серверов...")

# 1. Берем только быстрые из основы
try:
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        # Перебираем регионы
        for _, region in data.items():
            if isinstance(region, dict) and "top10" in region:
                for item in region["top10"]:
                    # ФИЛЬТР: Берем только если есть ключ и пинг < 200
                    if isinstance(item, dict) and item.get("latency_ms", 999) < 200:
                        final_list.append(item["key"])
except Exception as e:
    print(f"Основная база временно недоступна: {e}")

# 2. Если серверов мало, добираем из резервов
if len(final_list) < 10:
    for url in backup_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                keys = re.findall(r'(vless://[^\s"\x27\,]+|vmess://[^\s"\x27\,]+|trojan://[^\s"\x27\,]+)', content)
                final_list.extend(keys)
        except: continue

# Очистка и перемешивание
final_list = list(set(final_list))
random.shuffle(final_list)
final_list = final_list[:10]

# Запись
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_list))

print(f"🏁 Готово! В sub.txt записано {len(final_list)} самых быстрых серверов.")

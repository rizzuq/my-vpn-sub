import urllib.request, json, re

json_url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"
vless_links = []
print("Запуск бронебойного парсера...")

try:
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        raw_text = response.read().decode('utf-8', errors='ignore')
        all_keys = re.findall(r'(vless://[^\s"\x27\,]+|vmess://[^\s"\x27\,]+|ss://[^\s"\x27\,]+|trojan://[^\s"\x27\,]+)', raw_text)
        clean_keys = []
        for key in all_keys:
            if key not in clean_keys: clean_keys.append(key)
        vless_links = clean_keys[:5]
except Exception as e:
    print(f"Ошибка: {e}")

if not vless_links: vless_links.append("vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_ПУСТО")

with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(vless_links))

print(f"🏁 Сбор окончен! Сохранено ровно {len(vless_links)} серверов.")

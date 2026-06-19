import urllib.request, re, random, time

# Берем только крупные агрегаторы, первый проблемный сайт выкидываем
urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_links.txt"
]

all_keys = []
print("Начинаем жесткий отбор...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            text = response.read().decode('utf-8', errors='ignore')
            # Ищем только VLESS и VMESS
            keys = re.findall(r'(vless://[^\s]+|vmess://[^\s]+)', text)
            all_keys.extend(keys)
    except:
        pass

# Убираем дубликаты
unique_keys = list(set(all_keys))

# Перемешиваем, чтобы при каждом запуске были новые
random.shuffle(unique_keys)

# ЖЕСТКИЙ ЛИМИТ: берем ровно 5 штук
final_list = unique_keys[:5]

# Добавляем метку времени, чтобы Хапп видел, что файл реально обновился
timestamp = f"# Updated at {time.strftime('%Y-%m-%d %H:%M:%S')}"
final_list.insert(0, timestamp)

# Записываем в файл
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_list))

print("🏁 Готово! Записано строго 5 серверов.")

import urllib.request
import json
import random
import time

# Используем проверенную базу, где ключи лежат по отдельности в JSON
json_url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"
final_list = []

print("Начинаем чистый отбор...")

try:
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        # Обходим регионы в JSON (каждый регион имеет список top10)
        for region_name, region_data in data.items():
            if isinstance(region_data, dict) and "top10" in region_data:
                for item in region_data["top10"]:
                    if isinstance(item, dict) and "key" in item:
                        # Берем чистую ссылку vless
                        clean_key = item["key"].strip()
                        if clean_key.startswith("vless://"):
                            final_list.append(clean_key)
except Exception as e:
    print(f"Ошибка при чтении базы: {e}")

# Очищаем от дублей
final_list = list(set(final_list))

# Перемешиваем, чтобы при каждом запуске Гитхаба сервера были новые
random.shuffle(final_list)

# ЖЕСТКИЙ ЛИМИТ: берем строго 5 отдельных серверов
final_list = final_list[:5]

# Добавляем метку времени первой строкой, чтобы Hiddify видел обновление
timestamp = f"# Updated at {time.strftime('%Y-%m-%d %H:%M:%S')}"
final_list.insert(0, timestamp)

# Записываем аккуратно по строкам
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_list))

print(f"🏁 Готово! Записано строго {len(final_list) - 1} серверов + метка времени.")

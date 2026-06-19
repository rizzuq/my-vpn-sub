import urllib.request
import json
import re

# Прямая ссылка на сам JSON файл в репозитории автора
json_url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"

vless_links = []

print("Запуск сверхбыстрого JSON-парсера...")

try:
    # Запрашиваем файл, притворяясь обычным браузером
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        # Читаем и загружаем JSON структуру
        data = json.loads(response.read().decode('utf-8'))
        
        # Перебираем все страны в файле (baltics, germany, finland и т.д.)
        for region, region_data in data.items():
            if isinstance(region_data, dict) and "top10" in region_data:
                # Достаем ключи из списка лучших серверов региона
                for item in region_data["top10"]:
                    if "key" in item:
                        vless_links.append(item["key"])
                        
        print(f"Успешно обработан JSON. Найдено базовых ключей: {len(vless_links)}")

except Exception as e:
    print(f"Не удалось спарсить JSON напрямую: {e}")

# На всякий случай прогоним регуляркой по всему тексту, если структура изменится
if not vless_links:
    try:
        print("План Б: Поиск ключей через регулярные выражения...")
        with urllib.request.urlopen(req, timeout=15) as response:
            text_content = response.read().decode('utf-8')
            vless_links = re.findall(r'(vless://[^\s"\x27]+|vmess://[^\s"\x27]+|ss://[^\s"\x27]+|trojan://[^\s"\x27]+)', text_content)
    except Exception as e:
        print(f"Ошибка Плана Б: {e}")

# Очищаем от дубликатов
vless_links = list(set(vless_links))

# Если пусто, создаем рабочую заглушку
if not vless_links:
    vless_links.append("vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_ПУСТО_ПОВТОРЮ_ПОЗЖЕ")

# Записываем всё в итоговый текстовый файл для Hiddify
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(vless_links))

print(f"🏁 Сбор завершен! В sub.txt сохранено {len(vless_links)} уникальных конфигураций.")

import urllib.request
import json
import re

# Прямая ссылка на JSON файл
json_url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"

vless_links = []

print("Запуск исправленного JSON-парсера...")

try:
    # Запрашиваем файл, притворяясь браузером
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        # Читаем и загружаем JSON структуру
        data = json.loads(response.read().decode('utf-8'))
        
        # Перебираем всё, что есть в JSON
        for key, value in data.items():
            # Если это регион (внутри лежит словарь с "top10")
            if isinstance(value, dict) and "top10" in value:
                for item in value["top10"]:
                    if isinstance(item, dict) and "key" in item:
                        vless_links.append(item["key"])
            
            # Дополнительно проверяем одиночное поле "best", если оно есть в регионе
            elif isinstance(value, dict) and "best" in value:
                if isinstance(value["best"], str) and value["best"].startswith(("vless://", "vmess://", "ss://", "trojan://")):
                    vless_links.append(value["best"])
                        
        print(f"Успешно обработан JSON. Найдено базовых ключей: {len(vless_links)}")

except Exception as e:
    print(f"Ошибка при разборе структуры JSON: {e}")

# Запасной План Б: Если по структуре не вышло, собираем тупо регуляркой по всему тексту
if not vless_links:
    try:
        print("План Б: Сбор через регулярные выражения...")
        req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            text_content = response.read().decode('utf-8')
            # Ищет всё, что похоже на vless://, vmess:// и т.д.
            vless_links = re.findall(r'(vless://[^\s"\x27]+|vmess://[^\s"\x27]+|ss://[^\s"\x27]+|trojan://[^\s"\x27]+)', text_content)
            print(f"Регулярка нашла ключей: {len(vless_links)}")
    except Exception as e:
        print(f"Ошибка Плана Б: {e}")

# Удаляем дубликаты
vless_links = list(set(vless_links))

# Если вообще ничего не нашлось, создаем заглушку, чтобы Hiddify не ругался на пустой файл
if not vless_links:
    vless_links.append("vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_ПУСТО_ПОВТОРЮ_ПОЗЖЕ")

# Записываем всё в файл для Hiddify
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(vless_links))

print(f"🏁 Сбор завершен! В sub.txt сохранено {len(vless_links)} уникальных конфигураций.")

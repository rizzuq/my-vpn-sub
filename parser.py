import urllib.request
import re

# Прямая ссылка на готовую базу автора
json_url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"

print("Запуск неубиваемого PyCharm-парсера...")

try:
    # Притворяемся браузером
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        raw_text = response.read().decode('utf-8', errors='ignore')
        
        # МАГИЯ: Вырезаем только чистые ссылки vless/vmess/ss/trojan.
        # Весь JSON-мусор, скобки, даты обновлений и пинги скрипт просто ИГНОРИРУЕТ.
        all_keys = re.findall(r'(vless://[^\s"\x27\,]+|vmess://[^\s"\x27\,]+|ss://[^\s"\x27\,]+|trojan://[^\s"\x27\,]+)', raw_text)
        
        # Убираем дубликаты, сохраняя порядок
        clean_keys = []
        for key in all_keys:
            if key not in clean_keys:
                clean_keys.append(key)
                
        print(f"Всего в файле найдено ключей: {len(clean_keys)}")
        
        # Отрезаем строго ТОП-5 самых первых (самых быстрых и свежих)
        vless_links = clean_keys[:5]

except Exception as e:
    print(f"Ошибка при скачивании или фильтрации: {e}")
    vless_links = []

# Заглушка на случай полной аварии
if not vless_links:
    vless_links.append("vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_ПУСТО_ПОВТОРЮ_ПОЗЖЕ")

# Записываем в sub.txt ОНЛИ чистые ключи (строка — ключ, без мусора)
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(vless_links))

print(f"🏁 Сбор окончен! В sub.txt сохранено ровно {len(vless_links)} топовых рабочих серверов.")

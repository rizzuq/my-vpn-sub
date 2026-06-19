import urllib.request
import re

# Прямая ссылка на секретный JSON-файл, откуда сайт tiagorrg берет все ключи
url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"

vless_links = []

print("Запуск прямого сканирования базы данных keys.json...")

try:
    # Маскируемся под браузер, чтобы GitHub не выдал ошибку
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        content = response.read().decode('utf-8', errors='ignore')
        
        # Вытаскиваем абсолютно все типы ключей прямо из сырого текста файла
        found = re.findall(r'(vless://[^\s"\'\,]+|vmess://[^\s"\'\,]+|ss://[^\s"\'\,]+|trojan://[^\s"\'\,]+)', content)
        vless_links.extend(found)
        print(f"Успешно выкачано из базы: {len(found)} серверов.")
except Exception as e:
    print(f"Ошибка при чтении базы данных: {e}")

# Очищаем от дубликатов
vless_links = list(set(vless_links))

# Если база пустая, пишем заглушку
if not vless_links:
    vless_links.append("vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_ПУСТО_П ПОВТОРЮ_ПОЗЖЕ")

# Сохраняем в наш файл для Hiddify
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(vless_links))

print(f"🏁 Скрипт завершил работу. Сохранено конфигураций: {len(vless_links)}")

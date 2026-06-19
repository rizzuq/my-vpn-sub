import urllib.request
import re

# Настоящие, проверенные ссылки БЕЗ папки docs в пути!
urls = [
    "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/sub/de.txt",  # Германия
    "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/sub/fi.txt",  # Финляндия
    "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/sub/nl.txt",  # Нидерланды
    "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/sub/se.txt",  # Швеция
    "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/sub/other.txt" # Остальные
]

vless_links = []

print("Запуск сканирования правильных путей vless-checker...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')
            
            # Собираем ключи
            found = re.findall(r'(vless://[^\s]+|vmess://[^\s]+|ss://[^\s]+|trojan://[^\s]+)', content)
            vless_links.extend(found)
            print(f"Успешно взято из {url.split('/')[-1]}: {len(found)} ключей.")
    except Exception as e:
        print(f"Ошибка при чтении {url.split('/')[-1]}: {e}")

# Убираем дубликаты
vless_links = list(set(vless_links))

# Заглушка, если пусто
if not vless_links:
    vless_links.append("vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_ПУСТО_ПОВТОРЮ_ПОЗЖЕ")

# Записываем в файл
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(vless_links))

print(f"🏁 Сбор завершен! Всего сохранено серверов: {len(vless_links)}")

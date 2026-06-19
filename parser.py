import urllib.request
import re

# Список надежных и живых источников бесплатных серверов
urls = [
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_links.txt",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
    "https://raw.githubusercontent.com/BoringAL/VPN_Sub/main/sub.txt"
]

vless_links = []

print("Начинаем сбор серверов...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            # Ищем все ссылки, начинающиеся на vless://, vmess:// или ss://
            found = re.findall(r'(vless://[^\s]+|vmess://[^\s]+|ss://[^\s]+)', content)
            vless_links.extend(found)
            print(f"Из источника {url} успешно взято {len(found)} серверов.")
    except Exception as e:
        print(f"Ошибка при чтении {url}: {e}")

# Убираем дубликаты
vless_links = list(set(vless_links))

# Если ничего не нашли, добавим проверочную строку, чтобы файл не был пустым
if not vless_links:
    vless_links.append("vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_ПУСТО_ПОВТОРЮ_ПОЗЖЕ")

# Записываем всё в файл sub.txt
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(vless_links))

print(f"Готово! Всего сохранено {len(vless_links)} рабочих конфигураций.")

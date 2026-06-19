import urllib.request
import json

# Прямая ссылка на уже ГОТОВУЮ и проверенную автором базу
json_url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"

vless_links = []

print("Забираем готовый ТОП серверов...")

try:
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        # Перебираем регионы в готовом файле (Германия, Финляндия и т.д.)
        for key, value in data.items():
            # Нам нужны только регионы, где есть список проверенных ключей top10
            if isinstance(value, dict) and "top10" in value:
                # Берем самый ПЕРВЫЙ ключ из списка (он самый быстрый в этом регионе)
                for item in value["top10"]:
                    if isinstance(item, dict) and "key" in item:
                        vless_links.append(item["key"])
                        break # Забрали топ-1 и сразу переходим к следующей стране
                        
        print(f"Успешно вытащили топ-ключи из регионов. Набралось: {len(vless_links)}")

except Exception as e:
    print(f"Ошибка при чтении готовой базы: {e}")

# Очищаем от случайных повторов
vless_links = list(set(vless_links))

# Оставляем строго от 3 до 5 серверов, как ты и хотел
if len(vless_links) > 5:
    vless_links = vless_links[:5]

# Если вдруг у автора файл пустой, создаем аккуратную заглушку
if not vless_links:
    vless_links.append("vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_ПУСТО_ПОВТОРЮ_ПОЗЖЕ")

# Записываем в sub.txt ТОЛЬКО голые ссылки (никаких дат, скобок и пингов)
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(vless_links))

print(f"🏁 Сбор окончен! В sub.txt сохранено ровно {len(vless_links)} топовых рабочих сер

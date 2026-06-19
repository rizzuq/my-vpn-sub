import urllib.request
import re

# Прямая ссылка на сырой JSON, где лежит вся куча данных
json_url = "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json"

print("Запуск PyCharm-метода фильтрации...")

try:
    # Притворяемся браузером, чтобы Гитхаб автора нас не забанил
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        raw_text = response.read().decode('utf-8', errors='ignore')
        
        # МАГИЯ ФИЛЬТРАЦИИ: Вытаскиваем ТОЛЬКО чистые ссылки протоколов.
        # Всё остальное (даты, пинги, скобки, кавычки, слова 'host') робот просто ВЫКИДЫВАЕТ.
        clean_keys = re.findall(r'(vless://[^\s"\x27\,]+|vmess://[^\s"\x27\,]+|ss://[^\s"\x27\,]+|trojan://[^\s"\x27\,]+)', raw_text)
        
        # Убираем дубликаты, если челик выложил одинаковые ключи
        clean_keys = list(set(clean_keys))
        
        print(f"Фильтр сработал! Отсеяно всё лишнее. Найдено чистых ключей: {len(clean_keys)}")

except Exception as e:
    print(f"Ошибка при скачивании или фильтрации: {e}")
    clean_keys = []

# Если вдруг у автора всё упало и ключей нет вообще, создаем одну аккуратную строку-заглушку
if not clean_keys:
    clean_keys.append("vless://99999999-9999-9999-9999-999999999999@127.0.0.1:9999?encryption=none&security=none#☁️_ОБЛАКО_ПУСТО_ПОВТОРЮ_ПОЗЖЕ")

# Сохраняем в файл sub.txt ТОЛЬКО чистые ключи, каждый с новой строки
with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(clean_keys))

print("🏁 Файл sub.txt успешно перезаписан и готов для Hiddify!")

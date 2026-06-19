import urllib.request, re, random

# Список источников: если один упадет, другие подхватят
urls = [
    "https://raw.githubusercontent.com/tiagorrg/vless-checker/main/docs/keys.json",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_links.txt"
]

all_extracted_keys = []

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            # Ищем только чисто VLESS/VMESS/TROJAN ссылки
            keys = re.findall(r'(vless://[^\s"\x27\,]+|vmess://[^\s"\x27\,]+|trojan://[^\s"\x27\,]+)', content)
            all_extracted_keys.extend(keys)
    except: continue

# Оставляем только уникальные
unique_keys = list(set(all_extracted_keys))
random.shuffle(unique_keys)

# Берем 10 случайных, чтобы было из чего выбрать в Hiddify
final_list = unique_keys[:10] if len(unique_keys) >= 10 else unique_keys

with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_list))

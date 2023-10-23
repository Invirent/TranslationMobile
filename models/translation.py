import requests

def translate(to_translate, lang):
    if lang == "en":
        src = "id"
    else:
        src = "en"
    langpair = "%s|%s" % (src,lang)
    print(langpair)
    get_value = f"get?q={to_translate}&langpair={langpair}"
    api_key = f"https://api.mymemory.translated.net/{get_value}"
    
    response = requests.get(str(api_key))
    if response.status_code == 200:
        translated = response.json()["responseData"]["translatedText"]
        matches = response.json()["matches"]
        for data in matches:
            if data["created-by"] == "MT!":
                translated = data["translation"]
        return translated
    else:
        return False
    

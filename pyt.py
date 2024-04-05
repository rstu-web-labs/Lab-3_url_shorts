import requests

def generate_short_link(original_link):
    api_url = "http://tinyurl.com/api-create.php?url=" + original_link
    response = requests.get(api_url)
    
    if response.status_code == 200:
        short_link = response.text
        return {"original_link": original_link, "short_link": short_link}
    else:
        return {"error": "Failed to generate short link"}

# Пример использования функции
original_link = "https://www.example.com"
result = generate_short_link(original_link)
print(result)
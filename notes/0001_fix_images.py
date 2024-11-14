import os
import requests
import json
import time

# Wczytanie danych z pliku JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

download_count = 0
max_downloads = 10  # Maksymalna liczba pobranych obrazków

for item in data:
    image_url = item.get("image_url")
    local_filename = item.get("id") + ".jpg"
    #if not os.path.exists(".\\data2"):
    #    os.makedirs(".\\data2")
    file_path = os.path.abspath(f".\\data_img\\{local_filename}")
    
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded image for ID {item['id']}")
            item["img_local"] = local_filename
            download_count += 1
        else:
            raise Exception("Failed to download image")
    except Exception as e:
        print(f"Failed to download image for ID {item['id']}: {e}")
        item["img_local"] = None

    # Przerwanie po pobraniu 10 obrazków
    #if download_count >= max_downloads:
    #    print("Downloaded 10 images. Stopping.")
    #    break

    # Opcjonalne opóźnienie między pobraniami
    time.sleep(0.02)  # 1 sekunda opóźnienia między pobraniami

# Zapisanie zmienionych danych do pliku JSON
with open("updated_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Process completed.")

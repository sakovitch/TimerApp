import requests

def check_for_update(current_version):
    url = "https://api.github.com/repos/sakovitch/TimerApp/releases/latest"  # URL na GitHub API pre najnovší release
    try:
        response = requests.get(url)
        response.raise_for_status()
        latest_version = response.json()["tag_name"]  # Získa názov tagu (napr. "v1.1")
        if latest_version != current_version:
            return latest_version
        return None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return None

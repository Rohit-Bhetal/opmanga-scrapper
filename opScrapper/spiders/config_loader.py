from pathlib import Path
import json


def test_config():
    try:
        root_dir=Path(__file__).parent
        config_path=root_dir / 'config.json'
        print(root_dir)
        if(config_path):
            with config_path.open('r') as file:
                config=json.load(file)
            return config
        else:
            print("⚠️ Config file not found.")
            return None
    except FileNotFoundError:
        print("⚠️ Config file not found.")
        return None
    except json.JSONDecodeError:
        print("⚠️ Config file not valid.")
        return None
    except PermissionError:
        print("⚠️ Config file permission denied.")
        return None
    except Exception as e:
        print(f"An unexpected error occured:{e}")
        return None

if __name__=="__main__":
    print("🔍 Testing configuration loading...")
    print(test_config())
import json

class Settings:
    contents = {}

    settings_file_path = 'Data/settings.json'

    def load():
        with open(Settings.settings_file_path, 'rb') as file:
            Settings.contents = json.load(file)

    def get(index):
        index = index.strip().lower()

        if index in Settings.contents:
            return Settings.contents.get(index)
        else:
            print(f'\nNo "{index}" setting found\n')
            quit()


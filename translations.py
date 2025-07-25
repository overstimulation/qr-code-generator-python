import json
import os
from typing import Dict, List


class TranslationManager:
    """Manages translations for the QR Code Generator"""

    def __init__(self, translations_dir: str = "translations"):
        # Use absolute path relative to this file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.translations_dir = os.path.join(current_dir, translations_dir)
        self.current_language = "en"
        self.translations: Dict[str, Dict] = {}
        self.available_languages = {
            "en": {"name": "English", "flag": "🇬🇧"},
            "pl": {"name": "Polski", "flag": "🇵🇱"},
            "ja": {"name": "日本語", "flag": "🇯🇵"}
        }
        self.load_all_translations()

    def load_all_translations(self):
        """Load all available translation files"""
        for lang_code in self.available_languages.keys():
            try:
                file_path = os.path.join(self.translations_dir, f"{lang_code}.json")
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                    print(f"Successfully loaded translation for {lang_code}")
                else:
                    print(f"Warning: Translation file for {lang_code} not found at {file_path}")
            except Exception as e:
                print(f"Error loading translation for {lang_code}: {e}")

    def set_language(self, language_code: str):
        """Set the current language"""
        if language_code in self.available_languages:
            self.current_language = language_code
        else:
            print(f"Warning: Language {language_code} not available, staying with {self.current_language}")

    def get(self, key_path: str, **kwargs) -> str:
        """
        Get a translation by key path (e.g., 'app.title' or 'inputs.wifi.ssid.label')
        Supports string formatting with kwargs
        """
        if self.current_language not in self.translations:
            return key_path  # Fallback to key if translation not available

        # Navigate through nested dictionary
        keys = key_path.split('.')
        value = self.translations[self.current_language]

        try:
            for key in keys:
                value = value[key]

            # Handle string formatting
            if isinstance(value, str) and kwargs:
                return value.format(**kwargs)

            return value
        except (KeyError, TypeError):
            # Fallback to English if key not found in current language
            if self.current_language != "en" and "en" in self.translations:
                try:
                    value = self.translations["en"]
                    for key in keys:
                        value = value[key]
                    if isinstance(value, str) and kwargs:
                        return value.format(**kwargs)
                    return value
                except (KeyError, TypeError):
                    pass

            # Ultimate fallback
            return key_path

    def get_list(self, key_path: str) -> List[str]:
        """Get a list of translations"""
        result = self.get(key_path)
        if isinstance(result, list):
            return result
        return [str(result)]

    def get_language_options(self) -> Dict[str, str]:
        """Get formatted language options for selectbox"""
        return {
            code: f"{info['flag']} {info['name']}"
            for code, info in self.available_languages.items()
        }

    def get_current_language_name(self) -> str:
        """Get the display name of current language"""
        info = self.available_languages.get(self.current_language, {})
        return f"{info.get('flag', '')} {info.get('name', self.current_language)}"


# Global translation manager instance
t = TranslationManager()

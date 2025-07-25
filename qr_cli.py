import os

from qr_core import QRCodeGenerator, QRConfig
from translations import t


class QRCodeCLI:
    def __init__(self):
        self.generator = QRCodeGenerator()

    def select_language(self):
        """Allow user to select language at startup"""
        print("🌍 Select Language / Wybierz język / 言語を選択:")
        language_options = t.get_language_options()

        print("Available languages:")
        for i, (code, display) in enumerate(language_options.items()):
            print(f"{i + 1}. {display}")

        while True:
            try:
                choice = input(f"Enter choice (1-{len(language_options)}): ").strip()
                if choice.isdigit():
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(language_options):
                        selected_lang = list(language_options.keys())[choice_idx]
                        t.set_language(selected_lang)
                        print(f"✅ {t.get('language_selected', lang=language_options[selected_lang])}")
                        return
                print("Invalid choice. Please try again.")
            except (ValueError, KeyboardInterrupt):
                print("Invalid input. Please try again.")

    def get_choice(self, prompt: str, valid_choices: list) -> str:
        """Get valid choice from user"""
        while True:
            choice = input(prompt).strip()
            if choice in valid_choices:
                return choice
            print(t.get("cli.invalid_choice", choices=', '.join(valid_choices)))

    def get_non_empty_input(self, prompt: str) -> str:
        """Get non-empty input from user"""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print(t.get("cli.field_required"))

    def get_optional_input(self, prompt: str) -> str:
        """Get optional input from user"""
        return input(prompt).strip()

    def get_positive_int(self, prompt: str, default: int) -> int:
        """Get positive integer from user"""
        while True:
            try:
                value = input(f"{prompt} ({t.get('cli.default')}: {default}): ").strip()
                if not value:
                    return default
                result = int(value)
                if result <= 0:
                    raise ValueError
                return result
            except ValueError:
                print(t.get("cli.positive_integer_required"))

    def get_non_negative_int(self, prompt: str, default: int) -> int:
        """Get non-negative integer from user"""
        while True:
            try:
                value = input(f"{prompt} ({t.get('cli.default')}: {default}): ").strip()
                if not value:
                    return default
                result = int(value)
                if result < 0:
                    raise ValueError
                return result
            except ValueError:
                print(t.get("cli.non_negative_integer_required"))

    def get_qr_type(self) -> str:
        """Get QR code type from user"""
        print(f'\n{t.get("cli.welcome")}')
        print(t.get("cli.choose_type"))

        type_map = {
            '0': 'text', '1': 'url', '2': 'wifi', '3': 'contact',
            '4': 'email', '5': 'sms', '6': 'whatsapp', '7': 'phone',
            '8': 'location', '9': 'event'
        }

        for key, qr_type in type_map.items():
            print(f'{key}. {t.get(f"qr_types.{qr_type}.title")} - {t.get(f"qr_types.{qr_type}.desc")}')

        choice = self.get_choice(
            t.get("cli.enter_number"),
            list(type_map.keys())
        )
        return type_map[choice]

    def get_qr_data(self, qr_type: str) -> dict:
        """Get QR code data based on type"""
        print(f'\n{t.get("cli.you_chose", type=t.get(f"qr_types.{qr_type}.title"))}')

        if qr_type == 'text':
            return {'text': self.get_non_empty_input(t.get("inputs.text.label") + " ")}

        elif qr_type == 'url':
            return {'url': self.get_non_empty_input(t.get("inputs.url.label") + " ")}

        elif qr_type == 'wifi':
            data = {}
            data['ssid'] = self.get_non_empty_input(t.get("inputs.wifi.ssid.label") + " ")
            data['password'] = self.get_optional_input(t.get("inputs.wifi.password.label") + " ")

            while True:
                encryption = input(t.get("inputs.wifi.encryption.label") + " (WPA/WPA2/WEP/None): ").strip().upper()
                if self.generator.validate_encryption(encryption):
                    data['encryption'] = encryption
                    break
                print(t.get("cli.invalid_encryption"))
            return data

        elif qr_type == 'contact':
            data = {}
            data['name'] = self.get_non_empty_input(t.get("inputs.contact.name.label") + " ")
            data['email'] = self.get_optional_input(t.get("inputs.contact.email.label") + " ")
            data['phone'] = self.get_optional_input(t.get("inputs.contact.phone.label") + " ")
            data['address'] = self.get_optional_input(t.get("inputs.contact.address.label") + " ")
            return data

        elif qr_type == 'email':
            data = {}
            data['email'] = self.get_non_empty_input(t.get("inputs.email.email.label") + " ")
            data['subject'] = self.get_optional_input(t.get("inputs.email.subject.label") + " ")
            data['body'] = self.get_optional_input(t.get("inputs.email.body.label") + " ")
            return data

        elif qr_type == 'sms':
            data = {}
            data['phone'] = self.get_non_empty_input(t.get("inputs.sms.phone.label") + " ")
            data['message'] = self.get_optional_input(t.get("inputs.sms.message.label") + " ")
            return data

        elif qr_type == 'whatsapp':
            data = {}
            data['phone'] = self.get_non_empty_input(t.get("inputs.whatsapp.phone.label") + " ")
            data['message'] = self.get_non_empty_input(t.get("inputs.whatsapp.message.label") + " ")
            return data

        elif qr_type == 'phone':
            return {'phone': self.get_non_empty_input(t.get("inputs.phone.phone.label") + " ")}

        elif qr_type == 'location':
            data = {}
            data['latitude'] = self.get_non_empty_input(t.get("inputs.location.latitude.label") + " ")
            data['longitude'] = self.get_non_empty_input(t.get("inputs.location.longitude.label") + " ")
            return data

        elif qr_type == 'event':
            data = {}
            data['name'] = self.get_non_empty_input(t.get("inputs.event.name.label") + " ")
            data['start_date'] = self.get_non_empty_input(t.get("inputs.event.start_date.label") + " ")
            data['end_date'] = self.get_optional_input(t.get("inputs.event.end_date.label") + " ")
            data['location'] = self.get_optional_input(t.get("inputs.event.location.label") + " ")
            data['description'] = self.get_optional_input(t.get("inputs.event.description.label") + " ")
            return data

    def get_logo_path(self) -> str:
        """Get custom logo path"""
        use_logo = self.get_choice(
            f'\n{t.get("cli.add_logo")} (y/n): ',
            ['y', 'n']
        )

        if use_logo == 'n':
            return None

        while True:
            logo_path = input(t.get("cli.enter_logo_path") + " ").strip()
            if not logo_path:
                return None
            if self.generator.validate_logo_path(logo_path):
                return logo_path
            print(t.get("cli.invalid_path"))

    def get_save_path(self) -> str:
        """Get save path for QR code"""
        default_path = os.path.join(os.path.dirname(__file__), 'qr_code.png')
        change_path = self.get_choice(
            f'\n{t.get("cli.default_save_path")}: {default_path}\n{t.get("cli.change_path")} (y/n): ',
            ['y', 'n']
        )

        if change_path == 'n':
            return default_path

        save_path = input(t.get("cli.enter_save_path") + " ").strip()
        if not save_path.endswith('.png'):
            save_path += '.png'
        return save_path

    def get_config_options(self, has_logo: bool) -> dict:
        """Get configuration options"""
        config = {}

        # Error correction
        if has_logo:
            print(f'\n{t.get("cli.logo_detected")}')
            config['error_correction_level'] = 'H'
        else:
            change_error = self.get_choice(
                f'\n{t.get("cli.default_error_correction")} {t.get("cli.change_it")} (y/n): ',
                ['y', 'n']
            )
            if change_error == 'y':
                config['error_correction_level'] = self.get_choice(
                    t.get("cli.enter_error_correction") + ' (L/M/Q/H): ',
                    ['L', 'M', 'Q', 'H']
                )
            else:
                config['error_correction_level'] = 'L'

        # Box size
        change_box = self.get_choice(
            f'{t.get("cli.default_box_size")} {t.get("cli.change_it")} (y/n): ',
            ['y', 'n']
        )
        if change_box == 'y':
            config['box_size'] = self.get_positive_int(t.get("cli.enter_box_size"), 10)
        else:
            config['box_size'] = 10

        # Border size
        change_border = self.get_choice(
            f'{t.get("cli.default_border_size")} {t.get("cli.change_it")} (y/n): ',
            ['y', 'n']
        )
        if change_border == 'y':
            config['border_size'] = self.get_non_negative_int(t.get("cli.enter_border_size"), 4)
        else:
            config['border_size'] = 4

        # Colors
        change_colors = self.get_choice(
            f'{t.get("cli.default_colors")} {t.get("cli.change_it")} (y/n): ',
            ['y', 'n']
        )
        if change_colors == 'y':
            config['fill_color'] = input(t.get("cli.fill_color") + " ").strip() or 'black'
            config['back_color'] = input(t.get("cli.back_color") + " ").strip() or 'white'
        else:
            config['fill_color'] = 'black'
            config['back_color'] = 'white'

        return config

    def run(self):
        """Main CLI application loop"""
        try:
            # Language selection
            self.select_language()

            # Get QR type and data
            qr_type = self.get_qr_type()
            qr_data = self.get_qr_data(qr_type)

            # Process the data
            processed_data = self.generator.process_qr_data(qr_type, qr_data)

            # Get logo and save path
            logo_path = self.get_logo_path()
            save_path = self.get_save_path()

            # Get configuration options
            config_options = self.get_config_options(bool(logo_path))

            # Create QR config
            config = QRConfig(
                data_to_encode=processed_data,
                custom_logo=logo_path,
                save_path=save_path,
                **config_options
            )

            # Generate QR code
            if self.generator.generate_qr_code(config):
                print(f'\n✅ {t.get("cli.success", path=save_path)}')
            else:
                print(f'\n❌ {t.get("cli.generation_failed")}')

        except KeyboardInterrupt:
            print(f'\n\n{t.get("cli.cancelled")}')
        except Exception as e:
            print(f'\n❌ {t.get("cli.error_occurred", error=str(e))}')


def main():
    cli = QRCodeCLI()
    cli.run()


if __name__ == '__main__':
    main()

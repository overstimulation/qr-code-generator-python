import os

from qr_core import QRCodeGenerator, QRConfig


class QRCodeCLI:
    def __init__(self):
        self.generator = QRCodeGenerator()

    def get_choice(self, prompt: str, valid_choices: list) -> str:
        """Get valid choice from user"""
        while True:
            choice = input(prompt).strip()
            if choice in valid_choices:
                return choice
            print(f"Invalid choice. Please select from: {', '.join(valid_choices)}")

    def get_non_empty_input(self, prompt: str) -> str:
        """Get non-empty input from user"""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("This field cannot be empty. Please try again.")

    def get_optional_input(self, prompt: str) -> str:
        """Get optional input from user"""
        return input(prompt).strip()

    def get_positive_int(self, prompt: str, default: int) -> int:
        """Get positive integer from user"""
        while True:
            try:
                value = input(f"{prompt} (default: {default}): ").strip()
                if not value:
                    return default
                result = int(value)
                if result <= 0:
                    raise ValueError
                return result
            except ValueError:
                print("Please enter a positive integer.")

    def get_non_negative_int(self, prompt: str, default: int) -> int:
        """Get non-negative integer from user"""
        while True:
            try:
                value = input(f"{prompt} (default: {default}): ").strip()
                if not value:
                    return default
                result = int(value)
                if result < 0:
                    raise ValueError
                return result
            except ValueError:
                print("Please enter a non-negative integer.")

    def get_qr_type(self) -> str:
        """Get QR code type from user"""
        print('\nWelcome to the QR Code Generator')
        print('Choose the type of QR code you want to create:')

        type_map = {
            '0': 'text', '1': 'url', '2': 'wifi', '3': 'contact',
            '4': 'email', '5': 'sms', '6': 'whatsapp', '7': 'phone',
            '8': 'location', '9': 'event'
        }

        for key, qr_type in type_map.items():
            print(f'{key}. {self.generator.QR_TYPES[qr_type]}')

        choice = self.get_choice(
            'Please enter the number (0-9): ',
            list(type_map.keys())
        )
        return type_map[choice]

    def get_qr_data(self, qr_type: str) -> dict:
        """Get QR code data based on type"""
        print(f'\nYou chose {self.generator.QR_TYPES[qr_type]}.')

        if qr_type == 'text':
            return {'text': self.get_non_empty_input('Enter the text: ')}

        elif qr_type == 'url':
            return {'url': self.get_non_empty_input('Enter the URL: ')}

        elif qr_type == 'wifi':
            data = {}
            data['ssid'] = self.get_non_empty_input('SSID (Network Name): ')
            data['password'] = self.get_optional_input('Password: ')

            while True:
                encryption = input('Encryption (WPA/WPA2/WEP/None): ').strip().upper()
                if self.generator.validate_encryption(encryption):
                    data['encryption'] = encryption
                    break
                print('Invalid encryption. Please enter WPA, WPA2, WEP, or None.')
            return data

        elif qr_type == 'contact':
            data = {}
            data['name'] = self.get_non_empty_input('Name: ')
            data['email'] = self.get_optional_input('Email (optional): ')
            data['phone'] = self.get_optional_input('Phone (optional): ')
            data['address'] = self.get_optional_input('Address (optional): ')
            return data

        elif qr_type == 'email':
            data = {}
            data['email'] = self.get_non_empty_input('Email Address: ')
            data['subject'] = self.get_optional_input('Subject (optional): ')
            data['body'] = self.get_optional_input('Body (optional): ')
            return data

        elif qr_type == 'sms':
            data = {}
            data['phone'] = self.get_non_empty_input('Phone Number: ')
            data['message'] = self.get_optional_input('Message (optional): ')
            return data

        elif qr_type == 'whatsapp':
            data = {}
            data['phone'] = self.get_non_empty_input('Phone Number (with country code): ')
            data['message'] = self.get_non_empty_input('Message: ')
            return data

        elif qr_type == 'phone':
            return {'phone': self.get_non_empty_input('Enter the phone number: ')}

        elif qr_type == 'location':
            data = {}
            data['latitude'] = self.get_non_empty_input('Latitude: ')
            data['longitude'] = self.get_non_empty_input('Longitude: ')
            return data

        elif qr_type == 'event':
            data = {}
            data['name'] = self.get_non_empty_input('Event Name: ')
            data['start_date'] = self.get_non_empty_input('Start Date (YYYYMMDDTHHMMSS): ')
            data['end_date'] = self.get_optional_input('End Date (optional): ')
            data['location'] = self.get_optional_input('Location (optional): ')
            data['description'] = self.get_optional_input('Description (optional): ')
            return data

    def get_logo_path(self) -> str:
        """Get custom logo path"""
        use_logo = self.get_choice(
            '\nDo you want to add a custom logo? (y/n): ',
            ['y', 'n']
        )

        if use_logo == 'n':
            return None

        while True:
            logo_path = input('Enter logo image path (or empty for no logo): ').strip()
            if not logo_path:
                return None
            if self.generator.validate_logo_path(logo_path):
                return logo_path
            print('Invalid path. Please enter a valid image file path.')

    def get_save_path(self) -> str:
        """Get save path for QR code"""
        default_path = os.path.join(os.path.dirname(__file__), 'qr_code.png')
        change_path = self.get_choice(
            f'\nDefault save path: {default_path}\nChange it? (y/n): ',
            ['y', 'n']
        )

        if change_path == 'n':
            return default_path

        save_path = input('Enter new save path (with filename): ').strip()
        if not save_path.endswith('.png'):
            save_path += '.png'
        return save_path

    def get_config_options(self, has_logo: bool) -> dict:
        """Get configuration options"""
        config = {}

        # Error correction
        if has_logo:
            print('\nCustom logo detected. Error correction set to H for better visibility.')
            config['error_correction_level'] = 'H'
        else:
            change_error = self.get_choice(
                '\nDefault error correction: L. Change it? (y/n): ',
                ['y', 'n']
            )
            if change_error == 'y':
                config['error_correction_level'] = self.get_choice(
                    'Enter error correction level (L/M/Q/H): ',
                    ['L', 'M', 'Q', 'H']
                )
            else:
                config['error_correction_level'] = 'L'

        # Box size
        change_box = self.get_choice('Default box size: 10. Change it? (y/n): ', ['y', 'n'])
        if change_box == 'y':
            config['box_size'] = self.get_positive_int('Enter box size', 10)
        else:
            config['box_size'] = 10

        # Border size
        change_border = self.get_choice('Default border size: 4. Change it? (y/n): ', ['y', 'n'])
        if change_border == 'y':
            config['border_size'] = self.get_non_negative_int('Enter border size', 4)
        else:
            config['border_size'] = 4

        # Colors
        change_colors = self.get_choice(
            'Default colors - Fill: black, Back: white. Change them? (y/n): ',
            ['y', 'n']
        )
        if change_colors == 'y':
            config['fill_color'] = input('Fill color (default: black): ').strip() or 'black'
            config['back_color'] = input('Back color (default: white): ').strip() or 'white'
        else:
            config['fill_color'] = 'black'
            config['back_color'] = 'white'

        return config

    def run(self):
        """Main CLI application loop"""
        try:
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
                print(f'\n✅ QR code successfully saved to: {save_path}')
            else:
                print('\n❌ Failed to generate QR code.')

        except KeyboardInterrupt:
            print('\n\nOperation cancelled by user.')
        except Exception as e:
            print(f'\n❌ An error occurred: {e}')


def main():
    cli = QRCodeCLI()
    cli.run()


if __name__ == '__main__':
    main()

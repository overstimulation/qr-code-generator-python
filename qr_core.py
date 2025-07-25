import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import qrcode
from PIL import Image


@dataclass
class QRConfig:
    """Configuration for QR code generation"""
    data_to_encode: str
    custom_logo: Optional[str] = None
    save_path: str = "qr_code.png"
    error_correction_level: str = "L"
    box_size: int = 10
    border_size: int = 4
    fill_color: str = "black"
    back_color: str = "white"


class QRDataProcessor:
    """Handles processing different types of QR code data"""

    @staticmethod
    def process_text(text: str) -> str:
        return text.strip()

    @staticmethod
    def process_url(url: str) -> str:
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    @staticmethod
    def process_wifi(ssid: str, password: str, encryption: str) -> str:
        encryption = encryption.upper()
        if encryption not in ['WPA', 'WPA2', 'WEP', 'NONE']:
            raise ValueError("Invalid encryption type")
        return f'WIFI:S:{ssid};T:{encryption};P:{password};H:false;'

    @staticmethod
    def process_contact(name: str, email: str = "", phone: str = "", address: str = "") -> str:
        data = f'BEGIN:VCARD\nVERSION:3.0\nFN:{name}\n'
        if email:
            data += f'EMAIL:{email}\n'
        if phone:
            data += f'TEL:{phone}\n'
        if address:
            data += f'ADR:{address}\n'
        data += 'END:VCARD'
        return data

    @staticmethod
    def process_email(email: str, subject: str = "", body: str = "") -> str:
        data = f'MAILTO:{email}'
        if subject or body:
            data += '?'
            if subject:
                data += f'SUBJECT={subject}'
            if body:
                if subject:
                    data += '&'
                data += f'BODY={body}'
        return data

    @staticmethod
    def process_sms(phone_number: str, message: str = "") -> str:
        data = f'SMS:{phone_number}'
        if message:
            data += f'?BODY={message}'
        return data

    @staticmethod
    def process_whatsapp(phone_number: str, message: str) -> str:
        return f'whatsapp://send?phone={phone_number}&text={message}'

    @staticmethod
    def process_phone(phone_number: str) -> str:
        if not phone_number.startswith('tel:'):
            phone_number = 'tel:' + phone_number
        return phone_number

    @staticmethod
    def process_location(latitude: str, longitude: str) -> str:
        return f'geo:{latitude},{longitude}'

    @staticmethod
    def process_event(event_name: str, start_date: str, end_date: str = "",
                      location: str = "", description: str = "") -> str:
        data = f'BEGIN:VEVENT\nSUMMARY:{event_name}\nDTSTART:{start_date}\n'
        if end_date:
            data += f'DTEND:{end_date}\n'
        if location:
            data += f'LOCATION:{location}\n'
        if description:
            data += f'DESCRIPTION:{description}\n'
        data += 'END:VEVENT'
        return data


class QRCodeGenerator:
    """Main QR code generation logic"""

    QR_TYPES = {
        'text': 'Text',
        'url': 'URL',
        'wifi': 'Wi-Fi Network',
        'contact': 'Contact (vCard)',
        'email': 'Email',
        'sms': 'SMS',
        'whatsapp': 'WhatsApp Message',
        'phone': 'Phone Number',
        'location': 'Location',
        'event': 'Event (iCalendar)'
    }

    ERROR_CORRECTION_LEVELS = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H,
    }

    def __init__(self):
        self.processor = QRDataProcessor()

    def validate_logo_path(self, logo_path: str) -> bool:
        """Validate if logo file exists"""
        return os.path.isfile(logo_path) if logo_path else True

    def validate_encryption(self, encryption: str) -> bool:
        """Validate WiFi encryption type"""
        return encryption.upper() in ['WPA', 'WPA2', 'WEP', 'NONE']

    def generate_qr_code(self, config: QRConfig) -> bool:
        """Generate QR code with given configuration"""
        try:
            # Set error correction level
            if config.custom_logo:
                error_correction = self.ERROR_CORRECTION_LEVELS['H']
            else:
                error_correction = self.ERROR_CORRECTION_LEVELS.get(
                    config.error_correction_level,
                    qrcode.constants.ERROR_CORRECT_L
                )

            # Create QR code
            qr = qrcode.QRCode(
                version=None,
                error_correction=error_correction,
                box_size=config.box_size,
                border=config.border_size,
            )
            qr.add_data(config.data_to_encode)
            qr.make(fit=True)

            # Generate image
            qr_img = qr.make_image(fill_color=config.fill_color, back_color=config.back_color)
            qr_img.save(config.save_path)

            # Add logo if specified
            if config.custom_logo:
                self._add_logo_to_qr(config.save_path, config.custom_logo, config.back_color)

            return True

        except Exception as e:
            print(f"Error generating QR code: {e}")
            return False

    def _add_logo_to_qr(self, qr_path: str, logo_path: str, back_color: str):
        """Add logo to existing QR code"""
        qr_img = Image.open(qr_path).convert("RGBA")
        logo = Image.open(logo_path).convert("RGBA")

        logo_size = qr_img.size[0] // 4
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # Create border around logo
        border_size = logo_size // 8
        bordered_logo_size = logo_size + 2 * border_size
        logo_with_border = Image.new("RGBA", (bordered_logo_size, bordered_logo_size), back_color)
        logo_with_border.paste(logo, (border_size, border_size), logo)

        # Center logo on QR code
        left = (qr_img.size[0] - bordered_logo_size) // 2
        top = (qr_img.size[1] - bordered_logo_size) // 2

        qr_img.paste(logo_with_border, (left, top), logo_with_border)
        qr_img.save(qr_path)

    def process_qr_data(self, qr_type: str, data: Dict[str, Any]) -> str:
        """Process QR data based on type"""
        if qr_type == 'text':
            return self.processor.process_text(data['text'])
        elif qr_type == 'url':
            return self.processor.process_url(data['url'])
        elif qr_type == 'wifi':
            return self.processor.process_wifi(data['ssid'], data['password'], data['encryption'])
        elif qr_type == 'contact':
            return self.processor.process_contact(
                data['name'], data.get('email', ''),
                data.get('phone', ''), data.get('address', '')
            )
        elif qr_type == 'email':
            return self.processor.process_email(
                data['email'], data.get('subject', ''), data.get('body', '')
            )
        elif qr_type == 'sms':
            return self.processor.process_sms(data['phone'], data.get('message', ''))
        elif qr_type == 'whatsapp':
            return self.processor.process_whatsapp(data['phone'], data['message'])
        elif qr_type == 'phone':
            return self.processor.process_phone(data['phone'])
        elif qr_type == 'location':
            return self.processor.process_location(data['latitude'], data['longitude'])
        elif qr_type == 'event':
            return self.processor.process_event(
                data['name'], data['start_date'], data.get('end_date', ''),
                data.get('location', ''), data.get('description', '')
            )
        else:
            raise ValueError(f"Unknown QR type: {qr_type}")

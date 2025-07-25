import os

import qrcode
from PIL import Image


def main() -> None:
    print('Welcome to the QR Code Generator by @overstimulation')
    print('This script will guide you through creating a custom QR code.')
    print('First, choose the type of QR code you want to create:')
    print('0. Text')
    print('1. URL')
    print('2. Wi-Fi Network')
    print('3. Contact (vCard)')
    print('4. Email')
    print('5. SMS')
    print('6. Whatsapp Message')
    print('7. Phone Number')
    print('8. Location')
    print('9. Event (iCalendar)')
    print('Please enter the number corresponding to your choice (1-9):')
    choice = input().strip()
    while choice not in [str(i) for i in range(0, 10)]:
        print('Invalid choice. Please enter a number between 0 and 9:')
        choice = input().strip()

    # Data to encode in the QR code (prompt user until valid input)
    match choice:
        case '0':
            print('You chose Text. Enter the text to encode in the QR code:')
            data_to_encode = input().strip()
            while not data_to_encode.strip():
                print('Enter the text to encode in the QR code:')
                data_to_encode = input().strip()
        case '1':
            print('You chose URL. Enter the URL to encode in the QR code:')
            data_to_encode = input().strip()
            while not data_to_encode.strip():
                print('Enter the text to encode in the QR code:')
                data_to_encode = input().strip()
            if not data_to_encode.startswith(('http://', 'https://')):
                print('Warning: URL should start with "http://" or "https://". Adding "https://" by default.')
                data_to_encode = 'https://' + data_to_encode
        case '2':
            print('You chose Wi-Fi Network. Enter the following details:')
            ssid = input('SSID (Network Name): ').strip()
            while not ssid:
                print('SSID cannot be empty. Please enter the Network Name:')
                ssid = input('SSID (Network Name): ').strip()
            password = input('Password: ').strip()
            encryption = input('Encryption (WPA/WPA2/WEP/None): ').strip().upper()
            while encryption not in ['WPA', 'WPA2', 'WEP', 'NONE']:
                print('Invalid encryption type. Please enter WPA, WPA2, WEP, or None:')
                encryption = input('Encryption (WPA/WPA2/WEP/None): ').strip().upper()
            data_to_encode = f'WIFI:S:{ssid};T:{encryption};P:{password};H:false;'
        case '3':
            print('You chose Contact (vCard). Enter the following details:')
            name = input('Name: ').strip()
            while not name:
                print('Name cannot be empty. Please enter the Name:')
                name = input('Name: ').strip()
            email = input('Email (optional): ').strip()
            phone = input('Phone (optional): ').strip()
            address = input('Address (optional): ').strip()
            data_to_encode = f'BEGIN:VCARD\nVERSION:3.0\nFN:{name}\n'
            if email:
                data_to_encode += f'EMAIL:{email}\n'
            if phone:
                data_to_encode += f'TEL:{phone}\n'
            if address:
                data_to_encode += f'ADR:{address}\n'
            data_to_encode += 'END:VCARD'
        case '4':
            print('You chose Email. Enter the following details:')
            email = input('Email Address: ').strip()
            while not email:
                print('Email Address cannot be empty. Please enter the Email Address:')
                email = input('Email Address: ').strip()
            subject = input('Subject (optional): ').strip()
            body = input('Body (optional): ').strip()
            data_to_encode = f'MAILTO:{email}'
            if subject or body:
                data_to_encode += '?'
                if subject:
                    data_to_encode += f'SUBJECT={subject}'
                if body:
                    if subject:
                        data_to_encode += '&'
                    data_to_encode += f'BODY={body}'
        case '5':
            print('You chose SMS. Enter the following details:')
            phone_number = input('Phone Number: ').strip()
            while not phone_number:
                print('Phone Number cannot be empty. Please enter the Phone Number:')
                phone_number = input('Phone Number: ').strip()
            message = input('Message (optional): ').strip()
            data_to_encode = f'SMS:{phone_number}'
            if message:
                data_to_encode += f'?BODY={message}'
        case '6':
            print('You chose Whatsapp Message. Enter the following details:')
            phone_number = input('Phone Number (with country code, e.g., +1234567890): ').strip()
            while not phone_number:
                print('Phone Number cannot be empty. Please enter the Phone Number (with country code):')
                phone_number = input('Phone Number (with country code, e.g., +1234567890): ').strip()
            message = input('Message: ').strip()
            while not message:
                print('Message cannot be empty. Please enter the Message:')
                message = input('Message: ').strip()
            data_to_encode = f'whatsapp://send?phone={phone_number}&text={message}'
        case '7':
            print('You chose Phone Number. Enter the phone number to encode in the QR code:')
            data_to_encode = input().strip()
            while not data_to_encode.strip():
                print('Enter the phone number to encode in the QR code:')
                data_to_encode = input().strip()
            if not data_to_encode.startswith('tel:'):
                data_to_encode = 'tel:' + data_to_encode
        case '8':
            print('You chose Location. Enter the following details:')
            latitude = input('Latitude: ').strip()
            while not latitude:
                print('Latitude cannot be empty. Please enter the Latitude:')
                latitude = input('Latitude: ').strip()
            longitude = input('Longitude: ').strip()
            while not longitude:
                print('Longitude cannot be empty. Please enter the Longitude:')
                longitude = input('Longitude: ').strip()
            data_to_encode = f'geo:{latitude},{longitude}'
        case '9':
            print('You chose Event (iCalendar). Enter the following details:')
            event_name = input('Event Name: ').strip()
            while not event_name:
                print('Event Name cannot be empty. Please enter the Event Name:')
                event_name = input('Event Name: ').strip()
            start_date = input('Start Date (YYYYMMDDTHHMMSS): ').strip()
            while not start_date:
                print('Start Date cannot be empty. Please enter the Start Date (YYYYMMDDTHHMMSS):')
                start_date = input('Start Date (YYYYMMDDTHHMMSS): ').strip()
            end_date = input('End Date (YYYYMMDDTHHMMSS, optional): ').strip()
            location = input('Location (optional): ').strip()
            description = input('Description (optional): ').strip()
            data_to_encode = f'BEGIN:VEVENT\nSUMMARY:{event_name}\nDTSTART:{start_date}\n'
            if end_date:
                data_to_encode += f'DTEND:{end_date}\n'
            if location:
                data_to_encode += f'LOCATION:{location}\n'
            if description:
                data_to_encode += f'DESCRIPTION:{description}\n'
            data_to_encode += 'END:VEVENT'

    # Custom logo (optional, prompt user for path)
    custom_logo = None
    print('Do you want to add a custom logo to the QR code? (y/n)')
    choice = input().strip().lower()
    if choice == 'y':
        print('Enter the path to the logo image (leave empty for no logo):')
        while True:
            custom_logo = input().strip()
            if not custom_logo or os.path.isfile(custom_logo):
                break
            print('Invalid path. Please enter a valid path to the logo image or leave it empty for no logo.')

    # Save path for the QR code image (default is current directory + 'qr_code.png')
    save_path = os.path.join(os.path.dirname(__file__), 'qr_code.png')
    print(f'Default save path for QR code image: {save_path}, would you like to change it? (y/n)')
    choice = input().strip().lower()
    if choice == 'y':
        print('Enter the new save path including filename (use "./" for current directory):')
        save_path = input().strip()
        if not save_path.endswith('.png'):
            save_path += '.png'

    # Error correction level (L, M, Q, H)
    if custom_logo:
        print('Custom logo detected. Default error correction level will be set to H for better logo visibility.')
        error_correction_level = qrcode.constants.ERROR_CORRECT_H
    else:
        error_correction_level = 'L'
        print(f'Default error correction level: {error_correction_level}. Would you like to change it? (y/n)')
        choice = input().strip().lower()
        if choice == 'y':
            print('Enter the error correction level (L, M, Q, H):')
            while True:
                user_input = input().strip().upper()
                if user_input in ['L', 'M', 'Q', 'H']:
                    error_correction_level = user_input
                    break
                print('Invalid input. Please enter L, M, Q, or H.')
        error_correction_level = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H,
        }[error_correction_level]

    # Box size (size of each box in pixels, default is 10)
    box_size = 10
    print(f'Default box size: {box_size}. Would you like to change it? (y/n)')
    choice = input().strip().lower()
    if choice == 'y':
        print('Enter the box size (default is 10):')
        while True:
            try:
                box_size = int(input().strip())
                if box_size <= 0:
                    raise ValueError
                break
            except ValueError:
                print('Invalid input. Please enter a positive integer.')

    # Border size (default is 4)
    border_size = 4
    print(f'Default border size: {border_size}. Would you like to change it? (y/n)')
    choice = input().strip().lower()
    if choice == 'y':
        print('Enter the border size (default is 4):')
        while True:
            try:
                border_size = int(input().strip())
                if border_size < 0:
                    raise ValueError
                break
            except ValueError:
                print('Invalid input. Please enter a non-negative integer.')

    # Fill and back color (default is black and white)
    fill_color = 'black'
    back_color = 'white'
    print(f'Default fill color: {fill_color}, back color: {back_color}. Would you like to change them? (y/n)')
    choice = input().strip().lower()
    if choice == 'y':
        print('Enter the fill color (default is black):')
        fill_color = input().strip() or fill_color
        print('Enter the back color (default is white):')
        back_color = input().strip() or back_color

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction_level,
        box_size=box_size,
        border=border_size,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)
    qr_img.save(save_path)

    if custom_logo:
        qr_img = Image.open(save_path).convert("RGBA")
        logo = Image.open(custom_logo).convert("RGBA")

        logo_size = qr_img.size[0] // 4
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # Create a border around the logo
        border_size = logo_size // 8  # Adjust border thickness as needed
        bordered_logo_size = logo_size + 2 * border_size
        logo_with_border = Image.new("RGBA", (bordered_logo_size, bordered_logo_size), back_color)
        logo_with_border.paste(logo, (border_size, border_size), logo)

        left = (qr_img.size[0] - bordered_logo_size) // 2
        top = (qr_img.size[1] - bordered_logo_size) // 2

        qr_img.paste(logo_with_border, (left, top), logo_with_border)
        qr_img.save(save_path)

    print(f'QR code saved to {save_path}')


if __name__ == '__main__':
    main()

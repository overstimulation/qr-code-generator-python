import os

import qrcode


def main() -> None:
    # Data to encode in the QR code (prompt user until valid input)
    data_to_encode = ''
    while not data_to_encode.strip():
        print('Enter the data to encode in the QR code:')
        data_to_encode = input().strip()

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
        version=1,
        error_correction=error_correction_level,
        box_size=box_size,
        border=border_size,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)
    qr_img.save(save_path)

    print(f'QR code saved to {save_path}')


if __name__ == '__main__':
    main()

import qrcode


def main() -> None:
    data_to_encode = 'https://github.com/overstimulation/qr-code-generator-python'

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    img.save('qrcode.png')


if __name__ == '__main__':
    main()

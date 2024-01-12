import qrcode

def create_and_print_QR(text):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,  # Adjust box_size for better visibility in the terminal
        border=2,
    )

    # Add data to the QR code
    qr.add_data(text)
    qr.make(fit=True)

    # Create an ASCII representation of the QR code
    qr_ascii = qr.make_ascii()

    # Print the ASCII representation in the terminal
    print(qr_ascii)
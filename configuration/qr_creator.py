import qrcode

#
# Create and save the qr
# return the final path where
# the qr is been saved
#
def create_and_save_QR(text):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Adjust box_size for better visibility in the terminal
        border=2,
    )

    # Add data to the QR code
    qr.add_data(text)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image or display it
    img.save("./my_qr_code.png")
    return "./my_qr_code.png"
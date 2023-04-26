import base64

if __name__ == "__main__":
    with open("logo.ico", "rb") as logo:
        encoded_string = base64.b64encode(logo.read())
        image_file = "logo_bytes = " + str(encoded_string)

    with open("logo_bytes.py", "w") as logo_bytes:
        logo_bytes.write(image_file)
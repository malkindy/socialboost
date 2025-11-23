# app/utils/qr_generator.py

import qrcode
from io import BytesIO
import base64
from typing import Optional

def generate_qr_code(data: str, save_path: Optional[str] = None) -> str:
    """
    Generate a QR code PNG and return a base64 string.
    Optionally save the PNG file locally if save_path is provided.
    """

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save PNG file if path provided
    if save_path:
        img.save(save_path)

    # Convert to base64 string
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_str

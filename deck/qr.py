"""Generate a clean QR code PNG (dark modules on white, quiet zone)."""
import os
import qrcode

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "out", "_qr")


def render(text, dark="1A365D", box=12, border=3):
    os.makedirs(CACHE_DIR, exist_ok=True)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=box, border=border)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=f"#{dark}", back_color="white")
    path = os.path.join(CACHE_DIR, "qr.png")
    img.save(path)
    return path

import qrcode
from app.database.session import SessionLocal
from app.database.models import Token

# Open a DB session
db = SessionLocal()

# Fetch the latest token
token_obj = db.query(Token).order_by(Token.id.desc()).first()

if token_obj is None:
    print("No token found in the database.")
else:
    qr_data = token_obj.qr_url  # This is the URL stored in the database
    img = qrcode.make(qr_data)

    # Save QR code to a file
    filename = f"{token_obj.token}.png"
    img.save(filename)
    print(f"QR code saved as {filename}")

db.close()

#!/usr/bin/env python3

from app.database.session import SessionLocal
from app.database.models import Device, Base
from app.database.session import engine

# Create tables (if not exist)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Add test devices if table is empty
if not db.query(Device).first():
    db.add_all([
        Device(name="Display 1", status="online"),
        Device(name="Display 2", status="offline"),
        Device(name="Display 3", status="online"),
    ])
    db.commit()
    print("Devices added successfully!")

# Print all devices
devices = db.query(Device).all()
print("Current devices in DB:")
for d in devices:
    print(f"{d.id} | {d.name} | {d.status}")

db.close()

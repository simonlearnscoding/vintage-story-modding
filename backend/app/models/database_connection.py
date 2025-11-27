import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base

# we can hardcode this for now because it's just local
DATABASE_URL = os.getenv("postgresql://vsuser:vspassword@localhost:5433/vintagestory")

engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


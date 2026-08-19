import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'fastapi_app'))
from fastapi_app.models import Base, engine
Base.metadata.create_all(bind=engine)
print("Tables created")

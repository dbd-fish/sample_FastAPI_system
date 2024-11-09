from sqlalchemy import Column, Integer, String
from app.database import Base

class SampleModel3(Base):
    __tablename__ = "sample_table3"
    idsss = Column(Integer, primary_key=True, index=True)
    namesss = Column(String, index=True)
    descriptionsss = Column(String)

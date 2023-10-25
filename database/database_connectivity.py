from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship

Base = declarative_base()
ENGINE = create_engine("mysql+pymysql://root:abcd1234@localhost:3306/hospitaldb")

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    availabilities = relationship('Availability', back_populates='doctor')

class Specialty(Base):
    __tablename__ = 'specialties'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    availabilities = relationship('Availability', back_populates='specialty')

class Availability(Base):
    __tablename__ = 'availability'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    specialty_id = Column(Integer, ForeignKey('specialties.id'))
    day = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    doctor = relationship('Doctor', back_populates='availabilities')
    specialty = relationship('Specialty', back_populates='availabilities')

Session = sessionmaker(bind=ENGINE)

def get_doctor_availability(first_name, last_name, day):
    session = Session()
    availability = session.query(Availability).join(Doctor).filter(Doctor.first_name == first_name, Doctor.last_name == last_name, Availability.day == day).all()
    session.close()
    return availability

def search_doctors_by_name(name):
    session = Session()
    doctors = session.query(Doctor, Specialty).join(Availability).join(Specialty).filter((Doctor.first_name == name) | (Doctor.last_name == name)).all()
    session.close()
    return doctors


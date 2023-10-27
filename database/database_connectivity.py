from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship


Base = declarative_base()
ENGINE = create_engine("mysql+pymysql://root:abcd1234@localhost:3306/chatbot")

class Doctor(Base):
    __tablename__ = 'doctors'
    DoctorID = Column(Integer, primary_key=True)
    First_name = Column(String)
    Last_name = Column(String)
    availabilities = relationship('Availability', back_populates='doctor')

class Specialty(Base):
    __tablename__ = 'specialties'
    SpecialtyID = Column(Integer, primary_key=True)
    SpecialtyName = Column(String)
    availabilities = relationship('Availability', back_populates='specialty')

# class Availability(Base):
#     __tablename__ = 'availability'
#     id = Column(Integer, primary_key=True)
#     DoctorID = Column(Integer, ForeignKey('doctors.id'))
#     SpecialtyID = Column(Integer, ForeignKey('specialties.id'))
#     Day = Column(String)
#     Start Time = Column(Time)
#     End_time = Column(Time)
#     doctor = relationship('Doctor', back_populates='availabilities')
#     specialty = relationship('Specialty', back_populates='availabilities')

class Availability(Base):
    __tablename__ = 'availability'
    DoctorID = Column(Integer, ForeignKey('doctors.DoctorID'), primary_key=True)
    SpecialtyID = Column(Integer, ForeignKey('specialties.SpecialtyID'))
    Day = Column(String, primary_key=True)
    Start_Time = Column(Time)
    End_time = Column(Time)
    doctor = relationship('Doctor', back_populates='availabilities')
    specialty = relationship('Specialty', back_populates='availabilities')

Session = sessionmaker(bind=ENGINE)

def get_doctor_availability(first_name, last_name, Day):
    session = Session()
    availability = session.query(Availability).join(Doctor).filter(Doctor.First_name == first_name, Doctor.Last_name == last_name, Availability.Day == Day).all()
    session.close()
    return availability

def search_doctors_by_name(name):
    session = Session()
    doctors = session.query(Doctor, Specialty).join(Availability).join(Specialty).filter((Doctor.First_name == name) | (Doctor.Last_name == name)).all()
    session.close()
    return doctors

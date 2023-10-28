from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy import func


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

class Patient(Base):
    __tablename__ = 'patients'
    PatientID = Column(Integer, primary_key=True, autoincrement=True)
    Phone_number = Column(String)
    First_name = Column(String)
    Last_name = Column(String)
    Age = Column(Integer)

class Appointment(Base):
    __tablename__ = 'appointments'
    Appointment_ID = Column(Integer, primary_key=True, autoincrement=True)
    PatientID = Column(Integer, ForeignKey('patients.PatientID'))
    DoctorID = Column(Integer, ForeignKey('doctors.DoctorID'))
    Appointment_day = Column(String)
    Appointment_time = Column(Time)
    Appointment_number = Column(Integer)

    patient = relationship('Patient')
    doctor = relationship('Doctor')

Session = sessionmaker(bind=ENGINE)

# --------------------- Functions ---------------------

def add_new_appointment(patientID, doctor_name, appointment_time,appointment_day):
    session = Session()

    appointments_same_day = session.query(Appointment).filter(
        Appointment.DoctorID == get_doctorID_by_name(doctor_name,session),
        Appointment.Appointment_day == appointment_day
    ).count()

    appointment_number = appointments_same_day + 1
   
    new_appointment = Appointment(
        PatientID=patientID,
        DoctorID=get_doctorID_by_name(doctor_name,session), 
        Appointment_day=appointment_day,
        Appointment_time=appointment_time,
        Appointment_number=appointment_number
    )
    session.add(new_appointment)
    session.commit()
    session.close()

def add_new_patient(first_name, last_name, age, phone_number):
    session = Session()
    if not session.query(Patient)\
            .filter(Patient.Phone_number == phone_number, 
                    func.lower(Patient.First_name) == func.lower(first_name), 
                    func.lower(Patient.Last_name) == func.lower(last_name))\
            .first():        
        new_patient = Patient(First_name=first_name, Last_name=last_name, Age=age, Phone_number=phone_number)
        session.add(new_patient)
        session.commit()
        new_patientId = new_patient.PatientID
    # else:
    #     existing_patient = session.query(Patient).filter(Patient.Phone_number == phone_number).first()
    #     if existing_patient.First_name.lower() != first_name.lower() and existing_patient.Last_name.lower() != last_name.lower():
    #         new_patient_added = False
    #     else:
    #         existing_patient.Age = age
    #         session.commit()
    #         new_patient_added = False
    else:
        new_patientId = session.query(Patient)\
            .filter(Patient.Phone_number == phone_number, 
                    func.lower(Patient.First_name) == func.lower(first_name), 
                    func.lower(Patient.Last_name) == func.lower(last_name))\
            .first().PatientID
    session.close()
    return new_patientId

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

def get_doctorID_by_name(doctor_name,session):
    first_name, last_name = doctor_name.split(" ", 1)
    return session.query(Doctor).filter(Doctor.First_name == first_name, Doctor.Last_name == last_name).first().DoctorID
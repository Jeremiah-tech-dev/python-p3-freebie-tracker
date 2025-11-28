from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref, Session
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    freebies = relationship('Freebie', back_populates='company')
    devs = relationship('Dev', secondary='freebies', back_populates='companies', viewonly=True)

    def give_freebie(self, dev, item_name, value):
        from sqlalchemy.orm import object_session
        session = object_session(self)
        if session is None:
            from sqlalchemy import create_engine
            engine = create_engine('sqlite:///freebies.db')
            session = Session(engine)
        freebie = Freebie(dev=dev, company=self, item_name=item_name, value=value)
        session.add(freebie)
        session.commit()
        return freebie
    
    @classmethod
    def oldest_company(cls):
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///freebies.db')
        session = Session(engine)
        oldest = session.query(cls).order_by(cls.founding_year).first()
        session.close()
        return oldest

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    
    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs', viewonly=True)
    
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)
    
    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev

    def __repr__(self):
        return f'<Dev {self.name}>'

class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))
    
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')
    
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."
    
    def __repr__(self):
        return f'<Freebie {self.item_name}>'

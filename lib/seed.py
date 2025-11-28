#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie, Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Clear existing data
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()
    
    # Create companies
    google = Company(name="Google", founding_year=1998)
    apple = Company(name="Apple", founding_year=1976)
    microsoft = Company(name="Microsoft", founding_year=1975)
    
    # Create devs
    alice = Dev(name="Alice")
    bob = Dev(name="Bob")
    charlie = Dev(name="Charlie")
    
    # Add to session
    session.add_all([google, apple, microsoft, alice, bob, charlie])
    session.commit()
    
    # Create freebies
    freebie1 = Freebie(dev=alice, company=google, item_name="T-shirt", value=25)
    freebie2 = Freebie(dev=bob, company=apple, item_name="Stickers", value=5)
    freebie3 = Freebie(dev=alice, company=microsoft, item_name="Mug", value=15)
    freebie4 = Freebie(dev=charlie, company=google, item_name="Hoodie", value=50)
    
    session.add_all([freebie1, freebie2, freebie3, freebie4])
    session.commit()
    
    print("Seed data created successfully!")
    session.close()

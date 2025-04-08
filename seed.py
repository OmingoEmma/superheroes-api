from app import create_app, db
from app.models import Hero, Power, HeroPower

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    h1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    h2 = Hero(name="Gwen Stacy", super_name="Spider-Gwen")

    p1 = Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed")
    p2 = Power(name="super strength", description="gives the wielder super-human strengths")

    db.session.add_all([h1, h2, p1, p2])
    db.session.commit()

    hp1 = HeroPower(strength="Strong", hero_id=h1.id, power_id=p1.id)
    hp2 = HeroPower(strength="Average", hero_id=h2.id, power_id=p2.id)

    db.session.add_all([hp1, hp2])
    db.session.commit()

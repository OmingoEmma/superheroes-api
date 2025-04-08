from flask import jsonify, request
from models import db, Hero, Power, HeroPower

def register_routes(app):

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Superheroes API!"})

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)
        if not hero:
            return jsonify({"error": "Hero not found"}), 404
        return jsonify({
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "hero_powers": [
                {
                    "id": hp.id,
                    "strength": hp.strength,
                    "power_id": hp.power_id,
                    "hero_id": hp.hero_id,
                    "power": hp.power.to_dict()
                } for hp in hero.hero_powers
            ]
        })

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404
        return jsonify(power.to_dict())

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404

        data = request.get_json()
        power.description = data.get("description")

        errors = power.validate()
        if errors:
            return jsonify({"errors": errors}), 400

        db.session.commit()
        return jsonify(power.to_dict())

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()
        hero_power = HeroPower(
            strength=data.get("strength"),
            hero_id=data.get("hero_id"),
            power_id=data.get("power_id")
        )

        errors = hero_power.validate()
        if errors:
            return jsonify({"errors": errors}), 400

        db.session.add(hero_power)
        db.session.commit()

        hero = Hero.query.get(hero_power.hero_id)
        return jsonify(hero.to_dict()), 201
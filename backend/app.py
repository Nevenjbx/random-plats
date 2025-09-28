import random
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask import request, Response



app = Flask(__name__, static_folder="../frontend", static_url_path="/")



# Configuration de SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://plats_db_user:gqg1djCTtbXHHi5XVb1PDKGjP6Qrt2qC@dpg-d3c5rjqdbo4c73du2050-a/plats_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)



# Modèle de données
class Plat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)



# Créer la base si elle n'existe pas
with app.app_context():
    db.create_all()



USERNAME = "invite"
PASSWORD = "0000"

@app.before_request
def require_login():
    auth = request.authorization
    if not auth or auth.username != USERNAME or auth.password != PASSWORD:
        return Response(
            "Accès restreint 🚫", 401,
            {"WWW-Authenticate": "Basic realm='Login Required'"}
        )
    

last_plat = None

@app.route("/api/random-plat")
def random_plat():
    global last_plat

    # Taille de la table
    total = db.session.query(func.count(Plat.id)).scalar()
    if total == 0:
        return jsonify({"error": "Aucun plat disponible"}), 404

    # Tenter jusqu'à trouver un plat différent du dernier
    for _ in range(5):  # max 5 tentatives pour éviter boucle infinie
        random_index = random.randint(0, total - 1)
        plat = db.session.query(Plat).offset(random_index).limit(1).scalar_one()

        if not last_plat or plat.id != last_plat.id:
            last_plat = plat
            return jsonify({"plat": plat.nom})

    # Si jamais on n'a trouvé que le même plat (cas: table avec 1 ligne)
    return jsonify({"error": "Pas assez de plats pour garantir du random"}), 400



@app.route("/api/add-plat", methods=["POST"])
def add_plat():
    data = request.get_json()
    nom = data.get("plat")
    if not nom:
        return jsonify({"error": "Nom invalide"}), 400

    if Plat.query.filter_by(nom=nom).first():
        return jsonify({"error": "Plat déjà présent"}), 400

    nouveau_plat = Plat(nom=nom)
    db.session.add(nouveau_plat)
    db.session.commit()
    return jsonify({"message": f"Plat ajouté : {nom}"})



@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")



if __name__ == "__main__":
    app.run(debug=True)

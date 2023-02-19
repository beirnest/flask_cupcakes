"""Flask app for Cupcakes"""

from flask import Flask, render_template, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON of all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def add_new_cupcake():
    """Creates cupcake and returns JSON"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    # Return w/status code 201 --- return tuple (json, status)
    return ( jsonify(cupcake=serialized), 201 )

@app.route("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return JSON of single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake details"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.query(Cupcake).filter_by(id=cupcake_id).update(request.json)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return {
        "Message": "Deleted"
    }

@app.route('/')
def load_home():
    cupcakes = Cupcake.query.all()
    return render_template("base.html", cupcakes = cupcakes)


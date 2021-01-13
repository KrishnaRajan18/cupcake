"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify
from models import db, connect_db, Cupcake
from helpers import serialize_cupcakes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root123@localhost/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "so-so-secret"

connect_db(app)




@app.route('/')
def home_page():
    """ Display home page """
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_all_cupcakes():
    """ Returns JSON for all cupcakes """
    cupcakes = [cupcake.serialize_cupcakes() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """ Returns JSON for a cupcake """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize_cupcakes())


@app.route('/api/cupcakes', methods=['POST'])
def make_cupcake():
    """ 
        Create a cupcake 
        Returns JSON for created cupcake
    """
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json.get('image', None)
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    if image:
        new_cupcake.image = image

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize_cupcakes()), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """ 
        Update a cupcake 
        Returns JSON for updated cupcake 
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size) 
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize_cupcakes())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """ Deletes a cupcake """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message=f"Cupcake Deleted; id:{cupcake_id}")




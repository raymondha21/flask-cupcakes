"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, Cupcake, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'thebestsecretkey'

connect_db(app)
db.create_all()

@app.route('/')
def homepage_cupcakes():
    """Front page list of cupcakes"""
    cupcakes = Cupcake.query.all()

    return render_template('index.html',cupcakes=cupcakes)

@app.route('/api/cupcakes')
def list_cupcakes():
    """List of all cupcakes"""

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get a single cupcake"""

    cupcake = Cupcake.query.get_or_404(id).serialize()

    return jsonify(cupcake=cupcake)    

@app.route('/api/cupcakes',methods=['POST'])
def create_cupcake():
    """Create a cupcake"""

    new_cupcake = Cupcake(flavor=request.json['flavor'], 
    rating=request.json['rating'],
    size=request.json['size'],
    image=request.json['image'])

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()),201)

@app.route('/api/cupcakes/<int:id>',methods=['PATCH'])
def update_cupcake(id):
    """Update an existing cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    
    cupcake.flavor=request.json['flavor']
    cupcake.rating=request.json['rating']
    cupcake.size=request.json['size']
    cupcake.image=request.json['image']
    
    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>',methods=['DELETE'])
def delete_cupcake(id):
    """Delete a cupcake"""

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message="Deleted")
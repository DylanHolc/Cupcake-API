from flask import Flask, jsonify, request, render_template
from models import Cupcake, connect_db, db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route('/api/cupcakes')
def get_cupcakes():
    """Return all cupcakes"""
    cupcakes = [cupcake.convert_to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Return a specified cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.convert_to_dict())

@app.route('/api/cupcakes', methods = ['POST'])
def add_cupcake():
    """Adds a new cupcake to the DB"""
    data = request.json

    cupcake = Cupcake(
        flavor = data['flavor'],
        size = data['size'],
        rating = data['rating'],
        image = data['image']
    )

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake = cupcake.convert_to_dict()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ['PATCH'])
def edit_cupcake(cupcake_id):
    """Update an existing cupcake"""
    
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor =data['flavor']
    cupcake.size =data['size']
    cupcake.rating =data['rating']
    cupcake.image =data['image']
   
    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake = cupcake.convert_to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """Delete an existing cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message = ' Cupcake Deleted')

@app.route('/')
def homepage():
    return render_template('index.html')

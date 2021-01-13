from models import Cupcake

def serialize_cupcakes(cupcake):
    """ Serialize a cupcake SQLAlchemy object into python dictionary """
    return {
        'id' : cupcake.id,
        'flavor' : cupcake.flavor,
        'size' : cupcake.size,
        'rating' : cupcake.rating,
        'image' : cupcake.image
    }

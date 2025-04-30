from flask import Blueprint

# Define blueprints
auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)
customer = Blueprint('customer', __name__)
racket = Blueprint('racket', __name__)
string = Blueprint('string', __name__)
order = Blueprint('order', __name__)

# Import routes after blueprints are defined
from . import auth_routes
from . import main_routes
from . import customer_routes
from . import racket_routes
from . import string_routes
from . import order_routes 
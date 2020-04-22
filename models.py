from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ArrowType
from sqlalchemy import create_engine 
import arrow

db = SQLAlchemy

class customer(db.Model):
    """List of customers"""
    __tablename__ = "customers"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(500), nullable=False)
    street_address = db.Column(db.String(100), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    state = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    country = db.Column(db.String(500), nullable=False)
    honour_points = db.Column(db.Integer, nullable=False)
    projects = db.relationship("Projects", backref="customers")
    last_active = db.relationship(db.String(15), nullable=False)

    def __repr__(self):

        return "<Customer id={}, first_name={}, last_name={}, email={}>".format(self.user_id,
                                                                                self.first_name,
                                                                                self.last_name,
                                                                                self.email)

class store(db.Model):
    """List of stores""" 
    """If store is an online and offline retailer set online_store to 2. If just a retailer set to 0, else if online store"""

    __tablename__ = "stores"

    store_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    multiple = db.Column(db.Integer, nullable = False)
    store_name = db.Column(db.Integer, nullable = False)
    online_store = db.Column(db.Integer, autoincrement = False, nullable = False)
    delivery_allowed = db.Column(db.Integer, nullable = True) #if set to 1 store allows delivery
    Store_address = db.Column(db.String(500), nullable = True)
    zipcode = db.Column(db.String(15), nullable=True)
    state = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(500),  nullable = True, unique=False)
    phone = db.Column(db.String(30), nullable=True)
    country = db.Column(db.String(500), nullable=False)

    products = db.Column(db.Integer, db.ForeignKey('products.store_id'))
    reservations = db.relationship("Reservations", backref="customers")

    def __repr__(self):
        
        return "<Store id={}, name={}, type={}, franchise={}, phone={}, email{}>".format(self.store_id, self.store_name, self.online_store,
                                                                                         self.multiple, self.phone, self.email)
class Products(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, autoincrement=True , Primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Unicode, nullable=True)
    price = db.Column(db.Numeric(asdecimal=False), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(500), nullable=True)
    icon_id = db.Column(db.Integer, db.ForeignKey('icons.icon_id'), nullable=True)
    location_id = db.relationship("store", backref="products")
    tags = db.relationship("Tag", secondary="product_tags", backref="products")
    size = db.Column(db.String(10), nullable=True) 
    weight = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    aisle = db.Column(db.String(50), nullable=True)

    delivery_qty = db.relationship("Delivery_Quantity", backref="products")
    order_qty = db.relationship("Order_Quantity", backref="products")   
    reservation = db.relationship("Reservations", backref="products")

class Icon(db.Model):
    """Icon for web usage"""

    __tablename__ = "icons"

    icon_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    credit = db.Column(db.String(100), nullable=False)

    def __repr__(self):

        return "<Icon icon_id={} url={} credit={}>".format(self.icon_id,
                                                           self.url,
                                                           self.credit)


class Tag(db.Model):
    """Tag for products i.e. Certified Organic, Locally Grown"""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):

        return "<Tag tag_id={} name={}>".format(self.tag_id, self.name)


class Product_Tag(db.Model):
    """Association table relating Tag class to Product class"""

    __tablename__ = "product_tags"

    prod_tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)

    def __repr__(self):

        return "<Product_Tag prod_tag_id={} product_id={} tag_id={}>".format(self.prod_tag_id,
                                                                             self.product_id,
                                                                             self.tag_id)

class Delivery(db.Model):
    """A delivery of incoming products, composed of Delivery-Quantities"""

    __tablename__ = "deliveries"

    delivery_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_name = db.Column(db.String(500), nullable=True)
    received_at = db.Column(ArrowType, nullable=False)  # or db.DateTime v. db.TimeStamp?

    quantities = db.relationship("Delivery_Quantity", backref="delivery")

    def __repr__(self):

        return "<Delivery delivery_id={} vendor={} received_at={}>".format(self.delivery_id,
                                                                           self.vendor,
                                                                           self.received_at)


class Delivery_Quantity(db.Model):
    """An amount of a certain product, in each delivery"""

    __tablename__ = "delivery_quantities"

    deliv_qty_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    product_qty = db.Column(db.Integer, nullable=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey("deliveries.delivery_id"), nullable=False)

    def __repr__(self):

        return "<Delivery_Quantity deliv_qty_id={} product_id={} product_qty={} delivery_id={}>".format(self.deliv_qty_id,
                                                                                                        self.product_id,
                                                                                                        self.product_qty,
                                                                                                        self.delivery_id)


class Order(db.Model):
    """An order placed by a customer, composed of Order-Quantities"""

    __tablename__ = "orders"

    order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.user_id"), nullable=False)
    placed_at = db.Column(ArrowType, nullable=False)  # or db.DateTime v. db.TimeStamp?
    total = db.Column(db.Numeric, nullable=False)
    pickup_id = db.Column(db.Integer, db.ForeignKey("stores.store_id"), nullable=False)
    received_at = db.Column(ArrowType, nullable=True)  # or db.DateTime v. db.TimeStamp?

    pickup = db.relationship("Store", backref="orders")

    quantities = db.relationship("Order_Quantity", backref="orders")

    def __repr__(self):

        return "<Order order_id={} customer_id={} total={} placed_at={} received_at={}>".format(self.order_id,
                                                                                                self.customer_id,
                                                                                                self.total,
                                                                                                self.placed_at,
                                                                                                self.received_at)


class Order_Quantity(db.Model):
    """An amount of a certain product, in each order"""

    __tablename__ = "order_quantities"

    order_qty_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    product_qty = db.Column(db.Integer, nullable=False, default=1)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)

    def __repr__(self):

        return "<Order_Quantity order_qty_id={} product_id={} product_qty={} order_id={}>".format(self.order_qty_id,
                                                                                                  self.product_id,
                                                                                                  self.product_qty,
                                                                                                  self.order_id)

class Reservations(db.Model):
    """Reserving objects to try"""
    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.store_id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))

    quantities = db.relationship("Reservation_Quantity", backref="reservations")

class Reservation_Quantity(db.Model):
    """An amount of a certain product in each order"""

    __tablename__ = "reservation_quantities
    reservation_quantity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    product_qty = db.Column(db.Integer, nullable=False, default=1)
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.reservation_id"), nullable=False)


def connect_to_db(app, database='postgresql://postgres:Bbklct321@localhost:5432/FS'):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from routes import app
    connect_to_db(app)
    db.create_all()
    example_data()
    print("Connected to DB.")

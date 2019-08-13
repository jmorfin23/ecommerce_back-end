from app import app, db
from flask import request, jsonify
from app.models import Product, Cart

@app.route('/')
def index():
    #nothing renders on the page
    return ''

#in order to use the flask shell for db
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'product': Product}

#api route for saving products
@app.route('/api/save', methods=['POST'])
def save():

    try: #getting headers
        title = request.headers.get('title')
        price = request.headers.get('price')
        description = request.headers.get('description')


        #if ANY info missing, make them enter in every
        if not title or not price or not description:
            return jsonify({'Error': 'Enter all information' })

        #this runs if all info is included, now save the product
        product = Product(title=title, price=price, description=description)


        #then we commit to the database through sessions
        db.session.add(product)
        db.session.commit()

        #if this all gets run then return a success # NOTE:
        return jsonify({'Success': 'Your product was saved'})
    except:
        return jsonify({'Error': 'Error #001, could not be saved'})


#route for deleting from product table
@app.route('/api/delete', methods=['DELETE'])
def delete():

    try:
        id = request.headers.get('id')
        #querying the database
        product = Product.query.filter_by(id=id).first()

        if not product:
            return jsonify({ 'success': 'the product does not exist'})

        name = product.title

        #delete product from database
        db.session.delete(product)

        db.session.commit()

        return jsonify({'Success': f'Product: {name} deleted.'})
    except:
        return jsonify({'Error': 'Error 002: Something is wrong'})

#route for retrieving the whole product list table
@app.route('/api/retrieve', methods=['GET'])
def retrieve():

    try:
        #querying all data in the product table to display in front end.
        product = Product.query.all()

        if product == []:
            return jsonify ({ 'Error': 'No products'})

        alist = []

        for p in product:
            blist = {
            'id': p.id,
            'title': p.title,
            'price': p.price,
            'description': p.description
            }
            alist.append(blist)

        return jsonify({ 'success': {
        'products': alist
        }})

    except:
        return jsonify({ 'Error': 'Error something is wrong. check it out.'})

#route for saving to cart
@app.route('/api/saved', methods=['POST', 'GET'])
def saved():
    try:
        #get headers
        title = request.headers.get('title')
        price = request.headers.get('price')
        description = request.headers.get('description')

        cart = Cart(title=title, price=price, description=description)

        if not cart:
            return jsonify({ 'Error': 'Not cart ha.'})

        # adding to cart table in database
        db.session.add(cart)

        #committing dis
        db.session.commit()

        #querying the database to get the whole cart as I save it
        ca = Cart.query.all()
        # print(ca)
        if ca == []:
            return jsonify({ 'Error' :'Your cart is empty'})

        clist = []

        for c in ca:
            dlist = {
            'id': c.id,
            'title': c.title,
            'price': c.price,
            'description': c.description
            }
            clist.append(dlist)

        return jsonify({ 'Success': {
        'cart': clist
        }})

    except:
        return jsonify({'Error': 'Try again haha'})


#route for deleted from cart.
@app.route('/api/deleted', methods=['DELETE', 'GET'])
def deleted():

    try:
        id = request.headers.get('id')

        cart = Cart.query.filter_by(id=id).first()

        if cart == []:
            return jsonify({ 'Success': 'That product is not in the cart'})

        name = cart.title


        #deleting product from cart
        db.session.delete(cart)

        #commit
        db.session.commit()

        # #querying new cart to update state
        # new_cart = Cart.query.all()
        #
        #
        # if new_cart == []:
        #     return jsonify({ 'Error' :'Your cart is empty'})
        #
        # print('test')
        # print(new_cart)
        #
        # zlist = []
        #
        # for a in new_cart:
        #     print(new_cart[a])
        # for new in new_cart:
        #     print(new_cart[new])

        return jsonify({'Success': f'Product: {name} deleted.'})

    except:
        return jsonify({ 'Error': 'There was an issue with your request'})

#route for getting the cart.
@app.route('/api/retrieved', methods=['GET'])
def retrieved():
    carts = Cart.query.all()

    if carts == []:
        return jsonify ({ 'Success': {
        'cart': []
        }})

    clist = []

    for cart in carts:
        dlist = {
        'id': cart.id,
        'title': cart.title,
        'price': cart.price,
        'description': cart.description
        }
        clist.append(dlist)

    return jsonify({ 'Success': {
    'cart': clist
    }})

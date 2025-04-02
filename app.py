from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

products = [
    {"sku": "001", "name": "Dell Laptop XP500", "price": 1299.99, "quantity": 10,
        "description": "A high-performance laptop", "cpu": "Intel i7 -Nvidia GTX - 32GB"},
    {"sku": "002", "name": "Apple MacBook Pro", "price": 1599.99, "quantity": 20,
        "description": "good laptop", "cpu": "Mac - Nvidia GTX - 64GB"},
    {"sku": "003", "name": "Dell", "price": 999.99, "quantity": 13,
        "description": "okay laptop", "cpu": "XP - Nvidia GTX - 128GB"}
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(products)


@app.route("/api/products/<string:sku>", methods=["GET"])
def get_product(sku):
    for product in products:
        if sku == product.get("sku"):
            return jsonify(product), 200
    return jsonify({"error": f"The product with sku {sku} not found."}), 404


@app.route("/api/products", methods=["POST"])
def add_product():
    new_product = request.json
    if not new_product:
        return jsonify({"error": "The payload cannot be empty"}), 400
    if "sku" not in new_product or "name" not in new_product:
        return jsonify({"error": "Missing a required field, (name, sku) are required"}), 400
    for product in products:
        if new_product.get("sku") == product.get("sku"):
            return jsonify({"error": "sku is already present"}), 400

    products.append(new_product)

    return jsonify(new_product), 201


@app.route("/api/products/<string:sku>", methods=["PUT"])
def update_product(sku):
    product_update = None
    for product in products:
        if sku == product.get("sku"):
            product_update = product

    if product_update:
        new_product = request.json
        product_update.update(new_product)
        return jsonify({"status": "product successfully updated", "products": products})

    return jsonify({"error": "Product not found"})


@app.route("/api/products/<string:sku>", methods=["DELETE"])
def delete_product(sku):
    product_delete = None
    for product in products:
        if sku == product.get("sku"):
            product_delete = product

    if product_delete:
       products.remove(product_delete)
       return jsonify({"status": "product successfully deleted", "products": products})

    return jsonify({"error": "Product not found"})


if __name__ == "__main__":
    app.run(debug=True)

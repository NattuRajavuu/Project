from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from utils.helpers import cart_items, cart_totals, find_product, load_products, product_matches


product_bp = Blueprint("products", __name__)


@product_bp.get("/products")
def products():
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "All")
    sort = request.args.get("sort", "featured")
    items = load_products()

    if query:
        items = [item for item in items if query in f"{item['name']} {item['description']} {item['category']}".lower()]
    if category != "All":
        items = [item for item in items if item["category"] == category]
    if sort == "low":
        items = sorted(items, key=lambda item: item["price"])
    elif sort == "high":
        items = sorted(items, key=lambda item: item["price"], reverse=True)
    elif sort == "rating":
        items = sorted(items, key=lambda item: item["rating"], reverse=True)

    categories = ["All", *sorted({item["category"] for item in load_products()})]
    return render_template("products.html", products=items, categories=categories, selected_category=category, query=query, sort=sort)


@product_bp.get("/product/<product_id>")
def product_details(product_id):
    product = find_product(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products.products"))
    related = [item for item in load_products() if item["category"] == product["category"] and item["id"] != product_id][:3]
    viewed = session.setdefault("recently_viewed", [])
    if product_id in viewed:
        viewed.remove(product_id)
    viewed.insert(0, product_id)
    session["recently_viewed"] = viewed[:5]
    return render_template("product_details.html", product=product, related=related)


@product_bp.post("/cart/add/<product_id>")
def add_to_cart(product_id):
    quantity = max(1, int(request.form.get("quantity", 1)))
    if not find_product(product_id):
        flash("Product not found.", "error")
        return redirect(url_for("products.products"))
    cart = session.setdefault("cart", {})
    cart[product_id] = int(cart.get(product_id, 0)) + quantity
    session["cart"] = cart
    flash("Added to cart.", "success")
    return redirect(request.referrer or url_for("products.cart"))


@product_bp.post("/cart/update/<product_id>")
def update_cart(product_id):
    quantity = int(request.form.get("quantity", 1))
    cart = session.setdefault("cart", {})
    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity
    session["cart"] = cart
    return redirect(url_for("products.cart"))


@product_bp.get("/cart")
def cart():
    return render_template("cart.html", items=cart_items(), totals=cart_totals())


@product_bp.get("/checkout")
def checkout():
    return render_template("checkout.html", items=cart_items(), totals=cart_totals())


@product_bp.post("/checkout")
def place_order():
    if not cart_items():
        flash("Add an item before checkout.", "error")
        return redirect(url_for("products.products"))
    session["last_order"] = {"items": cart_items(), "totals": cart_totals(), "order_id": "LA-2056"}
    session["cart"] = {}
    flash("Order placed successfully.", "success")
    return redirect(url_for("products.profile"))


@product_bp.post("/wishlist/<product_id>")
def wishlist_toggle(product_id):
    if not find_product(product_id):
        flash("Product not found.", "error")
        return redirect(url_for("products.products"))
    wishlist = session.setdefault("wishlist", [])
    if product_id in wishlist:
        wishlist.remove(product_id)
        flash("Removed from wishlist.", "success")
    else:
        wishlist.append(product_id)
        flash("Saved to wishlist.", "success")
    session["wishlist"] = wishlist
    return redirect(request.referrer or url_for("products.wishlist"))


@product_bp.get("/wishlist")
def wishlist():
    products_by_id = {product["id"]: product for product in load_products()}
    items = [products_by_id[item] for item in session.get("wishlist", []) if item in products_by_id]
    return render_template("wishlist.html", products=items)


@product_bp.get("/profile")
def profile():
    products_by_id = {product["id"]: product for product in load_products()}
    recent = [products_by_id[item] for item in session.get("recently_viewed", []) if item in products_by_id]
    return render_template("profile.html", recent=recent, totals=cart_totals(), last_order=session.get("last_order"))


@product_bp.get("/api/products")
def api_products():
    return jsonify({"products": load_products()})


@product_bp.get("/api/recommendations")
def api_recommendations():
    message = request.args.get("q", "")
    return jsonify({"products": product_matches(message)})

from flask import Blueprint, flash, redirect, render_template, request, session, url_for


auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/login")
def login():
    return render_template("login.html")


@auth_bp.post("/login")
def login_submit():
    email = request.form.get("email", "").strip()
    if not email:
        flash("Email is required.", "error")
        return redirect(url_for("auth.login"))
    session["user"] = {"name": email.split("@")[0].title(), "email": email, "tier": "Black"}
    flash("Welcome back.", "success")
    return redirect(url_for("products.profile"))


@auth_bp.get("/register")
def register():
    return render_template("register.html")


@auth_bp.post("/register")
def register_submit():
    name = request.form.get("name", "Atelier Member").strip()
    email = request.form.get("email", "").strip()
    if not email:
        flash("Email is required.", "error")
        return redirect(url_for("auth.register"))
    session["user"] = {"name": name, "email": email, "tier": "Black"}
    flash("Account created.", "success")
    return redirect(url_for("products.profile"))


@auth_bp.post("/logout")
def logout():
    session.pop("user", None)
    flash("Signed out.", "success")
    return redirect(url_for("home"))

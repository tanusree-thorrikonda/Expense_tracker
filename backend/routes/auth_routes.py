from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from ..models import db
from ..models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if session.get("user_id"):
        return redirect(
            url_for("transaction.dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )


        if not username or not email or not password:

            flash(
                "All required fields must be completed.",
                "error"
            )

            return render_template("register.html")


        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return render_template("register.html")


        if len(password) < 8:

            flash(
                "Password must contain at least 8 characters.",
                "error"
            )

            return render_template("register.html")


        existing_username = User.query.filter_by(
            username=username
        ).first()


        if existing_username:

            flash(
                "Username is already registered.",
                "error"
            )

            return render_template("register.html")


        existing_email = User.query.filter_by(
            email=email
        ).first()


        if existing_email:

            flash(
                "Email is already registered.",
                "error"
            )

            return render_template("register.html")


        user = User(
            username=username,
            email=email
        )

        user.set_password(password)


        db.session.add(user)

        db.session.commit()


        flash(
            "Registration successful. Please log in.",
            "success"
        )


        return redirect(
            url_for("auth.login")
        )


    return render_template("register.html")


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if session.get("user_id"):
        return redirect(
            url_for("transaction.dashboard")
        )


    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        user = User.query.filter_by(
            email=email
        ).first()


        if user is None or not user.check_password(password):

            flash(
                "Invalid email or password.",
                "error"
            )

            return render_template("login.html")


        session.clear()

        session["user_id"] = user.id

        session["username"] = user.username


        flash(
            "Login successful.",
            "success"
        )


        return redirect(
            url_for("transaction.dashboard")
        )


    return render_template("login.html")


@auth_bp.route(
    "/logout",
    methods=["POST"]
)
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )
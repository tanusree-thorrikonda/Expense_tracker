from flask import Flask

from .config import Config
from .models import db
from .routes.auth_routes import auth_bp
from .routes.transaction_routes import transaction_bp


def create_app():

    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    app.config.from_object(Config)

    db.init_app(app)


    with app.app_context():
        db.create_all()


    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)

    # Initialize Flask-Admin database web viewer
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
    from flask import session
    from .models.user import User
    from .models.transaction import Transaction

    class SecureModelView(ModelView):
        def is_accessible(self):
            return session.get("user_id") is not None

    admin = Admin(app, name='Database Viewer')
    admin.add_view(SecureModelView(User, db.session, endpoint='admin_user'))
    admin.add_view(SecureModelView(Transaction, db.session, endpoint='admin_transaction'))

    @app.context_processor
    def inject_user():
        from flask import session
        from .models.user import User
        user = None
        if session.get("user_id"):
            user = User.query.get(session["user_id"])
        return dict(current_user=user)

    return app
from .auth.views import bp as auth_bp
from .home.views import bp as home_bp


def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

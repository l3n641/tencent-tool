from .auth.views import bp as auth_bp
from .home.views import bp as home_bp
from .config_type.views import bp as config_type_bp


def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(config_type_bp)

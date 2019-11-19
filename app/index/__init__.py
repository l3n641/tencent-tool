from .index.views import bp as index_bp


def init_app(app):
    app.register_blueprint(index_bp)

from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request
from flask_babel import Babel, _

babel = Babel()

def get_locale():
    lang = request.cookies.get('lang')
    print(f"get_locale: cookie lang = {lang}")
    if lang in ['en', 'es']:
        return lang
    best = request.accept_languages.best_match(['en', 'es']) or 'en'
    print(f"get_locale: fallback lang = {best}")
    return best


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = '../translations'

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    babel.init_app(app, locale_selector=get_locale)

    # Combine both into one context processor
    @app.context_processor
    def inject_globals():
        return dict(_=_, lang=get_locale())

    from .routes import main
    app.register_blueprint(main)

    return app

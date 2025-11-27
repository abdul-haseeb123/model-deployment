import os
from dotenv import load_dotenv
from flask import Flask

from api.extensions import celery_init_app


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.config["CELERY"] = {
        "broker_url": os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),
        "result_backend": os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379"),
    }
    env_path = os.path.join(os.getcwd(), ".env.local")
    load_dotenv(env_path)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    celery_init_app(app)
    from . import routes
    app.register_blueprint(routes.bp)


    return app
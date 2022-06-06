from flask import Flask, jsonify, request, render_template
from flask_babel import Babel
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest

from config import Config
from exceptions import APIError, APIAuthError

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    @app.errorhandler(BadRequest)
    def handle_bad_request(err):
        response = {"error": err.description, "message": ""}
        if len(err.args) > 0:
            response["message"] = err.args[0]
        # Add some logging so that we can monitor different types of errors
        app.logger.error(f"{err.description}: {response['message']}")
        if request.is_json:
            return jsonify(response), 400
        return err.description, 400

    @app.errorhandler(APIError)
    def handle_exception(err):
        """Return custom JSON when APIError or its children are raised"""
        response = {"error": err.description, "message": ""}
        if len(err.args) > 0:
            response["message"] = err.args[0]
        # Add some logging so that we can monitor different types of errors
        app.logger.error(f"{err.description}: {response['message']}")
        if request.is_json:
            return jsonify(response), err.code
        return err.description

    from users import bp as user_bp
    app.register_blueprint(user_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

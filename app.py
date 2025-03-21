

"""import os
from flask import Flask
from flask_smorest import Api
from db import db
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
 
def create_app(db_url=None):
    app = Flask(__name__)
         
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_NODIFICATIONS"]=False
    db.init_app(app)

 
    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()
 
 
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app"""


import os
from flask import Flask,jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
 
from db import db
import models           #includes all the  file present in model folder;since __init__file meh 2 file import kar diya already

from blocklist import BLOCKLIST 
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.store import blp as StoreBlueprint
from resources.user import blp as UserBlueprint


import secrets

 
def create_app(db_url=None):
    app = Flask(__name__)# Creating a Flask app instance
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    migrate=Migrate(app,db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"]= "222426618778384915599074949804341355139"
    jwt=JWTManager(app)


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return(
            jsonify(
                {"description":"The token has been revoked","error":"token_revoked"}

            ),
            401,
        )
        

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
       #look in the database and see whether the  user is an admin
       if identity=='1':
           return {"is_admin":True}
       return {"is_admin":False}


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )
 
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )
 
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
 
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
   
   
    
   
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
 





 

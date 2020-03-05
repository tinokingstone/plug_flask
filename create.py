from plug_app import db
from plug_app.models import User, Post , Skilltag, Projects

db.drop_all()
db.create_all()


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INET
import src.webui as webui
from sqlalchemy.orm import relationship

webui.app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ipeuser:ipeuser@localhost:5432/ipe"
webui.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(webui.app)


#  Class for table host
class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'))
    value = db.Column(INET, nullable=False)

    def __repr__(self):
        return '<Host>'


#  Class for table vulnerability
# TODO: after creating table User add field "creator" (Integer - id of user)
class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'))
    object = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    full_path = db.Column(db.String, nullable=False)
    criticality = db.Column(db.Integer, default=1)
    probability = db.Column(db.Integer, default=1)
    final_criticality = db.Column(db.Integer, default=1)
    description = db.Column(db.Text, nullable=False)
    risk = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=False)
    recommendation = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Vulnerability>'


#  Class for table project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    host_history = db.Column(db.Integer, nullable=True)
    retro_delete = db.Column(db.Boolean, default=False)

    # relationships for CASCADE delete
    host = relationship(Host, backref="project", passive_deletes=True)
    vulnerability = relationship(Vulnerability, backref="project", passive_deletes=True)

    def __repr__(self):
        return '<Project>'
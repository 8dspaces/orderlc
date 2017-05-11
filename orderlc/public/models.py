# -*- coding: utf-8 -*-
from flask_login import current_user
from flask import current_app

from datetime import date

from orderlc.database import (
    Column,
    # ReferenceCol,
    relationship,
    db,
    Model,
    # SurrogatePK,
)
from sqlalchemy.types import Enum

#货柜, 长x宽x高=体积
class Container(Model):

    __tablename__ = 'container'
    LOCATION = (
        u'广州',
        u'老挝',
        u'在途'
    )

    id = Column(db.Integer, primary_key=True)

    length = Column(db.Integer)
    width = Column(db.Integer)
    height = Column(db.Integer)

    #广州／老挝／在途，根据位置决定下一步逻辑
    location = Column(Enum(*LOCATION,name='container_location'))

    def __repr__(self):
        return 'Container #' + str(self.id)
    def __str__(self):
        return 'Container #' + str(self.id)

class Customer(Model):

    __tablename__ = 'customer'

    id = Column(db.Integer, primary_key=True)

    name = Column(db.String(120), nullable=False)

    phone = Column(db.String(120), nullable=False)
    email = Column(db.String(120), nullable=False)
    address = Column(db.String(120), nullable=False)
    register_date = Column(db.Date, default=date.today)

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

#货柜, 长x宽x高=体积
class Good(Model):

    __tablename__ = 'good'

    id = Column(db.Integer, primary_key=True)

    name = Column(db.String(120), nullable=False)

    length = Column(db.Integer)
    width = Column(db.Integer)
    height = Column(db.Integer)
    quantity = Column(db.Integer)
    weight = Column(db.Float)

    input_date = Column(db.Date, default=date.today)

    container_id = db.Column(db.Integer, db.ForeignKey('container.id'))
    container = db.relationship('Container')


    to_address = Column(db.String(120), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer')

    unit_price = Column(db.Float)
    amount = Column(db.Float)

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

    def get_location(self):
        return self.container.location

    # created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    # updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, onupdate=db.func.now())
    #
    # description = Column(db.String(255), nullable=True)
    #
    # # Default priority for this script to run. The lesser of this vs. the user priority is the job priority
    # priority = Column(db.Integer, unique=False, nullable=False, default=1)
    #
    # is_active = Column(db.Boolean(), default=True)
    #
    # # Defines whether a login is required to run this script, note that without a login the result of
    # # any execution must be public. Probably requires a warning for those users not to upload sensitive data
    # requires_login = Column(db.Boolean(), unique=False, nullable=False, default=True)
    #
    #
    # def load_config(self):
    #     '''
    #     Load JSON config from file
    #     :return: dict of config
    #     '''
    #
    #     with open(self.config_path, 'r') as f:
    #         return json.load(f)
    #
    # def load_docs(self):
    #     '''
    #     Load JSON config from file
    #     :return: dict of config
    #     '''
    #     if self.doc_path:
    #         with open(self.doc_path, 'r') as f:
    #             return f.read()
    #     else:
    #         return None

    # @property
    # def is_authorised(self):
    #     return self.requires_login is False or current_user.is_authenticated()


# class Job(SurrogatePK, Model):
#
#     __tablename__ = 'jobs'
#
#     script_id = ReferenceCol('scripts')
#     script = relationship('Script', backref='jobs')
#
#     user_id = ReferenceCol('users', nullable=True)
#     user = relationship('User', backref='jobs')
#
#     path = Column(db.String(255), unique=True, nullable=False)
#
#     created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
#     updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, onupdate=db.func.now())
#
#     # Job start and stop times; must check for status to determine if stop is failure or completion
#     started_at = Column(db.DateTime, nullable=True, default=None)
#     stopped_at = Column(db.DateTime, nullable=True, default=None)
#
#     status = Column(db.Enum(STATUS_WAITING, STATUS_RUNNING, STATUS_COMPLETE, STATUS_ERROR, name='status'), nullable=False, default=STATUS_WAITING)
#
#     # Calculated priority for this job (the lesser of the script priority and the user priority)
#     priority = Column(db.Integer, unique=False, nullable=False, default=1)
#
#     pid = Column(db.Integer, unique=False, nullable=True)
#
#     config = Column(db.String(), nullable=True)
#
#     @hybrid_property
#     def priority_score(self):
#         return float( (dt.datetime.utcnow-self.created_at).minutes ) / self.priority
#
#     @property
#     def is_waiting(self):
#         return self.status == STATUS_WAITING
#
#     @property
#     def is_running(self):
#         return self.status == STATUS_RUNNING
#
#     @property
#     def is_complete(self):
#         return self.status == STATUS_COMPLETE
#
#     @property
#     def is_error(self):
#         return self.status == STATUS_ERROR
#
#     @property
#     def duration(self):
#         return self.stopped_at - self.started_at
#
#     @property
#     def console(self):
#         try:
#             with open(os.path.join(self.path, 'STDOUT'), 'rU') as f:
#                 console = f.read() #.decode('utf8')
#
#         except IOError:
#             console = ""
#
#         return console
#
#     def get_output_files(self):
#         cwd = os.path.join(self.path, 'output')
#         files = ''
#         if os.path.isdir(cwd):  # Execution has begun/finished
#             # Filter files for files and not excluded above list
#             # FIXME: The exclude list should come from config
#             # FIXME: Add excluded list of *extensions* for download
#             files = [os.path.join(cwd, f) for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))
#                      and os.path.splitext(f)[1] not in current_app.config.get('EXCLUDED_EXTENSIONS_FOR_DOWNLOAD', [])
#                      and f not in current_app.config.get('EXCLUDED_FILES_FOR_DOWNLOAD', [])]
#         return files
#
#     @property
#     def has_output(self):
#         return self.stopped_at is not None and len(self.get_output_files()) > 0

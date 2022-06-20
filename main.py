from flask import Flask, Blueprint
from clientes import clientes_blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.register_blueprint(clientes_blueprint)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@0.0.0.0/cliente'
db = SQLAlchemy(app)

class Cliente (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable = False)
    razao_social = db.Column(db.String(50), nullable = False)
    cnpj = db.Column(db.String(20), nullable = False)
    data_inclusao = db.Column(db.DateTime, nullable = False)
    
    def to_json (self):
        return {"id":  self.id, "Nome": self.nome, "Razao social": self.razao_social, "Cnpj": self.cnpj, "Data de inclusao": self.data_inclusao}
  
app.run()
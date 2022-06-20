from flask import Blueprint, request, Response
from main import db, Cliente
import json

clientes_blueprint = Blueprint('clientes', __name__)

@clientes_blueprint.route("/clientes", methods=["GET"])
def seleciona_clientes ():
    clientes_objeto = Cliente.query.all()
    clientes_json = [Cliente.to_json() for cliente in clientes_objeto ]
    
    return gerar_response(200, "clientes", clientes_json)

@clientes_blueprint.route("/cliente/<id>", methods=["GET"])
def seleciona_cliente ():
    cliente_objeto = Cliente.query.filter_by(id = id).first()
    cliente_json = Cliente.to_json()
    
    return gerar_response (200, "clientes", cliente_json)

@clientes_blueprint.route("/cliente", methods=["POST"])
def cria_cliente():
    body = request.get_json()
    try: 
        cliente = Cliente(nome=body["Nome"], razao_social=body["Razao social"], cnpj=body["Cnpj"], data_inclusao=body["Data de inclusao"])
        db.session.add(cliente)
        db.session.commit()
        
        return gerar_response(201, "cliente", cliente.to_json(), "Cliente criado com sucesso!")
        
    except Exception as e:
        print (e)
        
        return gerar_response(400, "cliente", {}, "Erro ao cadastrar")
    
@clientes_blueprint.route("/cliente/<id>", methods=["PUT"])
def update_cliente(id):
    cliente_objeto = Cliente.query.filter_by(id = id).first()
    body = request.get_json()
    try: 
        if ('Nome' in body):
            cliente_objeto.nome = body["Nome"]
        if ('Razao social' in body):
            cliente_objeto.razao_social = body["Razao social"]
        if ('Cnpj' in body): 
            cliente_objeto.cnpj= body["Cnpj"]
        if ('Data de inclusao' in body):
            cliente_objeto.data_inclusao= body["Data de inclusao"]
            
        db.session.add(cliente_objeto)
        db.session.commit()
        return gerar_response (200, "cliente", Cliente.to_json(), "Cliente atualizado com sucesso")
    
    except Exception as e:
        print (e)
        return gerar_response (400, "cliente", {}, "Erro ao atualizar cliente")   

@clientes_blueprint.route("/cliente/<id>", methods=["DELETE"])
def deleta_cliente(id):
    cliente_objeto = Cliente.query.filter_by(id = id).first()
    try:
        db.session.delete(cliente_objeto)
        db.session.commit()
        return gerar_response(200, "cliente", cliente_objeto.to_json(), "Cliente deletado com sucesso")
    
    except Exception as e:
        print (e)
        return gerar_response (400, "cliente", {}, "Erro ao deletar cliente")

def gerar_response (status, nome_do_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_do_conteudo] = conteudo
    
    if (mensagem):
        body["mensagem"] = mensagem
        
    return Response (json.dumps(body), status=status, mimetype="application/json")
from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios, status_aceitos
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# USUARIOS = {
#     'rafael':'123',
#     'leandro':'321'
# }
#
# @auth.verify_password
# def verificacao(login, senha):
#     if not(login, senha):
#         return False
#     return Usuarios.get(login) == senha

@auth.verify_password
def verificacao(login, senha):
    if not(login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response={
                'nome': pessoa.nome,
                'idade':pessoa.idade,
                'id':pessoa.id
            }
            return response

        except AttributeError:
            response={
                'status':'error',
                'mensagem':'Pessoa nao encontrada'
            }
            return response

    @auth.login_required
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json

        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()

        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

    @auth.login_required
    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            pessoa.delete()
            response = {
                'status':'sucesso',
                'mensagem': 'Pessoa de nome {} deletada'.format(nome)
            }
            return response
        except IndexError:
            response = {
                'status': 'erro',
                'mensagem': 'Não foi possível localizar a pessoa {} '.format(nome)
            }
            return response

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()

        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

class ListaAtividade(Resource):
    def get(self):

        atividades = Atividades.query.all()
        response = []
        for i in atividades:
            try:
                # pessoa = Pessoas.query.filter_by(id=i.pessoa_id)
                response.append({
                    'id': i.id,
                    'nome': i.nome,
                    'pessoa': i.pessoa.nome,
                    'status': i.status
                })
            except AttributeError:
                continue
        if(response != []):
            return response
        else:
            response = {
                'status': 'erro',
                'mensagem': 'Não há atividades cadastradas'
            }
            return response

    def post(self):
        dados = request.json
        if dados['status'] in status_aceitos:
            try:
                pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
                atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status=dados['status'])
                atividade.save()
                response = {
                    'pessoa':atividade.pessoa.nome,
                    'nome':atividade.nome,
                    'status':atividade.status,
                    'id':atividade.id
                }
                return response

            except AttributeError:
                response = {
                    'status': 'erro',
                    'mensagem': 'Pessoa {} não encontrada '.format(dados['pessoa'])
                }
                return response

        else:
            response = {
                'status': 'erro',
                'mensagem': 'Status {} inválido, somente são aceitos: {} '.format(dados['status'], status_aceitos)
            }
            return response

class ListaAtividadesPorResponsavel(Resource):
    @auth.login_required
    def get(self, resp):
        try:
            responsavel = Pessoas.query.filter_by(nome=resp).first()
            atividadesResponsavel = Atividades.query.filter_by(pessoa=responsavel)
            response = dict()
            response['nome'] = responsavel.nome
            response['atividades'] = [{"id":i.id, "nome":i.nome} for i in atividadesResponsavel]
            return response

        except IndexError:
            response = {
                'status':'erro',
                'mensagem':'Responsavel {} inexistente'.format(resp)
            }
            return response

class AtividadePorID(Resource):
    @auth.login_required
    def get(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            response={
                'id':atividade.id,
                'nome':atividade.nome,
                'responsavel':atividade.pessoa.nome,
                'status':atividade.status
            }
            return response

        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Não há atividade para o id {}'.format(id)
            }
            return response

    @auth.login_required
    def put(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            alteracao = request.json
            if alteracao['status'] in status_aceitos:
                atividade.status = alteracao['status']
                atividade.save()
            response = {
                'id': atividade.id,
                'nome': atividade.nome,
                'responsavel': atividade.pessoa.nome,
                'status': atividade.status
            }
            return response

        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Não há atividade para o id {}'.format(id)
            }
            return response

api.add_resource(Pessoa, "/pessoa/<string:nome>/")
api.add_resource(ListaPessoas, "/pessoa/")
api.add_resource(ListaAtividade, "/atividades/")
api.add_resource(ListaAtividadesPorResponsavel, '/atividades/<string:resp>/')
api.add_resource(AtividadePorID, '/atividades/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)
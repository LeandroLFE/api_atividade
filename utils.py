from models import Pessoas, Atividades

# Insere na Tabela Pessoas
def insere_pessoas():
    pessoa = Pessoas(nome='Gui', idade=28)
    print(pessoa)
    pessoa.save()

# Consulta a Tabela Pessoas
def consulta():
    pessoa = Pessoas.query.all()
    print(pessoa)
    # pessoa = Pessoas.query.filter_by(nome='Leandro').first()
    # print(pessoa.nome, " " ,pessoa.idade)

# Altera uma Pessoa na Tabela Pessoas
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='leandro').first()
    pessoa.nome = "leandro"
    pessoa.save()
    print(pessoa)

# Exclui uma Pessoa na Tabela Pessoas
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Rafael').first()
    pessoa.delete()

#########################################################################

def consulta_atividade():
    atividades = Atividades.query.all()
    print(atividades)

def altera_atividade():
    atividades = Pessoas.query.all()
    for i in atividades:
        i.status = "pendente"
        i.save()
    # atividade.status = "pendente"

    print("ok")

def exclui_Atividade():
    atividades = Atividades.query.all()
    for i in atividades:
        i.delete()
    print("deletado")

if __name__ == '__main__':
    # altera_pessoa()
    insere_pessoas()
    # exclui_pessoa()
    # consulta()
    # consulta_atividade()
    # altera_atividade()
    # exclui_Atividade()
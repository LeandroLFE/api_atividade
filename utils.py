from models import Pessoas

# Insere na Tabela Pessoas
def insere_pessoas():
    pessoa = Pessoas(nome='Rafael', idade=25)
    print(pessoa)
    pessoa.save()

# Consulta a Tabela Pessoas
def consulta():
    pessoa = Pessoas.query.all()
    print(pessoa)
    pessoa = Pessoas.query.filter_by(nome='Leandro').first()
    print(pessoa.nome, " " ,pessoa.idade)

# Altera uma Pessoa na Tabela Pessoas
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Guilherme').first()
    pessoa.nome = "Gui"
    pessoa.save()
    print(pessoa)

# Exclui uma Pessoa na Tabela Pessoas
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Rafael').first()
    pessoa.delete()

if __name__ == '__main__':
    # altera_pessoa()
    # insere_pessoas()
    # exclui_pessoa()
    consulta()
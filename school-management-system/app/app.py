from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

# Lista de professores
professores_data = [
    {"nome": "Max Moura", "cargo": "Professor", "conteudo": []},
    {"nome": "Thaynan Rezende", "cargo": "Professor", "conteudo": []},
    {"nome": "Karine Moço", "cargo": "Professora / Coordenadora", "conteudo": []},
    {"nome": "Ana Maria Bragança", "cargo": "Professora", "conteudo": []},
    {"nome": "Roberta pereira", "cargo": "Professora", "conteudo": []},
    {"nome": "Keison Costa", "cargo": "Professor", "conteudo": []},
]

@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/professores', methods=['GET'])
def professores():
    return render_template('professores.html', professores=professores_data)

# Rota para adicionar conteúdo programático ao professor
@app.route('/professores/adicionar-conteudo', methods=['POST'])
def adicionar_conteudo_professor():
    nome_prof = request.form.get('professor')
    conteudo = request.form.get('conteudo')
    for prof in professores_data:
        if prof['nome'] == nome_prof:
            prof['conteudo'].append(conteudo)
            break
    return redirect(url_for('professores'))


# Cadastro de Aluno
@app.route('/alunos', methods=['GET'])
def alunos():
    return render_template('cadastro_aluno.html')

# Rota para processar cadastro de aluno (futuro)
@app.route('/alunos/cadastrar', methods=['POST'])
def cadastrar_aluno():
    # Aqui você pode processar e salvar os dados do aluno futuramente
    # Por enquanto, apenas redireciona para a página de alunos
    return redirect(url_for('alunos'))

@app.route('/agenda')
def agenda():
    return render_template('agenda.html')

@app.route('/conteudo')
def conteudo():
    return render_template('placeholder.html', title='Conteúdo Programático')

@app.route('/jornal')
def jornal():
    return render_template('jornal.html')

@app.route('/lista-alunos')
def lista_alunos():
    return render_template('placeholder.html', title='Lista de Alunos')


# Login do Professor
@app.route('/login-professor', methods=['GET', 'POST'])
def login_professor():
    if request.method == 'POST':
        # Aqui será feita a autenticação futuramente
        login = request.form.get('login')
        senha = request.form.get('senha')
        # Apenas redireciona para dashboard por enquanto
        return redirect(url_for('dashboard'))
    return render_template('login_professor.html')

# Cadastro de Professor
@app.route('/cadastro-professor', methods=['GET', 'POST'])
def cadastro_professor():
    if request.method == 'POST':
        # Aqui será feito o cadastro real futuramente
        nome = request.form.get('nome')
        identidade = request.form.get('identidade')
        login = request.form.get('login')
        senha = request.form.get('senha')
        # Foto e outros dados podem ser processados aqui
        # Apenas redireciona para login por enquanto
        return redirect(url_for('login_professor'))
    return render_template('cadastro_professor.html')

if __name__ == '__main__':
    app.run(debug=True)

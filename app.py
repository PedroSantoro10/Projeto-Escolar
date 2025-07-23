from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

professores = []
alunos = []
avisos = []

base_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ONG Futurista</title>
    <style>
        body { background: linear-gradient(135deg, #0f2027, #2c5364); color: #fff; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; }
        nav { background: rgba(0,0,0,0.8); padding: 1em; display: flex; gap: 2em; justify-content: center; }
        nav a { color: #00ffe7; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        nav a:hover { color: #ff00cc; }
        main { max-width: 600px; margin: 2em auto; background: rgba(20,20,40,0.85); padding: 2em; border-radius: 16px; box-shadow: 0 0 32px #00ffe7; }
        input, textarea { width: 100%; padding: 0.7em; margin: 0.5em 0; border-radius: 8px; border: none; background: #222; color: #fff; }
        button { background: #00ffe7; color: #222; border: none; padding: 0.7em 2em; border-radius: 8px; font-weight: bold; cursor: pointer; transition: background 0.3s; }
        button:hover { background: #ff00cc; }
        ul { list-style: none; padding: 0; }
        li { background: #222; margin: 0.5em 0; padding: 0.5em; border-radius: 8px; }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('index') }}">Início</a>
        <a href="{{ url_for('cadastro_professor') }}">Cadastro de Professores</a>
        <a href="{{ url_for('matricula_aluno') }}">Matrícula de Aluno</a>
        <a href="{{ url_for('jornal') }}">Jornal da Escola</a>
    </nav>
    <main>
        {{ conteudo|safe }}
    </main>
</body>
</html>
"""

@app.route('/')
def index():
    conteudo = "<h1>Bem-vindo à ONG Futurista</h1><p>Escolha uma das opções acima para começar.</p>"
    return render_template_string(base_html, conteudo=conteudo)

@app.route('/cadastro_professor', methods=['GET', 'POST'])
def cadastro_professor():
    if request.method == 'POST':
        professores.append({
            'nome': request.form['nome'],
            'idade': request.form['idade'],
            'materia': request.form['materia'],
            'senha': request.form['senha']
        })
        return redirect(url_for('cadastro_professor'))
    conteudo = '''
<h2>Cadastro de Professor</h2>
<form method="post">
    <input type="text" name="nome" placeholder="Nome" required>
    <input type="number" name="idade" placeholder="Idade" required>
    <input type="text" name="materia" placeholder="Matéria" required>
    <input type="password" name="senha" placeholder="Senha" required>
    <button type="submit">Cadastrar</button>
</form>
<h3>Professores cadastrados:</h3>
<ul>
{% for p in professores %}
    <li>{{ p.nome }} - {{ p.materia }}</li>
{% endfor %}
</ul>
'''
    return render_template_string(base_html, conteudo=conteudo, professores=professores)

@app.route('/matricula_aluno', methods=['GET', 'POST'])
def matricula_aluno():
    if request.method == 'POST':
        alunos.append({
            'nome': request.form['nome'],
            'idade': request.form['idade'],
            'turma': request.form['turma']
        })
        return redirect(url_for('matricula_aluno'))
    conteudo = '''
        <h2>Matrícula de Aluno</h2>
        <form method="post">
            <input type="text" name="nome" placeholder="Nome" required>
            <input type="number" name="idade" placeholder="Idade" required>
            <input type="text" name="turma" placeholder="Turma" required>
            <button type="submit">Matricular</button>
        </form>
        <h3>Alunos matriculados:</h3>
        <ul>
        {% for a in alunos %}
            <li>{{ a.nome }} - {{ a.turma }}</li>
        {% endfor %}
        </ul>
    '''
    return render_template_string(base_html, conteudo=conteudo, alunos=alunos)

@app.route('/jornal', methods=['GET', 'POST'])
def jornal():
    if request.method == 'POST':
        avisos.append(request.form['aviso'])
        return redirect(url_for('jornal'))
    conteudo = '''
        <h2>Jornal da Escola</h2>
        <form method="post">
            <textarea name="aviso" placeholder="Digite o aviso..." required></textarea>
            <button type="submit">Publicar Aviso</button>
        </form>
        <h3>Avisos publicados:</h3>
        <ul>
        {% for aviso in avisos %}
            <li>{{ aviso }}</li>
        {% endfor %}
        </ul>
    '''
    return render_template_string(base_html, conteudo=conteudo, avisos=avisos)

if __name__ == '__main__':
    app.run(debug=True)
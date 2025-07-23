from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, session
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy  # Adicione esta linha
import sqlalchemy
print(sqlalchemy.__file__)

app = Flask(__name__)

app.secret_key = 'segredo'  # Necessário para usar sessão

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_escolar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(120), nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    pdf = db.Column(db.String(200))
    plano_pdf = db.Column(db.String(200))
    conteudo_programatico = db.Column(db.Text)
    foto = db.Column(db.String(200))
    dias = db.Column(db.Text)  # Armazene como string separada por vírgula

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    turma = db.Column(db.String(120), nullable=False)
    rg_responsavel = db.Column(db.String(200))
    doc_aluno = db.Column(db.String(200))
    comprovante_residencia = db.Column(db.String(200))
    foto = db.Column(db.String(200))
    professor = db.Column(db.String(120))
    rendimento = db.Column(db.String(120))

# Criação das tabelas
with app.app_context():
    db.create_all()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

base_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>PROJETO SEGAR</title>
    <style>
        body {
            min-height: 100vh;
            margin: 0;
            color: #eee;
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #0a0a0a;
            background: linear-gradient(90deg, #0a0a0a 80%, #2d0066 100%);
            position: relative;
        }
        body::after {
            content: "";
            position: fixed;
            top: 0; right: 0; bottom: 0; left: 0;
            pointer-events: none;
            background: radial-gradient(circle at 90% 30%, rgba(120,0,255,0.18) 0, rgba(0,0,0,0) 40%);
            z-index: 0;
        }
        nav { 
            background: #18122B;
            padding: 1em 0;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0;
            position: relative;
            z-index: 1;
        }
        nav ul {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0;
            margin: 0;
            padding: 0;
            width: 100%;
            max-width: 1200px;
            list-style: none;
        }
        nav ul li {
            flex: 1 1 0;
            text-align: center;
        }
        nav a { 
            display: block;
            color: #fff; /* Branco puro */
            /* Removido o text-shadow para não brilhar */
            text-decoration: none;
            font-weight: bold;
            font-size: 1.08em;
            letter-spacing: 1px;
            text-transform: uppercase;
            padding: 0.7em 0;
            transition: color 0.3s, background 0.3s;
            border-radius: 8px;
        }
        nav a:hover { 
            color: #fff;
            background: #2d0066;
        }
        main { max-width: 700px; margin: 2em auto; background: #181818cc; padding: 2em; border-radius: 16px; box-shadow: 0 0 32px #000; position: relative; z-index: 1;}
        input, textarea { width: 100%; padding: 0.7em; margin: 0.5em 0; border-radius: 8px; border: none; background: #222; color: #fff; }
        button { background: #222; color: #a084ff; border: none; padding: 0.7em 2em; border-radius: 8px; font-weight: bold; cursor: pointer; transition: background 0.3s, color 0.3s; }
        button:hover { background: #a084ff; color: #181818; }
        ul { list-style: none; padding: 0; }
        li { background: #181818; margin: 0.5em 0; padding: 0.5em; border-radius: 8px; }
        a.pdf-link { color: #a084ff; text-decoration: underline; }
        table { background: #181818cc; }
        th, td { background: #222; border: 1px solid #333; }
        th { color: #a084ff; }
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="{{ url_for('index') }}">INÍCIO</a></li>
            <li><a href="{{ url_for('cadastro_professor') }}">CADASTRO DE PROFESSORES</a></li>
            <li><a href="{{ url_for('matricula_aluno') }}">MATRÍCULA DE ALUNO</a></li>
            <li><a href="{{ url_for('jornal') }}">JORNAL DO PROJETO SEGAR</a></li>
            <li><a href="{{ url_for('agenda') }}">AGENDA</a></li>
            <li><a href="{{ url_for('conteudo_programatico') }}">CONTEÚDO PROGRAMÁTICO</a></li>
            <li><a href="{{ url_for('login_professor') }}">LOGIN PROFESSOR</a></li>
            <li><a href="{{ url_for('alunos_cadastrados') }}">ALUNOS CADASTRADOS</a></li>
        </ul>
    </nav>
    <main>
        {{ conteudo|safe }}
    </main>
</body>
</html>
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    conteudo = '''
    <div style="text-align:center;">
        <img src="{}" alt="Logo ONG" style="width:120px; margin-bottom:20px;">
        <div style="margin-top:20px;">
            <h1 style="text-align:center;">Bem-vindo ao Projeto Segar</h1>
            <p style="text-align:center;">Escolha uma das opções acima para começar.</p>
        </div>
    </div>
    '''.format(url_for('static', filename='logo.png'))
    return render_template_string(base_html, conteudo=conteudo)

@app.route('/cadastro_professor', methods=['GET', 'POST'])
def cadastro_professor():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        materia = request.form['materia']
        senha = request.form['senha']
        pdf_filename = None
        file = request.files.get('conteudo_pdf')
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{nome}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pdf_filename = filename
        foto_filename = None
        foto = request.files.get('foto_professor')
        if foto and allowed_file(foto.filename):
            foto_filename = secure_filename(f"{nome}_foto_{foto.filename}")
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))
        novo_prof = Professor(
            nome=nome,
            idade=idade,
            materia=materia,
            senha=senha,
            pdf=pdf_filename,
            plano_pdf=None,
            conteudo_programatico='',
            foto=foto_filename,
            dias=''
        )
        db.session.add(novo_prof)
        db.session.commit()
        return redirect(url_for('cadastro_professor'))
    
    # Gerar a lista de professores em HTML
    professores_html = []
    for professor in Professor.query.all():
        pdf_link = f'- <a class="pdf-link" href="{url_for("download_pdf", filename=professor.pdf)}" target="_blank">Ver PDF</a>' if professor.pdf else ''
        plano_link = f'- <a class="pdf-link" href="{url_for("plano_aula", prof_id=professor.id)}">Plano de Aula</a>'
        conteudo_link = f'- <a class="pdf-link" href="{url_for("editar_conteudo", prof_id=professor.id)}">Editar Conteúdo Programático</a>'
        conteudo_prog = f'<br><b>Conteúdo:</b> {professor.conteudo_programatico}' if professor.conteudo_programatico else ''
        foto_img = f'<br><img src="{url_for("download_pdf", filename=professor.foto)}" alt="Foto de {professor.nome}" style="width:100px;height:auto;border-radius:50%;">' if professor.foto else ''
        professores_html.append(f'<li>{professor.nome} - {professor.materia} {pdf_link} {plano_link} {conteudo_link} {conteudo_prog} {foto_img}</li>')
    
    conteudo = f'''
<h2>Cadastro de Professor</h2>
<form method="post" enctype="multipart/form-data">
    <input type="text" name="nome" placeholder="Nome" required>
    <input type="number" name="idade" placeholder="Idade" required>
    <input type="text" name="materia" placeholder="Matéria" required>
    <input type="password" name="senha" placeholder="Senha" required>
    <label>Conteúdo (PDF):</label>
    <input type="file" name="conteudo_pdf" accept=".pdf">
    <label>Foto do Professor:</label>
    <input type="file" name="foto_professor" accept=".jpg,.jpeg,.png">
    <button type="submit">Cadastrar</button>
</form>
<h3>Professores cadastrados:</h3>
<ul>
{"".join(professores_html)}
</ul>
'''
    return render_template_string(base_html, conteudo=conteudo)

@app.route('/uploads/<filename>')
def download_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/matricula_aluno', methods=['GET', 'POST'])
def matricula_aluno():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        turma = request.form['turma']

        rg_resp = request.files.get('rg_responsavel')
        doc_aluno = request.files.get('doc_aluno')
        comprovante = request.files.get('comprovante_residencia')
        foto_aluno = request.files.get('foto_aluno')

        rg_filename = doc_filename = comp_filename = foto_filename = None

        if rg_resp and allowed_file(rg_resp.filename):
            rg_filename = secure_filename(f"{nome}_rg_{rg_resp.filename}")
            rg_resp.save(os.path.join(app.config['UPLOAD_FOLDER'], rg_filename))
        if doc_aluno and allowed_file(doc_aluno.filename):
            doc_filename = secure_filename(f"{nome}_doc_{doc_aluno.filename}")
            doc_aluno.save(os.path.join(app.config['UPLOAD_FOLDER'], doc_filename))
        if comprovante and allowed_file(comprovante.filename):
            comp_filename = secure_filename(f"{nome}_comp_{comprovante.filename}")
            comprovante.save(os.path.join(app.config['UPLOAD_FOLDER'], comp_filename))
        if foto_aluno and allowed_file(foto_aluno.filename):
            foto_filename = secure_filename(f"{nome}_foto_{foto_aluno.filename}")
            foto_aluno.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

        novo_aluno = Aluno(
            nome=nome,
            idade=idade,
            turma=turma,
            rg_responsavel=rg_filename,
            doc_aluno=doc_filename,
            comprovante_residencia=comp_filename,
            foto=foto_filename,
            professor='',  # Pode ser preenchido depois
            rendimento=''
        )
        db.session.add(novo_aluno)
        db.session.commit()
        return redirect(url_for('matricula_aluno'))

    alunos_html = []
    for a in Aluno.query.all():
        foto_img = f"<img src='{url_for('download_pdf', filename=a.foto)}' alt='Foto de {a.nome}' style='width:60px;height:60px;border-radius:50%;object-fit:cover;'>" if a.foto else ''
        prof = a.professor if a.professor else 'Não definido'  # Corrigido aqui!
        rendimento = a.rendimento if a.rendimento else ''
        alunos_html.append(
            f"<tr>"
            f"<td>{foto_img}</td>"
            f"<td>{a.nome}</td>"
            f"<td>{prof}</td>"
            f"<td>"
            f"<form method='post' style='display:inline;'>"
            f"<input type='hidden' name='aluno_id' value='{a.id}'>"
            f"<input type='text' name='rendimento' value='{rendimento}' style='width:100px;'>"
            f"<button type='submit'>Salvar</button>"
            f"</form>"
            f"</td>"
            f"</tr>"
        )

    conteudo = f'''
<h2>Matrícula de Aluno</h2>
<form method="post" enctype="multipart/form-data">
  <label>Nome:</label><br>
  <input type="text" name="nome" required><br>
  <label>Idade:</label><br>
  <input type="number" name="idade" required><br>
  <label>Turma:</label><br>
  <input type="text" name="turma" required><br><br>
  <label>RG do Responsável (PDF):</label>
  <input type="file" name="rg_responsavel" accept=".pdf" required><br>
  <label>DOC do Aluno (PDF):</label>
  <input type="file" name="doc_aluno" accept=".pdf" required><br>
  <label>Comprovante de Residência (PDF):</label>
  <input type="file" name="comprovante_residencia" accept=".pdf" required><br><br>
  <label>Foto do Aluno:</label>
  <input type="file" name="foto_aluno" accept=".jpg,.jpeg,.png"><br>
  <button type="submit">Matricular</button>
</form>
<h3>Alunos cadastrados:</h3>
<table style="width:100%;color:#fff;text-align:center;border-collapse:collapse;">
<tr>
    <th>Foto</th>
    <th>Nome</th>
    <th>Professor</th>
    <th>Rendimento</th>
</tr>
{''.join(alunos_html)}
</table>
'''
    return render_template_string(base_html, conteudo=conteudo)

@app.route('/jornal', methods=['GET', 'POST'])
def jornal():
    if request.method == 'POST':
        avisos.append(request.form['aviso'])
        return redirect(url_for('jornal'))
    conteudo = '''
<h2>Jornal do Projeto Segar</h2>
<form method="post">
    <textarea name="aviso" placeholder="Digite o aviso..." required></textarea>
    <button type="submit">Publicar Aviso</button>
</form>
<h3>Avisos publicados:</h3>
<ul>
<div class="avisos-container">
    <!-- Os avisos serão inseridos aqui via JavaScript -->
</div>
</ul>
'''
    return render_template_string(base_html, conteudo=conteudo, avisos=avisos)
    return render_template_string(base_html, conteudo=conteudo, avisos=avisos)

@app.route('/plano_aula/<int:prof_id>', methods=['GET', 'POST'])
def plano_aula(prof_id):
    professor = Professor.query.get(prof_id)
    if not professor:
        return "Professor não encontrado", 404
    if request.method == 'POST':
        file = request.files.get('plano_pdf')
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{professor.nome}_plano_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            professor.plano_pdf = filename
            db.session.commit()
            return redirect(url_for('cadastro_professor'))
    plano_link = f'<a class="pdf-link" href="{url_for("download_pdf", filename=professor.plano_pdf)}" target="_blank">Ver Plano de Aula</a>' if professor.plano_pdf else 'Nenhum plano enviado'
    conteudo = f'''
    <h2>Plano de Aula de {professor.nome}</h2>
    <form method="post" enctype="multipart/form-data">
        <label>Enviar PDF do Plano de Aula:</label>
        <input type="file" name="plano_pdf" accept=".pdf" required>
        <button type="submit">Enviar</button>
    </form>
    <p>{plano_link}</p>
    <a href="{url_for('cadastro_professor')}">Voltar</a>
    '''
    return render_template_string(base_html, conteudo=conteudo)

@app.route('/agenda')
def agenda():
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    professores = [
        {"nome": "Ana", "curso": "Educação Infantil", "dias": dias},
        {"nome": "Roberta", "curso": "Educação Infantil", "dias": dias},
        {"nome": "Keison", "curso": "Educação Infantil", "dias": dias},
        {"nome": "Karine", "curso": "Coordenação", "dias": dias},
        {"nome": "Max Moura", "curso": ["Teclado", "Informática", "Violão e Contra Baixo"], "dias": ["Segunda", "Terça", "Quarta"]},
        {"nome": "Pedro Santoro", "curso": ["Bateria"], "dias": ["Terça"]},
    ]

    agenda_html = "<h2>Agenda de Aulas</h2>"
    for prof in professores:
        agenda_html += f"<h3>{prof['nome']} - {prof['curso'] if isinstance(prof['curso'], str) else ', '.join(prof['curso'])}</h3>"
        agenda_html += "<table style='width:100%;color:#fff;text-align:center;margin-bottom:20px;border-collapse:collapse;'>"
        agenda_html += "<tr>"
        for dia in dias:
            agenda_html += f"<th>{dia}</th>"
        agenda_html += "</tr><tr>"
        for dia in dias:
            # Para Max Moura e Pedro Santoro, mostrar o curso do dia
            if prof['nome'] == "Max Moura":
                if dia == "Segunda":
                    cell = "Teclado"
                elif dia == "Terça":
                    cell = "Informática"
                elif dia == "Quarta":
                    cell = "Violão e Contra Baixo"
                else:
                    cell = "-"
            elif prof['nome'] == "Pedro Santoro":
                cell = "Bateria" if dia == "Terça" else "-"
            else:
                cell = prof['curso']
            agenda_html += f"<td>{cell}</td>"
        agenda_html += "</tr></table>"
    return render_template_string(base_html, conteudo=agenda_html)

@app.route('/conteudo_programatico', methods=['GET', 'POST'])
def conteudo_programatico():
    if not professores:
        table = "<h2>Conteúdo Programático Anual</h2><p style='color:#fff;'>Nenhum professor cadastrado.</p>"
        return render_template_string(base_html, conteudo=table)
    table = "<h2>Conteúdo Programático Anual</h2>"
    table += "<table style='width:100%;color:#fff;text-align:center;border-collapse:collapse;'>"
    table += "<tr>"
    for idx, prof in enumerate(professores):
        table += f"<th>{prof.nome}<br><span style='font-size:12px;color:#00ffe7'>{prof.materia}</span></th>"
    table += "</tr><tr>"
    for idx, prof in enumerate(professores):
        if prof.pdf:
            pdf_link = f"<a class='pdf-link' href='{url_for('download_pdf', filename=prof.pdf)}' target='_blank'>Ver PDF</a>"
        else:
            pdf_link = "Nenhum PDF"
        upload_form = f"""
        <form method='post' enctype='multipart/form-data' action='{url_for('upload_conteudo_pdf', prof_id=idx)}'>
            <input type='file' name='conteudo_pdf' accept='.pdf' required style='width:80px;'>
            <button type='submit'>Enviar</button>
        </form>
        """
        table += f"<td>{pdf_link}<br>{upload_form}</td>"
    table += "</tr></table>"
    return render_template_string(base_html, conteudo=table)

@app.route('/editar_conteudo/<int:prof_id>', methods=['GET', 'POST'])
def editar_conteudo(prof_id):
    professor = Professor.query.get(prof_id)
    if not professor:
        return "Professor não encontrado", 404
    if request.method == 'POST':
        professor.conteudo_programatico = request.form['conteudo_programatico']
        db.session.commit()
        return redirect(url_for('cadastro_professor'))
    conteudo = f'''
    <h2>Conteúdo Programático de {professor.nome}</h2>
    <form method="post">
        <textarea name="conteudo_programatico" rows="8" style="width:100%;" required>{professor.conteudo_programatico}</textarea>
        <br>
        <button type="submit">Salvar</button>
    </form>
    <a href="{url_for('cadastro_professor')}">Voltar</a>
    '''
    return render_template_string(base_html, conteudo=conteudo)

@app.route('/upload_conteudo_pdf/<int:prof_id>', methods=['POST'])
def upload_conteudo_pdf(prof_id):
    professor = Professor.query.get(prof_id)
    if not professor:
        return "Professor não encontrado", 404
    file = request.files.get('conteudo_pdf')
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{professor.nome}_conteudo_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        professor.pdf = filename
        db.session.commit()
    return redirect(url_for('conteudo_programatico'))

@app.route('/login_professor', methods=['GET', 'POST'])
def login_professor():
    erro = ''
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        professor = Professor.query.filter_by(nome=nome, senha=senha).first()
        if professor:
            session['prof_id'] = professor.id
            return redirect(url_for('area_professor'))
        erro = 'Nome ou senha inválidos.'
    conteudo = f'''
    <h2>Login do Professor</h2>
    <form method="post">
        <input type="text" name="nome" placeholder="Nome" required>
        <input type="password" name="senha" placeholder="Senha" required>
        <button type="submit">Entrar</button>
    </form>
    <p style="color:#ff8080;">{erro}</p>
    '''
    return render_template_string(base_html, conteudo=conteudo)

@app.route('/area_professor', methods=['GET', 'POST'])
def area_professor():
    prof_id = session.get('prof_id')
    if prof_id is None:
        return redirect(url_for('login_professor'))
    prof = Professor.query.get(prof_id)
    if not prof:
        return redirect(url_for('login_professor'))

    # Troca de foto
    if request.method == 'POST' and 'nova_foto' in request.files:
        nova_foto = request.files['nova_foto']
        if nova_foto and allowed_file(nova_foto.filename):
            foto_filename = secure_filename(f"{prof.nome}_foto_{nova_foto.filename}")
            nova_foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))
            prof.foto = foto_filename
            db.session.commit()

    # Seleção de dias de aula
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    if request.method == 'POST' and 'dias_aula' in request.form:
        dias_selecionados = request.form.getlist('dias_aula')
        prof.dias = dias_selecionados

    # Foto
    if prof.foto:
        foto_html = f"<img src='{url_for('download_pdf', filename=prof.foto)}' alt='Foto' style='width:120px;border-radius:50%;margin-bottom:10px;'>"
    else:
        foto_html = "<div style='width:120px;height:120px;background:#333;border-radius:50%;display:inline-block;margin-bottom:10px;'></div>"
    # Dias de aula
    dias = prof.dias if prof.dias else []
    dias_html = ", ".join(dias) if dias else "Nenhum selecionado"
    # Conteúdo programático
    conteudo_prog = prof.conteudo_programatico if prof.conteudo_programatico else 'Não cadastrado'
    conteudo = f'''
    <div style="text-align:center;">{foto_html}</div>
    <form method="post" enctype="multipart/form-data" style="text-align:center;margin-bottom:20px;">
        <label style="color:#a084ff;">Trocar foto do professor:</label><br>
        <input type="file" name="nova_foto" accept=".jpg,.jpeg,.png">
        <button type="submit">Atualizar Foto</button>
    </form>
    <form method="post" style="text-align:center;margin-bottom:20px;">
        <label style="color:#a084ff;">Selecione os dias que você dará aula:</label><br>
        {''.join(f'<label style="margin-right:10px;"><input type="checkbox" name="dias_aula" value="{dia}" {"checked" if dia in dias else ""}> {dia}</label>' for dia in dias_semana)}
        <br>
        <button type="submit">Salvar Dias de Aula</button>
    </form>
    <h2>Bem-vindo, {prof.nome}</h2>
    <p><b>Matéria:</b> {prof.materia}</p>
    <p><b>Dias de Aula:</b> {dias_html}</p>
    <h3>Conteúdo Programático</h3>
    <div style="background:#222;padding:10px;border-radius:8px;">{conteudo_prog}</div>
    <br>
    <a href="{url_for('editar_conteudo', prof_id=prof_id)}">Editar Conteúdo Programático</a>
    <br><br>
    <a href="{url_for('logout_professor')}" style="color:#ff8080;">Sair</a>
    '''
    return render_template_string(base_html, conteudo=conteudo)

@app.route('/logout_professor')
def logout_professor():
    session.pop('prof_id', None)
    return redirect(url_for('login_professor'))

@app.route('/alunos_cadastrados', methods=['GET', 'POST'])
def alunos_cadastrados():
    # Professores podem editar o rendimento dos alunos
    if request.method == 'POST':
        idx = int(request.form['aluno_id'])
        rendimento = request.form['rendimento']
        aluno = Aluno.query.get(idx)
        if aluno:
            aluno.rendimento = rendimento
            db.session.commit()

    alunos_html = []
    for a in Aluno.query.all():
        foto_img = f"<img src='{url_for('download_pdf', filename=a.foto)}' alt='Foto de {a.nome}' style='width:60px;height:60px;border-radius:50%;object-fit:cover;'>" if a.foto else ''
        prof = a.professor if a.professor else 'Não definido'  # Corrigido aqui!
        rendimento = a.rendimento if a.rendimento else ''
        alunos_html.append(
            f"<tr>"
            f"<td>{foto_img}</td>"
            f"<td>{a.nome}</td>"
            f"<td>{prof}</td>"
            f"<td>"
            f"<form method='post' style='display:inline;'>"
            f"<input type='hidden' name='aluno_id' value='{a.id}'>"
            f"<input type='text' name='rendimento' value='{rendimento}' style='width:100px;'>"
            f"<button type='submit'>Salvar</button>"
            f"</form>"
            f"</td>"
            f"</tr>"
        )

    conteudo = f'''
    <h2>Alunos Cadastrados</h2>
    <table style="width:100%;color:#fff;text-align:center;border-collapse:collapse;">
    <tr>
        <th>Foto</th>
        <th>Nome</th>
        <th>Professor</th>
        <th>Rendimento</th>
    </tr>
    {''.join(alunos_html)}
    </table>
    '''
    return render_template_string(base_html, conteudo=conteudo)

if __name__ == '__main__':
    app.run(debug=True)
    
    # inserir quadro de horários e dias de aula/ 5 professores  = agenda da sala manhã e tarde
    # lançar conteudo programatico anual do cursos, bateria, violão, teclado e informática, abrir aba para cada curso e professor designado
    # adicionar funcionalidade de login para professores e alunos, com autenticação básica
    # aba nome e rendimento do aluno com foto + nota de cada matéria
    # presença dos alunos 
    # adicionar funcionalidade de upload de fotos dos alunos e professores
    # Area do professor

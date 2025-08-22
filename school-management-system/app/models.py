from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(200), nullable=True)  # Caminho do arquivo
    identidade = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    coordenador = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Professor {self.nome}>'

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(200), nullable=True)  # Caminho do arquivo
    rg_arquivo = db.Column(db.String(200), nullable=True)  # Caminho do arquivo
    comprovante_residencia = db.Column(db.String(200), nullable=True)  # Caminho do arquivo
    idade = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Aluno {self.nome}>'
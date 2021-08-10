from re import search
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://prgrdems:imF8o_dDVMlRdARYQyFkjwmlpmLXFRl0@kesavan.db.elephantsql.com/prgrdems'
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(250), nullable=False)
    imagem = db.Column(db.String(500), nullable=False)
    descricao = db.Column(db.String(600), nullable=False)
    tipo = db.Column(db.String(150), nullable=False) 

    def __init__(self, nome, imagem, descricao, tipo):
        self.nome = nome
        self.imagem = imagem
        self.descricao = descricao
        self.tipo = tipo

@app.route('/')
def index():
    pokedex = Pokemon.query.all()
    return render_template('index.html', title='Pokedéx', pokedex=pokedex)

@app.route('/add', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        pokemon = Pokemon(request.form['nome'],
        request.form['imagem'],
        request.form['descricao'],
        request.form['tipo'])
        db.session.add(pokemon)
        db.session.commit()
        return redirect('/')    

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    pokemon = Pokemon.query.get(id) 
    pokedex = Pokemon.query.all()   
    if request.method == 'POST':
        pokemon.nome = request.form['nome']
        pokemon.descricao = request.form['descricao']
        pokemon.imagem = request.form['imagem']
        pokemon.tipo = request.form['tipo']
        db.session.commit()
        return redirect ('/')
    return render_template ('index.html', pokemon=pokemon, pokedex=pokedex)

@app.route('/<id>')
def get_by_id(id):
    pokemon = Pokemon.query.get(id)
    all = Pokemon.query.all()
    return render_template ('index.html', pokemonDelete=pokemon, pokedex=all)

@app.route('/delete/<id>')
def delete(id):
    pokemon = Pokemon.query.get(id)
    db.session.delete(pokemon)
    db.session.commit()
    return redirect ('/')

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    tipo = request.form['search']
    pokedex = Pokemon.query.filter(Pokemon.tipo.ilike(f'%{tipo}%')).all()
    return render_template ('index.html', pokedex=pokedex)

@app.route('/filter/<param>')
def filter_by_param(param):
    pokedex = Pokemon.query.filter_by(tipo=param).all()
    return render_template ('index.html', pokedex=pokedex)

if __name__=='__main__':
    db.create_all()
    app.run(debug=True, port=3000)
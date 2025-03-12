# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' # Configuração do banco de dados
db = SQLAlchemy(app) # Inicialização do banco de dados

# 
# Modelagem do Banco de Dados
# 

# Tabela de Produtos
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(50), nullable=False) # Limita o tamanho do campo
    description = db.Column(db.Text, nullable=True) # Campo não obrigatório, não limita o tamanho

# 
# ROTAS
# 

# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/api/products/', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_json = []
    for product in products:
        products_json.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    return products_json

@app.route('/api/products/add/', methods=['POST'])
def add_product():
    try:
        data = request.json
        if 'name' in data and 'price' in data:
            product = Product(price=data["price"], name=data["name"], description=data.get("description", ""))
            db.session.add(product)
            db.session.commit()
            return jsonify({'message': 'Produto adicionado com sucesso!'})
        else:
            return jsonify({'error': 'Dados inválidos'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
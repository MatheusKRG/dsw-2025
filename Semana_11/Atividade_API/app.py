from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

produtos = [
    {"id": 1, "nome": "Produto 1", "preco": 19.99, "estoque": 10},
    {"id": 2, "nome": "Produto 2", "preco": 29.99, "estoque": 5},
    {"id": 3, "nome": "Produto 3", "preco": 9.99, "estoque": 15}
]

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(produtos), 200

@app.route('/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    produto = next((p for p in produtos if p['id'] == id), None)
    if produto:
        return jsonify(produto), 200
    else:
        return jsonify({"error": "Produto não encontrado"}), 404

@app.route('/produtos', methods=['POST'])
def criar_produto():
    novo_produto = request.get_json()
    produto_id = max(p['id'] for p in produtos) + 1 if produtos else 1
    novo_produto['id'] = produto_id
    produtos.append(novo_produto)
    return jsonify(novo_produto), 201

@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = next((p for p in produtos if p['id'] == id), None)
    if produto:
        produto.update(request.get_json())
        return jsonify(produto), 200
    else:
        return jsonify({"error": "Produto não encontrado"}), 404

@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = next((p for p in produtos if p['id'] == id), None)
    if produto:
        produtos.remove(produto)
        return jsonify({"message": "Produto deletado com sucesso"}), 200
    else:
        return jsonify({"error": "Produto não encontrado"}), 404

@app.route('/produtos/<int:id>/comprar', methods=['POST'])
def comprar_produto(id):
    produto = next((p for p in produtos if p['id'] == id), None)
    if produto:
        if produto['estoque'] > 0:
            produto['estoque'] -= 1
            return jsonify(produto), 200
        else:
            return jsonify({"error": "Produto fora de estoque"}), 400
    else:
        return jsonify({"error": "Produto não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
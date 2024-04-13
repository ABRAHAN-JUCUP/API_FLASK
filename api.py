from flask import Flask, request, jsonify
from avl_tree import AVLTree

app = Flask(__name__)
tree = AVLTree()
root = None

# Ruta para cargar registros desde un archivo CSV
@app.route('/load_csv', methods=['POST'])
def load_csv():
    global root
    if 'file' not in request.files:
        return jsonify({'error': 'No se ha proporcionado ningún archivo'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se ha proporcionado ningún archivo'}), 400
    if file:
        data = file.read().decode('utf-8').split('\n')
        for line in data:
            if line:
                root = tree.insert(root, int(line.strip()))
        return jsonify({'message': 'Registros cargados exitosamente'}), 200
    return jsonify({'error': 'Error al cargar el archivo'}), 500

# Ruta para inserción manual de registros
@app.route('/insert', methods=['POST'])
def insert_record():
    global root
    data = request.get_json()
    if 'key' not in data:
        return jsonify({'error': 'Se requiere la clave del registro'}), 400
    key = data['key']
    root = tree.insert(root, key)
    return jsonify({'message': f'Registro con clave {key} insertado exitosamente'}), 200

# Ruta para buscar registros por identificador
@app.route('/search', methods=['GET'])
def search_record():
    global root
    key = int(request.args.get('key'))
    node = tree.search(root, key)
    if node:
        return jsonify({'message': f'Registro encontrado con clave {node.key}'}), 200
    else:
        return jsonify({'error': 'Registro no encontrado'}), 404

# Ruta para mostrar información del grupo
@app.route('/group_info', methods=['GET'])
def group_info():
    group_info = {
        'integrantes': [
            {'nombre': 'Nombre1', 'carnet': 'Carnet1', 'contribuciones': 'Contribuciones1'},
            {'nombre': 'Nombre2', 'carnet': 'Carnet2', 'contribuciones': 'Contribuciones2'}
            # Agregar información de más integrantes si es necesario
        ]
    }
    return jsonify(group_info), 200

if __name__ == '__main__':
    app.run(debug=True)

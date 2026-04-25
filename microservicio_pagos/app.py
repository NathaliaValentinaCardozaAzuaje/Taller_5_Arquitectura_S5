from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/v2/comprar', methods=['POST'], strict_slashes=False)
def realizar_compra():
    data = request.get_json(silent=True) or {}

    # Accept both keys to simplify transition from v1 clients.
    producto_id = data.get('producto_id') or data.get('libro_id')
    cantidad = data.get('cantidad', 1)

    if not producto_id:
        return jsonify({'error': 'Falta el ID del producto (producto_id/libro_id)'}), 400

    return jsonify(
        {
            'mensaje': 'Compra procesada exitosamente por el Microservicio Flask (v2)',
            'producto_id': producto_id,
            'cantidad': cantidad,
            'status': 'Aprobado',
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configura la conexión a la base de datos
db_config = {
    'host': 'vacacionesql.mysql.database.azure.com',
    'user': 'SebasLucy',
    'password': 'Vacaciones2023',
    'database': 'vacaciones2023'
}


@app.route('/webhook', methods=['POST'])
def webhook():
    # Obtener los datos de la solicitud
    request_json = request.get_json()

    # Obtener el número de VHUR del parámetro
    vhur_number = request_json['queryResult']['parameters']['vhur']

    # Fecha de corte fija
    fecha_corte = "11 de abril de 2023"

    # Conectarse a la base de datos
    conn = mysql.connector.connect(**db_config)

    # Obtener los datos de la base de datos para el número de VHUR especificado
    cursor = conn.cursor()
    query = f"SELECT VHUR, NOMBRE_APELLIDOS, DIAS_PENDIENTES FROM vacaciones WHERE VHUR = '{vhur_number}'"
    cursor.execute(query)
    row = cursor.fetchone()

    if row is not None:
        # Formatear el mensaje de respuesta con los datos obtenidos de la base de datos
        vhur = row[0]
        nombres_apellidos = row[1]
        dias_pendientes = row[2]
        message = f"El VHUR {vhur} con nombre y apellidos {nombres_apellidos} tiene {dias_pendientes} días pendientes. La fecha de corte es el {fecha_corte}."
    else:
        # Si no se encuentra el VHUR en la base de datos, mostrar un mensaje de error
        message = f"No se encontró el VHUR {vhur_number} en la base de datos."

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()

    # Crear la respuesta en formato JSON
    response = {
        'fulfillment_response': {
            'messages': [
                {
                    'text': {
                        'text': [message]
                    }
                }
            ]
        }
    }

    # Retornar la respuesta en formato JSON
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)

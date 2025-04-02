import os
from flask import request, jsonify
from core.blacklist_service import BlacklistService


def verify_jwt_token(token):
    if token is None:
        return False
    if token != f"Bearer {os.getenv('STATIC_JWT_TOKEN')}":
        return False
    return True


def register_routes(app):
    @app.route('/blacklists', methods=['POST'])
    def add_to_blacklist():
        
        auth_header = request.headers.get('Authorization', None)
        app.logger.info(f"validando el token...")
        
        if not auth_header or not verify_jwt_token(auth_header):
            app.logger.warning("Token no válido o no proporcionado.")
            return jsonify({"message": "Token inválido o no proporcionado"}), 401

        app.logger.info(f"validación del token satisfactoria...")

        data = request.get_json()
        app.logger.info(f"adicionando email a lista negra: {data}")
        
        email = data.get('email')
        app_uuid = data.get('app_uuid')
        blocked_reason = data.get('blocked_reason', None)
        ip_address = request.remote_addr
        
        app.logger.info(f"valores adicionados: {data}")
        return BlacklistService.add_to_blacklist(email, app_uuid, blocked_reason, ip_address)

    @app.route('/blacklists/<string:email>', methods=['GET'])
    def check_blacklist(email):
        auth_header = request.headers.get('Authorization', None)

        app.logger.info(f"validando el token...")
        if not auth_header or not verify_jwt_token(auth_header):
            app.logger.warning("Token no válido o no proporcionado.")
            return jsonify({"message": "Token inválido o no proporcionado"}), 401
        
        app.logger.info(f"validación del token satisfactoria, retornando valores...")
        return BlacklistService.check_blacklist(email)

    @app.route('/ping', methods=['GET'])
    def ping():
        try:
            return jsonify({"status": "El servicio esta activo"}), 200
        except Exception as e:
            return jsonify({"error": "Ha ocurrido un error consultando el estado de salud del servicio", "details": str(e)}), 500



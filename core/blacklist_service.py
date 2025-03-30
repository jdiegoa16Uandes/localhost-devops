from datetime import datetime
from flask import jsonify
from core.models import Blacklist
from extensions.database import db

class BlacklistService:
    @staticmethod
    def add_to_blacklist(email, app_uuid, blocked_reason, ip_address):
  
        if Blacklist.query.filter_by(email=email).first():
            return jsonify({"msg": "El email ya está en la lista negra"}), 400


        new_blacklist = Blacklist(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=blocked_reason,
            ip_address=ip_address,
            request_date=datetime.utcnow()
        )

        try:
            db.session.add(new_blacklist)
            db.session.commit()
            return jsonify({"msg": "El email ha sido agregado a la lista negra"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": f"Error al agregar el email: {str(e)}"}), 500

    @staticmethod
    def check_blacklist(email):
      
        blacklist_entry = Blacklist.query.filter_by(email=email).first()

        if blacklist_entry:
            return jsonify({
                "is_blacklisted": True,
                "blocked_reason": blacklist_entry.blocked_reason
            }), 200
        else:
            return jsonify({
                "is_blacklisted": False,
                "blocked_reason": None
            }), 200

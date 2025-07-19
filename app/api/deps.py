from typing import Generator
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status

# from app.core.security import decode_jwt  # Optionnel : si gestion JWT
# from app.models.user import User          # Optionnel : si gestion user

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- OPTIONNEL : Dépendances pour sécurité/auth utilisateur (JWT) ---
# À activer si tu veux de l’auth API

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
#     try:
#         payload = decode_jwt(token)
#         user_id: int = payload.get("user_id")
#         user = db.query(User).get(user_id)
#         if user is None:
#             raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
#         return user
#     except Exception:
#         raise HTTPException(status_code=401, detail="Token invalide")


from jose import jwt, JWTError, ExpiredSignatureError

# === À personnaliser ===
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0b25AZW1haWwuZnIiLCJ1c2VyX2lkIjoyLCJleHAiOjE3NTI1Njc3MDN9.HL6HtB6ErcEuhDRKiB0VMbMLtWQJ7IBUzFL2uKlPSS8"       # <-- Ton token (copie le depuis le front)
SECRET_KEY = "mohana_ma_fille_cherie_elle_est_nee_le_27/11/2020"  # <-- Ta SECRET_KEY du .env
ALGORITHM = "HS256"

try:
    decoded = jwt.decode(TOKEN, SECRET_KEY, algorithms=[ALGORITHM])
    print("Token décodé :")
    print(decoded)
except ExpiredSignatureError:
    print("Erreur : le token est expiré !")
except JWTError as e:
    print("Erreur de vérification JWT :", str(e))

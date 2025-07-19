# app/schemas/registre.py  ────────────────────────────────────────────────────
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RegistreBase(BaseModel):
    nom_traitement:       str  = Field(..., max_length=255)
    finalite:             str
    personnes_concernees: Optional[str] = None
    base_legale:          str
    duree_conservation:   str
    categorie_donnees:    Optional[str] = None
    mesures_securite:     Optional[str] = None
    commentaire:          Optional[str] = None


class RegistreCreate(RegistreBase):
    """Champs envoyés lors de la création (le backend ajoute user_id)."""
    pass


class RegistreUpdate(BaseModel):
    """Mise à jour partielle ; tous les champs sont optionnels."""
    nom_traitement:       Optional[str] = Field(None, max_length=255)
    finalite:             Optional[str] = None
    personnes_concernees: Optional[str] = None
    base_legale:          Optional[str] = None
    duree_conservation:   Optional[str] = None
    categorie_donnees:    Optional[str] = None
    mesures_securite:     Optional[str] = None
    commentaire:          Optional[str] = None


class RegistreRead(RegistreBase):
    id:         int
    user_id:    int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

"""
Enregistre tous les modèles dans Base.metadata
(Python exécute chaque import ; l'ordre est donc important pour les FK).
"""
from app.db.base_class import Base  # exporté pour env.py

# ─── Noyau sans dépendance/clé étrangère ───────────────────────────────
from .tenant   import Tenant           # noqa: F401
from .company  import Company          # noqa: F401
from .site     import Site, SitePhoto, SiteDocument  # noqa: F401

# ─── Utilisateurs (FK → Tenant / Company) ───────────────────────────────
from .user     import User             # noqa: F401

# ─── Autres domaines (dépendent parfois de Site / User) ─────────────────
from .securite           import SecuriteControle  # noqa: F401  (FK → Site)
from .processing         import Processing        # noqa: F401
from .processing_action  import ProcessingAction  # noqa: F401
from .checklist          import Checklist         # noqa: F401
from .checklist_item     import ChecklistItem     # noqa: F401
from .certif             import Certif            # noqa: F401
from .ouvrier            import Ouvrier           # noqa: F401
from .gdpr_action        import GdprAction        # noqa: F401
from .registre           import Registre          # noqa: F401

# ─── RGPD ───────────────────────────────────────────────────────────────
from .rgpd_exigence       import RgpdExigence       # noqa: F401
from .rgpd_audit          import RgpdAudit          # noqa: F401
from .rgpd_audit_exigence import RgpdAuditExigence  # noqa: F401

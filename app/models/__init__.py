"""
Centralise l’import de tous les modèles afin que SQLAlchemy les
enregistre dans son registry avant toute configuration/création
de tables. IMPORTANT : ne rien exécuter d’autre ici.
"""

from .tenant            import Tenant             # noqa: F401
from .user              import User               # noqa: F401
from .certif            import Certif             # noqa: F401
from .ouvrier           import Ouvrier            # noqa: F401
from .securite          import SecuriteControle   # noqa: F401
from .processing        import Processing         # noqa: F401
from .gdpr_action       import GdprAction         # noqa: F401
from .processing_action import processing_actions # noqa: F401
from .checklist         import Checklist          # noqa: F401
from .checklist_item    import ChecklistItem      # noqa: F401
from .register    import Register      # noqa: F401

# ...ajoute ici les modèles au fur et à mesure (1 par ligne)

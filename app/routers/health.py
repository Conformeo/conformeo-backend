# backend/app/routers/health.py
"""Simple liveness & readiness probes.

Expose both `/health` and `/readiness` (GET & HEAD) so that:
- `/health`  → basique *liveness* : l'API répond.
- `/readiness` → hooké si plus tard tu veux vérifier la DB, Redis, etc.

Les deux routes sont montées **deux fois** dans `app.main` :
- Sous `/api` pour le front.
- À la racine pour les orchestrateurs/monitoring (k8s, traefik, etc.).
"""

from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/health", tags=["health"])

# ---------------------------------------------------------------------------
# 🫀 Liveness (ping)
# ---------------------------------------------------------------------------
@router.get("/", summary="Liveness probe – API up")
@router.head("/", include_in_schema=False)
async def ping() -> dict[str, str]:
    """Retourne **200 OK** si l'application est vivante.
    HEAD renvoie juste le status sans body (utile pour load‑balancers).
    """
    return {"status": "OK"}

# ---------------------------------------------------------------------------
# ✅ Readiness (future checks)
# ---------------------------------------------------------------------------
@router.get("/readiness", summary="Readiness probe – dependencies up")
@router.head("/readiness", include_in_schema=False)
async def readiness(resp: Response) -> dict[str, str]:
    """Ici tu pourras brancher des checks : DB, cache, ext. services…
    Pour l'instant on renvoie *always‑ready*.
    """
    # Exemple : if not database_alive(): resp.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "READY"}

# app/services/charts.py
import io, base64
import matplotlib.pyplot as plt
import numpy as np

def rgpd_radar(score_dict: dict[str, float]) -> str:
    """Retourne un PNG base64 du radar RGPD."""
    labels = list(score_dict.keys())
    values = list(score_dict.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=1)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_yticklabels([])
    ax.set_ylim(0, 100)

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

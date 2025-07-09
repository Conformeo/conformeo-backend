from sqlalchemy.orm import Session
from app.models.gdpr_action import GdprAction, ActionScope

def get_all(db: Session) -> list[GdprAction]:
    actions = db.query(GdprAction).all()
    if actions:
        return actions

    seed = [
        # label, article, scope, advice, critical
        ("Tenir un registre des traitements", "Art. 30", ActionScope.ALL,
         "Le registre des traitements est obligatoire pour la majorité des entreprises, même les plus petites. Il permet d’identifier, de cartographier et de suivre tous les traitements de données personnelles réalisés par votre structure.", True),
        ("Informer les personnes concernées", "Art. 13-14", ActionScope.ALL,
         "Vous devez informer les personnes de leurs droits, de la finalité de la collecte, des destinataires, etc. Affichez une politique de confidentialité claire.", True),
        ("Limiter la conservation des données", "Art. 5-1-e)", ActionScope.ALL,
         "Les données ne doivent pas être conservées au-delà de ce qui est nécessaire à la finalité du traitement. Prévoyez un nettoyage ou une anonymisation régulière.", True),
        ("Mettre en place une AIPD au besoin", "Art. 35", ActionScope.ALL,
         "Une AIPD est requise pour les traitements susceptibles d’engendrer un risque élevé pour les droits et libertés des personnes. Consultez la liste de la CNIL.", True),
        ("Documenter une procédure de violation", "Art. 33-34", ActionScope.ALL,
         "Vous devez être capable de réagir rapidement en cas de fuite ou de perte de données. La procédure doit inclure la notification à la CNIL et aux personnes concernées si nécessaire.", True),
        ("Nommer un DPO (si requis)", "Art. 37", ActionScope.ALL,
         "La nomination d’un DPO est obligatoire dans certains cas (secteur public, traitements à grande échelle, données sensibles, etc.). Sinon, il reste conseillé de désigner un référent.", True),
        ("Mettre en place des clauses de confidentialité", "Art. 28-3 b", ActionScope.ALL,
         "Chaque contrat avec un sous-traitant doit inclure des engagements clairs de confidentialité et de sécurité concernant les données personnelles.", True),
        ("Documenter les modalités d’exercice des droits", "Art. 12-15", ActionScope.ALL,
         "Les personnes doivent pouvoir exercer facilement leurs droits. Préparez une procédure claire et formez vos équipes à la traiter dans les délais légaux.", True),
        ("Vérifier la sécurité des sous-traitants", "Art. 28", ActionScope.ALL,
         "Exigez des garanties, contrôlez les pratiques et privilégiez des prestataires respectant le RGPD.", True),
        ("Mettre en place une politique de conservation", "Art. 5-1 e)", ActionScope.ALL,
         "Définissez des durées de conservation pour chaque catégorie de données, et mettez en place des règles de suppression automatique ou d’archivage.", True),
        ("Gérer les violations de données (procédure)", "Art. 33-34", ActionScope.ALL,
         "La procédure doit couvrir la détection, la gestion et la notification des incidents dans les délais légaux.", True),
        ("Former les collaborateurs", "Art. 39-1 b", ActionScope.ALL,
         "La sensibilisation des équipes est clé. Prévoyez des formations régulières adaptées à chaque métier.", True),
        ("Recueillir un consentement explicite", "Art. 7", ActionScope.LEGAL_BASIS,
         "Le consentement doit être libre, spécifique, éclairé et univoque. Prévoyez une preuve du recueil du consentement.", True),
        ("Permettre le retrait du consentement", "Art. 7-3", ActionScope.LEGAL_BASIS,
         "Le retrait du consentement doit être aussi facile que son recueil. Ajoutez une procédure claire (lien de désabonnement, formulaire, etc.).", True),
        ("Informer sur la base contractuelle", "Art. 6-1 b", ActionScope.LEGAL_BASIS,
         "Mentionnez la base contractuelle dans votre politique de confidentialité et vos contrats.", False),
        ("Mettre à jour les CGU / contrats", "Art. 6-1 b", ActionScope.LEGAL_BASIS,
         "Révisez régulièrement les documents contractuels pour rester en conformité.", False),
        ("Justifier l’obligation légale applicable", "Art. 6-1 c", ActionScope.LEGAL_BASIS,
         "Documentez et conservez la référence légale pour chaque traitement fondé sur une obligation réglementaire.", False),
        ("Conserver les pièces justificatives légales", "Art. 6-1 c", ActionScope.LEGAL_BASIS,
         "Gardez les documents qui prouvent que les obligations légales sont respectées (factures, contrats, etc.).", False),
        ("Documenter l’intérêt légitime (LIA / Balance)", "Art. 6-1 f", ActionScope.LEGAL_BASIS,
         "Pour chaque traitement fondé sur l’intérêt légitime, il faut prouver que les droits des personnes ne sont pas lésés.", False),
        ("Mettre à disposition la LIA sur demande", "Art. 6-1 f", ActionScope.LEGAL_BASIS,
         "Préparez un document de synthèse prêt à transmettre si besoin.", False),
        ("Chiffrer les données sensibles au repos", "Art. 32", ActionScope.ALL,
         "Le chiffrement au repos limite les risques en cas de vol ou de perte de matériel.", True),
        ("Chiffrer les transferts externes", "Art. 32", ActionScope.ALL,
         "Utilisez le chiffrement (TLS, VPN, etc.) lors des échanges de données personnelles.", True),
        ("Mettre en place un contrôle d’accès", "Art. 32", ActionScope.ALL,
         "Attribuez les accès selon le principe du moindre privilège, tenez à jour les droits.", True),
        ("Revoir les habilitations périodiquement", "Art. 32", ActionScope.ALL,
         "Prévoyez une revue périodique (ex : chaque année ou lors des départs de collaborateurs).", True),
        ("Sauvegarder et tester la restauration", "Art. 32", ActionScope.ALL,
         "Les sauvegardes doivent être fréquentes, chiffrées et testées pour garantir leur efficacité.", True),
        ("Journaliser les accès aux données", "Art. 32-2 d", ActionScope.ALL,
         "Conservez les logs pour pouvoir investiguer en cas d’incident ou de contrôle.", True),
        ("Gérer les correctifs de sécurité (patching)", "Art. 32", ActionScope.ALL,
         "Le patch management est essentiel pour réduire les risques d’intrusion.", True),
        ("Signer des CT / BAA avec les sous-traitants", "Art. 28", ActionScope.ALL,
         "Formalisez la relation et les obligations en matière de confidentialité et sécurité des données personnelles.", True),
        ("Vérifier le transfert hors UE (clauses, BCR…)", "Chap. V", ActionScope.ALL,
         "Les transferts hors UE doivent être couverts par des clauses contractuelles ou des BCR validées.", True),
        ("Tester / auditer la sécurité", "Art. 32-1 d", ActionScope.ALL,
         "Planifiez des audits ou des tests d’intrusion pour vérifier l’efficacité de vos mesures de sécurité.", True),
    ]
    for label, article, scope, advice, critical in seed:
        db.add(GdprAction(label=label, article=article, scope=scope, advice=advice, critical=critical))
    db.commit()
    return db.query(GdprAction).all()

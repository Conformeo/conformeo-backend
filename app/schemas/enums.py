# app/schemas/enums.py
from enum import Enum

class AnswerEnum(str, Enum):
    CONFORME = "CONFORME"
    NON_CONFORME = "NON_CONFORME"
    NA = "NA"

    @classmethod                  # <-- autorise le front à envoyer en minuscules
    def _missing_(cls, value):
        lookup = {
            "conforme": cls.CONFORME,
            "non_conforme": cls.NON_CONFORME,
            "non_applicable": cls.NA,
            "na": cls.NA,
        }
        return lookup.get(str(value).lower())

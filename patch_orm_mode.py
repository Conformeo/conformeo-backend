import os
import re

BASE_DIR = "./app/schemas"
RE_ORM_MODE = re.compile(
    r"class\s+(\w+)\(BaseModel\):([\s\S]+?)(?:(?:class\s+Config:\s+([\s\S]+?))?orm_mode\s*=\s*True([\s\S]+?))?(?=\nclass|\Z)",
    re.MULTILINE
)

def patch_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    # Si pas de orm_mode dans le fichier, on skippe
    if "orm_mode = True" not in code:
        return False

    # Ajoute import ConfigDict s'il manque
    if "ConfigDict" not in code:
        code = "from pydantic import ConfigDict\n" + code

    # Remplace chaque bloc orm_mode par model_config
    def replace_block(match):
        class_def, before, config_block, after = match.groups()
        # Supprime l'éventuel "class Config" avec orm_mode
        code_block = before
        # Ajoute le model_config à la fin de la classe
        return f"class {class_def}(BaseModel):{code_block}    model_config = ConfigDict(from_attributes=True)\n"

    code = RE_ORM_MODE.sub(replace_block, code)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Patched: {filepath}")
    return True

def main():
    patched = 0
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                if patch_file(path):
                    patched += 1
    print(f"\nFait ! {patched} fichiers patchés.")

if __name__ == "__main__":
    main()

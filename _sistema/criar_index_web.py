import os

SISTEMA_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SISTEMA_DIR)
CENTRAL_PATH = os.path.join(BASE_DIR, 'BIBLIOTECA_CENTRAL.html')
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')

with open(CENTRAL_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

with open(INDEX_PATH, 'w', encoding='utf-8') as f_out:
    f_out.write(html)

print("SUCESSO: index.html sincronizado com BIBLIOTECA_CENTRAL.html!")

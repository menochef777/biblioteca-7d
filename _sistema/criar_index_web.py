import os
import re

SISTEMA_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SISTEMA_DIR)
CENTRAL_PATH = os.path.join(BASE_DIR, 'BIBLIOTECA_CENTRAL.html')
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')

with open(CENTRAL_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Para a versão Web / Vercel:
# Desativa checagem de servidor local de IA, ativando direto a Narração Neural Nativa Web Speech
html = html.replace('checkVoiceServer();', '// Web Edition: 100% nativo sem servidor local\n    isServerOnline = false;')
html = html.replace('setInterval(checkVoiceServer, 10000);', '// Web Edition: Zero requisições de fundo')

with open(INDEX_PATH, 'w', encoding='utf-8') as f_out:
    f_out.write(html)

print("SUCESSO: index.html criado para o GitHub Pages!")


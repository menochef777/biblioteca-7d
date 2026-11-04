import os
import re

SISTEMA_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SISTEMA_DIR)
CENTRAL_PATH = os.path.join(BASE_DIR, 'BIBLIOTECA_CENTRAL.html')
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')

with open(CENTRAL_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove voice button and status from public web edition
html = re.sub(r'<!-- Locução Exclusiva Pablo Marçal -->[\s\S]*?🔥 Pablo Marçal</span>', '<!-- Modo Leitura Pura Sem Travamentos -->', html)
html = html.replace('<span id="voice-badge" class="voice-badge" style="display:none;">○ Conectando...</span>', '')

# 2. Desativa polling de servidor de voz no GitHub Pages
html = html.replace('checkVoiceServer();', '// Web Edition: 100% nativo sem servidor')
html = html.replace('setInterval(checkVoiceServer, 10000);', '// Web Edition: Zero requisições de fundo')

with open(INDEX_PATH, 'w', encoding='utf-8') as f_out:
    f_out.write(html)

print("SUCESSO: index.html criado para o GitHub Pages!")


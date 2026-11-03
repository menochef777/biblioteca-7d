import re

with open(r'C:\Users\USER\Desktop\7D\Livros\BIBLIOTECA_CENTRAL.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove voice button and status from public web edition
html = re.sub(r'<!-- Locução Exclusiva Pablo Marçal -->[\s\S]*?🔥 Pablo Marçal</span>', '<!-- Modo Leitura Pura Sem Travamentos -->', html)
html = html.replace('<span id="voice-badge" class="voice-badge" style="display:none;">○ Conectando...</span>', '')

# 2. Desativa polling de servidor de voz no GitHub Pages
html = html.replace('checkVoiceServer();', '// Web Edition: 100% nativo sem servidor')
html = html.replace('setInterval(checkVoiceServer, 10000);', '// Web Edition: Zero requisições de fundo')

with open(r'C:\Users\USER\Desktop\7D\Livros\index.html', 'w', encoding='utf-8') as f_out:
    f_out.write(html)

print("SUCESSO: index.html criado para o GitHub Pages!")

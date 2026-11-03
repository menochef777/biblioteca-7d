import json, sys
sys.stdout.reconfigure(encoding='utf-8')
data_js = r'C:\Users\USER\Desktop\7D\Livros\_sistema\biblioteca_data\livros_data.js'
with open(data_js, 'r', encoding='utf-8') as f:
    text = f.read()
data = json.loads(text.split('window.BIBLIOTECA_LIVROS = ')[1].rstrip(';\n'))
for b in data:
    w = sum(len(x.get('text','').split()) for x in b['content'] if x.get('type')=='paragraph')
    m = w // 200
    h = m // 60
    rm = m % 60
    t = f"{h}h {rm}min" if h > 0 else f"{rm}min"
    print(f"ID: {b['id']} | Titulo: {b['title']} | Palavras: {w} | Tempo: {t} | Pags: {b['totalPages']}")


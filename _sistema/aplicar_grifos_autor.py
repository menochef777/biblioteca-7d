import os
import sys
import re
import json
import pymupdf

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

SISTEMA_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SISTEMA_DIR) # C:\Users\USER\Desktop\7D\Livros
DATA_FILE = os.path.join(SISTEMA_DIR, 'biblioteca_data', 'livros_data.js')

print(f"Lendo banco de dados: {DATA_FILE}...")
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    raw_content = f.read()

prefix = "// Banco de Dados Local da Biblioteca 7D\nwindow.BIBLIOTECA_LIVROS = "
json_str = raw_content.split(prefix)[1].rstrip(';\n')
books = json.loads(json_str)

total_grifos_aplicados = 0
total_capas_removidas = 0

pdf_map = {}
for fname in os.listdir(BASE_DIR):
    if fname.lower().endswith('.pdf'):
        # slugify aproximado para parear
        slug = re.sub(r'[^a-z0-9]+', '_', os.path.splitext(fname)[0].lower()).strip('_')[:40]
        pdf_map[slug] = os.path.join(BASE_DIR, fname)

for b in books:
    b_id = b["id"]
    b_title = b["title"]
    content = b.get("content", [])
    
    # 1. Remove imagens da página 1 (que são a capa repetida dentro do livro)
    new_content = []
    for item in content:
        if item.get("type") == "image" and item.get("page") == 1:
            total_capas_removidas += 1
            continue
        new_content.append(item)
    b["content"] = new_content
    
    # 2. Localizar o arquivo PDF correspondente para extrair os grifos e negritos originais
    pdf_path = pdf_map.get(b_id)
    if not pdf_path:
        for s, path in pdf_map.items():
            if s in b_id or b_id in s:
                pdf_path = path
                break
                
    if not pdf_path or not os.path.exists(pdf_path):
        print(f"PDF não encontrado para {b_title}, mantendo texto atual.")
        continue
        
    print(f"\nExtraindo grifos e ênfases originais do autor em: {b_title}...")
    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"  Erro ao abrir PDF: {e}")
        continue
        
    # Coleta spans em negrito por página
    page_bolds = {}
    for pno in range(len(doc)):
        p1based = pno + 1
        page = doc[pno]
        d = page.get_text("dict")
        bolds = []
        for block in d.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    flags = span.get("flags", 0)
                    font = span.get("font", "").lower()
                    text = span.get("text", "").strip()
                    
                    # Limpa hífens invisíveis
                    text = re.sub(r'\xad\s*', '', text)
                    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
                    text = re.sub(r'[ \t]+', ' ', text).strip()
                    
                    is_bold = ('bold' in font or 'black' in font or 'heavy' in font or flags & 16)
                    # Não marca números puros ou cabeçalhos curtos de 2 caracteres
                    if is_bold and len(text) > 2 and not text.isdigit():
                        bolds.append(text)
        if bolds:
            # Ordena por tamanho decrescente para substituir frases maiores primeiro
            bolds.sort(key=len, reverse=True)
            page_bolds[p1based] = bolds
            
    doc.close()
    
    # Aplica as tags <strong> nos parágrafos correspondentes
    book_grifos = 0
    for block in b["content"]:
        if block.get("type") == "paragraph":
            p_text = block.get("text", "")
            p_page = block.get("page", 1)
            
            bolds_to_apply = page_bolds.get(p_page, [])
            if not bolds_to_apply and p_page > 1:
                # Tenta também página anterior se foi fundido
                bolds_to_apply = page_bolds.get(p_page - 1, [])
                
            for bold_phrase in bolds_to_apply:
                # Evita marcar se já tiver tag ou for minúsculo
                if len(bold_phrase) < 3 or bold_phrase in ['o', 'a', 'de', 'em', 'para']:
                    continue
                if bold_phrase in p_text and f"<strong>{bold_phrase}</strong>" not in p_text:
                    # Substitui apenas palavras completas ou a frase exata
                    escaped_phrase = re.escape(bold_phrase)
                    # Substitui de forma segura
                    new_text, count = re.subn(rf'(?<!<strong>){escaped_phrase}(?!</strong>)', f'<strong>{bold_phrase}</strong>', p_text)
                    if count > 0:
                        p_text = new_text
                        book_grifos += count
                        total_grifos_aplicados += count
                        
            block["text"] = p_text
            
    print(f"  OK: {book_grifos} trechos grifados pelo autor destacados com sucesso!")

print(f"\n=======================================================")
print(f"RELATÓRIO DE GRIFOS & IMAGENS:")
print(f"-> Capas redundantes removidas de dentro dos livros: {total_capas_removidas}")
print(f"-> Trechos originais grifados pelo autor preservados: {total_grifos_aplicados}")
print(f"=======================================================\n")

print(f"Gravando banco de dados atualizado em: {DATA_FILE}...")
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    f.write(prefix)
    json.dump(books, f, ensure_ascii=False, indent=None)
    f.write(";\n")

file_size_mb = os.path.getsize(DATA_FILE) / (1024 * 1024)
print(f"Concluído com sucesso! Tamanho final: {file_size_mb:.2f} MB")


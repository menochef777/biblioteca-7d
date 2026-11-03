import json
import os
import re
import sys

# Garante UTF-8 no terminal
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

SISTEMA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SISTEMA_DIR, 'biblioteca_data', 'livros_data.js')

print(f"Lendo banco de dados: {DATA_FILE}...")
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    raw_content = f.read()

prefix = "// Banco de Dados Local da Biblioteca 7D\nwindow.BIBLIOTECA_LIVROS = "
json_str = raw_content.split(prefix)[1].rstrip(';\n')
books = json.loads(json_str)

total_cleaned_hyphens = 0
total_removed_headers = 0
total_merged_paras = 0

def clean_text_block(text):
    global total_cleaned_hyphens
    if not text:
        return ""
    
    # 1. Remove caracteres invisíveis (soft hyphen, zero-width spaces, BOM)
    # \xad seguido de espaço ou sem espaço: 'de\xad talhes' -> 'detalhes'
    original = text
    text = re.sub(r'\xad\s*', '', text)
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
    
    # 2. Corrige hifens seguidos de espaço no meio de palavras: 'apresen- tações' -> 'apresentações'
    # 'humi- lhado' -> 'humilhado', 'con- verti' -> 'converti'
    text = re.sub(r'(\b[a-zA-ZáéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ]+)-\s+([a-zA-ZáéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ]+\b)', r'\1\2', text)
    
    # 3. Corrige espaços duplos ou múltiplos
    text = re.sub(r'[ \t]+', ' ', text).strip()
    
    if text != original:
        total_cleaned_hyphens += 1
        
    return text

for b in books:
    b_id = b["id"]
    b_title = b["title"].strip()
    content = b.get("content", [])
    
    print(f"\nProcessando e refinando: {b_title}...")
    
    # 1. Identificar cabeçalhos/rodapés repetitivos deste livro
    para_texts = [x.get("text", "").strip() for x in content if x.get("type") == "paragraph"]
    from collections import Counter
    counts = Counter(para_texts)
    
    # Palavras/frases repetidas mais de 8 vezes ou que coincidem com o título/autor
    blacklist_phrases = set()
    for txt, count in counts.items():
        if count >= 8 and len(txt) <= 60:
            blacklist_phrases.add(txt)
    
    # Adiciona variações do título se forem parágrafos isolados
    blacklist_phrases.add(b_title)
    if "antimedo" in b_id:
        blacklist_phrases.add("Antimedo")
        blacklist_phrases.add("ANTIMEDO")
        blacklist_phrases.add("Pablo Marçal")
    elif "arte_da_guerra" in b_id:
        blacklist_phrases.add("A Arte da Guerra")
        blacklist_phrases.add("Sun Tzu")
    elif "inteligencia_emocional" in b_id:
        blacklist_phrases.add("Inteligência Emocional")
        blacklist_phrases.add("Daniel Goleman")
    elif "48_leis" in b_id:
        blacklist_phrases.add("As 48 Leis do Poder")
        blacklist_phrases.add("Robert Greene")
    elif "diabo" in b_id:
        blacklist_phrases.add("Mais Esperto que o Diabo")
        blacklist_phrases.add("Napoleon Hill")
    
    # Filtra blocos limpando texto e removendo cabeçalhos fantasmas
    filtered_blocks = []
    for block in content:
        b_type = block.get("type")
        if b_type == "paragraph":
            raw_t = block.get("text", "").strip()
            # Se for cabeçalho fantasma isolado, remove
            if raw_t in blacklist_phrases:
                total_removed_headers += 1
                continue
            
            cleaned_t = clean_text_block(raw_t)
            if cleaned_t:
                block["text"] = cleaned_t
                filtered_blocks.append(block)
        else:
            filtered_blocks.append(block)
            
    # 2. Costura parágrafos que foram cortados no meio pela quebra de página
    stitched_blocks = []
    i = 0
    while i < len(filtered_blocks):
        curr = filtered_blocks[i]
        
        # Se for parágrafo, verifica se pode juntar com o próximo
        if curr.get("type") == "paragraph" and i + 1 < len(filtered_blocks):
            next_block = filtered_blocks[i + 1]
            
            if next_block.get("type") == "paragraph":
                curr_text = curr.get("text", "").strip()
                next_text = next_block.get("text", "").strip()
                
                # Critério de união:
                # O parágrafo atual termina sem pontuação final forte (. ! ? : " ”) ou termina com letra minúscula/vírgula
                # E o próximo parágrafo começa com letra minúscula (ou vírgula/continuação direta)
                ends_open = not bool(re.search(r'[.!?:"”»]$', curr_text)) or curr_text.endswith(',') or curr_text.endswith(';')
                starts_lower = bool(re.match(r'^[a-záéíóúâêîôûãõç]', next_text))
                
                if ends_open and starts_lower:
                    # Une os dois parágrafos
                    joined = curr_text + " " + next_text
                    curr["text"] = joined
                    total_merged_paras += 1
                    i += 1 # pula o próximo pois foi fundido
                    stitched_blocks.append(curr)
                    i += 1
                    continue
                    
        stitched_blocks.append(curr)
        i += 1
        
    b["content"] = stitched_blocks
    print(f"  OK: {len(content)} blocos originais -> {len(stitched_blocks)} blocos refinados.")

print(f"\n=======================================================")
print(f"RELATÓRIO DE LIMPEZA TEXTUAL:")
print(f"-> Palavras/hifens corrigidos: {total_cleaned_hyphens}")
print(f"-> Cabeçalhos/rodapés fantasmas removidos: {total_removed_headers}")
print(f"-> Parágrafos fragmentados fundidos: {total_merged_paras}")
print(f"=======================================================\n")

print(f"Gravando banco de dados atualizado em: {DATA_FILE}...")
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    f.write(prefix)
    json.dump(books, f, ensure_ascii=False, indent=None)
    f.write(";\n")

file_size_mb = os.path.getsize(DATA_FILE) / (1024 * 1024)
print(f"Concluído com sucesso! Tamanho final: {file_size_mb:.2f} MB")


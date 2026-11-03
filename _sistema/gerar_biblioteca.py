import os
import sys
import re
import json
import html
import pymupdf

# Força UTF-8 no console
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

SISTEMA_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SISTEMA_DIR) # C:\Users\USER\Desktop\7D\Livros
DATA_DIR = os.path.join(SISTEMA_DIR, 'biblioteca_data')
IMAGES_DIR = os.path.join(DATA_DIR, 'images')
COVERS_DIR = os.path.join(DATA_DIR, 'covers')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(COVERS_DIR, exist_ok=True)

pdf_files = [f for f in os.listdir(BASE_DIR) if f.lower().endswith('.pdf')]
print(f"Encontrados {len(pdf_files)} livros PDF para processamento.")

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')[:40]

biblioteca = []

for idx, fname in enumerate(pdf_files):
    fpath = os.path.join(BASE_DIR, fname)
    slug = slugify(os.path.splitext(fname)[0])
    book_img_dir = os.path.join(IMAGES_DIR, slug)
    os.makedirs(book_img_dir, exist_ok=True)

    print(f"\n[{idx+1}/{len(pdf_files)}] Processando: {fname}...")
    try:
        doc = pymupdf.open(fpath)
    except Exception as e:
        print(f"  Erro ao abrir {fname}: {e}")
        continue

    total_pages = len(doc)
    clean_title = os.path.splitext(fname)[0].replace('_', ' ').replace('-', ' ')
    clean_title = re.sub(r'\s+', ' ', clean_title).strip()

    # Gerar Capa em PNG
    cover_filename = f"cover_{slug}.png"
    cover_path = os.path.join(COVERS_DIR, cover_filename)
    cover_rel_url = f"_sistema/biblioteca_data/covers/{cover_filename}"
    
    if total_pages > 0 and not os.path.exists(cover_path):
        try:
            p0 = doc[0]
            pix = p0.get_pixmap(dpi=150)
            pix.save(cover_path)
        except Exception as e:
            print(f"  Erro ao gerar capa: {e}")

    # Sumário / TOC
    raw_toc = doc.get_toc()
    toc_items = []
    page_to_headings = {}
    
    for t_idx, item in enumerate(raw_toc):
        lvl, title, page = item[0], item[1], item[2]
        c_title = title.replace('\xad', '').strip()
        anchor = f"h_{slug}_{t_idx}"
        toc_items.append({
            "id": anchor,
            "lvl": lvl,
            "title": c_title,
            "page": page
        })
        if page not in page_to_headings:
            page_to_headings[page] = []
        page_to_headings[page].append((lvl, c_title, anchor))

    # Processar Páginas: Texto & Imagens
    content_blocks = []
    total_images_extracted = 0
    extracted_xrefs = set()

    for p_num in range(total_pages):
        page_1based = p_num + 1
        page = doc[p_num]

        # Títulos do Sumário
        if page_1based in page_to_headings:
            for lvl, h_title, anchor in page_to_headings[page_1based]:
                content_blocks.append({
                    "type": "heading",
                    "lvl": lvl,
                    "title": h_title,
                    "id": anchor,
                    "page": page_1based
                })

        # Imagens da Página
        page_images = page.get_images()
        for img_info in page_images:
            xref = img_info[0]
            if xref in extracted_xrefs:
                continue
            extracted_xrefs.add(xref)
            try:
                base_img = doc.extract_image(xref)
                img_bytes = base_img["image"]
                img_ext = base_img["ext"]
                img_fname = f"img_p{page_1based}_{xref}.{img_ext}"
                img_disk_path = os.path.join(book_img_dir, img_fname)
                
                if not os.path.exists(img_disk_path):
                    with open(img_disk_path, "wb") as img_f:
                        img_f.write(img_bytes)

                rel_img_url = f"_sistema/biblioteca_data/images/{slug}/{img_fname}"
                content_blocks.append({
                    "type": "image",
                    "src": rel_img_url,
                    "page": page_1based,
                    "width": base_img.get("width", 0),
                    "height": base_img.get("height", 0)
                })
                total_images_extracted += 1
            except Exception:
                pass

        # Texto da Página
        blocks = page.get_text("blocks")
        for b in blocks:
            if b[6] == 0:  # text block
                raw_text = b[4].strip()
                if re.match(r'^\d+$', raw_text) or len(raw_text) < 3:
                    continue
                raw_text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', raw_text)
                raw_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', raw_text)
                paras = [p.strip() for p in raw_text.split('\n') if p.strip()]
                for p in paras:
                    if len(p) > 2:
                        p_clean = re.sub(r'[ \t]+', ' ', p)
                        content_blocks.append({
                            "type": "paragraph",
                            "text": p_clean,
                            "page": page_1based
                        })

    print(f"  OK: {total_pages} pgs, {total_images_extracted} imagens, {len(content_blocks)} blocos de texto.")

    biblioteca.append({
        "id": slug,
        "title": clean_title,
        "filename": fname,
        "cover": cover_rel_url,
        "totalPages": total_pages,
        "totalImages": total_images_extracted,
        "toc": toc_items,
        "content": content_blocks
    })

# Grava arquivo JS
js_output = os.path.join(DATA_DIR, 'livros_data.js')
print(f"\nGravando banco de dados da biblioteca em: {js_output}...")

with open(js_output, 'w', encoding='utf-8') as f:
    f.write("// Banco de Dados Local da Biblioteca 7D\n")
    f.write("window.BIBLIOTECA_LIVROS = ")
    json.dump(biblioteca, f, ensure_ascii=False, indent=None)
    f.write(";\n")

file_size_mb = os.path.getsize(js_output) / (1024 * 1024)
print(f"Extração concluída com sucesso! Tamanho: {file_size_mb:.2f} MB")

# 1. Executa limpeza e refinamento textual (remove hífens fantasmas e cabeçalhos)
clean_script = os.path.join(SISTEMA_DIR, 'limpar_texto.py')
if os.path.exists(clean_script):
    print("\nRefinando textos e corrigindo quebras de palavras...")
    try:
        import subprocess
        subprocess.run([sys.executable, clean_script], check=True)
    except Exception as e:
        print(f"Aviso na limpeza textual: {e}")

# 2. Executa enriquecimento pedagógico e tempos de leitura automaticamente
enrich_script = os.path.join(SISTEMA_DIR, 'enrich_books.py')
if os.path.exists(enrich_script):
    print("\nAplicando Curadoria Pedagógica e Cálculo de Tempos de Leitura...")
    try:
        import subprocess
        subprocess.run([sys.executable, enrich_script], check=True)
    except Exception as e:
        print(f"Aviso no enriquecimento: {e}")


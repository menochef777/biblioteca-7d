import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

SISTEMA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SISTEMA_DIR, 'biblioteca_data', 'livros_data.js')

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "// Banco de Dados Local da Biblioteca 7D\nwindow.BIBLIOTECA_LIVROS = "
json_str = text.split(prefix)[1].rstrip(';\n')
books = json.loads(json_str)

# Metadados pedagógicos refinados para cada livro
CURADORIA = {
    "antimedo_versa_o_2_0": {
        "order": 1,
        "category": "quick",
        "levelTitle": "Nível 1 • Vitórias Rápidas",
        "difficulty": "Fácil & Direto",
        "diffColor": "#10B981",
        "why": "O mais curto da estante. Destrava a coragem, quebra o bloqueio de ler e dá a primeira sensação de conquista rápida.",
        "complement": "Prepara a mente eliminando o medo de agir e a procrastinação."
    },
    "a_arte_da_guerra_sun_tzu": {
        "order": 2,
        "category": "quick",
        "levelTitle": "Nível 1 • Vitórias Rápidas",
        "difficulty": "Rápido & Dinâmico",
        "diffColor": "#10B981",
        "why": "Apenas 80 páginas com aforismos curtos. Ensina estratégia, planejamento e a vencer sem desgaste inútil.",
        "complement": "Ensina a pensar estrategicamente antes de entrar em ação."
    },
    "mais_esperto_que_o_diabo_o_mist_rio_reve": {
        "order": 3,
        "category": "quick",
        "levelTitle": "Nível 1 • Vitórias Rápidas",
        "difficulty": "Envolvente (Estilo Entrevista)",
        "diffColor": "#10B981",
        "why": "Escrito em formato de diálogo/interrogatório direto com o Diabo. Prende a atenção do começo ao fim como um filme.",
        "complement": "Revela como a alienação e a preguiça mental travam 98% das pessoas."
    },
    "pnl_t_cnicas_proibidas_de_persuas_o": {
        "order": 4,
        "category": "pnl",
        "levelTitle": "Nível 2 • PNL & Influência Prática",
        "difficulty": "Prático & Estimulante",
        "diffColor": "#F59E0B",
        "why": "Super prático e curioso. Ensina rapport imediato, leitura de linguagem corporal e padrões de persuasão.",
        "complement": "Você lê e já testa na prática nas suas conversas no mesmo dia."
    },
    "comunicar_vender_e_negociar_com_pnl": {
        "order": 5,
        "category": "pnl",
        "levelTitle": "Nível 2 • PNL & Influência Prática",
        "difficulty": "Prático & Negócios",
        "diffColor": "#F59E0B",
        "why": "Aplica as ferramentas de PNL em negociações, vendas e persuasão de alto valor.",
        "complement": "Transforma a teoria da PNL em dinheiro e resultados profissionais."
    },
    "poder_e_manipula_o": {
        "order": 6,
        "category": "pnl",
        "levelTitle": "Nível 2 • PNL & Influência Prática",
        "difficulty": "Defensivo & Alerta",
        "diffColor": "#F59E0B",
        "why": "Ensina a identificar quando estão tentando manipular você no trabalho, na família ou nos negócios.",
        "complement": "Cria um escudo psicológico contra armadilhas de pessoas manipuladoras."
    },
    "introdu_o_a_pnl_joseph_o_connor": {
        "order": 7,
        "category": "pnl",
        "levelTitle": "Nível 2 • PNL & Influência Prática",
        "difficulty": "Visual & Completo (54 Diagramas)",
        "diffColor": "#F59E0B",
        "why": "O manual completo e didático da PNL, repleto de esquemas visuais sobre como o cérebro processa sentimentos.",
        "complement": "Aprofunda a ciência de modelar comportamentos de sucesso."
    },
    "foco_by_daniel_goleman_z_lib_org_epub": {
        "order": 8,
        "category": "mind",
        "levelTitle": "Nível 3 • Foco & Inteligência Emocional",
        "difficulty": "Neurociência Prática",
        "diffColor": "#38BDF8",
        "why": "O ativo mais raro do século XXI: atenção. Ensina a combater distrações digitais e manter foco profundo.",
        "complement": "Prepara sua mente para absorver leituras maiores sem se dispersar."
    },
    "robert_b_cialdini_as_armas_da_persuas_o": {
        "order": 9,
        "category": "mind",
        "levelTitle": "Nível 3 • Foco & Inteligência Emocional",
        "difficulty": "Clássico da Psicologia Social",
        "diffColor": "#38BDF8",
        "why": "Os 6 gatilhos psicológicos universais: reciprocidade, escassez, autoridade, compromisso, afeição e prova social.",
        "complement": "A ciência exata do porquê as pessoas dizem 'sim'."
    },
    "inteligencia_emocional_daniel_goleman": {
        "order": 10,
        "category": "mind",
        "levelTitle": "Nível 3 • Foco & Inteligência Emocional",
        "difficulty": "Profundo & Transformador",
        "diffColor": "#38BDF8",
        "why": "O clássico mundial que provou que a inteligência emocional (QE) importa mais para o sucesso que o QI.",
        "complement": "Domínio da raiva, ansiedade, impulsividade e empatia."
    },
    "antifr_gil_coisas_que_se_beneficiam_com_": {
        "order": 11,
        "category": "mastery",
        "levelTitle": "Nível 4 • Estratégia Máxima & Maestria",
        "difficulty": "Avançado & Filosófico (64 Gráficos)",
        "diffColor": "#EF4444",
        "why": "Como não apenas resistir ao caos, mas ficar mais forte e lucrar com os choques da vida e dos negócios.",
        "complement": "Eleva seu modelo de mundo para um nível muito acima da média."
    },
    "as_48_leis_do_poder": {
        "order": 12,
        "category": "mastery",
        "levelTitle": "Nível 4 • Estratégia Máxima & Maestria",
        "difficulty": "O Livro Definitivo de Poder",
        "diffColor": "#EF4444",
        "why": "Três mil anos de história do poder condensados em 48 regras implacáveis. Cada lei possui lições históricas fascinantes.",
        "complement": "A coroação da sua jornada: a maestria das relações humanas e do poder."
    }
}

for b in books:
    b_id = b["id"]
    # Calculate words & reading time
    w = sum(len(x.get("text", "").split()) for x in b.get("content", []) if x.get("type") == "paragraph")
    m = w // 200
    h = m // 60
    rm = m % 60
    t = f"{h}h {rm}min" if h > 0 else f"{rm}min"
    
    b["wordCount"] = w
    b["readingTime"] = t
    
    cur = CURADORIA.get(b_id, {
        "order": 99,
        "category": "other",
        "levelTitle": "Geral",
        "difficulty": "Médio",
        "diffColor": "#F59E0B",
        "why": "Livro catalogado na biblioteca.",
        "complement": "Expansão de conhecimento."
    })
    
    b["order"] = cur["order"]
    b["category"] = cur["category"]
    b["levelTitle"] = cur["levelTitle"]
    b["difficulty"] = cur["difficulty"]
    b["diffColor"] = cur["diffColor"]
    b["why"] = cur["why"]
    b["complement"] = cur["complement"]

# Sort books by order
books.sort(key=lambda x: x["order"])

print(f"Atualizando {len(books)} livros com ordem pedagógica e tempos de leitura...")
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    f.write(prefix)
    json.dump(books, f, ensure_ascii=False, indent=None)
    f.write(";\n")

print("Sucesso! Livros organizados do 1º ao 12º.")


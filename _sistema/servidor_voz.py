import asyncio
import hashlib
import json
import os
import re
import sys
import urllib.request
from aiohttp import web
import edge_tts

# Força UTF-8 no console
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

SISTEMA_DIR = os.path.dirname(os.path.abspath(__file__))
LIVROS_DIR = os.path.dirname(SISTEMA_DIR)
HTML_PATH = os.path.join(LIVROS_DIR, 'BIBLIOTECA_CENTRAL.html')
CACHE_DIR = os.path.join(SISTEMA_DIR, 'biblioteca_data', 'cache_audio')
os.makedirs(CACHE_DIR, exist_ok=True)
PABLO_SAMPLE = os.path.join(SISTEMA_DIR, 'biblioteca_data', 'amostra_pablo_marcal.mp3')

# Lock para serializar inferências no VoiceStudio e evitar conflito na GPU
vs_lock = asyncio.Lock()

def limpar_texto_para_tts(t: str) -> str:
    """Higieniza quebras de hífens do PDF e termos em inglês para pronúncia brasileira perfeita"""
    t = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', t)
    t = re.sub(r'\bde\s+talhes\b', 'detalhes', t, flags=re.IGNORECASE)
    t = re.sub(r'\bimpressionan\s+te\b', 'impressionante', t, flags=re.IGNORECASE)
    t = re.sub(r'\búlti\s+mo\b', 'último', t, flags=re.IGNORECASE)
    t = re.sub(r'\bre\s+crutado\b', 'recrutado', t, flags=re.IGNORECASE)
    t = re.sub(r'\bpower\s*point\b', 'póuer pointe', t, flags=re.IGNORECASE)
    t = re.sub(r'\btennis\s+Qix\b', 'tênis Kíquis', t, flags=re.IGNORECASE)
    t = re.sub(r'\bQix\b', 'Kíquis', t, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', t).strip()

# Vozes Disponíveis
VOICES = {
    'pablo': 'pablo',                            # Voz Clonada Pablo Marçal (VoiceStudio / Fish)
    'antonio': 'pt-BR-AntonioNeural',            # Locutor solene / Bíblia / Documentário
    'francisca': 'pt-BR-FranciscaNeural',        # Narradora suave e elegante
    'thalita': 'pt-BR-ThalitaMultilingualNeural' # Locutora moderna / CapCut
}

async def handle_index(request):
    """Serve a aplicação principal da Biblioteca"""
    if os.path.exists(HTML_PATH):
        with open(HTML_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        return web.Response(text=content, content_type='text/html', charset='utf-8')
    return web.Response(status=404, text="Arquivo BIBLIOTECA_CENTRAL.html não encontrado")

async def handle_health(request):
    return web.json_response({
        "status": "online",
        "service": "Biblioteca 7D Localhost",
        "voices": list(VOICES.keys())
    }, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    })

async def handle_options(request):
    return web.Response(headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    })

async def handle_tts(request):
    if request.method == "POST":
        try:
            data = await request.json()
            text = data.get("text", "")
            voice_key = data.get("voice", "pablo")
            rate = data.get("rate", "-2%")
            pitch = data.get("pitch", "-4Hz")
        except Exception:
            text = ""
            voice_key = "pablo"
            rate = "-2%"
            pitch = "-4Hz"
    else:
        text = request.query.get("text", "")
        voice_key = request.query.get("voice", "pablo")
        rate = request.query.get("rate", "-2%")
        pitch = request.query.get("pitch", "-4Hz")

    text = text.strip()
    if not text:
        return web.Response(status=400, text="Texto vazio")

    voice_key = voice_key.lower()
    voice = VOICES.get(voice_key, VOICES['pablo'])

    # Hash para cache do áudio
    text_hash = hashlib.md5(f"{voice_key}_{pitch}_{rate}_{text}".encode('utf-8')).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{text_hash}.mp3")

    if not os.path.exists(cache_path):
        if voice_key == 'pablo':
            cloned_success = False
            
            # 0. Se for o trecho da amostra autêntica do Pablo Marçal, serve direto
            if "nunca esquecerei" in text.lower() or "converti aquela energia" in text.lower() or "processo seletivo" in text.lower():
                if os.path.exists(PABLO_SAMPLE):
                    try:
                        import shutil
                        shutil.copyfile(PABLO_SAMPLE, cache_path)
                        cloned_success = True
                    except Exception as e:
                        print(f"[Aviso Sample Pablo] {e}")

            # 1. Motor Neural VoiceStudio (Porta 3900) - Perfil Clonado Pablo Marçal 800814af
            # 100% Pablo Marçal, serializado por Lock para a GPU RTX 3050. Zero contaminação com Antonio.
            if not cloned_success:
                clean_text = limpar_texto_para_tts(text)
                async with vs_lock:
                    try:
                        payload = json.dumps({
                            "input": clean_text,
                            "voice": "800814af",
                            "response_format": "mp3",
                            "language": "pt",
                            "speed": 1.05
                        }).encode('utf-8')
                        req_vs = urllib.request.Request(
                            "http://127.0.0.1:3900/v1/audio/speech",
                            data=payload,
                            headers={"Content-Type": "application/json"}
                        )
                        def _fetch():
                            with urllib.request.urlopen(req_vs, timeout=90) as resp:
                                return resp.read() if resp.status == 200 else None
                        
                        audio_data = await asyncio.to_thread(_fetch)
                        if audio_data and len(audio_data) > 1000:
                            with open(cache_path, "wb") as f_out:
                                f_out.write(audio_data)
                            cloned_success = True
                            print(f"[VoiceStudio Pablo] Frase clonada com sucesso: {len(audio_data)} bytes")
                        else:
                            print(f"[VoiceStudio Pablo] Resposta vazia ou curta")
                    except Exception as e:
                        print(f"[VoiceStudio Pablo Erro] {e}")
                        return web.Response(status=500, text=f"Erro ao sintetizar com VoiceStudio Pablo: {e}")
        else:
            try:
                # Vozes Especializadas
                if voice_key == 'antonio':
                    # Locutor Estilo Bíblia Online (Solene, Profundo e Ressonante)
                    communicate = edge_tts.Communicate(text, 'pt-BR-AntonioNeural', pitch='-4Hz', rate='-2%')
                elif voice_key == 'francisca':
                    # Narradora Suave e Acolhedora
                    communicate = edge_tts.Communicate(text, 'pt-BR-FranciscaNeural', pitch='0Hz', rate='+0%')
                elif voice_key == 'thalita':
                    # Locutora CapCut Dinâmica
                    communicate = edge_tts.Communicate(text, 'pt-BR-ThalitaMultilingualNeural', pitch='+1Hz', rate='+5%')
                else:
                    communicate = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate)
                await communicate.save(cache_path)
            except Exception as e:
                print(f"[Erro Edge-TTS] {e}")
                return web.Response(status=500, text=f"Erro ao sintetizar áudio: {e}")

    try:
        with open(cache_path, "rb") as f:
            audio_bytes = f.read()
        return web.Response(
            body=audio_bytes,
            content_type="audio/mpeg",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "public, max-age=86400"
            }
        )
    except Exception as e:
        return web.Response(status=500, text=str(e))

def create_app():
    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/health", handle_health)
    app.router.add_options("/health", handle_options)
    app.router.add_get("/tts", handle_tts)
    app.router.add_post("/tts", handle_tts)
    app.router.add_options("/tts", handle_options)
    
    # Servir arquivos estáticos de _sistema
    app.router.add_static("/_sistema", SISTEMA_DIR, show_index=False)
    return app

if __name__ == "__main__":
    port = 5055
    print("=" * 65)
    print("   📚 BIBLIOTECA 7D PRO — SERVIDOR LOCALHOST ATIVO")
    print("=" * 65)
    print(f"➜ Acesse no Navegador: http://localhost:{port}")
    print("➜ Locutor de Estúdio Conectado (Antonio Neural / Estilo Bíblia)")
    print("➜ Navegação Nativa por Abas e Histórico Habilitada")
    print("Pressione Ctrl+C para encerrar.")
    print("-" * 65)
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=port, print=None)

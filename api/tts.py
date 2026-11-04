from http.server import BaseHTTPRequestHandler
from urllib import parse
import asyncio
import io
import json
import re
import edge_tts

def sanitize_text(text: str) -> str:
    """Higieniza o texto para narração perfeita e limpa"""
    if not text:
        return ""
    # Remove tags HTML
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove marcas de paginação
    text = re.sub(r'P[áa]g\.\s*\d+', '', text, flags=re.IGNORECASE)
    # Corrige hifens de quebra de linha de PDF (ex: trans- formação -> transformação)
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
    # Remove caracteres especiais desnecessários
    text = re.sub(r'[*_#~`]', '', text)
    # Normaliza espaços
    text = re.sub(r'\s+', ' ', text).strip()
    # Adiciona pontuação final se não houver
    if text and not text.endswith(('.', '!', '?', ';', ':')):
        text += '.'
    return text

class handler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = parse.urlparse(self.path)
        params = dict(parse.parse_qsl(parsed.query))
        text = params.get('text', '').strip()
        voice = params.get('voice', 'pt-BR-AntonioNeural')
        rate = params.get('rate', '-2%')
        pitch = params.get('pitch', '-3Hz')

        self._process_tts(text, voice, rate, pitch)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        text = ""
        voice = "pt-BR-AntonioNeural"
        rate = "-2%"
        pitch = "-3Hz"

        try:
            body = json.loads(post_data.decode('utf-8'))
            text = body.get('text', '')
            voice = body.get('voice', voice)
            rate = body.get('rate', rate)
            pitch = body.get('pitch', pitch)
        except Exception:
            pass

        self._process_tts(text, voice, rate, pitch)

    def _process_tts(self, raw_text: str, voice: str, rate: str, pitch: str):
        cleaned_text = sanitize_text(raw_text)
        if not cleaned_text:
            self.send_response(400)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Texto vazio'}).encode('utf-8'))
            return

        async def generate_speech():
            # pt-BR-AntonioNeural é a voz masculina solene de narrador bíblico
            selected_voice = voice if voice else 'pt-BR-AntonioNeural'
            communicate = edge_tts.Communicate(cleaned_text, selected_voice, rate=rate, pitch=pitch)
            buf = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk['type'] == 'audio':
                    buf.write(chunk['data'])
            return buf.getvalue()

        try:
            audio_bytes = asyncio.run(generate_speech())
            if not audio_bytes:
                raise ValueError("Nenhum byte de áudio retornado pelo sintetizador")

            self.send_response(200)
            self._set_cors_headers()
            self.send_header('Content-Type', 'audio/mpeg')
            self.send_header('Cache-Control', 'public, max-age=604800, immutable')
            self.send_header('Content-Length', str(len(audio_bytes)))
            self.end_headers()
            self.wfile.write(audio_bytes)
        except Exception as err:
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(err)}).encode('utf-8'))

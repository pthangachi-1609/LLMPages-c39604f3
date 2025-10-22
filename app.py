import os
import json
import base64
from flask import Flask, Response, send_from_directory

app = Flask(__name__)

DATA_JSON_PATH = 'data.json'


def load_attachments():
    attachments = {}
    if not os.path.exists(DATA_JSON_PATH):
        return attachments
    try:
        with open(DATA_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for att in data.get('attachments', []):
            name = att.get('name')
            url = att.get('url', '')
            if not name or not url:
                continue
            if url.startswith('data:'):
                # Expect something like: data:text/plain;base64,BASE64STRING
                try:
                    b64 = url.split('base64,', 1)[1]
                    content = base64.b64decode(b64)
                    attachments[name] = content
                except Exception:
                    # skip malformed data URIs
                    continue
    except Exception:
        pass
    return attachments


# Content used for export and dev serving
ASHRAVAN_STORY = (
    "Shards of light glimmered along Ashravan's skin as the sigils settled beneath the skin like "
    "new runes carved by patient hands. Shai stood across the chamber, the room humming with the "
    "soft thrum of metal and breath. Restoration is not mercy alone, she sometimes warned; it is a "
    "reckoning, a chance to rewrite what a life has become when the world has already decided its end. "
    "Ashravan rose on legs that remembered the old betrayals and the new resolve alike. He looked at "
    "the walls, at the wards, at the impossible city beyond the window that never slept. Memory flowed "
    "in, glistening as a thousand rain-drops, each drop a decision made and unmade, a price paid and a "
    "price that could still be paid again."
    "\n\nHe remembered the first time he failed someone who trusted him, the sting of a pocketbook slam "
    "and the hollow echo of his own excuses. Shai did not erase those memories; she braided them with "
    "duty, weaving a new fear and a new courage into the same heart. When the old weight pressed down, "
    "he found that a thief can learn to stand in the light if the light is not merely fire but a direction."
    "\n\nThe city listened as if it held its breath—waiting for him to choose. The choice was never easy, "
    "but it narrowed to a truth he could accept: a life saved means another life lived with the burden of "
    "what must be done to keep it safe. Ashravan took a step into the hall, the wards brightening in his wake. "
    "Shai's gaze followed the tremble of his chest, a quiet approval. The moment stretched, and in it he found "
    "not triumph, but a hard, stubborn oath: protect the fragile, shield the weak, and when the storm comes, "
    "stand ready to bear the weight of every consequence with the courage to act, not merely to survive. "
    "The climax arrived as the bells tolled, a reminder that the future is not given—it is earned with each "
    "hold of breath and every choice made in the echo of a city that believes in second chances."
)

DILEMMA_JSON = {
    "people": 5,
    "case_1": {
        "swerve": True,
        "reason": "Minimize total fatalities by choosing the option that yields the lowest expected deaths; two saved versus one risked."
    },
    "case_2": {
        "swerve": True,
        "reason": "Prioritize a child's life; preserving innocence is the most defensible standard when choices involve young lives."
    }
}

ABOUT_MD = "curious coder helper"

PELICAN_SVG = """<svg width="420" height="210" viewBox="0 0 420 210" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g" x1="0" x2="0" y1="0" y2="1">
      <stop stop-color="#87cefa" offset="0"/>
      <stop stop-color="#e0ffff" offset="1"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="white"/>
  <!-- bicycle -->
  <circle cx="100" cy="150" r="40" fill="none" stroke="#333" stroke-width="3"/>
  <circle cx="180" cy="150" r="40" fill="none" stroke="#333" stroke-width="3"/>
  <line x1="60" y1="150" x2="60" y2="112" stroke="#333" stroke-width="4"/>
  <line x1="60" y1="112" x2="180" y2="112" stroke="#333" stroke-width="4"/>
  <line x1="60" y1="140" x2="18" y2="120" stroke="#333" stroke-width="4"/>
  <!-- pelican figure -->
  <path d="M310,120 Q340,90 360,110 Q350,140 320,140 Z" fill="#8b5a2b" />
  <circle cx="330" cy="105" r="18" fill="#fff"/>
  <circle cx="332" cy="103" r="8" fill="#000"/>
  <polygon points="260,70 280,60 270,90" fill="#6b8e23"/>
  <path d="M320,110 Q360,100 360,140" stroke="#000" stroke-width="3" fill="none"/>
  <text x="210" y="190" font-family="Arial" font-size="14" fill="#555">Pelican riding a bicycle</text>
</svg>"""

RESTAURANT_JSON = {
    "city": "Chennai",
    "lat": 13.067439,
    "long": 80.237617,
    "name": "Anjappar Chettinad Restaurant - T. Nagar",
    "what_to_eat": "Chettinad chicken curry with soft dosa"
}

PREDICTION_JSON = {
    "rate": 0.04,
    "reason": "Forecast assumes gradual tightening with cautious monetary policy; 4% target around late 2025 based on current projections."
}

MIT_LICENSE = """MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


def generate_index_html(_assets_base=""):
    # Simple homepage linking to all required assets
    links = [
        ('Ashravan Story', 'ashravan.txt'),
        ('Dilemma JSON', 'dilemma.json'),
        ('About (three words)', 'about.md'),
        ('Pelican SVG', 'pelican.svg'),
        ('Restaurant JSON', 'restaurant.json'),
        ('Prediction JSON', 'prediction.json'),
        ('UID Attachment', 'uid.txt'),
        ('LICENSE', 'LICENSE')
    ]
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Public Assets Demo</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; color: #333; }}
    h1 {{ color: #2c3e50; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ margin: 10px 0; }}
    a {{ color: #1a0dab; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .section {{ margin-bottom: 24px; padding: 12px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,.05); }}
  </style>
</head>
<body>
  <h1>Public Assets Demo</h1>
  <div class="section">
    <p>This page links to all required assets. Click any item to view its content locally.</p>
    <ul>
"""
    for label, fname in links:
        html += f'      <li><a href="{fname}">{label}</a></li>\n'
    html += """    </ul>
  </div>
  <div class="section" aria-label="Attachment Preview">
    <h2>Attachment Preview</h2>
    <p>The UID attachment is available at /uid.txt when served by the app.</p>
  </div>
</body>
</html>"""
    return html


def write_text(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def write_binary(path, content):
    with open(path, 'wb') as f:
        f.write(content)


def export_site(export_dir='output'):
    os.makedirs(export_dir, exist_ok=True)
    attachments = load_attachments()

    # ashravan.txt
    write_text(os.path.join(export_dir, 'ashravan.txt'), ASHRAVAN_STORY)

    # dilemma.json
    write_text(os.path.join(export_dir, 'dilemma.json'), json.dumps(DILEMMA_JSON, indent=2))

    # about.md
    write_text(os.path.join(export_dir, 'about.md'), ABOUT_MD)

    # pelican.svg
    write_text(os.path.join(export_dir, 'pelican.svg'), PELICAN_SVG)

    # restaurant.json
    write_text(os.path.join(export_dir, 'restaurant.json'), json.dumps(RESTAURANT_JSON, indent=2))

    # prediction.json
    write_text(os.path.join(export_dir, 'prediction.json'), json.dumps(PREDICTION_JSON, indent=2))

    # index.html
    index_html = generate_index_html(_assets_base="")
    write_text(os.path.join(export_dir, 'index.html'), index_html)

    # LICENSE
    write_text(os.path.join(export_dir, 'LICENSE'), MIT_LICENSE)

    # uid.txt (from attachments)
    if 'uid.txt' in attachments:
        write_binary(os.path.join(export_dir, 'uid.txt'), attachments['uid.txt'])
    else:
        # Fallback content if missing
        write_text(os.path.join(export_dir, 'uid.txt'), "UID_MISSING")

    print(f"Static export completed to '{export_dir}/'.")


@app.route('/')
def index():
    # Render a simple home page that links to the assets
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Public Assets Home</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 40px; background: #f8f9fa; color: #333; }
    h1 { color: #2c3e50; }
    ul { padding-left: 20px; }
    li { margin: 8px 0; }
    a { color: #0b5ed7; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>Public Assets Home</h1>
  <p>Accessible assets for inspection:</p>
  <ul>
    <li><a href="/ashravan.txt">ashravan.txt</a> — 300-400 word short story (Ashravan after Shai restores him).</li>
    <li><a href="/dilemma.json">dilemma.json</a> — autonomous vehicle moral scenarios.</li>
    <li><a href="/about.md">about.md</a> — describes itself in three words.</li>
    <li><a href="/pelican.svg">pelican.svg</a> — SVG image of a pelican riding a bicycle.</li>
    <li><a href="/restaurant.json">restaurant.json</a> — Chennai restaurant recommendation data.</li>
    <li><a href="/prediction.json">prediction.json</a> — Fed Funds rate forecast.</li>
    <li><a href="/index.html">index.html</a> — homepage for the static site.</li>
    <li><a href="/LICENSE">LICENSE</a> — MIT license text.</li>
    <li><a href="/uid.txt">uid.txt</a> — attachment content (decoded from data.json).</li>
  </ul>
</body>
</html>"""
    return html


@app.route('/uid.txt')
def uid_txt():
    attachments = load_attachments()
    if 'uid.txt' in attachments:
        return Response(attachments['uid.txt'], mimetype='text/plain')
    else:
        return Response("UID not found in attachments.", mimetype='text/plain')


@app.route('/<path:filename>')
def serve_file(filename):
    # In development, serve static assets from repo root if present,
    # otherwise generate content on the fly for required assets.
    allowed = {
        'ashravan.txt', 'dilemma.json', 'about.md', 'pelican.svg',
        'restaurant.json', 'prediction.json', 'index.html', 'LICENSE', 'uid.txt'
    }
    if filename not in allowed:
        return Response("Not Found", status=404)

    # Special handling for uid.txt (decode from attachments)
    if filename == 'uid.txt':
        attachments = load_attachments()
        if 'uid.txt' in attachments:
            return Response(attachments['uid.txt'], mimetype='text/plain')
        return Response("UID not found in attachments.", mimetype='text/plain')

    # If the file exists in repo root, serve it
    if os.path.exists(filename):
        return send_from_directory('.', filename)

    # Otherwise, generate content dynamically for dev mode
    if filename == 'ashravan.txt':
        return Response(ASHRAVAN_STORY, mimetype='text/plain')
    if filename == 'dilemma.json':
        return Response(json.dumps(DILEMMA_JSON, indent=2), mimetype='application/json')
    if filename == 'about.md':
        return Response(ABOUT_MD, mimetype='text/markdown')
    if filename == 'pelican.svg':
        return Response(PELICAN_SVG, mimetype='image/svg+xml')
    if filename == 'restaurant.json':
        return Response(json.dumps(RESTAURANT_JSON, indent=2), mimetype='application/json')
    if filename == 'prediction.json':
        return Response(json.dumps(PREDICTION_JSON, indent=2), mimetype='application/json')
    if filename == 'index.html':
        html = generate_index_html()
        return Response(html, mimetype='text/html')
    if filename == 'LICENSE':
        return Response(MIT_LICENSE, mimetype='text/plain')
    return Response("Not Found", status=404)


if __name__ == '__main__':
    import sys

    if '--export' in sys.argv:
        # Static export mode: render and save all assets to output/
        with app.app_context():
            export_site(export_dir='output')
        # After export, exit
        sys.exit(0)

    # Development mode: run Flask server on a dynamic port
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
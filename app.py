import re
import os
from flask import Flask, request, jsonify, render_template_string
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InsightAI</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --bg: #080c12;
            --surface: #0f1621;
            --surface2: #162030;
            --gold: #c9a84c;
            --gold-light: #e8d5a3;
            --text: #d4e0ec;
            --text-muted: #6b7f96;
            --border: rgba(201,168,76,0.2);
        }
        .result-box li { margin: 0; padding: 2px 0; }
        .result-box ul, .result-box ol { margin: 8px 0; padding-left: 20px; }
        .result-box p { margin: 4px 0; }
        .result-box p:empty { display: none; }
.result-box br { display: none; }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
        }

        /* NAV */
        nav {
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 100;
            padding: 0 48px;
            height: 64px;
            background: rgba(8,12,18,0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .logo {
            font-family: 'Playfair Display', serif;
            font-size: 1.3rem;
            color: var(--gold);
            letter-spacing: 1px;
        }

        .nav-links {
            display: flex;
            gap: 8px;
        }

        .nav-links button {
            background: none;
            border: none;
            color: var(--text-muted);
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .nav-links button:hover, .nav-links button.active {
            color: var(--gold);
            background: rgba(201,168,76,0.08);
        }

        /* PAGES */
        .page { display: none; padding-top: 64px; min-height: 100vh; }
        .page.active { display: block; }

        /* HERO */
        .hero {
            padding: 100px 48px 80px;
            max-width: 900px;
            margin: 0 auto;
            text-align: center;
        }

        .hero-badge {
            display: inline-block;
            padding: 6px 16px;
            border: 1px solid var(--border);
            border-radius: 100px;
            font-size: 0.75rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 32px;
        }

        .hero h1 {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            line-height: 1.2;
            color: #fff;
            margin-bottom: 24px;
        }

        .hero h1 span { color: var(--gold); }

        .hero p {
            font-size: 1.1rem;
            color: var(--text-muted);
            line-height: 1.8;
            max-width: 600px;
            margin: 0 auto 48px;
        }

        .hero-cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 60px;
        }

        .hero-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 28px 24px;
            text-align: left;
            cursor: pointer;
            transition: all 0.3s;
        }

        .hero-card:hover {
            border-color: var(--gold);
            transform: translateY(-4px);
            background: var(--surface2);
        }

        .card-icon {
            font-size: 1.8rem;
            margin-bottom: 16px;
        }

        .hero-card h3 {
            font-size: 1rem;
            font-weight: 600;
            color: #fff;
            margin-bottom: 8px;
        }

        .hero-card p {
            font-size: 0.85rem;
            color: var(--text-muted);
            line-height: 1.6;
            margin: 0;
        }

        /* TOOL PAGES */
        .tool-page {
            max-width: 800px;
            margin: 0 auto;
            padding: 60px 48px;
        }

        .tool-header {
            margin-bottom: 40px;
        }

        .tool-header .back {
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 0.85rem;
            cursor: pointer;
            padding: 0;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: color 0.2s;
        }

        .tool-header .back:hover { color: var(--gold); }

        .tool-header h2 {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            color: #fff;
            margin-bottom: 8px;
        }

        .tool-header p {
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        textarea {
            width: 100%;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text);
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            line-height: 1.7;
            padding: 20px;
            resize: vertical;
            min-height: 180px;
            outline: none;
            transition: border-color 0.2s;
        }

        textarea::placeholder { color: var(--text-muted); }
        textarea:focus { border-color: var(--gold); }

        .analyze-btn {
            margin-top: 16px;
            padding: 14px 32px;
            background: var(--gold);
            color: #080c12;
            border: none;
            border-radius: 4px;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .analyze-btn:hover { background: var(--gold-light); }
        .analyze-btn:disabled { opacity: 0.5; cursor: not-allowed; }

        .result-box {
            margin-top: 32px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 28px;
            display: none;
            line-height: 1.8;
            font-size: 0.95rem;
            white-space: pre-wrap;
        }

        .result-box.visible { display: block; }

        .result-label {
            font-size: 0.75rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 16px;
        }

        .loading {
            display: none;
            align-items: center;
            gap: 12px;
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 20px;
            font-style: italic;
        }

        .loading.visible { display: flex; }

        .dot { animation: blink 1.2s infinite; }
        .dot:nth-child(2) { animation-delay: 0.2s; }
        .dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes blink { 0%,100%{opacity:0.2} 50%{opacity:1} }

        /* SENTIMENT SCORE */
        .sentiment-score {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
        }

        .score-circle {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            font-weight: 700;
            flex-shrink: 0;
        }

        .score-positive { background: rgba(34,197,94,0.15); color: #22c55e; border: 2px solid #22c55e44; }
        .score-negative { background: rgba(239,68,68,0.15); color: #ef4444; border: 2px solid #ef444444; }
        .score-neutral { background: rgba(201,168,76,0.15); color: var(--gold); border: 2px solid var(--border); }
    </style>
</head>
<body>

<nav>
    <div class="logo">InsightAI</div>
    <div class="nav-links">
        <button class="active" onclick="showPage('home')">Accueil</button>
        <button onclick="showPage('sentiment')">Sentiment</button>
        <button onclick="showPage('summary')">Résumé</button>
        <button onclick="showPage('persona')">Personas</button>
    </div>
</nav>

<!-- HOME -->
<div class="page active" id="page-home">
    <div class="hero">
        <div class="hero-badge">✦ Propulsé par l'IA</div>
        <h1>Transforme ton texte<br>en <span>intelligence</span></h1>
        <p>InsightAI analyse, résume et extrait les insights clés de n'importe quel contenu textuel en quelques secondes.</p>
        <div class="hero-cards">
            <div class="hero-card" onclick="showPage('sentiment')">
                <div class="card-icon">📊</div>
                <h3>Analyse de sentiment</h3>
                <p>Détecte le ton émotionnel et les insights business de n'importe quel texte.</p>
            </div>
            <div class="hero-card" onclick="showPage('summary')">
                <div class="card-icon">⚡</div>
                <h3>Résumeur intelligent</h3>
                <p>Condense articles, rapports et documents en points clés actionnables.</p>
            </div>
            <div class="hero-card" onclick="showPage('persona')">
                <div class="card-icon">👤</div>
                <h3>Générateur de personas</h3>
                <p>Crée des fiches personas détaillées à partir d'une description produit.</p>
            </div>
        </div>
    </div>
</div>

<!-- SENTIMENT -->
<div class="page" id="page-sentiment">
    <div class="tool-page">
        <div class="tool-header">
            <button class="back" onclick="showPage('home')">← Retour</button>
            <h2>Analyse de sentiment</h2>
            <p>Colle un avis client, un article ou n'importe quel texte pour analyser son ton et ses insights.</p>
        </div>
        <textarea id="sentiment-input" placeholder="Colle ton texte ici..."></textarea>
        <br>
        <button class="analyze-btn" onclick="analyzeSentiment()">Analyser →</button>
        <div class="loading" id="sentiment-loading">
            <span class="dot">●</span><span class="dot">●</span><span class="dot">●</span>
            <span>Analyse en cours...</span>
        </div>
        <div class="result-box" id="sentiment-result"></div>
    </div>
</div>

<!-- SUMMARY -->
<div class="page" id="page-summary">
    <div class="tool-page">
        <div class="tool-header">
            <button class="back" onclick="showPage('home')">← Retour</button>
            <h2>Résumeur intelligent</h2>
            <p>Colle un texte long pour obtenir un résumé structuré avec les points clés.</p>
        </div>
        <textarea id="summary-input" placeholder="Colle ton article, rapport ou document ici..."></textarea>
        <br>
        <button class="analyze-btn" onclick="summarize()">Résumer →</button>
        <div class="loading" id="summary-loading">
            <span class="dot">●</span><span class="dot">●</span><span class="dot">●</span>
            <span>Résumé en cours...</span>
        </div>
        <div class="result-box" id="summary-result"></div>
    </div>
</div>

<!-- PERSONA -->
<div class="page" id="page-persona">
    <div class="tool-page">
        <div class="tool-header">
            <button class="back" onclick="showPage('home')">← Retour</button>
            <h2>Générateur de personas</h2>
            <p>Décris ton produit ou ton entreprise pour générer des fiches personas clients détaillées.</p>
        </div>
        <textarea id="persona-input" placeholder="Ex: Application mobile de méditation pour cadres stressés, abonnement 15€/mois..."></textarea>
        <br>
        <button class="analyze-btn" onclick="generatePersona()">Générer →</button>
        <div class="loading" id="persona-loading">
            <span class="dot">●</span><span class="dot">●</span><span class="dot">●</span>
            <span>Génération des personas...</span>
        </div>
        <div class="result-box" id="persona-result"></div>
    </div>
</div>

<script>
function showPage(name) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-links button').forEach(b => b.classList.remove('active'));
    document.getElementById('page-' + name).classList.add('active');
    const idx = ['home','sentiment','summary','persona'].indexOf(name);
    document.querySelectorAll('.nav-links button')[idx].classList.add('active');
}

async function callAPI(endpoint, text, loadingId, resultId) {
    const loading = document.getElementById(loadingId);
    const result = document.getElementById(resultId);
    const btn = document.querySelector('#page-' + endpoint.split('/')[1] + ' .analyze-btn');

    loading.classList.add('visible');
    result.classList.remove('visible');
    if (btn) btn.disabled = true;

    const res = await fetch('/api/' + endpoint, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text})
    });
    const data = await res.json();

    loading.classList.remove('visible');
    result.innerHTML = data.result;
    result.classList.add('visible');
    if (btn) btn.disabled = false;
}

function analyzeSentiment() {
    const text = document.getElementById('sentiment-input').value.trim();
    if (!text) return;
    callAPI('sentiment', text, 'sentiment-loading', 'sentiment-result');
}

function summarize() {
    const text = document.getElementById('summary-input').value.trim();
    if (!text) return;
    callAPI('summary', text, 'summary-loading', 'summary-result');
}

function generatePersona() {
    const text = document.getElementById('persona-input').value.trim();
    if (!text) return;
    callAPI('persona', text, 'persona-loading', 'persona-result');
}
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/sentiment', methods=['POST'])
def sentiment():
    text = request.json.get('text', '')
    prompt = f"""Analyse le sentiment de ce texte de manière professionnelle.
Réponds en HTML avec cette structure exacte :
- Un titre h3 avec le sentiment global (Positif / Négatif / Neutre) et un emoji
- Un paragraphe "Tone général" 
- Une liste des émotions détectées
- Une section "Insights business" avec 2-3 points actionnables
- Un score de sentiment de 0 à 10
- Réponds UNIQUEMENT en HTML pur, sans balises markdown, sans ```html, sans aucun texte avant ou après le HTML
IMPORTANT: Ne mets aucun saut de ligne entre les balises HTML. Tout le HTML doit être sur une seule ligne compacte.

Texte à analyser: {text}"""
    
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
    clean = response.text.replace('```html', '').replace('```', '').strip()
    clean = clean.replace('<br>', '').replace('<br/>', '').replace('<br />', '')
    clean = re.sub(r'(<p>\s*</p>|<p>\s*<br\s*/?>\s*</p>)', '', clean)
    return jsonify({'result': clean})

@app.route('/api/summary', methods=['POST'])
def summary():
    text = request.json.get('text', '')
    prompt = f"""Résume ce texte de manière claire et structurée.
Réponds en HTML avec:
- Un titre h3 "Résumé"
- 2-3 phrases de résumé général
- Une section "Points clés" avec une liste de 4-6 bullet points
- Une section "À retenir" avec la takeaway principale en gras
- Réponds UNIQUEMENT en HTML pur, sans balises markdown, sans ```html, sans aucun texte avant ou après le HTML
IMPORTANT: Ne mets aucun saut de ligne entre les balises HTML. Tout le HTML doit être sur une seule ligne compacte.

Texte: {text}"""
    
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
    clean = response.text.replace('```html', '').replace('```', '').strip()
    clean = clean.replace('<br>', '').replace('<br/>', '').replace('<br />', '')
    clean = re.sub(r'(<p>\s*</p>|<p>\s*<br\s*/?>\s*</p>)', '', clean)
    return jsonify({'result': clean})

@app.route('/api/persona', methods=['POST'])
def persona():
    text = request.json.get('text', '')
    prompt = f"""Génère 2 personas clients détaillés pour ce produit/service.
Réponds en HTML avec pour chaque persona:
- Un titre h3 avec le nom et l'âge du persona
- Profession et situation
- Motivations principales (liste)
- Freins et objections (liste)  
- Canaux d'acquisition recommandés
- Citation typique entre guillemets et en italique
- Réponds UNIQUEMENT en HTML pur, sans balises markdown, sans ```html, sans aucun texte avant ou après le HTML
IMPORTANT: Ne mets aucun saut de ligne entre les balises HTML. Tout le HTML doit être sur une seule ligne compacte.

Produit/Service: {text}"""
    
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
    clean = response.text.replace('```html', '').replace('```', '').strip()
    clean = clean.replace('<br>', '').replace('<br/>', '').replace('<br />', '')
    clean = re.sub(r'(<p>\s*</p>|<p>\s*<br\s*/?>\s*</p>)', '', clean)
    return jsonify({'result': clean})

if __name__ == '__main__':
    app.run(debug=True)
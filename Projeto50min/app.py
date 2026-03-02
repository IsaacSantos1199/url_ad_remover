from flask import Flask, render_template, request
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
# urlparse = Separa a URL em partes
# urlencode = Transforma o dicionário de volta em string
# parse_qs = Transforma a string(?id=1&utm_source=abc) num dicionário
# urlunparse = junta todas as partes de volta numa URL completa
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    cleaned_url = None # Variável para guardar o resultado
    if request.method == "POST":
        original_url = request.form["original_url"] # Recebe o URL do formulário
        # Processamento do URL
        cleaned_url = clean_link(original_url)
    return render_template("index.html", cleaned_url=cleaned_url)

def clean_link(url):
    # Lista de parâmetros que queremos remover
    tracking_params = ["utm_source", "utm_medium", "utm_campaign", "fbclid", "gclid"]

    # Separa a URL em partes
    parsed = urlparse(url)

    # Pegar os parâmetros da query string
    query_dict = parse_qs(parsed.query)

    # Remover parâmetros de tracking
    for param in tracking_params:
        query_dict.pop(param, None) # Remove se existir e ignora se não existir

    # Recriar query string sem tracking
    cleaned_query = urlencode(query_dict, doseq=True)

    # Recriar URL completa
    cleaned_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        cleaned_query,
        parsed.fragment
    ))
    
    return cleaned_url

app.run(debug=True)
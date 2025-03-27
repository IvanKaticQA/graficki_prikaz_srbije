from flask import Flask, render_template
from priliv_turista import priliv_turista_bp
from izvoz_po_industriji import izvoz_po_industriji_bp
from bracni_status_po_godinama import bracni_status_bp
from uvoz_po_industriji import uvoz_po_industriji_bp
from stopa_nezaposlenosti import stopa_nezaposlenosti_bp
from stopa_zaposlenosti import stopa_zaposlenosti_bp
from prosecna_neto_zarada_po_industriji import prosecna_zarada_po_industriji_bp
from broj_zaposlenih_po_oblasti_delatnosti import broj_zaposlenih_po_oblasti_bp

app = Flask(__name__)

app.register_blueprint(priliv_turista_bp)
app.register_blueprint(izvoz_po_industriji_bp)
app.register_blueprint(uvoz_po_industriji_bp)
app.register_blueprint(bracni_status_bp)
app.register_blueprint(stopa_nezaposlenosti_bp)
app.register_blueprint(stopa_zaposlenosti_bp)
app.register_blueprint(prosecna_zarada_po_industriji_bp)
app.register_blueprint(broj_zaposlenih_po_oblasti_bp)

# Početna stranica
@app.route('/') 
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

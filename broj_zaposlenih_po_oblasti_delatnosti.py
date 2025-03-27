from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

broj_zaposlenih_po_oblasti_bp = Blueprint('broj_zaposlenih_po_oblasti', __name__)

CSV_URL = "https://data.gov.rs/sr/datasets/r/919c59c8-3f19-3f76-b6e0-ec8879636149"
df = pd.read_csv(CSV_URL, sep=";", on_bad_lines="skip", encoding="utf-8")
df = df[["nkd08", "god", "mes", "vrednost"]]  
df["god_mes"] = df["god"].astype(str) + '-' + df["mes"].astype(str).str.zfill(2)


#df.to_csv("broj_zaposlenih.csv", index=False, encoding="utf-8")

def create_chart(nkd08_value):
    filtered_df = df[df["nkd08"] == nkd08_value]
    
    if filtered_df.empty:
        return "<p class='text-red-500'>Nema podataka za izabrane filtere.</p>"
    filtered_df = filtered_df.sort_values(by="god_mes")
    fig = px.line(filtered_df, x="god_mes", y="vrednost", 
                  title=f"Broj zaposlenih po oblasti: {nkd08_value}", 
                  labels={"god_mes": "Godina-Kvartal", "vrednost": "Broj zaposlenih"})
    
    return pio.to_html(fig, full_html=False)

@broj_zaposlenih_po_oblasti_bp.route('/broj_zaposlenih_po_oblasti_delatnosti')
def broj_zaposlenih_po_oblasti():
    nkd08_values = df["nkd08"].unique()
    return render_template('broj_zaposlenih_po_oblasti_delatnosti.html', 
                           nkd08_values=nkd08_values)

@broj_zaposlenih_po_oblasti_bp.route('/get_chart_zaposleni', methods=['GET'])
def get_chart():
    nkd08_value = request.args.get('nkd08')
    chart_html = create_chart(nkd08_value)
    
    return jsonify(chart_html=chart_html)

from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

prosecna_zarada_po_industriji_bp = Blueprint('prosecna_zarada_po_industriji', __name__)

CSV_URL = "https://opendata.stat.gov.rs/data/WcfJsonRestService.Service1.svc/dataset/2403040102IND01/1/csv"
df = pd.read_csv(CSV_URL, sep=";", on_bad_lines="skip", encoding="utf-8")
df = df[["nkd08", "god", "mes", "vrednost"]]  
df["god_mes"] = df["god"].astype(str) + "-" + df["mes"].astype(str).str.zfill(2)  # Kombinacija god i mesec
#df.to_csv("prosecna_zarada.csv", index=False, encoding="utf-8")

def create_chart(nkd08_value):
    filtered_df = df[df["nkd08"] == nkd08_value]
    filtered_df.to_csv("test.csv", index=False, encoding="utf-8")
    if filtered_df.empty:
        return "<p class='text-red-500'>Nema podataka za izabrane filtere.</p>"
    
    filtered_df["god_mes"] = pd.to_datetime(filtered_df["god_mes"], format="%Y-%m")
    
    filtered_df = filtered_df.sort_values(by="god_mes")
    
    fig = px.line(filtered_df, x="god_mes", y="vrednost", 
                  title=f"Prosečna neto zarada po industriji: {nkd08_value}", 
                  labels={"god_mes": "Godina-Mesec", "vrednost": "Prosečna neto zarada"})
    
    return pio.to_html(fig, full_html=False)


@prosecna_zarada_po_industriji_bp.route('/prosecna_zarada_po_industriji')
def prosecna_zarada_po_industriji():
    nkd08_values = df["nkd08"].unique()
    return render_template('prosecna_zarada_po_industriji.html', 
                           nkd08_values=nkd08_values)

@prosecna_zarada_po_industriji_bp.route('/get_chart_zarada', methods=['GET'])
def get_chart():
    nkd08_value = request.args.get('nkd08')
    chart_html = create_chart(nkd08_value)
    
    return jsonify(chart_html=chart_html)

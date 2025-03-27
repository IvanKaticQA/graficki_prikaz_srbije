from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

uvoz_po_industriji_bp = Blueprint('uvoz_po_industriji', __name__)

CSV_URL = "https://opendata.stat.gov.rs/data/WcfJsonRestService.Service1.svc/dataset/1710IND02/1/csv"
df = pd.read_csv(CSV_URL, sep=";", on_bad_lines="skip", encoding="utf-8")
df = df[["nkd08", "god", "IDValuta", "vrednost"]]

def create_chart(nkd08_value, IDValuta_value):
    filtered_df = df[(df["nkd08"] == nkd08_value) & (df["IDValuta"] == IDValuta_value)]
    
    if filtered_df.empty:
        return "<p class='text-red-500'>Nema podataka za izabrane filtere.</p>"
    filtered_df["vrednost"] = filtered_df["vrednost"] * 1000
    
    fig = px.line(filtered_df, x="god", y="vrednost", 
                  title=f"uvoz za {nkd08_value} ({IDValuta_value})", 
                  labels={"god": "Godina", "vrednost": "Vrednost"})
    
    return pio.to_html(fig, full_html=False)

@uvoz_po_industriji_bp.route('/uvoz_po_industriji')
def uvoz_po_industriji():
    nkd08_values = df["nkd08"].unique()
    IDValuta_values = df["IDValuta"].unique()
    
    return render_template('uvoz_po_industriji.html', 
                           nkd08_values=nkd08_values, 
                           IDValuta_values=IDValuta_values)

@uvoz_po_industriji_bp.route('/get_chart_uvoz', methods=['GET'])
def get_chart():
    nkd08_value = request.args.get('nkd08')
    IDValuta_value = request.args.get('IDValuta')
    
    chart_html = create_chart(nkd08_value, IDValuta_value)
    
    return jsonify(chart_html=chart_html)

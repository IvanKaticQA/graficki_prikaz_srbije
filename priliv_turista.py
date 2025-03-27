from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

priliv_turista_bp = Blueprint('priliv_turista', __name__)

CSV_URL = "https://opendata.stat.gov.rs/data/WcfJsonRestService.Service1.svc/dataset/220206IND01/1/csv"
df = pd.read_csv(CSV_URL, sep=';', on_bad_lines='skip')
df = df[["nDrzave", "god","vrednost","nJedinicaMere"]]

def create_chart(nDrzave_value):
    filtered_df = df[df["nDrzave"] == nDrzave_value]
    
    if filtered_df.empty:
        return "<p class='text-red-500'>Nema podataka za izabranu državu.</p>"
    
    fig = px.line(filtered_df, x="god", y="vrednost", 
                  title=f"Priliv turista iz {nDrzave_value}", 
                  labels={"god": "Godina", "vrednost": "Broj turista"})
    
    return pio.to_html(fig, full_html=False)

@priliv_turista_bp.route('/priliv_turista')
def priliv_turista():
    nDrzave_values = df["nDrzave"].unique()
    return render_template('priliv_turista.html', nDrzave_values=nDrzave_values)

@priliv_turista_bp.route('/get_chart', methods=['GET'])
def get_chart():
    nDrzave_value = request.args.get('nDrzave')
    chart_html = create_chart(nDrzave_value)
    return jsonify(chart_html=chart_html)

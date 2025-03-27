from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

stopa_nezaposlenosti_bp = Blueprint('stopa_nezaposlenosti', __name__)

CSV_URL = "https://opendata.stat.gov.rs/data/WcfJsonRestService.Service1.svc/dataset/240003010102IND03/1/csv"
df = pd.read_csv(CSV_URL, sep=';', on_bad_lines='skip')
df = df[["god", "mes", "vrednost", "nStarGrupa", "nPol"]]

df["god_mes"] = df["god"].astype(str) + '-' + df["mes"].astype(str).str.zfill(2)

def create_chart(nStarGrupa_value, nPol_value):
    filtered_df = df[(df["nStarGrupa"] == nStarGrupa_value) & (df["nPol"] == nPol_value)]
    if filtered_df.empty:
        return "<p class='text-red-500'>Nema podataka za izabranu grupu i pol.</p>"
    
    filtered_df = filtered_df.sort_values(by="god_mes")

    fig = px.line(filtered_df, x="god_mes", y="vrednost", 
                  title=f"Stopa nezaposlenosti ({nStarGrupa_value}, {nPol_value})", 
                  labels={"god_mes": "Godina-Kvartal", "vrednost": "Stopa nezaposlenosti (%)"})
    
    return pio.to_html(fig, full_html=False)


@stopa_nezaposlenosti_bp.route('/stopa_nezaposlenosti')
def stopa_nezaposlenosti():
    nStarGrupa_values = df["nStarGrupa"].unique()
    nPol_values = df["nPol"].unique()
    return render_template('stopa_nezaposlenosti.html', nStarGrupa_values=nStarGrupa_values, nPol_values=nPol_values)

@stopa_nezaposlenosti_bp.route('/get_chart_nezaposlenost', methods=['GET'])
def get_chart():
    nStarGrupa_value = request.args.get('nStarGrupa')
    nPol_value = request.args.get('nPol')
    chart_html = create_chart(nStarGrupa_value, nPol_value)
    return jsonify(chart_html=chart_html)

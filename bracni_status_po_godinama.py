from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

bracni_status_bp = Blueprint('bracni_status', __name__)

CSV_URL = "https://opendata.stat.gov.rs/data/WcfJsonRestService.Service1.svc/dataset/3104020503IND01/1/csv"
df = pd.read_csv(CSV_URL, sep=';', on_bad_lines='skip')
df = df[["nTer", "nBracStatus", "god", "vrednost", "nGodRodj"]]
def create_chart(nTer_value, nBracStatus_value):
    filtered_df = df[(df["nTer"] == nTer_value) & (df["nBracStatus"] == nBracStatus_value)]

    
    if filtered_df.empty:
        return "<p class='text-red-500'>Nema podataka za izabrane filtere.</p>"
    
    fig = px.line(filtered_df, x="nGodRodj", y="vrednost", 
                  title=f"Bracni status {nBracStatus_value} za {nTer_value}", 
                  labels={"nGodRodj": "Godina", "vrednost": "Vrednost"})
    
    return pio.to_html(fig, full_html=False)

@bracni_status_bp.route('/bracni_status')
def bracni_status():
    nTer_values = df["nTer"].unique()
    nBracStatus_values = df["nBracStatus"].unique()
    return render_template('bracni_status.html', nTer_values=nTer_values, nBracStatus_values=nBracStatus_values)

@bracni_status_bp.route('/get_chart_brac_status', methods=['GET'])
def get_chart():
    nTer_value = request.args.get('nTer')
    nBracStatus_value = request.args.get('nBracStatus')
    chart_html = create_chart(nTer_value, nBracStatus_value)
    return jsonify(chart_html=chart_html)

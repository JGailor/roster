from flask import Flask, render_template, jsonify
from w40k.battlescribe.schema import BattlescribeCatSchema

app = Flask(__name__, static_folder="react-app/build/static", template_folder="react-app/build")

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/api/battlescribe/w40k_8th/schema.json")
def api_battlescribe_w40k_8th_schema():
    schema = BattlescribeCatSchema.parse("./sample_data/chaos_death_guard.cat")
    return jsonify(schema.jsonable())

print('Starting the w40k server...')
app.debug=True
app.run(host='0.0.0.0')
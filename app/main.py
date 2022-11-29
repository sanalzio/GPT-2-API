from flask import Flask,render_template,jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>This Is A GPT-2 API!</p>"
@app.route("/<string:content>")
def api(content):
    import json
    import requests
    API_TOKEN = "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"
    def query(payload='',parameters=None,options={'use_cache': False}):
        API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        body = {"inputs":payload,'parameters':parameters,'options':options}
        response = requests.request("POST", API_URL, headers=headers, data= json.dumps(body))
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return "Error:"+" ".join(response.json()['error'])
        else:
            return response.json()[0]['generated_text']
    parameters = {
        'max_new_tokens': 100,  # number of generated tokens
        'temperature': 0.5,   # controlling the randomness of generations
        'end_sequence': "###" # stopping sequence for generation
    }
    data = query(content, parameters)
    return jsonify({"content":data.replace("###", "")})#render_template("api.html", content = data.replace("###", ""))#data.replace("###", "")

#app.run(debug=True)

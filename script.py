from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        model = request.form['model']
        
        url = "http://localhost:11434/api/chat"
        
        payload = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "stream": False,
            "keep_alive": -1
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            try:
                returned_json = response.json()
                message = returned_json.get("message", {})
                content = message.get("content", "")
                print(content)
                return render_template('index.html', content=content)
            except json.JSONDecodeError as e:
                return "Error decoding JSON response: " + str(e)
        else:
            return "Error: " + str(response.status_code) + " " + response.text

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

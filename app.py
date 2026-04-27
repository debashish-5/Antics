from flask import Flask, render_template, request, jsonify,json
import os
from tool import agent

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template("analytics.html")

@app.route('/chat',methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    try:
        response = agent.run(message)
        return jsonify({'response':response})
    except Exception as e:
        return jsonify({"response": f"Sorry, I ran into an error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True,port=2007)    
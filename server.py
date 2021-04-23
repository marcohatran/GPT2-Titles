from transformers import pipeline
import torch
from flask import Flask, request, Response, jsonify
from flask import Flask, render_template, request, Response, send_file, jsonify

from torch.nn import functional as F
from queue import Queue, Empty
import time
import threading

# Server & Handling Setting
app = Flask(__name__)

requests_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1

device = 0 if torch.cuda.is_available() else -1
pipe = pipeline('text-generation', model="QianWeiTech/GPT2-Titles",
                 tokenizer="QianWeiTech/GPT2-Titles"
                 ,device=device)

def handle_requests_by_batch():
    while True:
        requests_batch = []
        while not (len(requests_batch) >= BATCH_SIZE):
            try:
                requests_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in requests_batch:
                requests['output'] = run_model(requests['input'][0])


threading.Thread(target=handle_requests_by_batch).start()

def run_model(prompt, num=1, length=30):
    try:
        generated_texts = pipe(prompt, pad_token_id=50256,do_sample=True, early_stopping=True, top_k=50, top_p=.9, min_length=10,max_length=100)[0]["generated_text"]
        return generated_texts

    except Exception as e:
        print(e)
        return 500

@app.route("/generate", methods=['GET'])
def generate():

    if requests_queue.qsize() > BATCH_SIZE:
        return jsonify({'error': 'Too Many Requests'}), 429

    try:
        args = []
        review=request.args.get('query')
        args.append(review)

    except Exception:
        print("Empty Text")
        return jsonify({'error': 'Fail'}), 400

    req = {
        'input': args
    }
    requests_queue.put(req)

    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)
    try:
      
      title = {'title ': req['output'].split("title")[-1]}

    except Exception:
        print("Empty Text")
        return jsonify({'error': 'Fail'}), 400    
    
    return jsonify(title)
  



# Health Check

@app.route('/healthz')
def health():
    return "ok", 200

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=80)

from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

DATA_FILE = 'tasks.json'

# --- Helper functions ---
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())

@app.route('/tasks', methods=['POST'])
def add_task():
    tasks = load_tasks()
    data = request.get_json()
    new_task = {"id": len(tasks) + 1, "text": data['text']}
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['text'] = request.get_json()['text']
            save_tasks(tasks)
            return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)

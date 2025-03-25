from flask import Flask, request, render_template, redirect, url_for
import csv
import os
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def assign_group(name, num_groups=2):
    return f"Group {chr(65 + (sum(ord(c) for c in name) % num_groups))}"  # A, B, C...

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".csv"):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)

            names = []

            with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    name = row.get("name") or row.get("Name")
                    if not name:
                        continue
                    names.append(name.strip())
                    
            random.shuffle(names)

            groups = {}
            for idx in range(0, len(names), 2):
                group_number = idx // 2 + 1
                group_name = f"Group {group_number}"
                groups[group_name] = names[idx:idx+2]

            return render_template("results.html", groups=groups)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

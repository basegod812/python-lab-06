"""Средние задания 2 и 4: Flask-приветствие и таблица данных."""
from flask import Flask, render_template_string, request

app = Flask(__name__)
STUDENTS = [
    {"name": "Анна", "group": "221141", "score": 5},
    {"name": "Иван", "group": "221141", "score": 4},
    {"name": "Герман", "group": "221141", "score": 5},
]

HTML = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><title>ЛР6 Flask</title>
<style>body{font-family:Arial;max-width:800px;margin:40px auto;line-height:1.6}
table{border-collapse:collapse;width:100%}td,th{padding:10px;border:1px solid #bbb}
input,button{padding:10px}</style></head>
<body><h1>ЛР №6: Flask</h1>
<form method="post"><input name="name" placeholder="Как вас зовут?" required>
<button type="submit">Приветствовать</button></form>
{% if name %}<h2>Привет, {{ name }}!</h2>{% endif %}
<h2>Таблица студентов</h2><table><thead>
<tr><th>Имя</th><th>Группа</th><th>Оценка</th></tr></thead><tbody>
{% for student in students %}<tr><td>{{ student.name }}</td>
<td>{{ student.group }}</td><td>{{ student.score }}</td></tr>
{% endfor %}</tbody></table></body></html>"""


@app.route("/", methods=["GET", "POST"])
def index():
    name = request.form.get("name", "").strip() if request.method == "POST" else ""
    return render_template_string(HTML, name=name, students=STUDENTS)


if __name__ == "__main__":
    app.run(port=5000)

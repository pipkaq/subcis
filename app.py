from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Порядок тиров
tier_order = ["HT1", "LT1", "HT2", "LT2", "HT3", "LT3", "HT4", "LT4", "HT5", "LT5"]

def get_kit_data(kit_name):
    conn = sqlite3.connect('ranks_log.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Получаем ник и тир из базы
    cursor.execute("""
        SELECT nickname, rank
        FROM rank_log
        WHERE tierlist = ?
    """, (kit_name,))
    rows = cursor.fetchall()
    conn.close()

    # Разбиваем по тир-листу
    tiers = {tier: [] for tier in tier_order}
    for row in rows:
        rank = row['rank']
        if rank in tiers:
            tiers[rank].append({
                'nickname': row['nickname'],
                'rank': rank
            })

    return tiers

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/kits/<kit_name>')
def api_kit(kit_name):
    data = get_kit_data(kit_name)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

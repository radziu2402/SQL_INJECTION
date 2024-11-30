import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Funkcja do łączenia się z bazą danych
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


def load_sql_script(db_name, sql_file):
    # Połącz się z bazą danych
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print("Opened database successfully")
    # Otwórz plik SQL i przeczytaj jego zawartość
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # Wykonaj skrypt SQL
    try:
        cursor.executescript(sql_script)
        conn.commit()  # Zatwierdź zmiany
        print(f"Skrypt SQL z pliku {sql_file} został pomyślnie załadowany do bazy {db_name}.")
    except sqlite3.Error as e:
        print(f"Błąd podczas ładowania skryptu SQL: {e}")
    finally:
        # Zamknij połączenie
        conn.close()


# Załaduj skrypt SQL przed uruchomieniem aplikacji
load_sql_script('users.db', 'db_poczatkowe.sql')


# Strona główna z formularzem logowania (Niezabezpieczona wersja)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Niezabezpieczona wersja (SQL Injection)
        conn = get_db_connection()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            return f"Zalogowano jako {user['username']}"
        else:
            return "Błąd logowania"

    return render_template('insecure.html')


# Zabezpieczona wersja logowania (właściwa)
@app.route('/secure', methods=['GET', 'POST'])
def secure():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Zabezpieczona wersja (bezpieczne zapytanie)
        conn = get_db_connection()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        user = conn.execute(query, (username, password)).fetchone()
        conn.close()

        if user:
            return f"Zalogowano jako {user['username']}"
        else:
            return "Błąd logowania"

    return render_template('secure.html')


if __name__ == '__main__':
    app.run(debug=True)

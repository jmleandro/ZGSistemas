from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_username = 'root'
db_password = 'senha1'
db_name = 'zgsistemas'

# Conectar ao banco de dados MySQL
db = mysql.connector.connect(
    host='127.0.0.1',
    port=3307,
    user=db_username,
    password=db_password,
    database=db_name
)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # Login bem-sucedido
        return redirect(url_for('dashboard'))  # Redireciona para a página de dashboard após o login
    else:
        # Login falhou
        return "Credenciais inválidas. Tente novamente."

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Página de dashboard após o login bem-sucedido
    return "Você está logado! Esta é a página de dashboard."

# cadastro
@app.route('/cadastrar', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrousu', methods=['POST'])
def cadastro_usuario():
    email = request.form['email']
    password = request.form['password']
    
    cursor = db.cursor()
    verifica_email ='Select email from users where email = %s'
    cursor.execute(verifica_email, (email,))
    var = cursor.fetchone()
    if var != "None":
        return "Email ja cadastrado"
    print(var)
    query = 'INSERT INTO users (password, email) VALUES (%s, %s)'
    cursor.execute(query, (password, email))
    db.commit()
    cursor.close()

    return "Usuario cadastrado com sucesso"
    
if __name__ == '__main__':
    app.run(debug=True)

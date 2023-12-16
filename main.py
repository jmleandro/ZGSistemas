from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_username = 'root'
db_password = 'senha1'
db_name = 'zgsistemas'

db = mysql.connector.connect(
    host='192.168.28.11',
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
    if email == '' or password == '':
        return render_template('index.html', output="Email ou Senha em branco")
    
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
    return "Você está logado! Esta é a página de dashboard."

# cadastro
@app.route('/cadastrar', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrousu', methods=['POST'])
def cadastro_usuario():
    email = request.form['email']
    password = request.form['password']
    if email == '' or password == '':
        return render_template('cadastro.html', output="Email ou Senha em branco")
    
    cursor = db.cursor()
    verifica_email ='Select email from users where email = %s'
    cursor.execute(verifica_email, (email,))
    var = cursor.fetchone()

    if var != None:
        return render_template('cadastro.html', output="Ja tem cadastrado")
    
    print(var)
    query = 'INSERT INTO users (password, email) VALUES (%s, %s)'
    cursor.execute(query, (password, email))
    db.commit()
    cursor.close()

    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)

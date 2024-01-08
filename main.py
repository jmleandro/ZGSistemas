from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import bcrypt

app = Flask(__name__)

db_username = "root"
db_password = "senha1"
db_name = "zgsistemas"
db_port = 3307

db = mysql.connector.connect(
    host="192.168.28.21",
    port=3307,
    user=db_username,
    password=db_password,
    database=db_name,
    autocommit=True,
    connection_timeout=10
)

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    if email == '' or password == '':
        return render_template("index.html", output="Email ou Senha em branco")
    
    cursor = db.cursor()
    busca_credenciais = "SELECT password FROM users WHERE email = %s"
    cursor.execute(busca_credenciais, (email,))
    usuario = cursor.fetchone()
    cursor.close()
    
    if usuario != None:
        hashed_password = usuario[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):        
            return redirect(url_for("dashboard"))
        else:
            return "Credenciais inválidas. Tente novamente."
    else:
        return "Credenciais inválidas. Tente novamente."
    

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return "Você está logado! Esta é a página de dashboard."

# cadastro
@app.route("/cadastrar", methods=["GET"])
def cadastro():
    return render_template("cadastro.html")

@app.route("/cadastrausuario", methods=["POST"])
def cadastro_usuario():
    email = request.form["email"]
    password = request.form["password"]
    if email == '' or password == '':
        return render_template("cadastro.html", output="Email ou Senha em branco")
    
    senha_criptografada = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor = db.cursor()
    busca_email ="Select email from users where email = %s"
    cursor.execute(busca_email, (email,))
    email_usuario = cursor.fetchone()

    if email_usuario != None:
        return render_template("cadastro.html", output="Email já cadastrado !")
    else:
        insere_usuario = "INSERT INTO users (password, email) VALUES (%s, %s)"
        cursor.execute(insere_usuario, (senha_criptografada, email))
        cursor.close()

    return redirect(url_for("index"))
    
if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host="0.0.0.0")

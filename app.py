# https://maxcnunes.com/post/2012/12/24/desenvolvendo-pequena-aplicacao-web-python-flask/

# Created by:  Alexsandro Monteiro
# Date:        19/02/2019
# Site for Tests Python / Flask

# Python any Where
# https://www.pythonanywhere.com/user/AlexsandroMO/
# pip install flask

from flask import Flask, render_template, url_for, request, redirect, send_file, send_from_directory
import db as db_ncr
import os
import lxml
import json
import requests
import calc_coin as coins
from datetime import date, datetime
from tinydb import TinyDB, Query, where
import random


# ==================================
app = Flask(__name__)

class Var_State():
    def __init__(self, login_acess):
        self.login_acess = login_acess


Var_State.login_acess = False


@app.route("/")
@app.route("/home")
def home():
    status = Var_State.login_acess
    title_status = 'Python | Flask'
    return render_template('home.html', status=status, title_status=title_status)

#-------------------------------- NCR_CC -------------------------------
@app.route("/home_ncr")
def home_ncr():
    status = Var_State.login_acess
    print('Status---------', status)
    title_status = 'Home | NCR'
    return render_template('ncr/home-ncr.html', status=status, title_status=title_status)

@app.route("/create")
def create():
    return render_template('ncr/create.html')

@app.route("/userarea_loged")
def userarea_loged():
    status = Var_State.login_acess
    title_status = 'Home | NCR'
    return render_template('ncr/userarea_loged.html', status=status, title_status=title_status)

@app.route("/fileform")
def fileform():
    status = Var_State.login_acess
    title_status = 'Upload | NCR'
    return render_template('ncr/fileform.html', status=status, title_status=title_status)


@app.route("/login")
def login():
    title_status = 'Login | NCR'
    return render_template('ncr/login.html', title_status=title_status)

@app.route("/create_table")
def create_table():
    status = Var_State.login_acess
    pasta = './static'
    status_files, status_files1, status_files2 = [],[],[]
    for diretorio in os.walk(pasta):
        for arquivo in diretorio[2]:
            print('-----',arquivo)
            if arquivo == 'INT_DELNT_CRTL_META_REV.xlsx':
                status_files1.append('-')
            elif arquivo == 'rai.xlsx':
                status_files2.append('-')

    if len(status_files1) != 1:
        status_files.append('INT_DELNT_CRTL_META_REV.xlsx')

    if len(status_files2) != 1:
        status_files.append('rai.xlsx')

    status_files_len = len(status_files)
    if status_files_len > 0:
        return render_template('ncr/message-erro-file.html', status_files=status_files, status_files_len=status_files_len, status=status)

    else:
        df = db_ncr.create_list()
        return render_template('ncr/upload.html', msg_df=df[1], status=status, df=df[0], tables=[df[0].to_html(classes='data')], titles=df[0].columns.values)

@app.route("/logout")
def logout():
    Var_State.login_acess = False
    return render_template('ncr/home-ncr.html')

@app.route("/download")
def download():
    status = Var_State.login_acess
    return redirect(url_for('static', filename='NCR_RAI_LIBERAR.xlsx'))

@app.route('/userarea', methods=['POST', 'GET'])
def userarea():

    title_status = 'Home | NCR'

    if request.method == 'POST':
        resultuserarea = request.form
        email = resultuserarea['email']
        password = resultuserarea['password']

        read_register = db_ncr.readDB(email, password)

        if email == '' or password == '':
            return f"""
            <h2>Atenção, Todos os campos precisam ser preenchidos... :( </h2><br><br><br>
            <p><a href="/login"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

            """
        if read_register[0] == True:
            Var_State.login_acess = True

            status = Var_State.login_acess

            if status == True:
                return render_template("ncr/userarea.html", title_status=title_status, title='Python_Flask', status=status,
                                       name_user=read_register[1].lower().capitalize())

            else:
                return render_template("ncr/login.html", title_status=title_status, email=email)

        else:
            return render_template("ncr/message.html", title_status=title_status, email=email)

@app.route('/delite_arq')
def delite_arq():

    pasta = './static'
    for diretorio in os.walk(pasta):
        for arquivo in diretorio[2]:
            if arquivo == 'INT_DELNT_CRTL_META_REV.xlsx':
                os.remove('static/INT_DELNT_CRTL_META_REV.xlsx')
            elif arquivo == 'rai.xlsx':
                os.remove("static/rai.xlsx")
            elif arquivo == 'NCR_RAI_LIBERAR':
                os.remove("NCR_RAI_LIBERAR.xlsx")
                
    return render_template('ncr/home-ncr.html') 


@app.route('/register')
def register():
    status = Var_State.login_acess
    return render_template('ncr/register.html', status=status)


@app.route('/erro')
def erro():
    return render_template('ncr/erro.html')


@app.route('/dbname', methods=['POST', 'GET'])
def dbname():
    if request.method == 'POST':
        resultdbname = request.form
        firstname = resultdbname['firstname']
        lastname = resultdbname['lastname']
        email1 = resultdbname['email1']
        email2 = resultdbname['email2']
        password1 = resultdbname['password1']
        password2 = resultdbname['password2']

        if firstname and lastname and email1 and email2 and password1 and password2 != '':
            if email1 != email2:
                return f"""
          <h2>Atenção! Senhas não São Identicas... :( </h2><br><br><br>
          <p><a href="/register"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

          """
            if password1 != password2:
                return f"""
          <h2>Atenção! Senhas não São Identicas... :( </h2><br><br><br>
          <p><a href="/register"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

          """
            else:
                db_ncr.registerDB(firstname.upper(), lastname.upper(), email1.upper(), password1)
                return render_template('ncr/dbname.html', firstname=firstname)
        else:
            return f"""
          <h2>Atenção, Todos os campos precisam ser preenchidos... :( </h2><br><br><br>
          <p><a href="/register"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

          """

@app.route('/handleUpload', methods=['POST'])
def handleFileUpload():
    if 'photo' in request.files:
        photo = request.files['photo']
        print('---------', photo)
        if photo.filename != '':
            print('foi')
            photo.save(os.path.join('static/', photo.filename))
    return redirect(url_for('userarea_loged'))

#------------------------------------------------------------------
#APPs
#------------------------------------------------------------------

@app.route("/index_coin")
def index_coin():

    title_status= 'COINS'

    lista = requests.get('https://economia.awesomeapi.com.br/all')
    cotation = json.loads(lista.text)

    df = coins.cotation_all(cotation)
    now = date.today()
    list_today = coins.today_is(now)

    hj = now

    day_week = list_today[0]
    day =  list_today[1]
    year =  list_today[2]
    month = list_today[3]

    Ass = 'A.M.O COTACÕES'

    coins.dollar_last_days(df)

    data_table = []
    for a in range(len(df['VALOR'])):
        data_table.append([df['MOEDA'].loc[a], df['VALOR'].loc[a], df['DATA_COTA'].loc[a]])

    #-------------------------------
    lista_dolar = coins.read_dollar_grafic()[0]
    lista_data = coins.read_dollar_grafic()[1]

    new_data = []
    for i in range(len(lista_dolar)):
        new_data.append([lista_data[i],lista_dolar[i]])

    data_ajust = []
    if len(new_data) >= 5:
        data_ajust = new_data[(len(new_data)-5):len(new_data)]

    #-------------------------------


    return render_template('coin/index-coin.html', new_data=data_ajust, title_status=title_status, day_week=day_week, day=day, month=month, year=year, hj=hj, Ass=Ass, data_table=data_table, tables=[df.to_html(classes='data')], titles=df.columns.values)



@app.route("/atualyze_table")
def atualyze_table():

    title_status= 'COINS'

    lista = requests.get('https://economia.awesomeapi.com.br/all')
    cotation = json.loads(lista.text)

    df = coins.cotation_all(cotation)
    now = date.today()
    list_today = coins.today_is(now)

    hj = now

    day_week = list_today[0]
    day =  list_today[1]
    year =  list_today[2]
    month = list_today[3]

    Ass = 'A.M.O COTACÕES'

    coins.dollar_last_days(df)


    data_table = []
    for a in range(len(df['VALOR'])):
        data_table.append([df['MOEDA'].loc[a], df['VALOR'].loc[a], df['DATA_COTA'].loc[a]])

    #-------------------------------
    lista_dolar = coins.read_dollar_grafic()[0]
    lista_data = coins.read_dollar_grafic()[1]

    new_data, new_ = [],[]
    for i in range(len(lista_dolar)):
        new_data.append([lista_data[i],lista_dolar[i]])
        new_.append([lista_data[i],lista_dolar[i]])

    data_ajust = []
    if len(new_data) >= 5:
        data_ajust = new_data[(len(new_data)-5):len(new_data)]

    #-------------------------------
    return render_template('coin/index-coin.html', new_=new_, new_data=data_ajust, title_status=title_status, day_week=day_week, day=day, month=month, year=year, hj=hj, Ass=Ass, data_table=data_table, tables=[df.to_html(classes='data')], titles=df.columns.values)


    #-------------------------------
    #xx = coins.dollar_last_days(df)


    


#---------------------------------------------------------------------------------
#-----------------------------
db_i = TinyDB('DB_JSON/dbi.json')
db_G = TinyDB('DB_JSON/dbg.json')
#Ft = Query()

l_db = TinyDB('DB_JSON/dbi.json')
g_db = TinyDB('DB_JSON/dbg.json')
#-----------------------------

@app.route("/index_game")
def index_game():
    title_status = 'HangmanGame'
    return render_template('game/index-game.html', title_status=title_status)


@app.route('/game_choise', methods = ['POST', 'GET'])
def game_choise():

    title_status = 'HangmanGame'

    if request.method == 'POST':
        result = request.form
        var_in = result['select']

    print('>>>>>>>>>>>>>',var_in)

    if var_in == '2':
        l_db.update({'life': 0})
        return render_template('game/game-choise.html', title_status=title_status)
    elif var_in == '1' or var_in == '0':
        l_db.update({'life': 0})
        return render_template('game/index-game.html', title_status=title_status)

    else:
        return redirect(url_for('index_game'))


@app.route('/result_game', methods = ['POST', 'GET'])
def result_game():

    title_status = 'HangmanGame'

    if request.method == 'POST':
        result = request.form
        var_word = result['word'].upper()
        var_dip = result['var-dip'].upper()

        l_db.update({'life': 5})
        l_db.update({'word': var_word})

        len_var_word = len(var_word)
        lines = '_ ' * len(var_word)
        word = lines.split()
        return render_template('game/result-game.html', title_status=title_status, word=word, var_dip=var_dip, len_var_word=len_var_word)


@app.route('/result_game_play', methods = ['POST', 'GET'])
def result_game_play():

    title_status = 'HangmanGame'

    if request.method == 'POST':
        result = request.form
        read_letter = result['letter'].upper()
        read_word = result['read-word']
        var_dip = result['var-dip'].upper()
        var_secret = result['var-secret']

        level = l_db.all()[0]['life']
        var_word = l_db.all()[0]['word']

        #---------------------------------
        read_word = read_word.replace('[','')
        read_word = read_word.replace(']','')
        read_word = read_word.replace("',",'')
        read_word = read_word.replace("'",'')
        read_word = read_word.split(' ')

        len_var_word = len(var_word)
        dados = []
        for a in range(0, len(var_word)):
            if var_word[a] == read_letter:
                read_word[a] = read_letter

            else:
                dados.append('empyt')

            if len(dados) == len(var_word):
                l_db.update({'life': level -1})

        test_read_word = []
        for i in read_word:
            if i == '_':
                test_read_word.append('_')

        if len(test_read_word) == 0:
            return render_template('game/win.html', title_status=title_status)

        elif level > 0:
            return render_template('game/result-game-.html', title_status=title_status, read_word=read_word, var_dip=var_dip, len_var_word=len_var_word, var_secret=var_secret, level=level)
        else:
            return render_template('game/loose.html', title_status=title_status, var_word=var_word)


@app.route("/win")
def win():

    title_status = 'HangmanGame'

    return render_template('game/win.html', title_status=title_status)


@app.route("/loose")
def loose():

    title_status = 'HangmanGame'

    return render_template('game/loose.html', title_status=title_status)



if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8000, debug=True)
    app.run(debug=True)

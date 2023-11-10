import os, secrets
from flask_login import login_required, logout_user, login_user, current_user
from flask import abort, session 
from app import app, db_1, db_2
from app.model import Compani, User
from flask import render_template, send_from_directory, request, flash, url_for, redirect, jsonify
from PIL import Image
from app.form import Sign_in, Sign_up, Create_Compani, Edit_Compani, Upload, Settings
from sqlalchemy.exc import IntegrityError
import mysql.connector
import json
import requests
from datetime import datetime, timedelta
import socket
ip_addres = socket.gethostbyname(socket.gethostname())

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sign_in'))

@app.route('/sign_in/', methods=('GET', 'POST'))
def sign_in():
    form = Sign_in()
    if form.validate_on_submit():
        user = db_1.session.query(User).filter(User.user_name == form.user.data).first()
        if user and user.password == form.password.data:
            session['id'] = user.id
            login_user(user, remember=form.remember.data)
            return redirect(url_for('about'))

    return render_template('sign_in.html', form=form)

@app.route('/sign_up/', methods=['POST', 'GET'])
def sign_up():
    form = Sign_up()
    if form.validate_on_submit():
        user = User(user_name=form.user.data,
                    password=form.password.data)
        db_1.session.add(user)
        db_1.session.commit()        
        return redirect(url_for('sign_in'))
    return render_template('sign_up.html', form=form)

@app.route('/')
@login_required
def about(): 
    cursor = db_2.cursor()
    
    cursor.execute("SELECT * FROM Campaign_KT.OPERATION WHERE Status = %s;" %(1))

    status_len = cursor.fetchall()

    cursor.execute("SELECT Loading FROM OPERATION;")

    records = cursor.fetchall()

    sym = 0

    for i in records:
        if i[0] != 0:
            sym += int(i[0])

    return render_template('about.html', is_admin=False, logout=True, status_len=len(status_len), loading_len=sym, len=len(records), date=datetime.today().strftime('%Y-%m-%d'))
    # else:
    #     return redirect(url_for('sign_in'))

@app.route('/<id>/compani/')
@login_required
def card_compani(id):
    if 'id' in session:
        # if current_user.is_admin:
        #    comp = Compani.query.filter(Compani.id == id).first()
        #    return render_template('card_compani.html', product=comp, is_admin=current_user.is_admin)
        cursor = db_2.cursor()
        cursor.execute("SELECT * FROM Campaign_KT.OPERATION WHERE Campaign_Name = '%s';" %(id))
        row_headers=[x[0] for x in cursor.description]
        records = cursor.fetchall()
        json_data=[]
        for result in records: 
            json_data.append(dict(zip(row_headers,result))) 
        # comp = (json_data, indent=4, sort_keys=True, default=str)
        return render_template('card_compani.html', data=json_data, id=session['id'])
    else:
        cursor = db_2.cursor()
        cursor.execute("SELECT * FROM Campaign_KT.OPERATION WHERE Campaign_Name = '%s';" %(id))
        row_headers=[x[0] for x in cursor.description]
        records = cursor.fetchall()
        json_data=[]
        for result in records: 
            json_data.append(dict(zip(row_headers,result))) 
        # comp = (json_data, indent=4, sort_keys=True, default=str)
        return render_template('card_compani.html', data=json_data)
    # else:
    #     cursor = db_2.cursor()
    #     # cursor.execute('''INSERT INTO Campaign_KT.CALLS_BUFFER (Extension, Calls_Limit) VALUES ('101', 1);''')
    #     # db.commit()
    #     cursor.execute("SELECT * FROM Campaign_KT.OPERATION WHERE Campaign_Name = '%s';" %(id))
    #     row_headers=[x[0] for x in cursor.description]
    #     records = cursor.fetchall()
    #     json_data=[]
    #     for result in records: 
    #         json_data.append(dict(zip(row_headers,result))) 
    
    #     # comp = (json_data, indent=4, sort_keys=True, default=str)
    #     return render_template('card_compani.html', data=json_data, admin=False) 

def save_pdf(bookpdf):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(bookpdf.filename)
    pdf_fn = random_hex + f_ext
    pdf_path = os.path.join(app.root_path, app.config['UPLOAD_FILE'], pdf_fn)

    print(f"{pdf_path}, {pdf_fn}")
    bookpdf.save(os.path.join(app.root_path, app.config['UPLOAD_FILE'], pdf_fn))


    return pdf_path

@app.route('/<id>/upload', methods=['POST', 'GET'])
@login_required
def upload_exls(id):
    form = Upload()


    if id == '4_1' or id == '4_2' or id == '4_3' or id == '4_4':
        try:
            r = requests.post('http://localhost:8000/crm_process')

            return redirect(f'http://{ip_addres}:8003/{id}/compani/')

        except Exception as ex:
            flash(f"{ex}")
            return redirect(f'http://{ip_addres}:8003/{id}/compani/')

    else:
        if form.validate_on_submit():
            try:
                exls = save_pdf(form.file.data)
                table_name = {'1': 'Input_AntiFraud_Actualization',
                        '2':'Input_AntiFraud_LTE',
                        '3':'Input_Proactiv',
                        '5':'Input_FD_TV_Smart',
                        '6':'Input_FD_Cinema',
                        '7':'Input_KT_Transfer1',
                        '8':'Input_KT_Transfer2',
                        '9':'Input_KT_Transfer3'}

                r = requests.post('http://localhost:8000/excel_process', json={"file_path": f"{exls}", "campaign_name" : id})
                if r.status_code == 200:
                    return redirect(url_for('about'))
                elif r.status_code == 400:
                    data = r.json()
                    flash(f"{data['detail']}")
                    return render_template('user.html', form=form, id=id)   
            except Exception as ex:
                 flash(f"{ex}")

        # cursor = db_2.cursor()
        # cursor.execute("SELECT Campaign_Caption FROM Campaign_KT.OPERATION WHERE Campaign_Name = '%s';" %(id))
        # data = cursor.fetchall()

        return render_template('user.html', form=form, id=id, ip=ip_addres)

@app.route('/<id>/chats/', methods=['POST'])
def chats(id):

    # f'{ip_addres}'
    cursor = db_2.cursor()
    # cursor.execute('''INSERT INTO Campaign_KT.CALLS_BUFFER (Extension, Calls_Limit) VALUES ('101', 1);''')
    # db.commit()
    cursor.execute("SELECT * FROM Campaign_KT.OPERATION WHERE Campaign_Caption = '%s';" %(id))
    row_headers=[x[0] for x in cursor.description]
    records = cursor.fetchall()
    json_data=[]
    for result in records: 
        json_data.append(dict(zip(row_headers,result))) 

    return render_template('chats.html', data=json_data)


@app.route('/<id>/start/')
def start(id):
    cursor = db_2.cursor()
    cursor.execute("UPDATE Campaign_KT.OPERATION SET Status = 1 WHERE Campaign_Caption = %s;", (id,) )
    db_2.commit()
    return "start"

@app.route('/<id>/stop/')                        
def stop(id):
    cursor = db_2.cursor()
    cursor.execute(f"UPDATE Campaign_KT.OPERATION SET Status = 3 WHERE Campaign_Caption = %s;", (id,) )
    db_2.commit()
    return "stop"

@app.route('/<id>/pause/')                        
def pause(id):
    cursor = db_2.cursor()
    cursor.execute(f"UPDATE Campaign_KT.OPERATION SET Status = 2 WHERE Campaign_Caption = %s;", (id,) )
    db_2.commit()
    return "pause"


@app.route('/api_comapni/', methods=['POST', 'GET'])
def api_search(): 
    cursor = db_2.cursor()
    cursor.execute("SELECT * FROM Campaign_KT.OPERATION;")
    row_headers=[x[0] for x in cursor.description]
    records = cursor.fetchall()
    json_data=[]
    for result in records:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)

@app.route('/api/search_com/<search_word>', methods=['POST', 'GET'])
def api_search_word(search_word):
    data = Compani.query.filter((Compani.Campaning_Name.contains(f"{search_word}"))).all()
    
    return jsonify(data)


def save_file(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    pdf_fn = random_hex + f_ext
    pdf_path = os.path.join(app.root_path, app.config['UPLOAD_FILE'], pdf_fn)

    print(f"{pdf_path}, {pdf_fn}")
    file.save(os.path.join(app.root_path, app.config['UPLOAD_FILE'], pdf_fn))


    return pdf_fn


@app.route('/create_product/', methods=('GET', 'POST'))
@login_required
def create_product():
    # if current_user.is_admin:
    form = Create_Compani()
    if form.validate_on_submit():
        file = save_file(form.file.data)   
        # comp = Compani(Campaning_Name=form.campaning_name.data,
        #             Status=form.status.data,
        #             License_In_Use=form.license_in_use.data,
        #             First_Call_Time=form.First_Call_Time.data,
        #             Last_Call_Time=form.Last_Call_Time.data)
        
        # db_1.session.add(comp)
        # db_1.session.commit()

        cursor = db_2.cursor()
        cursor.execute(f"""INSERT INTO Campaign_KT.OPERATION (Campaign_Name, Campaign_Date, Collection_Pointer,
                        Buffer_Pointer, Status, First_Call_Time, Last_Call_Time,
                        Attempt, Campaign_Caption, Attempts, Extension, Loading,
                        License_inUse, SIP_Trunk, Context_App, SIP-Server)
                            SELECT '%s', '%s', '%s', '%s', '%s', '%s', '%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'
                            WHERE NOT EXISTS (
                              SELECT 1
                              FROM Campaign_KT.OPERATION
                              WHERE Campaign_Name = {form.campaning_name.data});"""
                       (form.campaning_name.data, form.status.data,
                        form.license_in_use.data, form.First_Call_Time.data,
                        form.Last_Call_Time.data, datetime.utcnow,))
        db_2.commit()

        return redirect(url_for('about'))
        
    return render_template('create_compani.html', form=form)
    # elif not current_user.is_admin:
    #     return abort(404)

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60


@app.route('/<compani_id>/edit/', methods=('GET', 'POST'))
@login_required
def edit(compani_id):
    # if current_user.is_admin:
    form = Edit_Compani()
    if form.validate_on_submit():
        try:
            cursor = db_2.cursor()
            fdt = get_sec(str(form.First_Call_Time.data))
            ldt = get_sec(str(form.Last_Call_Time.data))
            print(ldt)
            print(fdt)
            print()
            print((form.campaign_caption.data, form.license_in_use.data, str(timedelta(seconds=fdt)), str(timedelta(seconds=ldt)), compani_id), sep='\n')
            query = "UPDATE OPERATION SET Campaign_Caption = '%s', License_InUse = %s, First_Call_Time = '%s', Last_Call_Time = '%s' WHERE Campaign_Name = '%s';" % (form.campaign_caption.data, form.license_in_use.data, str(timedelta(seconds=fdt)), str(timedelta(seconds=ldt)), compani_id)
            print(query)
            cursor.execute(query)
            # cursor.execute('''UPDATE Campaign_KT.OPERATION SET Campaign_Caption = '%s', License_InUse = %s, First_Call_Time = %s, Last_Call_Time = %s, WHERE Campaign_Name = '%s';''' % (form.campaign_caption.data, form.license_in_use.data, str(timedelta(seconds=fdt)), str(timedelta(seconds=ldt)), compani_id))
            db_2.commit()

            return redirect(url_for('about'))
        except Exception as ex:
            flash(f"{ex}")
            return redirect(url_for('about'))
      
    elif request.method == 'GET':
        cursor = db_2.cursor()
        cursor.execute("SELECT Campaign_Caption, License_InUse, Campaign_Name, First_Call_Time FROM Campaign_KT.OPERATION WHERE Campaign_Name = '%s';" %(compani_id))
        data = cursor.fetchall()
    
        print(data[0])

        form.campaign_caption.data = data[0][0]
        form.license_in_use.data =  data[0][1]
        form.First_Call_Time.data =  datetime.now()
        form.Last_Call_Time.data = datetime.now()
        return render_template('edit.html', form=form, Campaign_Name=data[0][2])
    # elif not current_user.is_admin:
    #     return abort(404)

def sip_update(sip_id, s_ip, time, r):
    cursor = db_2.cursor()

    sip_ip = ['asterisk1.telecom.kz', 'asterisk2.telecom.kz']
    sip_server = ['10.165.0.14', '10.165.0.15']
    server_ip = ['10.165.0.2', '10.165.0.6']

    cursor.execute("UPDATE Campaign_KT.Settings SET SIP_Server = %s, Sip_Ip = %s, SIP_Trunk = %s, TIME_Out = %s;", (sip_server[int(sip_id)], server_ip[int(s_ip)], sip_ip[int(sip_id)], str(time)))
    db_2.commit()

    if r is None:
        ...
    else:
        cursor.execute(f"UPDATE Campaign_KT.Settings SET Engine = %s;" %(int(request.form['Radio'])))
        db_2.commit()

def sip_insert(sip_id, s_ip, time, r):
    cursor = db_2.cursor()

    sip_ip = ['asterisk1.telecom.kz', 'asterisk2.telecom.kz']
    sip_server = ['10.165.0.14', '10.165.0.15']
    server_ip = ['10.165.0.2', '10.165.0.6']

    cursor.execute("INSERT INTO Campaign_KT.Settings (SIP_Server, SIP_Trunk, Time_Out, Sip_Ip) VALUES (?, ?, ?, ?);"  %(sip_server[int(sip_id)], sip_ip[int(sip_id)], str(time), server_ip[int(s_ip)]))
    db_2.commit()
    if r is None:
        ...
    else:
        cursor.execute(f"UPDATE Campaign_KT.Settings SET Engine = %s;" %(int(request.form['Radio'])))
        db_2.commit()

@app.route('/settings/', methods=('GET', 'POST'))
@login_required
def settings():
    form = Settings()
    if form.validate_on_submit():
        
        sip_ip = ['asterisk1.telecom.kz', 'asterisk2.telecom.kz']
        sip_server = ['10.165.0.14', '10.165.0.15']
        print(sip_ip[int(form.sip_server.data)], form.sip_server.data, form.time_out.data)
        cursor = db_2.cursor()
        cursor.execute("SELECT * FROM Campaign_KT.Settings")
        records = cursor.fetchone()
        
        if records is None :

            if request.form['Radio']:
                sip_insert(form.sip_server.data, form.server_ip.data, form.time_out.data, None)

                return redirect(url_for('about'))
        
        else:
            
            try:
                sip_update(form.sip_server.data, form.server_ip.data, form.time_out.data, request.form['Radio'])

                return redirect(url_for('about'))

            except:
                sip_update(form.sip_server.data, form.server_ip.data, form.time_out.data, None)

                return redirect(url_for('about'))

            
    elif request.method == 'GET':

        cursor = db_2.cursor()
        
        cursor.execute("SELECT * FROM Campaign_KT.Settings;")

        records = cursor.fetchone()

        if records is None:
            ...
        else:
            # form.server_ip.data = int(records[6])
            form.time_out.data = int(records[4])
    
        return render_template('settings.html', form=form)
    # elif not current_user.is_admin:
    #     return abort(404)      

@app.post('/<int:compani_id>/delete/')
@login_required
def delete(compani_id):
    if current_user.is_admin:
        book = Compani.query.get_or_404(compani_id)
        db_1.session.delete(book)
        db_1.session.commit()
        return redirect(url_for('about'))
    elif not current_user.is_admin:
        return abort(404)   

# @app.route('/test/')
# def test():
#     page = request.args.get('page', 1, type=int)
#     comp = Compani.query.paginate(page=page, per_page=12)
#     x = lambda x: for i in comp
#     return "hello"


@app.before_first_request
def create_tables():
    app.app_context().push()
    db_1.create_all()

    user_1 = User(user_name="admin1",
                    password="admin1admin1",
                    is_admin=True)
    db_1.session.add(user_1)

    user_2 = User(user_name="admin2",
                    password="admin2admin2",
                    is_admin=True)
    db_1.session.add(user_2)
    
    user_3 = User(user_name="admin3",
                    password="admin3admin3",
                    is_admin=True)
    db_1.session.add(user_3)

    user_4 = User(user_name="admin4",
                    password="admin4admin4",
                    is_admin=True)
    db_1.session.add(user_4)


    db_1.session.commit()


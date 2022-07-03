from flask import Flask, render_template, redirect, request, url_for, Blueprint, flash
from sim.mahasiswa.forms import Orang,login_org,Edit_org
from sim.models import Tmahasiswa, Tpengaduan
from sim import db, bcrypt
from flask_login import login_user,current_user,logout_user,login_required

rmahasiswa=Blueprint('rmahasiswa', __name__)

@rmahasiswa.route("/")
def rumah():
    return render_template("rumah.html")

@rmahasiswa.route("/tentang")
def tentang():
    return render_template("tentang.html")

@rmahasiswa.route("/daftar", methods=['GET', 'POST'])
def daftar():
    form=Orang()
    if (form.validate_on_submit()):
        pas_hash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')# ini adalah variabel yang akan mengamankan pasword yang dimasukan dan nanti pasword yang sudah di amankan akan di panggil di line selanjutnya
        add_mahasiswa=Tmahasiswa(npm=form.npm.data, nama=form.nama.data, email=form.email.data, password=pas_hash, kelas=form.kelas.data, alamat=form.alamat.data)
        db.session.add(add_mahasiswa)
        db.session.commit()
        flash(f'Akun- {form.npm.data} berhasil daftar', 'primary')
      
        return redirect(url_for('rmahasiswa.login'))
    return render_template("daftar.html", form=form)

@rmahasiswa.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('rmahasiswa.rumah'))
    form=login_org()
    if form.validate_on_submit():
        ceknpm= Tmahasiswa.query.filter_by(npm=form.npm.data).first()
        if ceknpm and bcrypt.check_password_hash(ceknpm.password, form.password.data):
            login_user(ceknpm)
            flash('Selamat Datang Kembali', 'warning')
            return redirect(url_for('rmahasiswa.akun'))
        else:
            flash('Login Gagal, Periksa NPM dan Password kembali', 'danger')
    return render_template ("login.html",form=form)


@rmahasiswa.route("/akun")
@login_required # ini akan membuat halamanya hanya bisa dibuka saat user sudah login
def akun():
    return render_template('akun.html')

@rmahasiswa.route("/keluar")
def keluar():
    logout_user()
    return redirect(url_for('rmahasiswa.rumah'))

@rmahasiswa.route("/edit", methods=['GET','POST'])
@login_required
def edit():
    form = Edit_org()
    if form.validate_on_submit():# ini adalah sintak untuk mengupdate data yang akan dimasukan ke dalam database
        current_user.npm=form.npm.data
        current_user.nama=form.nama.data
        current_user.email=form.email.data
        current_user.kelas=form.kelas.data
        current_user.alamat=form.alamat.data
        current_user.password=form.password.data
        db.session.commit()
        flash('Data berhasil di rubah ','warning ')
        return redirect(url_for('rmahasiswa.edit'))
    elif request.method=="GET":# ini sintak untuk menampilkan data ke dalam database
        form.npm.data=current_user.npm
        form.nama.data=current_user.nama 
        form.email.data=current_user.email
        form.kelas.data=current_user.kelas
        form.alamat.data=current_user.alamat
        form.password.data=current_user.password
        
    return render_template ('edit.html',form=form)

from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

class job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=False)
    posted_by = db.Column(db.String(100), nullable=False)

class application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    return "Welcome to Job Portal Application"

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        user1 = user(name=name, email=email, password=password, role=role)
        db.session.add(user1)
        db.session.commit()
        return redirect(f'/dashboard/{user1.id}')

    user_read = user.query.all()
    return render_template('home.html', user_read=user_read)

@app.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
def dashboard(user_id):
    user_obj = user.query.get_or_404(user_id)
    if request.method == 'POST' and user_obj.role == 'recruiter':
        title = request.form.get('title')
        company = request.form.get('company')
        description = request.form.get('description')
        salary = request.form.get('salary')
        posted_by = user_obj.name
        job_post = job(title=title, company=company, description=description, salary=salary, posted_by=posted_by)
        db.session.add(job_post)
        db.session.commit()
    jobs = job.query.all()
    return render_template('dashboard.html', jobs=jobs, user=user_obj)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job_obj = job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job_obj)

@app.route('/delete/user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    user_delete = user.query.get_or_404(id)
    db.session.delete(user_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/job/<int:id>', methods=['GET', 'POST'])
def delete_job(id):
    job_delete = job.query.get_or_404(id)
    db.session.delete(job_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/application/<int:id>', methods=['GET', 'POST'])
def delete_application(id):
    application_delete = application.query.get_or_404(id)
    db.session.delete(application_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    job_edit = job.query.get_or_404(id)
    if request.method == 'POST':
        job_edit.title = request.form.get('title')
        job_edit.company = request.form.get('company')
        job_edit.description = request.form.get('description')
        job_edit.salary = request.form.get('salary')
        job_edit.posted_by = request.form.get('posted_by')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_job.html', job=job_edit)

@app.route('/apply/job/<int:id>', methods=['GET', 'POST'])
def apply_job(id):
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_application = application(job_id=id, user_id=user_id)
        db.session.add(new_application)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('apply.html', job_id=id)

@app.route('/logout')
def logout():
    return redirect(url_for('home'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

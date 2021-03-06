from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, TicketForm, UpdateForm, InviteForm
from app.models import User, Ticket
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    opentickets = current_user.get_open_tickets().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    wiptickets = current_user.get_wip_tickets().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    testingtickets = current_user.get_testing_tickets().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    closedtickets = current_user.get_closed_tickets().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    return render_template('index.html', title='Home', opentickets = opentickets.items, wiptickets= wiptickets.items, testingtickets = testingtickets.items, closedtickets = closedtickets.items)

@app.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    form = InviteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('User does not exist')
            return redirect(url_for('invite'))
        flash('User will be notified of invite')
        return redirect(url_for('index'))
    return render_template('invite.html', form=form)

@login_required
@app.route('/ticket', methods = ['GET', 'POST'])
def ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(description=form.description.data, author=current_user, priority=form.priority.data, link=form.link.data, tag='open')
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket is now live!')
        return redirect(url_for('index'))
    return render_template('ticket.html', title='Home', form=form)

# need to add check if ticket exists after queriny specific id
@login_required
@app.route('/edit_ticket/<ticket_id>', methods = ['GET', 'POST'])
def edit_ticket(ticket_id):
    ticket = current_user.get_specific_ticket(ticket_id) # should check if they have the credentials to view that ticket
    form = UpdateForm(tag=ticket.tag, priority=ticket.priority)
    if form.validate_on_submit():
        ticket.priority = form.priority.data
        ticket.tag = form.tag.data
        db.session.commit()
        flash('Ticket Updated')
        return redirect(url_for('index'))
    return render_template('edit_ticket.html', title='Home', ticket = ticket, form=form)

@login_required
@app.route('/delete/<ticket_id>', methods = ['GET','POST'])
def delete_ticket(ticket_id):
    ticket = current_user.get_specific_ticket(ticket_id) # should check if they have the credentials to delete that ticket
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket Deleted')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
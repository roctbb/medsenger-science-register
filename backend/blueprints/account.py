from flask import Blueprint, request, render_template, make_response, redirect
from backend.methods import *

account_blueprint = Blueprint('activate', __name__)


@account_blueprint.route('/activate', methods=['get', 'post'])
def activate_view():
    key = request.args.get('key')
    if not key:
        return render_template('activate.html', critical_error='Некорректная активационная ссылка.')

    user = find_user_by_activation_key(key)
    if not user:
        return render_template('activate.html', critical_error='Пользователь не найден или уже активирован.')

    if request.method.lower() == 'get':
        return render_template('activate.html', user=user)
    else:
        error = ''

        name = request.form.get('name')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')

        if not name:
            error = 'Укажите ФИО'
        elif not password:
            error = 'Укажите пароль'
        elif len(password) < 8:
            error = 'Пароль слишком короткий'
        elif password != password_confirmation:
            error = 'Пароль не совпадает с подтверждением'

        if error:
            return render_template('activate.html', user=user, error=error)
        else:
            activate_user(user, password)
            token = create_token(user)

            response = make_response(redirect('/'))
            response.set_cookie('register_token', token.token)
            return response


@account_blueprint.route('/password/link', methods=['get', 'post'])
def password_link_view():
    if request.method.lower() == 'get':
        return render_template('reset_password_link.html')
    else:
        error = ''

        email = request.form.get('email')
        if not email:
            error = 'Укажите email'

        user = find_user_by_email(email)
        if not user:
            error = 'Пользователь с таким email не найден'

        if error:
            return render_template('reset_password_link.html', error=error, email=email)
        else:
            send_reset_link(user)

            return render_template('reset_password_link.html',
                                   info=f"Ссылка на восстановление пароля отправлена на почту {email}")


@account_blueprint.route('/password/reset', methods=['get', 'post'])
def password_reset_view():
    if request.method.lower() == 'get':
        user = find_user_by_password_reset_key(request.args.get('key'))
        error = ''

        if not user:
            error = 'Ссылка для восстановления пароля устарела.'

        return render_template('reset_password.html', critical_error=error)
    else:
        user = find_user_by_password_reset_key(request.args.get('key'))
        error = ''

        if not user:
            error = 'Ссылка для восстановления пароля устарела.'

        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')

        if not password:
            error = 'Укажите пароль'
        elif len(password) < 8:
            error = 'Пароль слишком короткий'
        elif password != password_confirmation:
            error = 'Пароль не совпадает с подтверждением'

        if error:
            return render_template('reset_password.html', error=error)
        else:
            change_user_password(user, password)

            token = create_token(user)

            response = make_response(redirect('/'))
            response.set_cookie('register_token', token.token)
            return response

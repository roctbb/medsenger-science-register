from flask import Blueprint, request, render_template, make_response, redirect
from backend.methods import *

activate_blueprint = Blueprint('activate', __name__)


@activate_blueprint.route('/', methods=['get', 'post'])
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

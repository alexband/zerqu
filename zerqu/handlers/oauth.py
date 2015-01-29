# coding: utf-8

from flask import Blueprint
from flask import request, render_template, jsonify
from flask_wtf import Form
from wtforms.fields import HiddenField
from ..scopes import filter_user_scopes
from ..models.auth import oauth, current_user


bp = Blueprint('oauth', __name__)


class OAuthForm(Form):
    scope = HiddenField()


@bp.route('/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    """Authorize handler for OAuth"""
    form = OAuthForm()
    if current_user and form.validate_on_submit():
        confirm = request.form.get('confirm', 'no')
        return confirm == 'yes'
    req = kwargs.pop('request')
    scopes = kwargs.pop('scopes')
    choices = filter_user_scopes(scopes)
    return render_template(
        'oauth_authorize.html',
        form=form,
        user=current_user,
        client=req.client,
        scopes=scopes,
        choices=choices, **kwargs
    )


@bp.route('/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return {}


@bp.route('/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token():
    return {}


@bp.route('/errors')
def errors():
    error = request.args.get('error', None)
    return jsonify(error=error)

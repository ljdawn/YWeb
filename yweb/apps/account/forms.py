# coding: UTF-8

from yweb.forms import Form
from wtforms import BooleanField, StringField, \
    validators, DateTimeField, TextAreaField, IntegerField, \
    PasswordField, FileField, SelectField, HiddenField
from wtforms.validators import ValidationError

from apps.auth.models import User

from yweb.utils.translation import ugettext_lazy as _
from apps.auth.forms import validate_password

class AvatarChangeForm(Form):

    avatar = FileField( _('My Avatar') )


class PasswordChangeForm(Form):

    current = PasswordField( _('Current Password'), default='' )
    password = PasswordField( _('New Password'), [
        validate_password,
        validators.DataRequired(),
        validators.EqualTo('confirm', message=_('Passwords must match'))
    ], default='' )
    confirm = PasswordField( _('Confirm New Password'), default='' )

    def validate_current(form, field):

        user = form._handler.current_user

        if not user.check_password( field.data ):
            raise ValidationError( _('Current password is incorrect.') )


class EmailChangeStep1Form(Form):

    '''修改我的邮箱地址步骤一：邮箱验证

    '''

    email = StringField(_('Email Address'), [
        validators.Length(min=6, max=35), validators.Email()])

    def validate_email(form, field):

        current_email = form._handler.current_user.email

        if field.data == current_email:
            raise ValidationError(_('This is your current E-mail.'))

        user = form._handler.db.query(User).filter_by(email=field.data).first()
        if user and user.email != current_email:
            raise ValidationError(_('Email address is exist.'))


class BasicInfoEditForm(Form):

    nickname = StringField( _('Nickname'), [
        validators.Length(min=1, max=64) ] )
    first_name = StringField( _('First Name'), [
        validators.Length(max=32) ] )
    last_name = StringField( _('Last Name'), [
        validators.Length(max=32) ] )
    gender = SelectField( _('Gender') )
    language = SelectField( _('Language') )


class AdminUserBasicEditForm(BasicInfoEditForm):

    email = StringField(_('Email Address'), [
        validators.Length(min=6, max=35), validators.Email()])

    avatar = FileField( _('My Avatar') )

    password = PasswordField( _('New Password'), [
        validators.EqualTo('confirm', message=_('Passwords must match'))
    ], default='' )

    confirm = PasswordField( _('Confirm New Password'), default='' )

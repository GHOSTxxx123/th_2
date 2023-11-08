from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, BooleanField, PasswordField, SelectField, MultipleFileField, TimeField, DateTimeField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email
from app.model import Compani, User



class Sign_in(FlaskForm):
    user = StringField('Login', validators=[DataRequired(),
                                             Length(min=2, max=100)])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                             Length(min=8, max=100)])
    remember = BooleanField("Запомнить меня")                                        
    submit = SubmitField('Вход')         


class Sign_up(FlaskForm):
    user = StringField('Login', validators=[DataRequired(),
                                             Length(min=2, max=100)])                                        
    password = PasswordField('Пароль', validators=[DataRequired(),
                                             Length(min=8, max=100)])                                                                               

    submit = SubmitField('Авторизация')                                             
    
    def validate_gmail(self, name):
        name = User.query.filter_by(user_name=name.data).first()
        if name:
            raise ValidationError('Такой пользователь уже существует !!!')

class Create_Compani(FlaskForm):

    campaning_name = StringField('Название кампании', validators=[DataRequired(),
                                             Length(min=2, max=200)])
    status = SelectField('Выбор приложении', choices=[('start', 'start'), ('stop', 'stop'), ('pause', 'pause'), 
                                ('schedule', 'schedule')])
    
    license_in_use = IntegerField('Количество лицензий', validators=[NumberRange(min=1, max=1000)])

    First_Call_Time = TimeField('Начало звонков', format='%H:%M')

    Last_Call_Time = TimeField('Окончание звонков', format='%H:%M')

    file = FileField('', validators=[DataRequired(), FileAllowed(['txt'])])
    
    submit = SubmitField('Создать') 

    def validate_full_name(self, campaning_name):
        campaning_name = Compani.query.filter(Compani.Campaning_Name == campaning_name.data).first()
        if campaning_name:
            raise ValidationError('Такой продукт уже создан !!!')


class Edit_Compani(FlaskForm):

    campaign_caption = StringField('Название кампании', validators=[DataRequired(),
                                             Length(min=2, max=200)])
    # status = SelectField('Выбор приложении', choices=[('start', 'start'), ('stop', 'stop'), ('pause', 'pause'), 
    #                             ('schedule', 'schedule')])
    
    license_in_use = IntegerField('Количество лицензий', validators=[NumberRange(min=1, max=12)])

    First_Call_Time = TimeField('Начало звонков', format='%H:%M')

    Last_Call_Time = TimeField('Окончание звонков', format='%H:%M')

    submit = SubmitField('Редактировать') 

    # def validate_full_name(self, campaning_name):
    #     campaning_name = Compani.query.filter(Compani.Campaning_Name == campaning_name.data).first()
    #     if campaning_name:
    #         raise ValidationError('Такой продукт уже создан !!!')

    # def validate_full_name(self, campaning_name):
    #     campaning_name = Compani.query.filter(Compani.Campaning_Name == campaning_name.data).first()
    #     if campaning_name:
    #         raise ValidationError('Такой продукт уже создан !!!')


class Settings(FlaskForm):

    sip_server = SelectField('SIP Server', choices=[('0', 'Сервер 1'), ('1', 'Сервер 2')])

    time_out = IntegerField('Тайм аут в секундах', validators=[DataRequired(),
                                                    NumberRange(min=5, max=30)])

    submit = SubmitField('Сохранить')


class Upload(FlaskForm):
    file = FileField('Выберете файл', validators=[DataRequired(), FileAllowed(['xlsx'])])
    
    submit = SubmitField('Добавить')
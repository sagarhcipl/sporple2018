from forms import query_selectors
from flask_wtf import Form
from wtforms import TextField
from wtforms import IntegerField
from wtforms import validators
from wtforms.fields import TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField


class LookingForForm(Form):
    position = QuerySelectField('Position',
            get_label='name',
            allow_blank=True)

    country_id = QuerySelectField('Country',
            get_label='name',
            allow_blank=True,
            query_factory=query_selectors.country)

    body = TextAreaField('Description')
    age_min = IntegerField('Age Min', [
            validators.Optional(),
            validators.NumberRange(0, 99)], default='0')
    age_max = IntegerField('Age Max', [
            validators.Optional(),
            validators.NumberRange(0, 99)], default='99')
    height_min = IntegerField('Height Min', [
            validators.Optional(),
            validators.NumberRange(0, 999)], default='0')
    height_max = IntegerField('Height Max', [
            validators.Optional(),
            validators.NumberRange(0, 999)], default='999')
    weight_min = IntegerField('Weight Min', [
            validators.Optional(),
            validators.NumberRange(0, 999)], default='0')
    weight_max = IntegerField('Weight Max', [
            validators.Optional(),
            validators.NumberRange(0, 999)], default='999')
    country_groups = QuerySelectMultipleField('Allowed Passports', get_label='name')

    def update_obj(self, looking_for, is_premium):
        looking_for.position = self.position.data
        looking_for.title = self.position.data.name
        looking_for.sport_id = self.position.data.sport_id
        looking_for.country_id = int(self.country_id.data.id) if self.country_id.data else None
        looking_for.body = self.body.data
        looking_for.age_min = self.age_min.data
        looking_for.age_max = self.age_max.data
        looking_for.height_min = self.height_min.data
        looking_for.height_max = self.height_max.data
        looking_for.weight_min = self.weight_min.data
        looking_for.weight_max = self.weight_max.data
        looking_for.country_groups = [c for c in self.country_groups.data if c.id]


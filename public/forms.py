from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Submit
from django.forms import ModelForm


class BaseFormMixin:
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'template'
        self.helper.wrapper_class = "row"
        self.helper.field_class = "col-10"
        self.helper.label_class = 'col-2'
        self.helper.layout = self.get_layout()
        super().__init__(*args, **kwargs)

    def get_base_layout(self):
        return Layout()

    def get_submit_layout(self):
        return Layout(Row(Div(Submit('save', 'Сохранить'), css_class='col-auto ml-auto')), )

    def get_layout(self, read_only=False):
        base_layout = self.get_base_layout()
        if not read_only:
            return Layout(base_layout, self.get_submit_layout())
        else:
            return base_layout


class BaseModelForm(BaseFormMixin, ModelForm):
    pass

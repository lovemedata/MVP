from django import forms

class Bootstrap:
    # 不要加上樣式的fields
    bootstrap_exclude_fields = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
                field.widget.attrs['autocomplete'] = 'off'
            else:
                field.widget.attrs={
                    'class': 'form-control',
                    'placeholder': field.label,
                    'autocomplete': 'off'
                }

class BootstrapForm(Bootstrap, forms.Form):
    pass

class BootstrapModelForm(Bootstrap, forms.ModelForm):
    pass

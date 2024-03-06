
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from apps.exercise_area import models
from apps.utils.bootstrap import BootstrapModelForm, BootstrapForm
# from apps.exercise_area.utils import 
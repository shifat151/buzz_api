from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import magic


class loginForm(forms.Form):
    username = forms.CharField(max_length=255, label="Username:")
    password = forms.CharField(label="Password:", widget=forms.PasswordInput)


class registrationForm(forms.Form):
    name = forms.CharField(max_length=55, label="Name: ")
    email = forms.EmailField(label="Email: ")
    phone = forms.CharField(max_length=55, label="Phone: ")
    full_address = forms.CharField(max_length=512, label="Full Address: ", required=False)
    name_of_university = forms.CharField(max_length=256, label="Name of University: ")
    # graduation_year=forms.CharField(widget=forms.NumberInput(attrs={'min':2015,'max': '2020'}), label="Graduation year: ", help_text="Enter your  graduation year. This should be between 2015 and 2020")
    graduation_year = forms.IntegerField(max_value=2020, min_value=2015, label="Graduation year: ",
                                         help_text="Enter your  graduation year. This should be between 2015 and 2020")
    cgpa = forms.FloatField(min_value=2.0, max_value=4.0, required=False, label="CGPA: ")
    experience_in_months = forms.IntegerField(max_value=100, min_value=0, required=False, label="Experience in month",
                                              help_text="Enter your professional experience in months")
    current_work_place_name = forms.CharField(max_length=256, required=False, label="Current work place name: ")
    apply_choice = [
        ('Mobile', 'Mobile'),
        ('Backend', 'Backend')
    ]
    applying_in = forms.ChoiceField(choices=apply_choice)
    expected_salary = forms.IntegerField(min_value=15000, max_value=60000, label="Expected Salary: ")
    field_buzz_reference = forms.CharField(max_length=256, label="Field Buzz Reference: ", required=False, )
    github_project_url = forms.URLField(label="Github project URL")


class fileUpload(forms.Form):
    # cv=forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    cv = forms.FileField(label="CV", help_text="CV must be in PDF format and should not exceed 4MB limit")

    def clean(self):
        file = self.cleaned_data["cv"]
        filetype = magic.from_buffer(file.read())
        if not "PDF" in filetype:
            raise ValidationError("Please upload a PDF file")
        return file

        limit = 4 * 1024 * 1024
        if file.size > limit:
            raise ValidationError('File too large. Size should not exceed 4 MiB.')

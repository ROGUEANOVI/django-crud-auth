from django import forms
from .models import Task

class FormCreateTask(forms.ModelForm):
  class Meta:
    model = Task
    fields = ["title", "description", "important"]
    widgets = {
      "title": forms.TextInput(attrs={
          "class": "form-control", "placeholder": "Write the title your task", 
      }),
      "description": forms.Textarea(attrs={
        "class": "form-control",
      })
    }
    

class FormEditTask(forms.ModelForm):
  class Meta:
    model = Task
    fields = ["title", "description", "important"]
    widgets = {
      "title": forms.TextInput(attrs={
          "class": "form-control", "placeholder": "Write the title your task", 
      }),
      "description": forms.Textarea(attrs={
        "class": "form-control",
      })
    }

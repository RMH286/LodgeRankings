from django import forms


class PongGameForm(forms.Form):
    winner1 = forms.CharField(label='First Winner netid', max_length=100)
    winner2 = forms.CharField(label='Second Winner netid', max_length=100,
        required=False)
    loser1 = forms.CharField(label='First Loser netid', max_length=100)
    loser2 = forms.CharField(label='Second Loser netid', max_length=100,
        required=False)
    date = forms.DateField(widget=forms.SelectDateWidget)
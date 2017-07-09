from django import forms


class PongGameForm(forms.Form):
    """Form used to add a new Pong Game.
    
        FIELDS:
            winner1     [Char Field]
                        first winner
            winner2     [Char Field] (optional)
                        second winner
            loser1      [Char Field]
                        first loser
            loser2      [Char Field] (optional)
                        second loser
            date        [Date Field]
                        date the game was played
    
    Note: the second winner and loser are both optional. Games can be
    1v1, 1v2, or 2v2"""
    
    winner1 = forms.CharField(label='First Winner netid', max_length=100)
    winner2 = forms.CharField(label='Second Winner netid', max_length=100,
        required=False)
    loser1 = forms.CharField(label='First Loser netid', max_length=100)
    loser2 = forms.CharField(label='Second Loser netid', max_length=100,
        required=False)
    date = forms.DateField(widget=forms.SelectDateWidget)
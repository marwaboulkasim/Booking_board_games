from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from tables_app.models import Game

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-input'})
    )
    pseudo = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Pseudo', 'class': 'form-input'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-input'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe', 'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'pseudo', 'password1', 'password2']

# --- Gestion Profil Utilisateur --- #

class ProfileForm(UserChangeForm):
    password = None
    
    favorite_games = forms.ModelMultipleChoiceField(
        queryset=Game.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Choisissez jusqu\'à 3 jeux'
    )
    
    class Meta:
        model = User
        fields = ['username', 'pseudo', 'first_name', 'last_name', 'phone', 'favorite_games'] # rajouter received_notifications une fois la fonction créée
    
    def clean_favorite_games(self):
        games = self.cleaned_data.get('favorite_games')
        if len(games) > 3:
            raise forms.ValidationError('Vous ne pouvez choisir que 3 jeux max.')
        return games


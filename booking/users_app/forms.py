from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from tables_app.models import Game, Booking

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
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.pseudo = self.cleaned_data['pseudo']
        if commit:
            user.save()
        return user
    
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['favorite_games'].queryset = Game.objects.all()
         
    def clean_favorite_games(self):
        games = self.cleaned_data.get('favorite_games')
        if len(games) > 3:
            raise forms.ValidationError('Vous ne pouvez choisir que 3 jeux max.')
        return games

# --- Gestion des réservations (User)  ---

class EditBookingForm(forms.ModelForm):
    slot_label = forms.ChoiceField(
        choices=[
            ("14h-18h", "14h-18h"),
            ("18h-20h", "18h-20h"),
            ("20h-00h", "20h-00h"),
        ],
        label="Créneau horaire"
    )

    class Meta:
        model = Booking
        fields = ["date", "booking_type", "table", "game"]

    def save(self, commit=True):
        booking = super().save(commit=False)
        from datetime import time, timedelta
        slots = {
            "14h-18h": (time(14, 0), time(18, 0)),
            "18h-20h": (time(18, 0), time(20, 0)),
            "20h-00h": (time(20, 0), time(23, 59)),
        }
        start, end = slots[self.cleaned_data['slot_label']]
        booking.start_time = start
        booking.duration = timedelta(hours=end.hour - start.hour, minutes=end.minute - start.minute)
        if commit:
            booking.save()
        return booking

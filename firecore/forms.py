from django import forms
from .models import Character, Class, PlayerShop

class PlayerShopForm(forms.ModelForm):
    class Meta:
        model = PlayerShop
        widgets = {'user': forms.HiddenInput()}
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PlayerShopForm, self).__init__(*args, **kwargs)

        self.fields['user'].initial = self.user.id


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        widgets = {'user': forms.HiddenInput()}
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CharacterForm, self).__init__(*args, **kwargs)

        self.fields['user'].initial = self.user.id

        self.fields['first_class'].queryset = Class.objects.none()
        self.fields['second_class'].queryset = Class.objects.none()
        self.fields['third_class'].queryset = Class.objects.none()

        if 'class_tree' in self.data:
            try:
                class_tree_id = int(self.data.get('class_tree'))
                self.fields['first_class'].queryset = Class.objects.filter(class_tree_id=class_tree_id).order_by('name')
                self.fields['second_class'].queryset = Class.objects.filter(class_tree_id=class_tree_id).order_by('name')
                self.fields['third_class'].queryset = Class.objects.filter(class_tree_id=class_tree_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['first_class'].queryset = self.instance.class_tree.class_set.order_by('name')
            self.fields['second_class'].queryset = self.instance.class_tree.class_set.order_by('name')
            self.fields['third_class'].queryset = self.instance.class_tree.class_set.order_by('name')
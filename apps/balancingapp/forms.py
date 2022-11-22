from django import forms
import floppyforms

from .models import *
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.core.exceptions import ValidationError
import numpy as np
import re

organization_list = ("ЦА", 'Балаковская АЭС', 'Белоярская АЭС', 'Билибинская АЭС', 'Калининская АЭС',
                     'Кольская АЭС', 'Курская АЭС', 'Ленинградская АЭС', 'Нововоронежская АЭС', 'Ростовская АЭС',
                     'Смоленская АЭС', 'ПАТЭС', 'Технологический филиал', 'ОДИЦ ВВЭР', 'ОДИЦ РБМК', 'Строящаяся Балтийская АЭС',
                     'ИЦ Аккую', 'Воронежская АСТ', 'Филиал в Бангладеш', 'Атомтехэнерго', 'АтомЭнергоСбыт', 'АтомЭнергоРемонт',
                     'ЗАЭС', 'АтомТеплоЭлектроСеть', 'Техническая Академия', 'ИКАО', 'НИЦ АЭС', 'ЭНИЦ', 'Энергоатоминвест',
                     'Балтийская АЭС, АО', 'Атомтранс', 'Атомтеплосбыт', 'ВНИИАЭС','Титан - 2','Консист - ОС', 'С - Плюс',
                     'Неорганические сорбенты', 'АТОМДАТА', 'Атомдата - Центр', 'Атомдата - Иннополис')


class CustomSelect(forms.Select):
    option_inherits_attrs = True

class CardsForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super().clean()
        post_weight = cleaned_data.get("weight")
        post_method = cleaned_data.get("method")
        post_low_level = cleaned_data.get("low_level")
        post_target_level = cleaned_data.get("target_level")
        post_high_level = cleaned_data.get("high_level")
        if post_weight==None or post_method==None or post_low_level==None or post_high_level==None or post_target_level==None:
            raise ValidationError(
                u"This field is required"
            )
        else:
            continuous_condition = len(re.findall(r"[^\d\,\.]", post_low_level)) != 0 or len(re.findall(r"[^\d\,\.]", post_target_level)) !=0 \
                                   or len(re.findall(r"[^\d\,\.]", post_high_level)) != 0
            if post_method == 3 and post_weight > 0:
                raise ValidationError(
                    u"the value must be less then 0"
                )
            elif post_method == 1 and continuous_condition:
                raise ValidationError(
                    u"only numeric"
                )
            else:
                if np.abs(post_weight) < 9 or np.abs(post_weight) > 61:
                    raise ValidationError(
                        u"weight must be between 10 and 60"
                    )
                if post_method == 0 or post_method == 1:
                    if post_weight % 5 != 0:
                        raise ValidationError(u"invalid")

    class Meta:
        model = Card
        fields = [
            'send',
            'organization',
            'role',
            'fio',
            'name',
            'method',
            'low_level',
            'target_level',
            'high_level',
            'weight',
            'status',
            'id',
            'verificator',
            'passport',
            'delete',
            'status_for_display',

        ]
        widgets = {
            'send': forms.CheckboxInput(),
            'role': forms.Textarea(attrs={'rows': 2,}),
            'fio': forms.Textarea(attrs={'rows': 2, }),
            'name': forms.Textarea(attrs={'rows': 2, }),
            'status_for_display': forms.TextInput(attrs={'readonly':"True"}),
            'delete': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'verificator': forms.Textarea(attrs={'rows': 2, }),

        }

class AdminCardsForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super().clean()
        post_weight = cleaned_data.get("weight")
        post_method = cleaned_data.get("method")
        post_low_level = cleaned_data.get("low_level")
        post_target_level = cleaned_data.get("target_level")
        post_high_level = cleaned_data.get("high_level")
        if post_weight==None or post_method==None or post_low_level==None or post_high_level==None or post_target_level==None:
            raise ValidationError(
                u"This field is required"
            )
        else:
            continuous_condition = len(re.findall(r"[^\d\,\.]", post_low_level)) != 0 or len(re.findall(r"[^\d\,\.]", post_target_level)) !=0 \
                                   or len(re.findall(r"[^\d\,\.]", post_high_level)) != 0
            if post_method == 3 and post_weight > 0:
                raise ValidationError(
                    u"the value must be less then 0"
                )
            elif post_method == 1 and continuous_condition:
                raise ValidationError(
                    u"only numeric"
                )
            else:
                if np.abs(post_weight) < 9 or np.abs(post_weight) > 61:
                    raise ValidationError(
                        u"weight must be between 10 and 60"
                    )
                if post_method == 0 or post_method == 1:
                    if post_weight % 5 != 0:
                        raise ValidationError(u"invalid")

    class Meta:
        model = Card
        fields = [
            'send',
            'delete',
            'organization',
            'function',
            'role',
            'fio',
            'name',
            'method',
            'low_level',
            'target_level',
            'high_level',
            'weight',
            'id',
            'verificator',
            'passport',

        ]
        widgets = {
            'send': forms.CheckboxInput(),
            'role': forms.Textarea(attrs={'rows': 2,}),
            'fio': forms.Textarea(attrs={'rows': 2, }),
            'name': forms.Textarea(attrs={'rows': 2, }),
            'delete': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'verificator': forms.Textarea(attrs={'rows': 2, }),

        }
CardFormSet = modelformset_factory(
    model=Card,
    form=CardsForm,
    extra=1,
    can_delete=True,
)

AdminCardFormSet = modelformset_factory(
    model=Card,
    form=AdminCardsForm,
    extra=1,
    can_delete=True,
)
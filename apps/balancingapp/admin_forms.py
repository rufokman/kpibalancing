from django import forms
from .models import *
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
import re
import numpy as np


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


            elif post_method == 0 or post_method == 1:
                if post_weight < 0:
                    raise ValidationError(
                        u"the value must be bigger then 0"
                    )
                elif post_method == 1:
                    cond_increase = (float(post_low_level) < float(post_target_level)) and (float(post_target_level) < float(post_high_level))
                    cond_decrease = (float(post_low_level) > float(post_target_level)) and (float(post_target_level) > float(post_high_level))

                    if cond_increase == True or cond_decrease == True:
                        print("ok")
                    else:

                        raise ValidationError(
                            u"only different value for levels"
                        )



                    if continuous_condition:
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
            'delete',
            'organization',
            'function',
            'role',
            'fio',
            'id_kpi',
            'name',
            'method',
            'low_level',
            'target_level',
            'high_level',
            'weight',
            'passport',
            'fact',
            'verificator',
            'comment_func',
            'comment_audit',
            'comment_audit_AES'

        ]
        widgets = {
            'role': forms.Textarea(attrs={'rows': 2, }),
            'fio': forms.Textarea(attrs={'rows': 2, }),
            'name': forms.Textarea(attrs={'rows': 2, }),
            'id_kpi': forms.Textarea(attrs={'rows': 2}),
            'verificator': forms.Textarea(attrs={'rows': 2, }),
            'fact': forms.Textarea(attrs={'rows': 2, }),
            'comment_func': forms.Textarea(attrs={'rows': 2, }),
            'comment_audit': forms.Textarea(attrs={'rows': 2, }),
            'comment_audit_AES': forms.Textarea(attrs={'rows': 2, }),
        }


AdminCardFormSet = modelformset_factory(
    model=Card,
    form=AdminCardsForm,
    extra=0,
)
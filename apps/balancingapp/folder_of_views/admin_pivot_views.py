from django.views import View
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from apps.balancingapp.admin_forms import *
from apps.balancingapp.models import *
from django_filters.views import FilterView
from django_filters import rest_framework as filters
from apps.balancingapp.filters import CardFilter


class AdminPivotView(TemplateView):
    template_name = "admin_pivot_tab.html"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CardFilter
    queryset = Card.objects.filter(status=0, delete=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Card.objects.filter(status=0, delete=0)
        formset = AdminCardFormSet(queryset=data)
        add_form = AdminCardsForm()

        last_download = Config.objects.first().last_download.strftime("%d.%m.%Y %H:%M")
        context['last_download'] = last_download
        context['formset'] = formset
        context['add_form'] = add_form

        return context

    def post(self, request):
        data = Card.objects.filter(status=0, delete=0)
        add_form = AdminCardsForm(request.POST, request.FILES)

        if add_form.is_valid():
            print("hhh")
            qform=add_form.save(commit=False)
            qform.user = request.user
            qform.status = 0
            qform.delete = 0

            if qform.method == 1:
                qform.low_level = format(float(qform.low_level.replace(',', '.')), '.3f')
                qform.target_level = format(float(qform.target_level.replace(',', '.')), '.3f')
                qform.high_level = format(float(qform.high_level.replace(',', '.')), '.3f')
            qform.save()
        else:
            print(add_form.errors.as_data())

        formset = AdminCardFormSet(request.POST, request.FILES, queryset=data)
        for form in formset:
            if form.is_valid():

                qform = form.save(commit=False)
                if qform.method == 1:
                    qform.low_level = format(float(qform.low_level.replace(',', '.')), '.3f')
                    qform.target_level = format(float(qform.target_level.replace(',', '.')), '.3f')
                    qform.high_level = format(float(qform.high_level.replace(',', '.')), '.3f')
                qform.save()

            else:
                print(form.errors.as_data())
        return redirect(reverse_lazy("admin_pivot"))





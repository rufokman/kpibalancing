import os
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django_filters import rest_framework as filters
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from rest_framework import generics
from balancing.settings import BASE_DIR, MEDIA_ROOT
from .filters import CardFilter
from .models import *
from .forms import *
from .tables import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\lib")
from weasyprint import HTML
import tempfile
import datetime

@login_required()
def cards_update_view(request):
    data = Card.objects.filter(function=request.user.function, delete=0)
    config_data = Config.objects.first()
    allow_edit = config_data.allow_edit
    context = {}

    if request.method == 'POST':
        formset = CardFormSet(request.POST, request.FILES, queryset=data)
        if formset.is_valid():
            if allow_edit == False:
                return redirect('update')
            n=0
            for form in formset:
                # form.empty_permitted = True
                if form.cleaned_data == {}:
                    continue
                pk = request.POST["form-{}-id".format(str(n))]
                changed_data = form.changed_data
                changed = form.has_changed()
                n+=1
                deleted=form.cleaned_data['DELETE']
                qform = form.save(commit=False)
                if qform.status == 1:
                    continue
                qform.user = request.user
                qform.function = request.user.function
                if deleted and 'delete' in request.POST:
                    qform.delete = 1
                if qform.method == 1:
                    qform.low_level = format(float(qform.low_level.replace(',', '.')), '.3f')
                    qform.target_level = format(float(qform.target_level.replace(',', '.')), '.3f')
                    qform.high_level = format(float(qform.high_level.replace(',', '.')), '.3f')
                if 'save' in request.POST and changed:
                    qform.status = 3
                if qform.send==True and qform.status == 3 and 'send_to_check' in request.POST and qform.passport!="":
                    qform.status = 1
                qform.status_for_display=qform.get_status_display()
                qform.send = False
                qform.save()
                for col in changed_data:
                    if pk != "":
                        Change.objects.create(id_kpi=pk, name_col=col)
            return redirect(reverse_lazy("update"))
    else:
        formset = CardFormSet(queryset=data)
    context['formset'] = formset
    return render(request, "home.html", context)

# def delete(request,pk):
#     object = Card.objects.get(pk=pk)
#     object.delete()
#     return redirect('update')


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=КПЭ' +\
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    card_data = Card.objects.filter(user=request.user, delete=0)

    html_string = render_to_string('pdf-output.html', {'card_data': card_data})
    html = HTML(string=html_string)

    result = html.write_pdf()

    output = tempfile.NamedTemporaryFile(delete=False)
    output.write(result)
    output.flush()
    output = open(output.name, 'rb')
    response.write(output.read())
    output.close()
    os.unlink(output.name)

    return response

def delete(request):            # meets the ajax request
    item_id = int(request.POST['pk'])
    print(item_id)
    order = get_object_or_404(Card, pk=int(request.POST['order_id']))
    order.remove_item(item_id)
    if order.is_empty():                   # if the last item is deleted
        order.untie(request.session)
        order.delete()
    return redirect('update')


class PivotCardView(SingleTableMixin, FilterView):
    queryset = Card.objects.filter(status=0, delete=0)
    table_class = CardTable
    # serializer_class = ServerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CardFilter
    template_name = "user_pivot_tab.html"


@login_required()
def home_view(request):
    return render(request, 'base.html')

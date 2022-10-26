import django_tables2 as tables
from .models import *

import itertools

class OnCheckingTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    accept = tables.TemplateColumn(verbose_name=('Решение'),
                                      template_name='accept_column.html',
                                      orderable=False)
    counter = tables.Column(empty_values=(), orderable=False, verbose_name="№ п/п")

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count())
        return next(self.row_counter) + 1

    class Meta:
        model = Card
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','selection','accept', "organization", 'function',
                 'role', 'fio','id_kpi', 'name', 'kpi_kls2',
                   'method', 'low_level', 'target_level',
                  'high_level', 'weight', 'fact', 'verificator',
                  'comment_func', 'comment_audit', 'comment_audit_AES', 'passport')

class CardTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    counter = tables.Column(empty_values=(), orderable=False, verbose_name="№ п/п")

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count())
        return next(self.row_counter) + 1

    class Meta:
        model = Card
        template_name = "django_tables2/bootstrap.html"
        fields = ('counter','selection', "organization", 'function',
                 'role', 'fio', 'id_kpi', 'name', 'kpi_kls2',
                   'method', 'low_level', 'target_level',
                  'high_level', 'weight', 'passport', 'fact', 'verificator',
                  'comment_func', 'comment_audit', 'comment_audit_AES', 'updated_at')
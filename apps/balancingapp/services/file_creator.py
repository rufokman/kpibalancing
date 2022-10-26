import datetime

import pandas as pd
from django.utils import timezone
from django.shortcuts import get_object_or_404
import xlwt
from django.http import HttpResponse
from ..models import *
import xlsxwriter


def get_update_data():
	card_data = Card.objects.filter(delete=0)
	config_data = get_object_or_404(Config, id=1)
	old_date = config_data.last_download
	config_data.last_download = timezone.now()
	config_data.save(update_fields=['last_download'])
	change_data = Change.objects.filter(update_at__range=(old_date, timezone.now()))

	return card_data, change_data


def download_excel_data(request):

	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="pivot.xlsx"'
	workbook = xlsxwriter.Workbook(response, {'in_memory': True})
	format = workbook.add_format()
	format.set_bg_color('#fdc433')

	ws = workbook.add_worksheet('Реестр')

	ws.set_column('A:A', 5)
	ws.set_column('B:B', 23)
	ws.set_column('C:C', 23, )
	ws.set_column('D:D', 23, )
	ws.set_column('E:E', 26, )
	ws.set_column('F:F', 11, )
	ws.set_column('G:G', 81, )
	ws.set_column('H:H', 16, )
	ws.set_column('I:I', 20, )
	ws.set_column('J:J', 20, )
	ws.set_column('K:K', 30, )
	ws.set_column('L:L', 20, )
	ws.set_column('M:M', 7, )
	ws.set_column('N:N', 17, )
	ws.set_column('O:O', 17, )
	ws.set_column('P:P', 40, )
	ws.set_column('Q:Q', 24, )
	ws.set_column('R:R', 24, )
	ws.set_column('S:S', 24, )
	columns = ['№ пп', 'Организация', 'Функция', 'Название должности',
			   'ФИО сотрудника, в чью карту устанавливается КПЭ',
			   'ID КПЭ в ИС РЕКОРД', 'Наименование КПЭ / КлС', 'КПЭ / КлС2',
			   'Тип КПЭ / КлС (Методика расчета)', 'Нижний уровень', "Целевой уровень",
			   "Верхний уровень", "Вес", "Паспорт", "Факт выполнения", "Инициатор / Верификатор",
			   "Комментарий от функции (по необходимости)",
			   "Комментарии по аудиту (заполняется СУП УК)",
			   "Комментарии по аудиту (заполняется сотрудником АЭС/ДО)",
			   ]
	row_num = 0
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num])
	swap_dict = {0: "Экономика и финансы",
				 1: 'Сооружение',
				 2: 'Международные и новые бизнесы',
				 3: 'Производство',
				 4: "Инвестиционная деятельность",
				 5: "Управление персоналом",
				 6: "Управление качеством",
				 7: "Генеральная инспекция",
				 8: "ФАИП и ГОЗ / КВЛ",
				 9: "Сбыт",
				 10: "Корпоративное управление, Правовое обеспечение, Управление имуществом, Непрофильные активы",
				 11: "Инновационная деятельность",
				 12: "Безопасность",
				 13: "Административное управление",
				 14: "Закупки и МТО",
				 15: "Внутренний контроль и аудит",
				 16: "Бухгалтерия"}
	changed_data = pd.DataFrame(get_update_data()[1].values('name_col', 'id_kpi'))
	if changed_data.shape[0]==0:
		changed_data = pd.DataFrame({'name_col':[],
									 'id_kpi': []},)
	print(changed_data)
	for my_row in get_update_data()[0]:
		row_num = row_num + 1
		ws.write(row_num, 0, row_num)
		if changed_data[(changed_data.name_col=='organization') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:

			ws.write(row_num, 1, my_row.organization, format)
		else:
			ws.write(row_num, 1, my_row.organization)
		if changed_data[(changed_data.name_col=='function') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 2, swap_dict[my_row.function], format)
		else:
			ws.write(row_num, 2, swap_dict[my_row.function])

		if changed_data[(changed_data.name_col=='role') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 3, my_row.role, format)
		else:
			ws.write(row_num, 1, my_row.role)
		if changed_data[(changed_data.name_col=='fio') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 4, my_row.fio, format)
		else:
			ws.write(row_num, 4, my_row.fio)
		if changed_data[(changed_data.name_col=='id_kpi') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 5, my_row.id_kpi, format)
		else:
			ws.write(row_num, 5, my_row.id_kpi)
		if changed_data[(changed_data.name_col=='name') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 6, my_row.name, format)
		else:
			ws.write(row_num, 6, my_row.name)
		if changed_data[(changed_data.name_col=='kpi_kls2') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 7, my_row.kpi_kls2, format)
		else:
			ws.write(row_num, 7, my_row.kpi_kls2)
		if changed_data[(changed_data.name_col=='method') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 8, my_row.method, format)
		else:
			ws.write(row_num, 8, my_row.method)
		if changed_data[(changed_data.name_col=='low_level') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 9, my_row.low_level, format)
		else:
			ws.write(row_num, 9, my_row.low_level)
		if changed_data[(changed_data.name_col=='target_level') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 10, my_row.target_level, format)
		else:
			ws.write(row_num, 10, my_row.target_level)
		if changed_data[(changed_data.name_col=='high_level') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 11, my_row.high_level, format)
		else:
			ws.write(row_num, 11, my_row.high_level)
		if changed_data[(changed_data.name_col=='weight') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 12, my_row.weight, format)
		else:
			ws.write(row_num, 12, my_row.weight)
		if changed_data[(changed_data.name_col=='passport') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 13, "", format)
		else:
			ws.write(row_num, 13, "")
		if changed_data[(changed_data.name_col=='fact') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 14, my_row.fact, format)
		else:
			ws.write(row_num, 14, my_row.fact)
		if changed_data[(changed_data.name_col=='verificator') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 15, my_row.verificator, format)
		else:
			ws.write(row_num, 15, my_row.verificator)
		if changed_data[(changed_data.name_col=='comment_func') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 16, my_row.comment_func, format)
		else:
			ws.write(row_num, 16, my_row.comment_func)
		if changed_data[(changed_data.name_col=='comment_audit') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 17, my_row.comment_audit, format)
		else:
			ws.write(row_num, 17, my_row.comment_audit)
		if changed_data[(changed_data.name_col=='comment_audit_AES') & (changed_data.id_kpi==my_row.id)].shape[0]!=0:
			ws.write(row_num, 18, my_row.comment_audit_AES, format)
		else:
			ws.write(row_num, 18, my_row.comment_audit_AES)
	workbook.close()
	return response
#
# def download_excel_data(request):
# 	data = Card.objects.all()
# 	response = HttpResponse(content_type='application/ms-excel')
# 	response['Content-Disposition'] = 'attachment; filename="pivot.xlsx"'
# 	workbook = xlsxwriter.Workbook(response, {'in_memory': True})
# 	ws = workbook.add_worksheet('Реестр')
# 	# wrap_format = ws.for add_format({'border': 1, 'text_wrap': True, 'align': 'left', 'valign': 'vcenter'})
# 	row_num = 0
# 	columns = ['№ пп', 'Организация', 'Функция', 'Название должности',
# 			   'ФИО сотрудника, в чью карту устанавливается КПЭ',
# 			   'ID КПЭ в ИС РЕКОРД', 'Наименование КПЭ / КлС', 'КПЭ / КлС2',
# 			   'Тип КПЭ / КлС (Методика расчета)', 'Нижний уровень', "Целевой уровень",
# 			   "Верхний уровень", "Вес", "Паспорт", "Факт выполнения", "Инициатор / Верификатор",
# 			   "Комментарий от функции (по необходимости)",
# 			   "Комментарии по аудиту (заполняется СУП УК)",
# 			   "Комментарии по аудиту (заполняется сотрудником АЭС/ДО)",
# 			   ]
#
# 	ws.set_column('A:A', 5)
# 	ws.set_column('B:B', 23)
# 	ws.set_column('C:C', 23, )
# 	ws.set_column('D:D', 23, )
# 	ws.set_column('E:E', 26, )
# 	ws.set_column('F:F', 11, )
# 	ws.set_column('G:G', 81, )
# 	ws.set_column('H:H', 16, )
# 	ws.set_column('I:I', 20, )
# 	ws.set_column('J:J', 20, )
# 	ws.set_column('K:K', 30, )
# 	ws.set_column('L:L', 20, )
# 	ws.set_column('M:M', 7, )
# 	ws.set_column('N:N', 17, )
# 	ws.set_column('O:O', 17, )
# 	ws.set_column('P:P', 40, )
# 	ws.set_column('Q:Q', 24, )
# 	ws.set_column('R:R', 24, )
# 	ws.set_column('S:S', 24, )
#
# 	for col_num in range(len(columns)):
# 		ws.write(row_num, col_num, columns[col_num])
#
# 	for my_row in data:
# 		row_num = row_num + 1
# 		ws.write(row_num, 0, row_num)
# 		ws.write(row_num, 1, my_row.organization)
# 		ws.write(row_num, 2, my_row.function)
# 		ws.write(row_num, 3, my_row.role)
# 		ws.write(row_num, 4, my_row.fio)
# 		ws.write(row_num, 5, "ID КПЭ в ИС РЕКОРД")
# 		ws.write(row_num, 6, my_row.name)
# 		ws.write(row_num, 7, "КПЭ / КлС2")
# 		ws.write(row_num, 8, my_row.method)
# 		ws.write(row_num, 9, my_row.low_level)
# 		ws.write(row_num, 10, my_row.target_level)
# 		ws.write(row_num, 11, my_row.high_level)
# 		ws.write(row_num, 12, my_row.weight)
# 		ws.write(row_num, 13, "Паспорт")
# 		ws.write(row_num, 14, "Факт выполнения")
# 		ws.write(row_num, 15, "Инициатор / Верификатор")
# 		ws.write(row_num, 16, "Комментарий от функции (по необходимости)")
# 		ws.write(row_num, 17, "Комментарии по аудиту (заполняется СУП УК)")
# 		ws.write(row_num, 18, "Комментарии по аудиту (заполняется сотрудником АЭС/ДО)")
#
# 	config_data = get_object_or_404(Config, id=1)
# 	config_data.last_download = datetime.datetime.now()
# 	config_data.save(update_fields=['last_download'])
# 	workbook.close()
#
# 	return response

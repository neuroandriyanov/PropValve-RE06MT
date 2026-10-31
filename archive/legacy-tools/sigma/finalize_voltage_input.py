"""Export the saved, independently verified ADC0 voltage-input calibration."""
import json,shutil
from pathlib import Path
from nrbf_project import Reader
folder=Path('проект_сигма');project=folder/'Design1_parker_v0.dspproj'
def read(path):
    r=Reader(path.read_bytes()).read();tables={};dc={}
    for obj in r.objects.values():
        f=obj.get('fields',{})
        if obj.get('$type')=='ADICtrls.LinearInterpolator':
            tables[r.resolve(f['name'])]={'min':float(r.resolve(f['Min'])),'max':float(r.resolve(f['Max'])),'coefficients':r.resolve(f['values'])['$array']}
        if obj.get('$type')=='ADICtrls.DCHex':dc[r.resolve(f['name'])]=r.resolve(f['textvalue'])
    return tables,dc
tables,dc=read(project);before,_=read(folder/'Design1_parker_before_voltage_input.dspproj')
for key in ['Interpolator1','CURRENT_0_3A','I_FEEDBACK_0_1']:assert tables[key]==before[key],key
assert dc['CURRENT_INPUT_0_1']==0 and dc['DC2_4']==0
table=tables['VIN_TABLE_0_10V'];assert table['min']==-1 and table['max']==1
rows=json.loads(Path('output/meter/voltage_input_verify.json').read_text())
assert len(rows)==11 and all(r['reference_source']=='multimeter' for r in rows)
maxerror=max(abs(r['error_volts']) for r in rows)
(folder/'voltage_input_0_10V.txt').write_text(''.join(f'{v:.12f}\n' for v in table['coefficients']))
settings={'R42_ohms':10000,'sample_rate_hz':96000,'filter_hz':20,'table':table,'normalized_output_limits':[0,1],
          'readback':'VIN_MEAS_0_1','volts_per_normalized_unit':10,'max_observed_difference_from_meter_volts':maxerror,'EEPROM_written':False}
(folder/'voltage_input_settings.json').write_text(json.dumps(settings,indent=2))
doc='''Калибровка входа 0–10 В, ADC0 — 27.10.2026

Пользователь установил перемычку X3–X4 и заменил R42 на 10 кОм.
Калибровка выполнена по подключённому мультиметру в режиме DC V.
Источник: ранее откалиброванный выход X3; измерения — непосредственно
на соединённых X3/X4. Проверены 11 точек, включая промежуточные и повторный ноль.

Рабочий проект: Design1_parker_v0.dspproj.
Контрольная полная копия: Design1_parker_io_calibrated.dspproj.
Загрузка выполнена в RAM, EEPROM не записывалась.

Цепь входа:
Input1, ADC0 -> VIN_LPF_20Hz -> VIN_TABLE_0_10V -> VIN_LIMIT_MIN -> VIN_LIMIT_MAX -> VIN_MEAS_0_1.
ФНЧ: первый порядок, 20 Гц, усиление 0 дБ. При Fs=96 кГц постоянная
времени около 8 мс; установление до 1% после ступени около 37 мс.
VIN_MEAS_0_1 — нормализованный вход: напряжение в вольтах = показание * 10.
ADC0_RAW — несглаженный ADC0; VIN_FILTERED — сглаженный ADC0 до нормализации.
Катушка во время калибровки имела нулевое задание.
Соединение VIN_MEAS_0_1 с заданием тока не добавлялось.

Min таблицы = -1, Max = +1. Это диапазон данных ADC0, а не напряжение X4.
В рабочем диапазоне 0..10 В ADC0 изменялся примерно -0.02050..+0.74948.
Насыщения не обнаружено. Полный диапазон таблицы оставлен для запаса;
её выход отдельно ограничен 0..1 двумя условными блоками.
VIN_ZERO=0, VIN_ONE=1, условие VIN_LIMIT_MIN: >, VIN_LIMIT_MAX: <.
Отрицательные и превышающие 1 коэффициенты на внешних узлах таблицы
являются экстраполяцией и допустимы. Итоговый сигнал ограничен 0..1.

Коэффициенты по узлам ADC0 = -1; -0.5; 0; +0.5; +1:
'''
doc+='\n'.join(f'{-1+i*.5:.2f} -> {v:.12f}' for i,v in enumerate(table['coefficients']))
doc+='\n\nПоследняя независимая проверка:\n'
doc+='\n'.join(f"Мультиметр {r['reference_volts']:.4f} В -> DSP {r['input_norm']:.8f}, эквивалент {r['input_volts']:.5f} В, разность {r['error_volts']*1000:+.3f} мВ" for r in rows)
doc+=f'\nМаксимальная наблюдавшаяся разность с показанием мультиметра: {maxerror*1000:.3f} мВ.\n'
doc+='''Это разность показаний в данной серии, а не оценка абсолютной
погрешности всей системы: она зависит также от точности и разрешения мультиметра.

Предыдущие таблицы выхода 0..10 В, задания 0..3 А и измерения тока
сравнены с резервной копией перед работой: коэффициенты и диапазоны не изменены.
По окончании выход напряжения и задание тока возвращены в ноль.

Файлы:
voltage_input_0_10V.txt — коэффициенты для загрузки таблицы.
voltage_input_settings.json — диапазон, фильтр, ограничения и прочие настройки.
output/meter/voltage_input_raw.json — исходная проверка ADC0.
output/meter/voltage_input_filtered.json — калибровочные точки после ФНЧ.
output/meter/voltage_input_verify.json — независимая проверка нормализованного входа.

Перед будущим пакетным чтением DSP нужно отключать непрерывные индикаторы
(Action -> Disable All Continuous ReadBack Controls, Ctrl+F12).
После программной компиляции API новые индикаторы следует привязать
штатной командой Action -> Link Compile Download (F7), затем Ctrl+F11.
Одноразовые скрипты build/connect/fit_voltage_input.py повторно не запускать.
'''
(folder/'Калибровка_входа_0_10В_2026-10-27.txt').write_text(doc,encoding='utf-8')
shutil.copy2(project,folder/'Design1_parker_io_calibrated.dspproj')
print(json.dumps({'max_difference_mV':maxerror*1000,'preserved_existing_tables':True,'settings':settings,'last_reference_volts':rows[-1]['reference_volts'],'last_norm':rows[-1]['input_norm']},ensure_ascii=False))

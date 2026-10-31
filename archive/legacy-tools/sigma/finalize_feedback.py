"""Export verified current command and measurement settings from saved project."""
import json,shutil
from pathlib import Path
from nrbf_project import Reader
folder=Path('проект_сигма');project=folder/'Design1_parker_v0.dspproj'
r=Reader(project.read_bytes()).read();tables={};source=None
for obj in r.objects.values():
    f=obj.get('fields',{})
    if obj.get('$type')=='ADICtrls.LinearInterpolator':
        name=r.resolve(f['name']);tables[name]={'min':r.resolve(f['Min']),'max':r.resolve(f['Max']),'coefficients':r.resolve(f['values'])['$array']}
    if obj.get('$type')=='ADICtrls.DCHex' and r.resolve(f['name'])=='CURRENT_INPUT_0_1':source=f['textvalue']
assert source==0
assert tables['Interpolator1']['coefficients']==[-.00102,-.077378,-.153747,-.230275,-.306728]
feedback=tables['I_FEEDBACK_0_1'];assert float(feedback['min'])==-.78 and float(feedback['max'])==.70
for name,key in [('current_command_0_3A','CURRENT_0_3A'),('current_feedback_0_3A','I_FEEDBACK_0_1')]:
    (folder/(name+'.txt')).write_text(''.join(f'{v:.12f}\n' for v in tables[key]['coefficients']))
settings={'R43_ohms':10000,'sample_rate_hz':96000,'measurement_lowpass_hz':20,'feedback_input_limits':[-.78,.70],'command':tables['CURRENT_0_3A'],'feedback':feedback,'EEPROM_written':False}
(folder/'current_calibration_settings.json').write_text(json.dumps(settings,indent=2))
rows=json.loads(Path('output/meter/feedback_final_verification.json').read_text())
old_doc=folder/'Калибровка_тока_2026-10-27.txt'
history=folder/'Калибровка_тока_до_замены_R43.txt'
if old_doc.exists() and not history.exists():shutil.copy2(old_doc,history)
doc='''Калибровка тока и обратной связи — 27.10.2026

R43 заменён пользователем: 180 Ом -> 10 кОм.
Рабочий проект: Design1_parker_v0.dspproj.
Контрольная копия: Design1_parker_current_calibrated.dspproj.
Fs=96 кГц. Проект загружен в RAM. EEPROM не записывалась.

CURRENT_INPUT_0_1 — вход задания 0..1, формат 5.23.
CURRENT_0_3A — таблица задания тока, диапазон входа 0..1.
ZERO_OFF — при команде <=0 цифровые задания DAC0/DAC1 равны нулю.
При положительной команде DAC0=таблица(x), DAC1=-таблица(x).
ZERO_CONSTANT должен оставаться равным нулю.

Измерение:
ADC1 -> CURRENT_LPF_20Hz -> FB_LIMIT_MIN -> FB_LIMIT_MAX -> I_FEEDBACK_0_1 -> I_MEAS_0_1.
CURRENT_LPF_20Hz — ФНЧ первого порядка, 20 Гц, усиление 0 дБ.
I_FEEDBACK_0_1 — 5-точечный интерполятор: Min=-0.78, Max=0.70.
FB_LIMIT_MIN/MAX явно ограничивают вход интерполятора диапазоном -0.78..0.70.
Константы FB_MIN_CONST=-0.78, FB_MAX_CONST=0.70 должны совпадать с Min/Max.
I_MEAS_0_1 — нормализованный измеренный ток; амперы = значение * 3.
ADC1_RAW — диагностический несглаженный сигнал ADC1.
Цифровой контур регулирования по I_MEAS_0_1 не замыкался;
аналоговый регулятор тока TL494 продолжает управлять силовой частью.

Коэффициенты задания:
'''
doc+='\n'.join(f'{i/4:.2f} -> {v:.12f}' for i,v in enumerate(tables['CURRENT_0_3A']['coefficients']))
doc+='\n\nКоэффициенты измерения при равномерных узлах от -0.78 до +0.70:\n'
doc+='\n'.join(f'{-.78+1.48*i/4:.3f} -> {v:.12f}' for i,v in enumerate(feedback['coefficients']))
doc+='\n\nНезависимая проверка мультиметром:\n'
doc+='\n'.join(f"Вход {p['input']:.3f}, цель {p['target_amps']:.3f} А, мультиметр {p['meter_amps']:.4f} А, DSP {p['feedback_norm']:.6f} = {p['feedback_amps']:.4f} А" for p in rows)
doc+='''

После замены R43 насыщения ADC1 в диапазоне 0..3 А не обнаружено:
несглаженный сигнал при ~3 А находился примерно от +0.658 до +0.754.
Сглаживание снижает разброс показаний, но не устраняет дрейф нуля.
В одной калибровочной серии нулевой уровень изменился примерно на
0.013 единицы ADC, что эквивалентно ~26 мА.
Фиксированная таблица не компенсирует изменения нуля между сериями.
Приведённая проверка описывает состояние платы во время измерений,
не является гарантией температурной точности после охлаждения/прогрева.
Сам интерполятор не обеспечивает корректного ограничения вне Min/Max:
до добавления FB_LIMIT_MIN/MAX это вызывало ошибочные показания на краях.
Ограничение теперь выполняют отдельные блоки перед интерполятором.
Команда CURRENT_INPUT_0_1 должна подаваться в заявленном диапазоне 0..1.

Полные протоколы: output/meter/feedback_*.json.
Файлы current_command_0_3A.txt и current_feedback_0_3A.txt содержат
только коэффициенты. Диапазоны Min/Max сохранены в проекте и JSON.
Калибровка напряжения DAC3 0..10 В проверена: коэффициенты не изменены.
По окончании команда установлена в ноль.
Одноразовые скрипты install_*.py и refine_feedback.py повторно не запускать.
'''
old_doc.write_text(doc,encoding='utf-8')
shutil.copy2(project,folder/'Design1_parker_current_calibrated.dspproj')
print(json.dumps({'settings':settings,'last_measurement':rows[-1],'max_command_error_amps':max(abs(p['command_error_amps']) for p in rows),'max_feedback_error_amps':max(abs(p['feedback_error_amps']) for p in rows)},ensure_ascii=False))

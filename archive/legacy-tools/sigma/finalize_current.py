"""Export the saved coefficients and preserve the verified project snapshot."""
import json,shutil
from pathlib import Path
from nrbf_project import Reader
p=Path('проект_сигма/Design1_parker_v0.dspproj')
r=Reader(p.read_bytes()).read();tables={}
for obj in r.objects.values():
    if obj.get('$type')=='ADICtrls.LinearInterpolator':
        f=obj['fields'];name=r.resolve(f['name'])
        tables[name]=r.resolve(f['values'])['$array']
assert tables['Interpolator1']==[-.001020,-.077378,-.153747,-.230275,-.306728]
coeff=tables['CURRENT_0_3A'];assert len(coeff)==5
Path('проект_сигма/current_command_0_3A.txt').write_text(''.join(f'{v:.9f}\n' for v in coeff))
readings=json.loads(Path('output/meter/current_verification.json').read_text())
maxerror=max(abs(v['error_amps']) for v in readings)
report='''Калибровка тока 27.10.2026 — предварительная

Рабочий проект: Design1_parker_v0.dspproj
Копия: Design1_parker_current_preliminary.dspproj
Частота DSP: 96 кГц. Загрузка выполнена в RAM; EEPROM не записывалась.

CURRENT_INPUT_0_1: вход задания 0..1, формат 5.23.
CURRENT_0_3A: линейный интерполятор, Min=0, Max=1, 5 точек.
ZERO_OFF: при входе <=0 оба цифровых задания DAC0/DAC1 равны нулю.
При входе >0: DAC0=таблица(x), DAC1=-таблица(x).
ZERO_CONSTANT должен оставаться равным 0.

Таблица задания:
'''
report+='\n'.join(f'{i/4:.2f} -> {v:.9f}' for i,v in enumerate(coeff))
report+='\n\nПоследняя независимая проверка мультиметром:\n'
report+='\n'.join(f"x={v['input']:.3f}: задание {v['target_amps']:.3f} А, измерено {v['amps']:.3f} А, ADC1={v['adc1_raw']:.6f}" for v in readings)
report+=f'\nМаксимальное отклонение: {maxerror:.3f} А.\n'
report+='''
Обнаружен медленный дрейф тока при прогреве. Статическая таблица его не устраняет.
По окончании установлено задание 0; мультиметр показал 0.000 А.

ОБРАТНАЯ СВЯЗЬ НЕ ОТКАЛИБРОВАНА:
ADC1 при нулевом токе выдаёт -1, при верхних токах +0.999998.
R43=180 Ом. Потерянную из-за насыщения информацию таблицей восстановить нельзя.
ADC1_RAW_PENDING_R43 сейчас выполняет тождественное преобразование -1..1,
а FB_NOT_CALIBRATED показывает сырой ADC1, НЕ нормированный ток.

Следующий аппаратный шаг: при отключённом питании заменить R43 на 10 кОм.
Затем заново измерить диапазон ADC1, проверить отсутствие насыщения и
откалибровать его интерполятор: 0 А -> 0, 3 А -> 1.
Проверить пульсации; для показаний среднего тока потребуется усреднение.

Калибровка напряжения DAC3 0..10 В сохранена без изменения коэффициентов.
Протоколы измерений находятся в output/meter/current_*.json.
tools/sigma/install_*.py — одноразовые скрипты сборки, повторно не запускать.
'''
Path('проект_сигма/Калибровка_тока_2026-10-27.txt').write_text(report,encoding='utf-8')
shutil.copy2(p,'проект_сигма/Design1_parker_current_preliminary.dspproj')
print(json.dumps({'coefficients':coeff,'max_error_amps':maxerror,'voltage_table_unchanged':True,'last_meter_amps':readings[-1]['amps']},ensure_ascii=False))

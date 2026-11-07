# English guide to the original BOM workbook

[Hardware](README.en.md) · [English workbook](Спецификация_для_пайк.en.xlsx) · [Russian original](Спецификация_для_пайк.xlsx)

This companion records every Russian cell label and note with its original sheet and cell address. The English workbook translates these cells, all three sheet names, and printed headers and footers. Numerical values, formula logic, cached results, links, reference designators and purchasing assumptions remain those of the original; references to renamed sheets are updated. Prices are historical estimates dated 20 September 2026, not current quotations. R42/R43 remain 180 Ω in this historical BOM; the working calibration requires 10 kΩ as explained in the hardware notes.

Source SHA256: `fd7d7ce15a02bc9ff0ae32e6ad3d1971385cc432c43b1d2ab8f9043551ba51b0`.

## Sheet 1: Порядок пайки — Soldering order

| Cell | Original label or note | English |
| --- | --- | --- |
| A1 | № пакета | Packet no. |
| B1 | Метки | Reference designators |
| C1 | Значение | Value |
| D1 | Тип | Type |
| E1 | Кол-во | Quantity |
| F1 | Цена/шт, ₽ | Unit price, RUB |
| G1 | Стоимость, ₽ | Cost, RUB |
| H1 | Спаяно | Soldered |
| A2 | 1. Резисторы и конденсаторы 0805 | 1. 0805 resistors and capacitors |
| A14 | 2. Мелкие диоды и транзисторы | 2. Small diodes and transistors |
| A18 | 3. Резисторы и конденсаторы 1206 | 3. 1206 resistors and capacitors |
| A34 | 4. Конденсаторы 1210 | 4. 1210 capacitors |
| A36 | 5. Микросхемы и генератор | 5. ICs and oscillator |
| A47 | 6. Защитные и выводные диоды | 6. Protection and through-hole diodes |
| A54 | 7. Силовые элементы и оптодрайвер | 7. Power components and optocoupled driver |
| C55 | 330 2ВТ | 330 ohm, 2 W |
| D55 | 330 2ВТ | 330 ohm, 2 W |
| A60 | 8. Разъёмы и кнопка | 8. Connectors and pushbutton |
| A65 | 9. Электролиты и модуль питания | 9. Electrolytic capacitors and power module |
| B70 | Итого: элементы и ориентировочная стоимость | Total: components and estimated cost |

## Sheet 2: Исходные данные — Source data

| Cell | Original label or note | English |
| --- | --- | --- |
| A1 | Метка | Reference designator |
| B1 | Значение | Value |
| C1 | Тип | Type |
| B92 | 330 2ВТ | 330 ohm, 2 W |
| C92 | 330 2ВТ | 330 ohm, 2 W |

## Sheet 3: Цены и источники — Prices and sources

| Cell | Original label or note | English |
| --- | --- | --- |
| A1 | Ориентировочные цены комплектующих | Estimated component prices |
| A2 | Проверено 20.09.2026. Цены за 1 шт.; без доставки, налогов, пошлин и наценок посредников. | Checked on 20 September 2026. Prices per unit; excluding shipping, taxes, duties and intermediary markups. |
| C3 | Курс ЦБ с 19.09.2026: https://www.cbr.ru/currency_base/daily/ | Central Bank exchange rate effective 19 September 2026: https://www.cbr.ru/currency_base/daily/ |
| A4 | «Каталог» — найденная цена выбранного исполнения. «Оценка» — предположение; «Оценка по серии» — цена похожего номинала. | Catalogue: a located price for the selected variant. Estimate: an assumption. Series estimate: a price for a similar value in the series. |
| A5 | Подбор исполнения служит только для оценки стоимости; метки, номиналы и типы в спецификации не заменены. | Variants were selected only to estimate cost; reference designators, values and types in the BOM were not replaced. |
| A7 | № пакета | Packet no. |
| B7 | Товар для оценки | Product used for estimate |
| C7 | Цена источника | Source price |
| D7 | Валюта | Currency |
| E7 | Цена/шт, ₽ | Unit price, RUB |
| F7 | Основание | Basis |
| G7 | Пояснение | Explanation |
| H7 | Источник | Source |
| B8 | Точный артикул не подобран | Exact part number not selected |
| F8 | Оценка | Estimate |
| G8 | Оценка для 3,3 нФ / 25 В / 0805; диэлектрик и допуск не заданы. | Estimate for 3.3 nF / 25 V / 0805; dielectric and tolerance unspecified. |
| H8 | Цена магазина не подтверждена | Retailer price not confirmed |
| B9 | Точный артикул не подобран | Exact part number not selected |
| F9 | Оценка | Estimate |
| G9 | Оценка для 56 нФ / 25 В / 0805; диэлектрик и допуск не заданы. | Estimate for 56 nF / 25 V / 0805; dielectric and tolerance unspecified. |
| H9 | Цена магазина не подтверждена | Retailer price not confirmed |
| F10 | Каталог | Catalogue |
| G10 | 100 нФ, 25 В, 0805, X7R, ±10%; пример исполнения для оценки. | 100 nF, 25 V, 0805, X7R, ±10%; example variant for estimating cost. |
| F11 | Каталог | Catalogue |
| G11 | 10 мкФ, 25 В, 0805, X5R; пример исполнения. Нет в наличии на странице. | 10 µF, 25 V, 0805, X5R; example variant. Listed as unavailable on the page. |
| B12 | RC0805FR-071KL (1 кОм) | RC0805FR-071KL (1 kΩ) |
| F12 | Оценка по серии | Series estimate |
| G12 | Ориентир по резистору 1 кОм серии 0805; цена именно номинала 51 не подтверждена. | Reference based on a 1 kΩ 0805 resistor; price for the exact value 51 not confirmed. |
| B13 | RC0805FR-071KL (1 кОм) | RC0805FR-071KL (1 kΩ) |
| F13 | Оценка по серии | Series estimate |
| G13 | Ориентир по резистору 1 кОм серии 0805; цена именно номинала 475 не подтверждена. | Reference based on a 1 kΩ 0805 resistor; price for the exact value 475 not confirmed. |
| B14 | RC0805FR-071KL (1 кОм) | RC0805FR-071KL (1 kΩ) |
| F14 | Каталог | Catalogue |
| G14 | Цена за 1 шт.; скидки за количество не применены. | Price per unit; quantity discounts not applied. |
| B15 | RC0805FR-071KL (1 кОм) | RC0805FR-071KL (1 kΩ) |
| F15 | Оценка по серии | Series estimate |
| G15 | Ориентир по резистору 1 кОм серии 0805; цена именно номинала 2.2K не подтверждена. | Reference based on a 1 kΩ 0805 resistor; price for the exact value 2.2K not confirmed. |
| B16 | RC0805FR-071KL (1 кОм) | RC0805FR-071KL (1 kΩ) |
| F16 | Оценка по серии | Series estimate |
| G16 | Ориентир по резистору 1 кОм серии 0805; цена именно номинала 10K не подтверждена. | Reference based on a 1 kΩ 0805 resistor; price for the exact value 10K not confirmed. |
| B17 | RC0805FR-071KL (1 кОм) | RC0805FR-071KL (1 kΩ) |
| F17 | Оценка по серии | Series estimate |
| G17 | Ориентир по резистору 1 кОм серии 0805; цена именно номинала 18K не подтверждена. | Reference based on a 1 kΩ 0805 resistor; price for the exact value 18K not confirmed. |
| B18 | RC0805FR-071KL (1 кОм) | RC0805FR-071KL (1 kΩ) |
| F18 | Оценка по серии | Series estimate |
| G18 | Ориентир по резистору 1 кОм серии 0805; цена именно номинала 100K не подтверждена. | Reference based on a 1 kΩ 0805 resistor; price for the exact value 100K not confirmed. |
| F19 | Каталог | Catalogue |
| G19 | Нет в наличии на странице; цена под заказ. | Listed as unavailable on the page; backorder price. |
| F20 | Каталог | Catalogue |
| G20 | Производитель в исходнике не задан; пример цены BAV99. | Manufacturer unspecified in the source; example BAV99 price. |
| F21 | Каталог | Catalogue |
| B22 | Точный артикул не подобран | Exact part number not selected |
| F22 | Оценка | Estimate |
| G22 | Оценка для 0,01 мкФ / 25 В / 1206; диэлектрик и допуск не заданы. | Estimate for 0.01 µF / 25 V / 1206; dielectric and tolerance unspecified. |
| H22 | Цена магазина не подтверждена | Retailer price not confirmed |
| B23 | Точный артикул не подобран | Exact part number not selected |
| F23 | Оценка | Estimate |
| G23 | Оценка для 0,03 мкФ / 25 В / 1206. Номинал 0,03 сохранён; не заменён на 0,033. | Estimate for 0.03 µF / 25 V / 1206. The 0.03 value is retained, not replaced with 0.033. |
| H23 | Цена магазина не подтверждена | Retailer price not confirmed |
| B24 | Точный артикул не подобран | Exact part number not selected |
| F24 | Оценка | Estimate |
| G24 | Оценка для 0,1 мкФ / 25 В / 1206; диэлектрик и допуск не заданы. | Estimate for 0.1 µF / 25 V / 1206; dielectric and tolerance unspecified. |
| H24 | Цена магазина не подтверждена | Retailer price not confirmed |
| F25 | Каталог | Catalogue |
| G25 | 47 мкФ, 25 В, 1206, X5R; пример исполнения. Нет в наличии на странице. | 47 µF, 25 V, 1206, X5R; example variant. Listed as unavailable on the page. |
| B26 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F26 | Оценка по серии | Series estimate |
| G26 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 10 не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 10 not confirmed. |
| B27 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F27 | Оценка по серии | Series estimate |
| G27 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 180 не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 180 not confirmed. |
| B28 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F28 | Каталог | Catalogue |
| G28 | Цена за 1 шт.; скидки за количество не применены. | Price per unit; quantity discounts not applied. |
| B29 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F29 | Оценка по серии | Series estimate |
| G29 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 2K не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 2K not confirmed. |
| B30 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F30 | Оценка по серии | Series estimate |
| G30 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 10K не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 10K not confirmed. |
| B31 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F31 | Оценка по серии | Series estimate |
| G31 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 14K не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 14K not confirmed. |
| B32 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F32 | Оценка по серии | Series estimate |
| G32 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 20K не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 20K not confirmed. |
| B33 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F33 | Оценка по серии | Series estimate |
| G33 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 25K не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 25K not confirmed. |
| B34 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F34 | Оценка по серии | Series estimate |
| G34 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 30K не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 30K not confirmed. |
| B35 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F35 | Оценка по серии | Series estimate |
| G35 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 51K не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 51K not confirmed. |
| B36 | RC1206FR-071KL (1 кОм) | RC1206FR-071KL (1 kΩ) |
| F36 | Оценка по серии | Series estimate |
| G36 | Ориентир по резистору 1 кОм серии 1206; цена именно номинала 100K не подтверждена. | Reference based on a 1 kΩ 1206 resistor; price for the exact value 100K not confirmed. |
| F37 | Каталог | Catalogue |
| G37 | 10 мкФ, 50 В, 1210, X7R; пример исполнения. Нет в наличии на странице. | 10 µF, 50 V, 1210, X7R; example variant. Listed as unavailable on the page. |
| F38 | Каталог | Catalogue |
| G38 | Для оценки взят TSSOP-8; корпус 24LC512 в исходнике не указан. | TSSOP-8 selected for the estimate; 24LC512 package unspecified in the source. |
| B39 | Точный артикул не подобран | Exact part number not selected |
| F39 | Оценка | Estimate |
| G39 | Оценка цены 74LVC1G125GV; предложение с подтверждённой ценой не найдено. | Estimated 74LVC1G125GV price; no offer with a confirmed price was found. |
| H39 | Цена магазина не подтверждена | Retailer price not confirmed |
| F40 | Каталог | Catalogue |
| G40 | Для оценки взято исполнение 5 А; в спецификации указан только ACS712. | 5 A variant selected for the estimate; the BOM specifies only ACS712. |
| F41 | Каталог | Catalogue |
| F42 | Каталог | Catalogue |
| G42 | Для оценки взято исполнение SOT-143-4. | SOT-143-4 variant selected for the estimate. |
| F43 | Каталог | Catalogue |
| G43 | Для оценки взят суффикс EC-T; полный суффикс в исходнике отсутствует. | EC-T suffix selected for the estimate; full suffix absent from the source. |
| F44 | Каталог | Catalogue |
| G44 | Нет в наличии на странице; цена под заказ. | Listed as unavailable on the page; backorder price. |
| F45 | Каталог | Catalogue |
| F46 | Каталог | Catalogue |
| G46 | Для оценки взят SOIC-8; полный суффикс отсутствует. Нет в наличии на странице. | SOIC-8 selected for the estimate; full suffix absent. Listed as unavailable on the page. |
| F47 | Каталог | Catalogue |
| G47 | Для оценки взят SOIC-16; корпус в исходнике не указан. | SOIC-16 selected for the estimate; package unspecified in the source. |
| F48 | Каталог | Catalogue |
| F49 | Каталог | Catalogue |
| F50 | Каталог | Catalogue |
| F51 | Каталог | Catalogue |
| F52 | Каталог | Catalogue |
| G52 | Цена для объединённых по указанию пользователя D9 и D15. | Price for D9 and D15 combined at the user's request. |
| B53 | Точный артикул не подобран | Exact part number not selected |
| F53 | Оценка | Estimate |
| G53 | Оценка SR540; цена точного артикула в магазине не подтверждена. | SR540 estimate; retailer price for the exact part number not confirmed. |
| H53 | Цена магазина не подтверждена | Retailer price not confirmed |
| B54 | Точный артикул не подобран | Exact part number not selected |
| F54 | Оценка | Estimate |
| G54 | Оценка резистора 330 Ом, 2 Вт; материал и допуск не заданы. | Estimate for a 330 Ω, 2 W resistor; material and tolerance unspecified. |
| H54 | Цена магазина не подтверждена | Retailer price not confirmed |
| F55 | Каталог | Catalogue |
| G55 | Для оценки взят DIP-8; суффикс в исходнике не указан. | DIP-8 selected for the estimate; suffix unspecified in the source. |
| F56 | Каталог | Catalogue |
| G56 | Для оценки взято 5 В, TO-220; напряжение и корпус уточнить. Нет в наличии на странице. | 5 V, TO-220 selected for the estimate; voltage and package need confirmation. Listed as unavailable on the page. |
| F57 | Каталог | Catalogue |
| G57 | Tayda Electronics; суффикс -08 взят для оценки. | Tayda Electronics; suffix -08 selected for the estimate. |
| F58 | Каталог | Catalogue |
| G58 | eBay, flex-direct: лот 2 шт. за $14,40. В смете учтена 1 шт.; покупка лота дороже. | eBay, flex-direct: lot of 2 for $14.40. The estimate includes 1 unit; buying the lot costs more. |
| B59 | Точный артикул не подобран | Exact part number not selected |
| F59 | Оценка | Estimate |
| G59 | Оценка клеммника DG103-02P; шаг и точное исполнение уточнить. | DG103-02P terminal-block estimate; pitch and exact variant need confirmation. |
| H59 | Цена магазина не подтверждена | Retailer price not confirmed |
| B60 | Точный артикул не подобран | Exact part number not selected |
| F60 | Оценка | Estimate |
| G60 | Оценка IDC10; тип, шаг и ориентация разъёма не заданы. | IDC10 estimate; connector type, pitch and orientation unspecified. |
| H60 | Цена магазина не подтверждена | Retailer price not confirmed |
| B61 | Точный артикул не подобран | Exact part number not selected |
| F61 | Оценка | Estimate |
| G61 | Оценка KLS7-TS6601-4.3-180; цена магазина не подтверждена. | KLS7-TS6601-4.3-180 estimate; retailer price not confirmed. |
| H61 | Цена магазина не подтверждена | Retailer price not confirmed |
| B62 | Точный артикул не подобран | Exact part number not selected |
| F62 | Оценка | Estimate |
| G62 | Бюджетный резерв на разъём. SWD1 — недостаточное обозначение для подбора товара. | Budget allowance for a connector. SWD1 is insufficient to select a product. |
| H62 | Цена магазина не подтверждена | Retailer price not confirmed |
| B63 | Точный артикул не подобран | Exact part number not selected |
| F63 | Оценка | Estimate |
| G63 | Оценка 220 мкФ, 50 В, радиальный электролит; размеры и серия не заданы. | Estimate for a 220 µF, 50 V radial electrolytic; dimensions and series unspecified. |
| H63 | Цена магазина не подтверждена | Retailer price not confirmed |
| B64 | Точный артикул не подобран | Exact part number not selected |
| F64 | Оценка | Estimate |
| G64 | Оценка 680 мкФ, 50 В, радиальный электролит; размеры и серия не заданы. | Estimate for a 680 µF, 50 V radial electrolytic; dimensions and series unspecified. |
| H64 | Цена магазина не подтверждена | Retailer price not confirmed |
| B65 | Точный артикул не подобран | Exact part number not selected |
| F65 | Оценка | Estimate |
| G65 | Оценка 1000 мкФ, 50 В, радиальный электролит; размеры и серия не заданы. | Estimate for a 1000 µF, 50 V radial electrolytic; dimensions and series unspecified. |
| H65 | Цена магазина не подтверждена | Retailer price not confirmed |
| F66 | Каталог | Catalogue |

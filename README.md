# Stock Price By Financials:  Создание модели для определения стоимости акции на основе ее финансовых показателей

## Введение

### Цель и основная идея работы

Идея данного проэкта является создания модели машинного обучения для определенния истинной стоимости компании. На рынке ценных бумаг часто можно заметить акции, цена которых значительно изменяется в течении непродолжительного временного промежутка, обычно это может быть связано с объективными и значительными изменениями в бизнесе компании, тем не менее не редки случаи когда акция компании получает черезмерную и необъективную популярность, или же наоборот, когда компания показывает хороший уровень отчетности, акции которой по каким то причинам не являются желланым приобретением у инвесторов, иногда такие акции являются идеальным вложением с перспективой на время, когда другие инвесторы так же заметят недооцененность акции. Поиск именно нахождение таких (недооценынных или же переоцененных) акций является основной целью данной работы.

### Тестирование модели
Тестирование и подбор лучших моделей будет проходить в способ "псевдо" инвестирования в акции (на срок в 1 год), цена которых модель посчитала необъективной, после чего программа учтёт изменение цен акций на следующий год и мы получим годовой доход этой модели. И в конце, записав результаты всех моделей во всех секторах, а так же определив из них 7 наилучших, создать список инвестиций каждой модели на 2024 год.

### Возможность реализации

   В реализации проета есть несколько неоднозначных моментов которые следует учитывать.

1. Основная цель обучении модели состоит в сопоставлении финансовых показателей компании с ценой ее акции, таким образом в лучшем случае модель в состоянии найти акцию, цена которой значительно отличается от других акций, при этом имея схожее с ними финансовое положение. Таким образом модель не в состоянии показать степень перегретости рынка и принимает цены акций на рынке как объективный показатель, пытаясь найти акции цена которых выделяется.
   
2. К большому сожалению сайт finance.yahoo предостовляет только 4 последних финансовых отчетностей, в связи с этим в проекте точность модели определяется только по краткосрочным инвестициям (1 год).  
   
3. Данные в проекте актуальны только на 2024 год, в последующем желательно обновить данные и возможно определить новые наилучшие модели.

## Выполнение проекта

### Сбор данных

Для обучения и тестирования моделей нужно получить доступ к ценам и финансовым отчетностям компаний. Для этого я использовал сервис finance.yahoo, а также библиотеку YFinance. Для начала стоило определить какие именно сектора а также компании использовать для обучения, для этого я спарсил данные на сайте macrotrends для получения тикеров компаний, а также их групировки по секторам для увеличения ефективности моделей. (Скрипт находится в файле data_collect.py)



## Итоги

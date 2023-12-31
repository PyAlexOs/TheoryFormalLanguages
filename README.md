# Theory of formal languages
## Table of contents
- [Курсовая работа](#курсовая-работа "Курсовая работа")
- [Практическая работа №1-2](#преобразователь-выражения-в-обратную-польскую-запись "преобразователь выражения в обратную польскую запись")
- [Практическая работа №3](#лексический-анализатор-на-базе-конечного-автомата "Лексический анализатор на базе конечного автомата")
- [Практическая работа №4](#преобразователь-недетерминированного-конечного-автомата-нка-в-детерминированный-дка "Преобразователь недетерминированного конечного автомата (НКА) в детерминированный (ДКА)")
- [Практическая работа №5](#простой-анализатор-json-файла-с-использованием-flex "Простой анализатор JSON файла с использованием FLEX")

---

## Курсовая работа
> **Разработка распознавателя модельного языка программирования.**

> [Распознаватель](course_work/main.py) модельного языка программирования, [описанного РБНФ](course_work/language_files/language_grammar.txt),
> состоит из лексического, синтаксического и семанического анализаторов, последние два из которых
> объединены.
> 
> [Лексический анализатор](course_work/tokenizer.py) разбивает исходный текст программы
> на модельном языке на последовательность лексем – минимальных элементов программы, несущих смысловую нагрузку.
> 
> [Синтаксический анализатор](course_work/parser.py) (объединён с семантическим) проверяет текст исходной программы на
> синтаксическую правильность, а также на соответствие типов при присваивании, выполнении операций, сравнении, описании
> предиката; проверяет была ли объявлена переменная до использования, и, если переменная используется в вычислениях или
> присваивается другой переменной, была ли она инициализирована.
> 
> Для реализации распознавателя используются [дополнительные модули](course_work/tools):
> - [Модуль](course_work/tools/structures.py), в котором описаны все существующие типы токенов
> (лексем), они делятся на несколько основных групп:
>   - Числа и идентификаторы
>   - Ключевые слова (end, dim, as, if, then, else, for, to, do, while, read, write, or, and, not, true, false);
>   - Разделители (<>, =, <, <=, \>, \>=, \[, ], (, ), ",", :, \n, +, -, *, /, {, }).
> - Также в данном модуле описаны структуры данных:
>  - Token - для более удобной работы с токенами (лексемами)
>    - Identifier - для более удобной работы с идентификаторами
> - Кроме вышеперечисленного, содержит матрицу двуместных операторов для обработки операций на этапе семантического анализа.
> - [Модуль](course_work/tools/tokenQueue.py), в котором определена структура данных очередь токенов для
> удобной работы с токенами (лексемами) на этапе синтаксического и семантического анализа, а также для записи токенов
> в файл и восстановления токенов из файла.
> - [Модуль](course_work/tools/file_methods.py) для записи токенов в файл и восстановления токенов из файла. Модуль
> предоставляет возможность записи токенов в файл и восстановления токенов в памяти из файла. Возможен выбор кодировки
> файла (по умолчанию: utf-8). Поддерживаемые форматы файла для ввода и вывода токенов:
>  * .json
>  * .tokenlist
> - [Модуль](course_work/tools/exceptions.py), описывающий виды ошибок языка программирования. Все виды ошибок
> для создания иерархии и удобства отлавливания унаследованы от ModelLanguageError, который в свою очередь
> унаследован от BaseException

> Запустить можно в среде разработки или из консоли:
> - Linux:
> ```commandline
> python3 ./course_work/main.py file_name
> ```
> - Windows:
> ```commandline
> python ./course_work/main.py file_name
> ```
> В папке с файлом ```file_name``` будет создан промежуточный файл с токенами (.json или .tokenlist).

---

## Преобразователь выражения в обратную польскую запись
> [Задание](1-2PR.py) реализовано с возможностью подставновки переменных для вычисления выражения.

---

## Лексический анализатор на базе конечного автомата
> [Лексический анализатор](3PR.py) на базе конечного автомата входного языка, 
> описанного на Рисунке. Обрабатывает текст из [файла](files/test.txt) разбивая
> лексемы по классам.

![machine](files/img.git.png)

---

## Преобразователь недетерминированного конечного автомата (НКА) в детерминированный (ДКА)
> После ввода множества состояний, множества входных состояний,
> множества конечных состояний, алфавита и функции переходов
> недетерминированного конечного автомата [преобразует](4PR.py) его в детерминированный
> конечный автомат и создаёт [графы](files/dependency_graphs) НКА и ДКА на языке Graphviz.

---

## Простой анализатор JSON файла с использованием FLEX
> [Обработка](5PR) несуществующей лексемы: вывести лексему без соотношения
> к определенному классу токенов. 
>
> Лексемы:
> * символы
>  * BEGIN_OBJECT ( { ); 
>  * END_OBJECT ( } ); 
>  * BEGIN_ARRAY ( [ ); 
>  * END_ARRAY ( ] ); 
>  * COMMA ( , ); 
>  * COLON ( : ); 
> * литералы 
>  * LITERAL ( true, false, null); 
> * строки 
>  * STRING ( “string” ); 
> * числа 
>  * NUMBER ( 1, -1, +1, 1e1000 ).

---

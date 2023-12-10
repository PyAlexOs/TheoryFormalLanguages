# Theory of formal languages
### Преобразователь выражения в обратную польскую запись (постфиксную)
> [Задание](1-2PR.py) реализовано с возможностью подставновки переменных для вычисления выражения.

---

### Лексический анализатор на базе конечного автомата входного языка
> [Лексический анализатор](3PR.py) на базе конечного автомата входного языка, 
> описанного на Рисунке. Обрабатывает текст из [файла](files/test.txt) разбивая
> лексемы по классам.

![machine](files/img.git.png)

---

### Преобразователь недетерминированного конечного автомата (НКА) в детерминированный (ДКА).
> После ввода множества состояний, множества входных состояний,
> множества конечных состояний, алфавита и функции переходов
> недетерминированного конечного автомата [преобразует](4PR.py) его в детерминированный
> конечный автомат и создаёт [графы](files/dependency_graphs) НКА и ДКА на языке Graphviz.

---

### Простой анализатор JSON файла с использованием FLEX
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

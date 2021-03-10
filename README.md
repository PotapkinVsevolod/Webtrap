# Webtrap

![GitHub main code](https://img.shields.io/github/languages/top/PotapkinVsevolod/Webtrap)
![GitHub repo size](https://img.shields.io/github/repo-size/potapkinvsevolod/Webtrap)

Webtrap - простейшее веб-приложение, отвечающее следующим функциям:
* возвращение 200 статуса, не зависимо от исхода обработки входных данных запроса
* логирование всех входящих запросов
* логирование запросов с методом, отличным от GET, как ошибку
* запрос с параметром invalid = 1 логировать, как ошибку
* запросы на путь, отличный от /api логировать как ошибку
* обработка запроса на /api:
```
def query(request):
...здесь логгируем изначальный запрос...
...здесь проверки на метод, путь и необходимая обработка...
   process1(request)
   process2(request)
   process3(request)
```
* реализация методов processX любая, отличная от полезной нагрузки, должна делаться соответствующая лог-запись
* в process2, в случае если был передан параметр notawaiting=1, валидация должна вызывать ошибку и соответствующе логгироваться.

## Необходимые условия

Прежде чем начать, убедитесь, что на вашем компьютере установлены:
* Python 3 (проект сделан на Python 3.8.5).
* Git

## Установка Webtrap

Для установки Webtrap, клонируйте репозиторий с github с помощью ссылки:

```
git clone https://github.com/PotapkinVsevolod/Webtrap.git
```
Для работы приложения необходимо установить все необходимые зависимости из файла requirements.txt.

## Использование Webtrap
Приложение можно запустить следующей командой
```
python webtrap.py --port=port_number
```
где port_number - порт, на котором будет работать web-приложение

## Примеры обращения к API.
```
curl -X GET 'http://localhost:port/api'
```
вернет OK, 200 статус код и соответствующие записи в main.log

## Контакты

Если возникли какие-либо вопросы, вы можете со мной связаться, написав на <potapkinvsevolod@gmail.com>.

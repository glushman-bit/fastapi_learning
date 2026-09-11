Запуск приложения:

```bash
uvicorn app.main:app --reload
```


### 1. Активируй Poetry-окружение

Если используешь Poetry:
```bash
poetry shell
```

Если poetry shell у тебя не настроен, можно запускать через:
```bash
poetry run uvicorn app.main:app --reload
```
### 2. Запусти сервер
```bash
uvicorn app.main:app --reload
```
После этого увидишь примерно:
```
Uvicorn running on http://127.0.0.1:8000
```
Открывай:
```
http://127.0.0.1:8000/docs
```
Если сервер уже запущен

В окне терминала, где он работает, нажми:
```textmate
Ctrl + C
```
Затем снова:
```bash
uvicorn app.main:app --reload
```
Но поскольку у тебя стоит --reload, после изменения main.py сервер обычно перезапускается сам. Для нашего ValueError handler достаточно сохранить файл и повторить POST-запрос.
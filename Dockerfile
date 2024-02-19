# Используем образ Python
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости и устанавливаем их
RUN pip install flask

# Копируем все файлы проекта в рабочую директорию контейнера
COPY new_oop_stats.py ./
COPY templates/ ./templates/

# Указываем команду для запуска приложения
CMD ["python", "new_oop_stats.py"]

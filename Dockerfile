# Используем базовый образ Python
FROM python:3.8

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы вашего бота в контейнер
COPY . .

# Запускаем ваш бот
CMD ["python", "main.py"]

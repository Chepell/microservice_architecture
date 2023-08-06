import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
np.random.seed(42)

# Загружаем датасет о диабете
X, y = load_diabetes(return_X_y=True)
# Формируем случайный индекс строки
random_row = np.random.randint(0, X.shape[0]-1)
features, y_true = X[random_row], y[random_row]

# Подключение к серверу на локальном хосте:
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создаём очереди
channel.queue_declare(queue='y_true')
channel.queue_declare(queue='features')

# Публикуем сообщение в очереди
channel.basic_publish(exchange='',
                      routing_key='y_true',
                      body=json.dumps(y_true))
print('Сообщение с правильным ответом отправлено в очередь y_true')

channel.basic_publish(exchange='',
                      routing_key='features',
                      body=json.dumps(list(features)))
print('Сообщение с вектором признаков отправлено в очередь features')

# Закрываем подключение
connection.close()
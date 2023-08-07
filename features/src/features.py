import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
import time
from datetime import datetime
np.random.seed(42)

while True:
    try:
        # Загружаем датасет о диабете
        X, y = load_diabetes(return_X_y=True)
        # Формируем случайный индекс строки
        random_row = np.random.randint(0, X.shape[0]-1)
        features, y_true = X[random_row], y[random_row]

        # Подключение к серверу на локальном хосте:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Создаём очереди
        channel.queue_declare(queue='y_true')
        channel.queue_declare(queue='features')

        time.sleep(3)
        message_id = datetime.timestamp(datetime.now())
        
        message_y_true = {'id': message_id,
                          'body': y_true
                          }
        # Публикуем сообщение в очереди
        channel.basic_publish(exchange='',
                            routing_key='y_true',
                            body=json.dumps(message_y_true))
        print('Сообщение с правильным ответом отправлено в очередь y_true')

        message_features = {'id': message_id,
                          'body': list(features)
                          }        
        channel.basic_publish(exchange='',
                            routing_key='features',
                            body=json.dumps(message_features))
        print('Сообщение с вектором признаков отправлено в очередь features')

        # Закрываем подключение
        connection.close()
    except:
        print('Не удалось подключиться к очереди')
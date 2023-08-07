import pika
import pickle
import numpy as np
import json


# Читаем файл с сериализованной моделью
with open('myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

try:
    # Создаём подключение к серверу на локальном хосте:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')

    # Создаём функцию callback для обработки данных из очереди y_pred
    def callback(ch, method, properties, msg):
        msg_dict = json.loads(msg)
        features = np.array(msg_dict['body']).reshape(1, -1)
        message_id = msg_dict['id']
        prediction = regressor.predict(features)[0]
        
        message_pred = {'id': message_id,
                            'body': prediction
                          }  
        # Публикуем сообщение в очередь y_pred
        channel.basic_publish(exchange='',
                            routing_key='y_pred',
                            body=json.dumps(message_pred))
        print(f'Предсказание {prediction} отправлено в очередь y_pred')

    # Извлекаем сообщение из очереди features
    channel.basic_consume(
        queue='features',
        on_message_callback=callback,
        auto_ack=True
    )
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    # Запускаем режим ожидания прихода сообщений
    channel.start_consuming()
except:
    print('Не удалось подключиться к очереди')
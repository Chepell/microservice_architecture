import pika
import json
import csv


# Clean file with header
header = ['id', 'y_true', 'y_pred', 'absolute_error']
# Open the file in write mode ('w') to clean it
with open('./logs/metric_log.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)


# словарь для хранения данных полученных из очередей
data_store = {
    'y_true': None,
    'y_pred': None
    }


def callback(ch, method, properties, body):
    # Обработчик данных полученных из очереди
    # из method.routing_key получаю имя очереди, кторое является ключом для data_store
    msg_dict = json.loads(body)
    key, message_id, val = method.routing_key, msg_dict['id'], msg_dict['body'] 
    data_store[key] = (message_id, val,)
        
    answer_string = f'Из очереди {key} получено значение {val}'
    with open('./logs/labels_log.txt', 'a') as log:
        log.write(answer_string +'\n')
        
    process_data()
        
        
def process_data():
    # Обработчик нужен для того что бы выводить результат и считать метрики,
    # только когда получены оба значения из очередей
    if data_store['y_true'] is not None and data_store['y_pred'] is not None \
        and data_store['y_true'][0] == data_store['y_pred'][0]:
            
        message_id = data_store['y_true'][0]
        y_true = data_store['y_true'][1]
        y_pred = data_store['y_pred'][1]
            
        print(f"message_id: {message_id}")    
        print(f"y_true: {y_true:.2f}, y_pred: {y_pred:.2f}")
            
        ae = abs(y_true - y_pred)
        print(f"Abs error: {ae:.2f}")
            
        csv_row = [message_id, y_true, y_pred, ae]
        # Open the file in append mode ('a')
        with open('./logs/metric_log.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)
            f.flush()  # Ensure the data is written to the file
            
        # Отчистка словаря для ожидания следующей пары значений
        data_store['y_true'] = None
        data_store['y_pred'] = None
        csv_row = None
        
        
try:  
    # Создаём подключение к серверу на локальном хосте:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    # Извлекаем сообщения из очередей
    channel.basic_consume(
        queue='y_true',
        on_message_callback=callback,
        auto_ack=True
    )

    channel.basic_consume(
        queue='y_pred',
        on_message_callback=callback,
        auto_ack=True
    )
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    # Запускаем режим ожидания прихода сообщений
    channel.start_consuming()
except Exception as err:
    print(f'Не удалось подключиться к очереди: {err}')
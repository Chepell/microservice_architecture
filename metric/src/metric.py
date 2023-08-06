import pika
import json

# словарь для хранения данных полученных из очередей
data_store = {
    'y_true': None,
    'y_pred': None
}

# Создаём подключение к серверу на локальном хосте:
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Объявляем очереди
channel.queue_declare(queue='y_true')
channel.queue_declare(queue='y_pred')

def process_data():
    # Обработчик нужен для того что бы выводить результат и считать метрики,
    # только когда получены оба значения из очередей
    if data_store['y_true'] is not None and data_store['y_pred'] is not None:
        print(f"y_true: {data_store['y_true']:.2f}, y_pred: {data_store['y_pred']:.2f}")
        
        mape = abs((data_store['y_true'] / data_store['y_pred'] - 1) * 100)
        print(f"MAPE: {mape:.2f} %")
        
        # Отчистка словаря для ожидания следующей пары значений
        data_store['y_true'] = None
        data_store['y_pred'] = None
        
def callback(ch, method, properties, body):
    # Обработчик данных полученных из очереди
    # из method.routing_key получаю имя очереди, кторое является ключом для data_store
    data_store[method.routing_key] = json.loads(body)
    process_data()

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
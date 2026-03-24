import os
import json
import aio_pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://user:password@localhost:5672/")

class RabbitMQPublisher:
    async def connect(self):
        self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
        self.channel = await self.connection.channel()
        await self.channel.declare_exchange("notebook_events", aio_pika.ExchangeType.TOPIC)
        
    async def publish(self, routing_key: str, message: dict):
        if not hasattr(self, 'channel') or self.channel.is_closed:
            await self.connect()
            
        exchange = await self.channel.get_exchange("notebook_events")
        
        message_body = aio_pika.Message(
            body=json.dumps(message).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await exchange.publish(message_body, routing_key=routing_key)

    async def close(self):
        if hasattr(self, 'connection') and not self.connection.is_closed:
            await self.connection.close()

publisher = RabbitMQPublisher()

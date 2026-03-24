import asyncio
import json
import logging
from src.infrastructure.queue.rabbitmq_client import RABBITMQ_URL
import aio_pika
from src.workers.playwright.runner import ColabExecutionRunner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_job(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        payload = json.loads(message.body.decode())
        logger.info(f"Received job: {payload['job_id']}")
        
        # Here we connect Phase 4 (Playwright) to Phase 5 (Queue)
        runner = ColabExecutionRunner(payload)
        try:
            await runner.execute()
            logger.info(f"Successfully completed job: {payload['job_id']}")
            # In a full microservice, you'd publish a 'job.completed' event here
        except Exception as e:
            logger.error(f"Job {payload['job_id']} failed: {str(e)}")
            # Publish a 'job.failed' event here

async def start_consumer():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    
    # Fair dispatch
    await channel.set_qos(prefetch_count=1)
    
    exchange = await channel.declare_exchange("notebook_events", aio_pika.ExchangeType.TOPIC)
    
    queue = await channel.declare_queue("execute_queue", durable=True)
    await queue.bind(exchange, routing_key="job.execute")
    
    logger.info("Worker started, waiting for jobs...")
    
    await queue.consume(process_job)
    
    try:
        await asyncio.Future() # Run forever
    finally:
        await connection.close()

if __name__ == "__main__":
    asyncio.run(start_consumer())

#!/usr/bin/env python3
"""
Script simples para teste rápido de envio de eventos
"""

import asyncio
import json
import os
from datetime import datetime
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from dotenv import load_dotenv

load_dotenv()

async def send_test_event():
    """Envia um evento de teste simples"""
    
    # Configuração
    connection_string = os.getenv("EVENT_HUB_CONNECTION_STRING")
    event_hub_name = os.getenv("EVENT_HUB_NAME")
    
    if not connection_string or not event_hub_name:
        print("Configure EVENT_HUB_CONNECTION_STRING e EVENT_HUB_NAME no arquivo .env")
        return
    
    # Dados do evento
    event_data = {
        "message": "Teste do Azure Event Hub",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "python-quick-test",
        "data": {
            "user_id": "test_user_001",
            "action": "test_event",
            "value": 42
        }
    }
    
    try:
        # Cria o producer
        producer = EventHubProducerClient.from_connection_string(
            conn_str=connection_string,
            eventhub_name=event_hub_name
        )
        
        # Prepara o evento
        event = EventData(json.dumps(event_data))
        event.properties = {"test": "true", "timestamp": event_data["timestamp"]}
        
        # Envia o evento
        async with producer:
            event_data_batch = await producer.create_batch()
            event_data_batch.add(event)
            await producer.send_batch(event_data_batch)
        
        print("Evento de teste enviado com sucesso!")
        print(f"Dados enviados: {json.dumps(event_data, indent=2)}")
        
    except Exception as e:
        print(f"Erro ao enviar evento: {e}")

if __name__ == "__main__":
    asyncio.run(send_test_event()) 
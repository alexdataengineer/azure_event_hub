#!/usr/bin/env python3
"""
Script para consumir eventos do Azure Event Hub
"""

import asyncio
import json
import os
from datetime import datetime
from azure.eventhub.aio import EventHubConsumerClient
from dotenv import load_dotenv

load_dotenv()

async def on_event(partition_context, event):
    """Callback executado quando um evento é recebido"""
    print(f"Evento recebido da partição {partition_context.partition_id}")
    print(f"   Offset: {event.offset}")
    print(f"   Sequence Number: {event.sequence_number}")
    print(f"   Enqueued Time: {event.enqueued_time}")
    print(f"   Properties: {event.properties}")
    
    try:
        # Tenta fazer parse do JSON
        event_body = event.body_as_json()
        print(f"   Body: {json.dumps(event_body, indent=2, ensure_ascii=False)}")
    except:
        # Se não for JSON, mostra como string
        print(f"   Body: {event.body_as_str()}")
    
    print("-" * 50)
    
    # Marca o evento como processado
    await partition_context.update_checkpoint(event)

async def on_partition_initialize(partition_context):
    """Callback executado quando uma partição é inicializada"""
    print(f"Inicializando partição {partition_context.partition_id}")

async def on_partition_close(partition_context, reason):
    """Callback executado quando uma partição é fechada"""
    print(f"Fechando partição {partition_context.partition_id}, razão: {reason}")

async def on_error(partition_context, error):
    """Callback executado quando ocorre um erro"""
    print(f"Erro na partição {partition_context.partition_id}: {error}")

async def receive_events():
    """Função principal para receber eventos"""
    
    # Configuração
    connection_string = os.getenv("EVENT_HUB_CONNECTION_STRING")
    event_hub_name = os.getenv("EVENT_HUB_NAME")
    consumer_group = os.getenv("CONSUMER_GROUP", "$Default")
    
    if not connection_string or not event_hub_name:
        print("Configure EVENT_HUB_CONNECTION_STRING e EVENT_HUB_NAME no arquivo .env")
        return
    
    # Cria o consumer client
    consumer = EventHubConsumerClient.from_connection_string(
        conn_str=connection_string,
        consumer_group=consumer_group,
        eventhub_name=event_hub_name
    )
    
    print(f"Iniciando consumo de eventos do Event Hub: {event_hub_name}")
    print(f"Consumer Group: {consumer_group}")
    print("Pressione Ctrl+C para parar...")
    print("=" * 60)
    
    try:
        # Inicia o consumo de eventos
        async with consumer:
            await consumer.receive(
                on_event=on_event,
                on_partition_initialize=on_partition_initialize,
                on_partition_close=on_partition_close,
                on_error=on_error,
                starting_position="-1",  # Começa do evento mais recente
                track_last_enqueued_event_properties=True
            )
    except KeyboardInterrupt:
        print("\nConsumo interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    asyncio.run(receive_events()) 
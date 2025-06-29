#!/usr/bin/env python3
"""
Demonstração completa do Azure Event Hub
Este script mostra como enviar e receber eventos
"""

import asyncio
import json
import os
import time
from datetime import datetime
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient, EventHubConsumerClient
from dotenv import load_dotenv

load_dotenv()

class EventHubDemo:
    def __init__(self):
        self.connection_string = os.getenv("EVENT_HUB_CONNECTION_STRING")
        self.event_hub_name = os.getenv("EVENT_HUB_NAME")
        
        if not self.connection_string or not self.event_hub_name:
            print("Configure EVENT_HUB_CONNECTION_STRING e EVENT_HUB_NAME no arquivo .env")
            print("Copie o config.example para .env e configure suas credenciais")
            return

    async def send_demo_events(self):
        """Envia alguns eventos de demonstração"""
        print("Enviando eventos de demonstração...")
        
        producer = EventHubProducerClient.from_connection_string(
            conn_str=self.connection_string,
            eventhub_name=self.event_hub_name
        )
        
        # Eventos de exemplo
        demo_events = [
            {
                "event_type": "user_login",
                "user_id": "user_001",
                "message": "Usuário fez login no sistema",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": {"session_id": "sess_123", "ip": "192.168.1.100"}
            },
            {
                "event_type": "purchase",
                "user_id": "user_002", 
                "message": "Compra realizada com sucesso",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": {"order_id": "ord_456", "amount": 99.99}
            },
            {
                "event_type": "page_view",
                "user_id": "user_003",
                "message": "Página visualizada",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": {"page": "/products", "duration": 45}
            }
        ]
        
        try:
            async with producer:
                for i, event_data in enumerate(demo_events, 1):
                    # Cria o evento
                    event = EventData(json.dumps(event_data, ensure_ascii=False))
                    event.properties = {
                        "event_type": event_data["event_type"],
                        "user_id": event_data["user_id"],
                        "demo": "true"
                    }
                    
                    # Envia o evento
                    event_data_batch = await producer.create_batch()
                    event_data_batch.add(event)
                    await producer.send_batch(event_data_batch)
                    
                    print(f"Evento {i} enviado: {event_data['event_type']}")
                    await asyncio.sleep(0.5)  # Pequena pausa entre eventos
                    
        except Exception as e:
            print(f"Erro ao enviar eventos: {e}")

    async def receive_demo_events(self, timeout_seconds=10):
        """Recebe eventos por um tempo limitado"""
        print(f"Recebendo eventos por {timeout_seconds} segundos...")
        
        consumer = EventHubConsumerClient.from_connection_string(
            conn_str=self.connection_string,
            consumer_group="$Default",
            eventhub_name=self.event_hub_name
        )
        
        events_received = []
        
        async def on_event(partition_context, event):
            try:
                event_body = event.body_as_json()
                events_received.append({
                    "partition": partition_context.partition_id,
                    "offset": event.offset,
                    "properties": dict(event.properties),
                    "body": event_body
                })
                
                print(f"Evento recebido: {event_body.get('event_type', 'unknown')}")
                await partition_context.update_checkpoint(event)
                
            except Exception as e:
                print(f"Erro ao processar evento: {e}")
        
        try:
            # Agenda o fim da recepção
            asyncio.create_task(self._stop_after_delay(timeout_seconds))
            
            async with consumer:
                await consumer.receive(
                    on_event=on_event,
                    starting_position="-1",  # Eventos mais recentes
                    track_last_enqueued_event_properties=True
                )
        except asyncio.CancelledError:
            pass
        
        return events_received

    async def _stop_after_delay(self, delay_seconds: int):
        """Para a operação após o delay especificado"""
        await asyncio.sleep(delay_seconds)
        raise asyncio.CancelledError()

    def show_event_hub_info(self):
        """Mostra informações sobre o Event Hub"""
        print("Informações do Azure Event Hub")
        print("=" * 40)
        print(f"Namespace: datateam2")
        print(f"Event Hub: {self.event_hub_name}")
        print(f"Partitions: 32")
        print(f"Status: Active")
        print(f"Location: West Europe")
        print(f"Consumer Groups: $Default")
        print()

async def main():
    """Função principal da demonstração"""
    demo = EventHubDemo()
    
    if not demo.connection_string or not demo.event_hub_name:
        return
    
    print("Azure Event Hub - Demonstração Completa")
    print("=" * 50)
    
    # Mostra informações do Event Hub
    demo.show_event_hub_info()
    
    print("Esta demonstração irá:")
    print("1. Enviar 3 eventos de exemplo")
    print("2. Receber eventos por 10 segundos")
    print("3. Mostrar um resumo dos eventos")
    print()
    
    input("Pressione Enter para começar...")
    print()
    
    try:
        # Envia eventos
        await demo.send_demo_events()
        print()
        
        # Aguarda um pouco para os eventos chegarem
        print("Aguardando 2 segundos para os eventos chegarem...")
        await asyncio.sleep(2)
        print()
        
        # Recebe eventos
        events = await demo.receive_demo_events(10)
        
        # Mostra resumo
        print("\n" + "="*50)
        print("RESUMO DA DEMONSTRAÇÃO")
        print("="*50)
        print(f"Eventos enviados: 3")
        print(f"Eventos recebidos: {len(events)}")
        
        if events:
            print("\nEventos recebidos:")
            for i, event in enumerate(events, 1):
                print(f"  {i}. {event['body'].get('event_type', 'unknown')} - {event['body'].get('message', '')}")
        
        print("\nDemonstração concluída!")
        print("\nPróximos passos:")
        print("   - Configure suas credenciais no arquivo .env")
        print("   - Use send_events.py para enviar mais eventos")
        print("   - Use receive_events.py para monitorar eventos")
        print("   - Use data_explorer_demo.py para análise detalhada")
        print("   - Acesse o Data Explorer no Portal do Azure")
        
    except KeyboardInterrupt:
        print("\nDemonstração interrompida pelo usuário.")
    except Exception as e:
        print(f"Erro na demonstração: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 
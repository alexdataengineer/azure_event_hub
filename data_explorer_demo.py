#!/usr/bin/env python3
"""
Demonstração de funcionalidades similares ao Data Explorer
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from azure.eventhub.aio import EventHubConsumerClient
from dotenv import load_dotenv

load_dotenv()

class EventHubDataExplorer:
    def __init__(self):
        self.connection_string = os.getenv("EVENT_HUB_CONNECTION_STRING")
        self.event_hub_name = os.getenv("EVENT_HUB_NAME")
        self.consumer_group = os.getenv("CONSUMER_GROUP", "$Default")
        
        self.events_buffer = []
        self.stats = {
            "total_events": 0,
            "events_by_type": {},
            "events_by_partition": {},
            "start_time": None,
            "end_time": None
        }

    async def collect_events(self, duration_seconds: int = 60):
        """Coleta eventos por um período específico"""
        
        consumer = EventHubConsumerClient.from_connection_string(
            conn_str=self.connection_string,
            consumer_group=self.consumer_group,
            eventhub_name=self.event_hub_name
        )
        
        self.stats["start_time"] = datetime.utcnow()
        
        async def on_event(partition_context, event):
            # Processa o evento
            event_data = {
                "partition_id": partition_context.partition_id,
                "offset": event.offset,
                "sequence_number": event.sequence_number,
                "enqueued_time": event.enqueued_time,
                "properties": dict(event.properties),
                "body": self._parse_event_body(event)
            }
            
            # Adiciona ao buffer
            self.events_buffer.append(event_data)
            
            # Atualiza estatísticas
            self.stats["total_events"] += 1
            
            # Conta por tipo de evento
            event_type = event_data["properties"].get("event_type", "unknown")
            self.stats["events_by_type"][event_type] = self.stats["events_by_type"].get(event_type, 0) + 1
            
            # Conta por partição
            partition_id = event_data["partition_id"]
            self.stats["events_by_partition"][partition_id] = self.stats["events_by_partition"].get(partition_id, 0) + 1
            
            # Marca como processado
            await partition_context.update_checkpoint(event)
        
        print(f"🔍 Coletando eventos por {duration_seconds} segundos...")
        
        try:
            async with consumer:
                # Agenda o fim da coleta
                asyncio.create_task(self._stop_after_delay(duration_seconds))
                
                await consumer.receive(
                    on_event=on_event,
                    starting_position="-1",  # Eventos mais recentes
                    track_last_enqueued_event_properties=True
                )
        except asyncio.CancelledError:
            pass
        
        self.stats["end_time"] = datetime.utcnow()

    async def _stop_after_delay(self, delay_seconds: int):
        """Para a coleta após o delay especificado"""
        await asyncio.sleep(delay_seconds)
        raise asyncio.CancelledError()

    def _parse_event_body(self, event):
        """Tenta fazer parse do body do evento"""
        try:
            return event.body_as_json()
        except:
            return event.body_as_str()

    def display_summary(self):
        """Exibe um resumo dos eventos coletados"""
        print("\n" + "="*60)
        print("📊 RESUMO DOS EVENTOS COLETADOS")
        print("="*60)
        
        duration = self.stats["end_time"] - self.stats["start_time"]
        print(f"⏱️  Período: {self.stats['start_time']} até {self.stats['end_time']}")
        print(f"⏱️  Duração: {duration}")
        print(f"📈 Total de eventos: {self.stats['total_events']}")
        
        if self.stats['total_events'] > 0:
            events_per_second = self.stats['total_events'] / duration.total_seconds()
            print(f"🚀 Taxa: {events_per_second:.2f} eventos/segundo")
        
        print("\n📋 Eventos por tipo:")
        for event_type, count in self.stats["events_by_type"].items():
            percentage = (count / self.stats["total_events"]) * 100
            print(f"   {event_type}: {count} ({percentage:.1f}%)")
        
        print("\n🔢 Eventos por partição:")
        for partition_id, count in sorted(self.stats["events_by_partition"].items()):
            percentage = (count / self.stats["total_events"]) * 100
            print(f"   Partição {partition_id}: {count} ({percentage:.1f}%)")

    def display_recent_events(self, limit: int = 10):
        """Exibe os eventos mais recentes"""
        print(f"\n📄 ÚLTIMOS {limit} EVENTOS:")
        print("-" * 60)
        
        recent_events = self.events_buffer[-limit:] if len(self.events_buffer) > limit else self.events_buffer
        
        for i, event in enumerate(reversed(recent_events), 1):
            print(f"\n{i}. Evento da Partição {event['partition_id']}")
            print(f"   Offset: {event['offset']}")
            print(f"   Sequence: {event['sequence_number']}")
            print(f"   Enqueued: {event['enqueued_time']}")
            print(f"   Properties: {event['properties']}")
            
            # Mostra o body de forma mais legível
            if isinstance(event['body'], dict):
                print(f"   Body: {json.dumps(event['body'], indent=6, ensure_ascii=False)}")
            else:
                print(f"   Body: {event['body']}")
            
            print("-" * 40)

    def export_to_json(self, filename: str = "events_export.json"):
        """Exporta os eventos para um arquivo JSON"""
        export_data = {
            "export_info": {
                "exported_at": datetime.utcnow().isoformat() + "Z",
                "total_events": len(self.events_buffer),
                "collection_period": {
                    "start": self.stats["start_time"].isoformat() + "Z" if self.stats["start_time"] else None,
                    "end": self.stats["end_time"].isoformat() + "Z" if self.stats["end_time"] else None
                }
            },
            "statistics": self.stats,
            "events": self.events_buffer
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Eventos exportados para: {filename}")

async def main():
    """Função principal"""
    explorer = EventHubDataExplorer()
    
    if not explorer.connection_string or not explorer.event_hub_name:
        print("❌ Configure EVENT_HUB_CONNECTION_STRING e EVENT_HUB_NAME no arquivo .env")
        return
    
    print("🔍 Azure Event Hub - Data Explorer Demo")
    print("=" * 50)
    
    try:
        # Coleta eventos por 30 segundos
        await explorer.collect_events(30)
        
        # Exibe resumo
        explorer.display_summary()
        
        # Exibe eventos recentes
        explorer.display_recent_events(5)
        
        # Exporta para JSON
        explorer.export_to_json()
        
    except KeyboardInterrupt:
        print("\n⏹️  Coleta interrompida pelo usuário.")
        explorer.display_summary()
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 
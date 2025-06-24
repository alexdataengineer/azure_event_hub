#!/usr/bin/env python3
"""
Script para enviar eventos para Azure Event Hub
Baseado nas configurações do seu Event Hub: datateam2
"""

import asyncio
import json
import os
import random
import time
from datetime import datetime
from typing import Dict, Any

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class EventHubSender:
    def __init__(self):
        self.connection_string = os.getenv("EVENT_HUB_CONNECTION_STRING")
        self.event_hub_name = os.getenv("EVENT_HUB_NAME")
        self.namespace = os.getenv("EVENT_HUB_NAMESPACE", "datateam2")
        
        if not self.connection_string:
            print("⚠️  Connection string não encontrada. Usando Azure Identity...")
            self.use_managed_identity = True
        else:
            self.use_managed_identity = False

    def generate_sample_data(self) -> Dict[str, Any]:
        """Gera dados de exemplo para enviar ao Event Hub"""
        event_types = ["user_login", "purchase", "page_view", "error", "api_call"]
        user_ids = [f"user_{i:03d}" for i in range(1, 101)]
        
        return {
            "event_id": f"evt_{int(time.time() * 1000)}",
            "event_type": random.choice(event_types),
            "user_id": random.choice(user_ids),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {
                "session_id": f"sess_{random.randint(1000, 9999)}",
                "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "page_url": f"https://example.com/page/{random.randint(1, 50)}",
                "value": random.uniform(10.0, 1000.0)
            },
            "metadata": {
                "source": "python-script",
                "version": "1.0.0",
                "environment": "development"
            }
        }

    async def send_single_event(self, producer: EventHubProducerClient, event_data: Dict[str, Any]):
        """Envia um único evento para o Event Hub"""
        try:
            # Converte o dicionário para JSON
            event_json = json.dumps(event_data, ensure_ascii=False)
            
            # Cria o objeto EventData
            event = EventData(event_json)
            
            # Adiciona propriedades personalizadas
            event.properties = {
                "event_type": event_data["event_type"],
                "user_id": event_data["user_id"],
                "timestamp": event_data["timestamp"]
            }
            
            # Envia o evento
            async with producer:
                event_data_batch = await producer.create_batch()
                event_data_batch.add(event)
                await producer.send_batch(event_data_batch)
                
            print(f"✅ Evento enviado: {event_data['event_id']} - {event_data['event_type']}")
            
        except Exception as e:
            print(f"❌ Erro ao enviar evento: {e}")

    async def send_batch_events(self, num_events: int = 10, delay: float = 1.0):
        """Envia múltiplos eventos em lote"""
        if self.use_managed_identity:
            # Usa Azure Identity (recomendado para produção)
            credential = DefaultAzureCredential()
            producer = EventHubProducerClient(
                fully_qualified_namespace=f"{self.namespace}.servicebus.windows.net",
                eventhub_name=self.event_hub_name,
                credential=credential
            )
        else:
            # Usa connection string
            producer = EventHubProducerClient.from_connection_string(
                conn_str=self.connection_string,
                eventhub_name=self.event_hub_name
            )

        print(f"🚀 Iniciando envio de {num_events} eventos...")
        
        for i in range(num_events):
            event_data = self.generate_sample_data()
            await self.send_single_event(producer, event_data)
            
            if i < num_events - 1:  # Não aguarda após o último evento
                await asyncio.sleep(delay)
        
        print(f"🎉 Envio concluído! {num_events} eventos enviados.")

    async def send_continuous_events(self, interval: float = 5.0):
        """Envia eventos continuamente em intervalos regulares"""
        if self.use_managed_identity:
            credential = DefaultAzureCredential()
            producer = EventHubProducerClient(
                fully_qualified_namespace=f"{self.namespace}.servicebus.windows.net",
                eventhub_name=self.event_hub_name,
                credential=credential
            )
        else:
            producer = EventHubProducerClient.from_connection_string(
                conn_str=self.connection_string,
                eventhub_name=self.event_hub_name
            )

        print(f"🔄 Iniciando envio contínuo de eventos (intervalo: {interval}s)")
        print("Pressione Ctrl+C para parar...")
        
        try:
            while True:
                event_data = self.generate_sample_data()
                await self.send_single_event(producer, event_data)
                await asyncio.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n⏹️  Envio contínuo interrompido pelo usuário.")

async def main():
    """Função principal"""
    sender = EventHubSender()
    
    print("📊 Azure Event Hub - Enviador de Eventos")
    print("=" * 50)
    
    # Verifica configuração
    if not sender.connection_string and not sender.use_managed_identity:
        print("❌ Configuração não encontrada!")
        print("Por favor, configure as variáveis de ambiente:")
        print("1. EVENT_HUB_CONNECTION_STRING - ou")
        print("2. Use Azure Identity com as variáveis apropriadas")
        return
    
    # Menu de opções
    print("\nEscolha uma opção:")
    print("1. Enviar 10 eventos (lote)")
    print("2. Enviar eventos continuamente")
    print("3. Enviar evento único")
    
    try:
        choice = input("\nDigite sua escolha (1-3): ").strip()
        
        if choice == "1":
            num_events = int(input("Quantos eventos enviar? (padrão: 10): ") or "10")
            await sender.send_batch_events(num_events)
            
        elif choice == "2":
            interval = float(input("Intervalo entre eventos em segundos? (padrão: 5): ") or "5")
            await sender.send_continuous_events(interval)
            
        elif choice == "3":
            await sender.send_batch_events(1)
            
        else:
            print("❌ Opção inválida!")
            
    except ValueError:
        print("❌ Valor inválido!")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 
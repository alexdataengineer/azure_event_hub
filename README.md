# Azure Event Hub - Projeto de Exemplo

Este projeto demonstra como enviar e receber eventos no Azure Event Hub usando Python.

## 📋 Pré-requisitos

- Python 3.7+
- Azure Event Hub configurado (namespace: `datateam2`)
- Connection string do Event Hub ou credenciais do Azure Identity

## 🚀 Configuração

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` baseado no `config.example`:

```bash
cp config.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Opção 1: Usar Connection String (mais simples para testes)
EVENT_HUB_CONNECTION_STRING=your_event_hub_connection_string_here
EVENT_HUB_NAME=your_event_hub_name_here

# Opção 2: Usar Azure Identity (recomendado para produção)
# AZURE_TENANT_ID=your_tenant_id
# AZURE_CLIENT_ID=your_client_id
# AZURE_CLIENT_SECRET=your_client_secret
# EVENT_HUB_NAMESPACE=datateam2
```

### 3. Obter Connection String

1. Acesse o [Portal do Azure](https://portal.azure.com)
2. Vá para seu Event Hub (`datateam2`)
3. Clique em "Shared access policies"
4. Selecione "RootManageSharedAccessKey"
5. Copie a "Connection string-primary key"

## 📤 Enviando Eventos

### Teste Rápido

```bash
python quick_test.py
```

### Script Completo

```bash
python send_events.py
```

Opções disponíveis:
- **1**: Enviar lote de eventos
- **2**: Enviar eventos continuamente
- **3**: Enviar evento único

## 📥 Recebendo Eventos

```bash
python receive_events.py
```

Este script irá:
- Conectar ao Event Hub
- Escutar eventos em tempo real
- Exibir detalhes de cada evento recebido
- Usar checkpoint para marcar eventos como processados

## 🔧 Estrutura do Projeto

```
azure_event_hub/
├── requirements.txt          # Dependências Python
├── config.example           # Exemplo de configuração
├── send_events.py          # Script completo para envio
├── quick_test.py           # Teste rápido
├── receive_events.py       # Consumo de eventos
└── README.md              # Este arquivo
```

## 📊 Formato dos Eventos

Os eventos enviados seguem este formato JSON:

```json
{
  "event_id": "evt_1234567890",
  "event_type": "user_login",
  "user_id": "user_001",
  "timestamp": "2025-01-23T21:30:00.000Z",
  "data": {
    "session_id": "sess_1234",
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0...",
    "page_url": "https://example.com/page/1",
    "value": 42.5
  },
  "metadata": {
    "source": "python-script",
    "version": "1.0.0",
    "environment": "development"
  }
}
```

## 🎯 Casos de Uso

### 1. Teste e Desenvolvimento
- Use `quick_test.py` para testes rápidos
- Use `send_events.py` para simular carga

### 2. Monitoramento
- Use `receive_events.py` para monitorar eventos em tempo real
- Verifique o Data Explorer no Portal do Azure

### 3. Produção
- Configure Azure Identity para autenticação segura
- Use consumer groups para processamento paralelo
- Implemente retry logic e error handling

## 🔍 Verificando Eventos no Portal

1. Acesse o [Portal do Azure](https://portal.azure.com)
2. Vá para seu Event Hub (`datateam2`)
3. Clique em "Data Explorer"
4. Visualize eventos em tempo real ou históricos

## 🛠️ Troubleshooting

### Erro de Conexão
- Verifique se a connection string está correta
- Confirme se o Event Hub está ativo
- Verifique as permissões da policy

### Erro de Autenticação
- Para Azure Identity: configure as variáveis de ambiente
- Para Connection String: verifique se não expirou

### Eventos não aparecem
- Verifique se está usando o consumer group correto
- Confirme se há eventos sendo enviados
- Use o Data Explorer para verificar

## 📚 Recursos Adicionais

- [Documentação Azure Event Hub](https://docs.microsoft.com/en-us/azure/event-hubs/)
- [SDK Python Azure Event Hub](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-send)
- [Azure Event Hub Data Explorer](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-explorer)
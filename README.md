# Azure Event Hub - Sample Project

This project demonstrates how to send and receive events in Azure Event Hub using Python.

## 📋 Prerequisites

- Python 3.7+
- Azure Event Hub configured (namespace: `datateam2`)
- Event Hub connection string or Azure Identity credentials

## 🚀 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file based on `config.example`:

```bash
cp config.example .env
```

Edit the `.env` file with your configurations:

```env
# Option 1: Use Connection String (simpler for testing)
EVENT_HUB_CONNECTION_STRING=your_event_hub_connection_string_here
EVENT_HUB_NAME=your_event_hub_name_here

# Option 2: Use Azure Identity (recommended for production)
# AZURE_TENANT_ID=your_tenant_id
# AZURE_CLIENT_ID=your_client_id
# AZURE_CLIENT_SECRET=your_client_secret
# EVENT_HUB_NAMESPACE=datateam2
```

### 3. Get Connection String

1. Access the [Azure Portal](https://portal.azure.com)
2. Go to your Event Hub (`datateam2`)
3. Click on "Shared access policies"
4. Select "RootManageSharedAccessKey"
5. Copy the "Connection string-primary key"

## 📤 Sending Events

### Quick Test

```bash
python quick_test.py
```

### Complete Script

```bash
python send_events.py
```

Available options:
- **1**: Send batch of events
- **2**: Send events continuously
- **3**: Send single event

## 📥 Receiving Events

```bash
python receive_events.py
```

This script will:
- Connect to Event Hub
- Listen to events in real-time
- Display details of each received event
- Use checkpoint to mark events as processed

## 🔧 Project Structure

```
azure_event_hub/
├── requirements.txt          # Python dependencies
├── config.example           # Configuration example
├── send_events.py          # Complete sending script
├── quick_test.py           # Quick test
├── receive_events.py       # Event consumption
└── README.md              # This file
```

## 📊 Event Format

Events sent follow this JSON format:

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

## 🎯 Use Cases

### 1. Testing and Development
- Use `quick_test.py` for quick tests
- Use `send_events.py` to simulate load

### 2. Monitoring
- Use `receive_events.py` to monitor events in real-time
- Check the Data Explorer in Azure Portal

### 3. Production
- Configure Azure Identity for secure authentication
- Use consumer groups for parallel processing
- Implement retry logic and error handling

## 🔍 Checking Events in Portal

1. Access the [Azure Portal](https://portal.azure.com)
2. Go to your Event Hub (`datateam2`)
3. Click on "Data Explorer"
4. View real-time or historical events

## 🛠️ Troubleshooting

### Connection Error
- Check if the connection string is correct
- Confirm if the Event Hub is active
- Check policy permissions

### Authentication Error
- For Azure Identity: configure environment variables
- For Connection String: check if it hasn't expired

### Events not appearing
- Check if you're using the correct consumer group
- Confirm if there are events being sent
- Use Data Explorer to verify

## 📚 Additional Resources

- [Azure Event Hub Documentation](https://docs.microsoft.com/en-us/azure/event-hubs/)
- [Python SDK Azure Event Hub](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-send)
- [Azure Event Hub Data Explorer](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-explorer)

## 👤 Author

This project was conceived, developed and documented by me, **Alexsander Silveira**.

I'm passionate about data, automation and cloud solutions, and I created this repository to facilitate integration, testing and monitoring of events in Azure Event Hub, both for learning and professional use.

If you have questions, suggestions or want to collaborate, feel free to open an issue or get in touch!

---
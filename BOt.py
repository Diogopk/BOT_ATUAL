from telegram import Bot
import asyncio
import pytz
from datetime import datetime, timedelta

# Definir o fuso horário (exemplo, o horário de Brasília)
timezone = pytz.timezone("America/Sao_Paulo")

# Seu token do bot
TOKEN = '7479524024:AAE0WAun0HEQo9QeHYnI5lALtdtWddQyFFU'
GROUP_CHAT_IDS = [
    '-1002248961927',
    '-1002233378018',
    '-1002244712891',
    '-1002486468642',
    '-1002172438260'
]  # IDs dos grupos

# Inicializar o bot
bot = Bot(token=TOKEN)

# Função para enviar mensagem
async def send_message(message):
    tasks = [
        bot.send_message(chat_id=chat_id, text=message)
        for chat_id in GROUP_CHAT_IDS
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for chat_id, result in zip(GROUP_CHAT_IDS, results):
        if isinstance(result, Exception):
            print(f"Erro ao enviar para {chat_id}: {result}")
        else:
            print(f"Mensagem enviada para o chat {chat_id}")

# Mensagem padrão
MESSAGE = """
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
🚴🚴‍♀️     🏍🏍

Próximo turno se inicia em 1 hora.

Entregadores que se agendaram ficarão disponíveis automaticamente no APP.

QUEM NÃO SE AGENDOU, POR FAVOR, FAÇA SUA SOLICITAÇÃO DE VAGA NO GRUPO.

Pedimos que caso não possam rodar no turno agendado, nos informem com antecedência, por favor.
Antes de cada turno ser iniciado.

Contamos com a compreensão de todos e que nos ajudem nessas questões ✌🏻

Equipe ABJP RJ Taquara 💙
"""

# Função para calcular o tempo restante até o próximo envio
def calculate_delay(hour, minute):
    now = datetime.now(timezone)
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target_time < now:
        target_time += timedelta(days=1)
    return (target_time - now).total_seconds()

# Função assíncrona para agendamento
async def schedule_messages():
    schedule_times = [(

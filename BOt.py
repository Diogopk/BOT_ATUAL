import schedule
from telegram import Bot
import asyncio
import pytz
from datetime import datetime

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

# Função para mensagens programadas
def schedule_task(message):
    asyncio.run(send_message(message))

# Função para obter a hora atual no fuso horário especificado
def get_current_time_in_timezone():
    now_utc = datetime.now(pytz.utc)  # Hora em UTC
    return now_utc.astimezone(timezone)  # Converte para o fuso horário desejado

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

# Agendar as mensagens
schedule.every().day.at("16:50").do(schedule_task, MESSAGE)  # Enviar primeira mensagem às 10:00
schedule.every().day.at("14:50").do(schedule_task, MESSAGE)  # Enviar segunda mensagem às 14:00
schedule.every().day.at("14:55").do(schedule_task, MESSAGE)  # Enviar terceira mensagem às 17:00
schedule.every().day.at("21:00").do(schedule_task, MESSAGE)  # Enviar quarta mensagem às 21:00

# Loop para executar o agendamento
async def run_scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# Executar o agendador
asyncio.run(run_scheduler())

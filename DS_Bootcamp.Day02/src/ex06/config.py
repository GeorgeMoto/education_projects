import logging
# Параметры для predict_random
num_of_steps = 3

logging.basicConfig(
    filename='analytics.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%f'
)
logger = logging.getLogger()

# Параметры для predict_random
num_of_steps = 3

# Параметры для Telegram уведомлений
telegram_bot_token = "5160363042:AAF9CSecs8MeSC-pUhcsDg9m_dtIDb2gtog"
telegram_channel_id = "-1002559915501"

# Шаблон для отчета
report_template = """Report\n
We have made {total_observations} observations from tossing a coin: 
{tails} of them were tails and {heads} of them were heads. 
The probabilities are {tails_percent:.2f}% and {heads_percent:.2f}%, respectively. 
Our forecast is that in the next {num_of_steps} observations we will have: {forecast_tails} tail 
and {forecast_heads} heads."""
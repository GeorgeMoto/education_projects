# Параметры для predict_random
num_of_steps = 3

# Шаблон для отчета
report_template = """Report\n
We have made {total_observations} observations from tossing a coin: 
{tails} of them were tails and {heads} of them were heads. 
The probabilities are {tails_percent:.2f}% and {heads_percent:.2f}%, respectively. 
Our forecast is that in the next {num_of_steps} observations we will have: {forecast_tails} tail 
and {forecast_heads} heads."""
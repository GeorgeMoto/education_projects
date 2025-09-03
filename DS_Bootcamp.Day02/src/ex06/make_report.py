import sys

from analytics import Research, Analytics
from config import num_of_steps, report_template, logger


def main() -> None:
    logger.info("Запуск программы make_report.py")

    if len(sys.argv) != 2:
        logger.error("Ошибка: не указан путь к файлу в качестве аргумента")
        print("Ошибка: укажите путь к файлу в качестве аргумента")
        sys.exit(1)

    path_to_file: str = sys.argv[1]
    logger.info(f"Указан путь к файлу: {path_to_file}")

    try:
        # Создаем объект Research и получаем данные
        logger.info("Создание объекта Research")
        research: Research = Research(path_to_file)
        data: list[list[int]] = research.file_reader()

        # Создаем объект Analytics с данными
        logger.info("Создание объекта Analytics")
        analytics: Analytics = Analytics(data)

        # Получаем количество орлов и решек
        logger.info("Подсчет орлов и решек")
        counts_result: tuple[int, int] = analytics.counts()
        heads_count: int = counts_result[0]
        tails_count: int = counts_result[1]

        # Получаем проценты орлов и решек
        logger.info("Расчет процентов орлов и решек")
        fractions_result: tuple[float, float] = analytics.fractions(counts_result)
        heads_percent: float = fractions_result[0]
        tails_percent: float = fractions_result[1]

        # Получаем случайные предсказания
        logger.info(f"Генерация {num_of_steps} случайных предсказаний")
        random_predictions: list[list[int]] = analytics.predict_random(num_of_steps)

        # Считаем прогноз орлов и решек в предсказаниях
        logger.info("Расчет прогноза")
        forecast_result: tuple[int, int] = analytics.calculate_forecast(random_predictions)
        forecast_heads: int = forecast_result[0]
        forecast_tails: int = forecast_result[1]

        # Формируем отчет
        logger.info("Формирование отчета")
        report = report_template.format(
            total_observations=len(data),
            tails=tails_count,
            heads=heads_count,
            tails_percent=tails_percent,
            heads_percent=heads_percent,
            num_of_steps=num_of_steps,
            forecast_tails=forecast_tails,
            forecast_heads=forecast_heads
        )

        # Сохраняем отчет в файл
        save_result: bool = analytics.save_file(report, "report", "txt")
        if save_result:
            print("Отчет успешно сохранен в файл report.txt\n")
        else:
            logger.error("Не удалось сохранить отчет в файл")
            print("Не удалось сохранить отчет в файл\n")

        # Отправляем уведомление в Telegram
        research.send_telegram_notification(save_result)

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        print(f"Ошибка: {e}")

        # В случае ошибки также пытаемся отправить уведомление
        try:
            research = Research(path_to_file)
            research.send_telegram_notification(False)
        except Exception as telegram_error:
            logger.error(f"Не удалось отправить уведомление об ошибке: {telegram_error}")

        sys.exit(1)


if __name__ == "__main__":
    main()
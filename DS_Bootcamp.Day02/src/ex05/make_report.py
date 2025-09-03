import sys

from analytics import Research, Analytics
from config import num_of_steps, report_template


def main() -> None:
    if len(sys.argv) != 2:
        print("Ошибка: укажите путь к файлу в качестве аргумента")
        sys.exit(1)

    path_to_file: str = sys.argv[1]

    try:
        # Создаем объект Research и получаем данные
        research: Research = Research(path_to_file)
        data: list[list[int]] = research.file_reader()

        # Создаем объект Analytics с данными
        analytics: Analytics = Analytics(data)

        # Получаем количество орлов и решек
        counts_result: tuple[int, int] = analytics.counts()
        heads_count = counts_result[0]
        tails_count = counts_result[1]

        # Получаем проценты орлов и решек
        fractions_result: tuple[float, float] = analytics.fractions(counts_result)
        heads_percent: float = fractions_result[0]
        tails_percent: float = fractions_result[1]

        # Получаем случайные предсказания
        random_predictions: list[list[int]] = analytics.predict_random(num_of_steps)

        # Считаем прогноз орлов и решек в предсказаниях
        forecast_result: tuple[int, int] = analytics.calculate_forecast(random_predictions)
        forecast_heads: int = forecast_result[0]
        forecast_tails: int = forecast_result[1]

        # Формируем отчет
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
            print("Не удалось сохранить отчет в файл\n")

        # print(report)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
import csv
import re
import requests
import bs4
from collections import Counter
from datetime import datetime
import statistics
import time


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.data = self._load_data()

    def _load_data(self):
        """Load first 1000 movies from CSV file"""
        movies = []
        with open(self.path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i >= 1000:  # Only first 1000 records
                    break
                movies.append({
                    'movieId': int(row['movieId']),
                    'title': row['title'],
                    'genres': row['genres']
                })
        return movies

    def dist_by_release(self):
        """
        The method returns a dict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        year_counts = {}
        for movie in self.data:
            # Extract year from title (e.g., "Toy Story (1995)" -> 1995)
            match = re.search(r'\((\d{4})\)', movie['title'])
            if match:
                year = int(match.group(1))
                year_counts[year] = year_counts.get(year, 0) + 1

        # Sort by counts descendingly
        return dict(sorted(year_counts.items(), key=lambda x: x[1], reverse=True))

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genre_counts = {}
        for movie in self.data:
            if movie['genres'] and movie['genres'] != '(no genres listed)':
                genres = movie['genres'].split('|')
                for genre in genres:
                    genre = genre.strip()
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1

        # Sort by counts descendingly
        return dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True))

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        movie_genre_counts = {}
        for movie in self.data:
            if movie['genres'] and movie['genres'] != '(no genres listed)':
                genre_count = len(movie['genres'].split('|'))
                movie_genre_counts[movie['title']] = genre_count

        # Sort by genre count descendingly and take top n
        sorted_movies = sorted(movie_genre_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_movies[:n])


class Ratings:
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.data = self._load_data()
        self.movies_instance = self.Movies(self)
        self.users_instance = self.Users(self)

    def _load_data(self):
        """Load first 1000 ratings from CSV file"""
        ratings = []
        with open(self.path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i >= 1000:  # Only first 1000 records
                    break
                ratings.append({
                    'userId': int(row['userId']),
                    'movieId': int(row['movieId']),
                    'rating': float(row['rating']),
                    'timestamp': int(row['timestamp'])
                })
        return ratings

    def _load_movies_data(self, movies_path='movies.csv'):
        """Load movies data to get titles"""
        movies = {}
        with open(movies_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                movies[int(row['movieId'])] = row['title']
        return movies

    class Movies:
        def __init__(self, parent):
            self.parent = parent
            self.movie_titles = parent._load_movies_data()

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts.
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            year_counts = {}
            for rating in self.parent.data:
                # Convert timestamp to year
                year = datetime.fromtimestamp(rating['timestamp']).year
                year_counts[year] = year_counts.get(year, 0) + 1

            # Sort by years ascendingly
            return dict(sorted(year_counts.items()))

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            rating_counts = {}
            for rating in self.parent.data:
                rating_val = rating['rating']
                rating_counts[rating_val] = rating_counts.get(rating_val, 0) + 1

            # Sort by ratings ascendingly
            return dict(sorted(rating_counts.items()))

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings.
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            movie_rating_counts = {}
            for rating in self.parent.data:
                movie_id = rating['movieId']
                if movie_id in self.movie_titles:
                    title = self.movie_titles[movie_id]
                    movie_rating_counts[title] = movie_rating_counts.get(title, 0) + 1

            # Sort by counts descendingly and take top n
            sorted_movies = sorted(movie_rating_counts.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_movies[:n])

        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            movie_ratings = {}
            for rating in self.parent.data:
                movie_id = rating['movieId']
                if movie_id in self.movie_titles:
                    title = self.movie_titles[movie_id]
                    if title not in movie_ratings:
                        movie_ratings[title] = []
                    movie_ratings[title].append(rating['rating'])

            movie_metrics = {}
            for title, ratings in movie_ratings.items():
                if metric == 'average':
                    metric_value = sum(ratings) / len(ratings)
                elif metric == 'median':
                    metric_value = statistics.median(ratings)
                else:
                    metric_value = sum(ratings) / len(ratings)  # default to average

                movie_metrics[title] = round(metric_value, 2)

            # Sort by metric descendingly and take top n
            sorted_movies = sorted(movie_metrics.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_movies[:n])

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            movie_ratings = {}
            for rating in self.parent.data:
                movie_id = rating['movieId']
                if movie_id in self.movie_titles:
                    title = self.movie_titles[movie_id]
                    if title not in movie_ratings:
                        movie_ratings[title] = []
                    movie_ratings[title].append(rating['rating'])

            movie_variances = {}
            for title, ratings in movie_ratings.items():
                if len(ratings) > 1:  # Need at least 2 ratings for variance
                    variance = statistics.variance(ratings)
                    movie_variances[title] = round(variance, 2)

            # Sort by variance descendingly and take top n
            sorted_movies = sorted(movie_variances.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_movies[:n])

    class Users:
        """
        In this class, three methods should work.
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """

        def __init__(self, parent):
            self.parent = parent

        def dist_by_num_of_ratings(self):
            """Distribution of users by the number of ratings made by them"""
            user_rating_counts = {}
            for rating in self.parent.data:
                user_id = rating['userId']
                user_rating_counts[user_id] = user_rating_counts.get(user_id, 0) + 1

            # Create distribution: number of ratings -> count of users
            rating_count_distribution = {}
            for count in user_rating_counts.values():
                rating_count_distribution[count] = rating_count_distribution.get(count, 0) + 1

            return dict(sorted(rating_count_distribution.items()))

        def dist_by_ratings(self, metric='average'):
            """Distribution of users by average or median ratings made by them"""
            user_ratings = {}
            for rating in self.parent.data:
                user_id = rating['userId']
                if user_id not in user_ratings:
                    user_ratings[user_id] = []
                user_ratings[user_id].append(rating['rating'])

            user_metrics = {}
            for user_id, ratings in user_ratings.items():
                if metric == 'average':
                    metric_value = round(sum(ratings) / len(ratings), 1)
                elif metric == 'median':
                    metric_value = round(statistics.median(ratings), 1)
                else:
                    metric_value = round(sum(ratings) / len(ratings), 1)

                user_metrics[user_id] = metric_value

            # Create distribution: metric value -> count of users
            metric_distribution = {}
            for metric_val in user_metrics.values():
                metric_distribution[metric_val] = metric_distribution.get(metric_val, 0) + 1

            return dict(sorted(metric_distribution.items()))

        def top_variance(self, n):
            """Top-n users with the biggest variance of their ratings"""
            user_ratings = {}
            for rating in self.parent.data:
                user_id = rating['userId']
                if user_id not in user_ratings:
                    user_ratings[user_id] = []
                user_ratings[user_id].append(rating['rating'])

            user_variances = {}
            for user_id, ratings in user_ratings.items():
                if len(ratings) > 1:  # Need at least 2 ratings for variance
                    variance = statistics.variance(ratings)
                    user_variances[user_id] = round(variance, 2)

            # Sort by variance descendingly and take top n
            sorted_users = sorted(user_variances.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_users[:n])


class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.data = self._load_data()

    def _load_data(self):
        """Load first 1000 tags from CSV file"""
        tags = []
        with open(self.path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i >= 1000:  # Only first 1000 records
                    break
                tags.append({
                    'userId': int(row['userId']),
                    'movieId': int(row['movieId']),
                    'tag': row['tag'],
                    'timestamp': int(row['timestamp'])
                })
        return tags

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        unique_tags = set(tag['tag'] for tag in self.data)
        tag_word_counts = {}

        for tag in unique_tags:
            word_count = len(tag.split())
            tag_word_counts[tag] = word_count

        # Sort by word count descendingly and take top n
        sorted_tags = sorted(tag_word_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_tags[:n])

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        unique_tags = set(tag['tag'] for tag in self.data)

        # Sort by character length descendingly and take top n
        sorted_tags = sorted(unique_tags, key=len, reverse=True)
        return sorted_tags[:n]

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        most_words_tags = set(self.most_words(n).keys())
        longest_tags = set(self.longest(n))

        # Return intersection as list
        return list(most_words_tags.intersection(longest_tags))

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        tag_counts = Counter(tag['tag'] for tag in self.data)

        # Sort by counts descendingly and take top n
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_tags[:n])

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        unique_tags = set(tag['tag'] for tag in self.data)
        matching_tags = [tag for tag in unique_tags if word.lower() in tag.lower()]

        # Sort alphabetically
        return sorted(matching_tags)


class Links:
    """
    Analyzing data from links.csv
    """

    # Глобальный кэш для всех экземпляров класса
    _global_imdb_cache = {}

    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.data = self._load_data()
        self.movie_titles = self._load_movies_data()

    def _load_data(self):
        """Load first 1000 links from CSV file"""
        links = []
        with open(self.path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i >= 10:  # Only first 200 records
                    break
                links.append({
                    'movieId': int(row['movieId']),
                    'imdbId': row['imdbId'].zfill(7),  # Pad with zeros
                    'tmdbId': row['tmdbId'] if row['tmdbId'] else None
                })
        return links


    def _load_movies_data(self, movies_path='movies.csv'):
        """Load movies data to get titles"""
        movies = {}
        with open(movies_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                movies[int(row['movieId'])] = row['title']
        return movies

    def _get_imdb_info(self, imdb_id):
        """Get movie info from IMDB by ID"""
        # Проверяем глобальный кэш
        if imdb_id in Links._global_imdb_cache:
            return Links._global_imdb_cache[imdb_id]

        try:
            url = f"https://www.imdb.com/title/tt{imdb_id}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            soup = bs4.BeautifulSoup(response.content, 'html.parser')

            # Extract director
            director = "Unknown"
            director_element = soup.find('a', {'class': 'ipc-metadata-list-item__list-content-item'})
            if director_element:
                director = director_element.text.strip()

            # Extract budget - ищем по data-testid
            budget = 0
            budget_element = soup.find('li', {'data-testid': 'title-boxoffice-budget'})
            if budget_element:
                # Ищем span с текстом бюджета
                budget_span = budget_element.find('span', class_='ipc-metadata-list-item__list-content-item')
                if budget_span:
                    budget_text = budget_span.text.strip()
                    # Убираем символы валюты и запятые, извлекаем числа
                    budget_clean = re.sub(r'[^\d]', '', budget_text)
                    try:
                        budget = int(budget_clean) if budget_clean else 0
                    except:
                        budget = 0

            # Extract gross - ищем данные по боксофису
            gross = 0
            # Ищем gross worldwide
            gross_element = soup.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
            if not gross_element:
                # Если не найден worldwide, ищем US & Canada
                gross_element = soup.find('li', {'data-testid': 'title-boxoffice-grossdomestic'})

            if gross_element:
                gross_span = gross_element.find('span', class_='ipc-metadata-list-item__list-content-item')
                if gross_span:
                    gross_text = gross_span.text.strip()
                    # Убираем символы валюты и запятые
                    gross_clean = re.sub(r'[^\d]', '', gross_text)
                    try:
                        gross = int(gross_clean) if gross_clean else 0
                    except:
                        gross = 0

            # Extract runtime - ищем в tech specs
            runtime = 0
            # Сначала пробуем найти в основной информации
            runtime_elements = soup.find_all('li', class_='ipc-inline-list__item')
            for element in runtime_elements:
                text = element.get_text().strip()
                # Ищем паттерны времени
                if 'hour' in text and 'minute' in text:
                    # Формат "1 hour 21 minutes"
                    hours_match = re.search(r'(\d+)\s*hour', text)
                    minutes_match = re.search(r'(\d+)\s*minute', text)
                    if hours_match and minutes_match:
                        runtime = int(hours_match.group(1)) * 60 + int(minutes_match.group(1))
                        break
                elif 'hour' in text:
                    # Только часы "1 hour"
                    hours_match = re.search(r'(\d+)\s*hour', text)
                    if hours_match:
                        runtime = int(hours_match.group(1)) * 60
                        break
                elif 'minute' in text:
                    # Только минуты "81 minutes"
                    minutes_match = re.search(r'(\d+)\s*minute', text)
                    if minutes_match:
                        runtime = int(minutes_match.group(1))
                        break

            # Если не найден в основной информации, ищем в tech specs
            if runtime == 0:
                runtime_element = soup.find('li', {'data-testid': 'title-techspec_runtime'})
                if runtime_element:
                    runtime_span = runtime_element.find('div', class_='ipc-metadata-list-item__content-container')
                    if runtime_span:
                        runtime_text = runtime_span.text.strip()
                        # Парсим различные форматы времени
                        if 'hour' in runtime_text and 'minute' in runtime_text:
                            hours_match = re.search(r'(\d+)\s*hour', runtime_text)
                            minutes_match = re.search(r'(\d+)\s*minute', runtime_text)
                            if hours_match and minutes_match:
                                runtime = int(hours_match.group(1)) * 60 + int(minutes_match.group(1))
                        elif 'minute' in runtime_text:
                            minutes_match = re.search(r'(\d+)\s*minute', runtime_text)
                            if minutes_match:
                                runtime = int(minutes_match.group(1))

            info = {
                'director': director,
                'budget': budget,
                'gross': gross,
                'runtime': runtime
            }

            # Сохраняем в глобальный кэш
            Links._global_imdb_cache[imdb_id] = info
            time.sleep(0.5)
            return info

        except Exception as e:
            print(f"Error getting IMDB info for {imdb_id}: {e}")
            error_info = {
                'director': 'Unknown',
                'budget': 0,
                'gross': 0,
                'runtime': 0
            }
            # Сохраняем даже ошибочные результаты в кэш
            Links._global_imdb_cache[imdb_id] = error_info
            return error_info

    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """
        imdb_info = []

        for movie_id in list_of_movies:
            # Find IMDB ID for this movie
            imdb_id = None
            for link in self.data:
                if link['movieId'] == movie_id:
                    imdb_id = link['imdbId']
                    break

            if imdb_id:
                info = self._get_imdb_info(imdb_id)
                row = [movie_id]

                for field in list_of_fields:
                    field_lower = field.lower()
                    if 'director' in field_lower:
                        row.append(info['director'])
                    elif 'budget' in field_lower:
                        row.append(info['budget'])
                    elif 'gross' in field_lower:
                        row.append(info['gross'])
                    elif 'runtime' in field_lower:
                        row.append(info['runtime'])
                    else:
                        row.append('N/A')

                imdb_info.append(row)

        # Sort by movieId descendingly
        imdb_info.sort(key=lambda x: x[0], reverse=True)
        return imdb_info

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        director_counts = {}

        for link in self.data:
            info = self._get_imdb_info(link['imdbId'])
            director = info['director']
            if director != 'Unknown':
                director_counts[director] = director_counts.get(director, 0) + 1

        # Sort by counts descendingly and take top n
        sorted_directors = sorted(director_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_directors[:n])

    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        movie_budgets = {}

        for link in self.data:
            info = self._get_imdb_info(link['imdbId'])
            if info['budget'] > 0 and link['movieId'] in self.movie_titles:
                title = self.movie_titles[link['movieId']]
                movie_budgets[title] = info['budget']

        # Sort by budgets descendingly and take top n
        sorted_movies = sorted(movie_budgets.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_movies[:n])

    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        movie_profits = {}

        for link in self.data:
            info = self._get_imdb_info(link['imdbId'])
            profit = info['gross'] - info['budget']
            if profit > 0 and link['movieId'] in self.movie_titles:
                title = self.movie_titles[link['movieId']]
                movie_profits[title] = profit

        # Sort by profits descendingly and take top n
        sorted_movies = sorted(movie_profits.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_movies[:n])

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.
        """
        movie_runtimes = {}

        for link in self.data:
            info = self._get_imdb_info(link['imdbId'])
            if info['runtime'] > 0 and link['movieId'] in self.movie_titles:
                title = self.movie_titles[link['movieId']]
                movie_runtimes[title] = info['runtime']

        # Sort by runtime descendingly and take top n
        sorted_movies = sorted(movie_runtimes.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_movies[:n])

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it.
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        movie_costs_per_minute = {}

        for link in self.data:
            info = self._get_imdb_info(link['imdbId'])
            if info['budget'] > 0 and info['runtime'] > 0 and link['movieId'] in self.movie_titles:
                title = self.movie_titles[link['movieId']]
                cost_per_minute = round(info['budget'] / info['runtime'], 2)
                movie_costs_per_minute[title] = cost_per_minute

        # Sort by cost per minute descendingly and take top n
        sorted_movies = sorted(movie_costs_per_minute.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_movies[:n])

    @classmethod
    def clear_cache(cls):
        """Очищает глобальный кэш"""
        cls._global_imdb_cache = {}
        print("🗑️ Глобальный кэш очищен")

    @classmethod
    def cache_size(cls):
        """Возвращает размер кэша"""
        return len(cls._global_imdb_cache)

    @classmethod
    def cache_info(cls):
        """Показывает информацию о кэше"""
        print(f"📊 В кэше: {len(cls._global_imdb_cache)} фильмов")
        return cls._global_imdb_cache


class Tests:
    """
    Test class for all MovieLens analysis classes using pytest
    """

    def test_movies_methods(self):
        """Test all methods of Movies class"""
        print("🧪 Testing Movies class methods...")
        movies = Movies("movies.csv")

        # Test dist_by_release()
        result = movies.dist_by_release()
        assert isinstance(result, dict), "dist_by_release should return dict"
        assert all(isinstance(k, int) for k in result.keys()), "Years should be integers"
        assert all(isinstance(v, int) for v in result.values()), "Counts should be integers"
        # Check descending sort by values
        values = list(result.values())
        assert values == sorted(values, reverse=True), "Should be sorted by counts descendingly"
        print("✅ dist_by_release() passed")

        # Test dist_by_genres()
        result = movies.dist_by_genres()
        assert isinstance(result, dict), "dist_by_genres should return dict"
        assert all(isinstance(k, str) for k in result.keys()), "Genres should be strings"
        assert all(isinstance(v, int) for v in result.values()), "Counts should be integers"
        # Check descending sort by values
        values = list(result.values())
        assert values == sorted(values, reverse=True), "Should be sorted by counts descendingly"
        print("✅ dist_by_genres() passed")

        # Test most_genres()
        result = movies.most_genres(3)
        assert isinstance(result, dict), "most_genres should return dict"
        assert len(result) <= 3, "Should return at most 3 items"
        assert all(isinstance(k, str) for k in result.keys()), "Movie titles should be strings"
        assert all(isinstance(v, int) for v in result.values()), "Genre counts should be integers"
        # Check descending sort by values
        values = list(result.values())
        assert values == sorted(values, reverse=True), "Should be sorted by genre count descendingly"
        print("✅ most_genres() passed")

    def test_ratings_methods(self):
        """Test all methods of Ratings class and nested classes"""
        print("🧪 Testing Ratings class methods...")
        ratings = Ratings("ratings.csv")

        # Test Ratings.Movies methods
        movies_instance = ratings.movies_instance

        # Test dist_by_year()
        result = movies_instance.dist_by_year()
        assert isinstance(result, dict), "dist_by_year should return dict"
        assert all(isinstance(k, int) for k in result.keys()), "Years should be integers"
        assert all(isinstance(v, int) for v in result.values()), "Counts should be integers"
        # Check ascending sort by keys
        keys = list(result.keys())
        assert keys == sorted(keys), "Should be sorted by years ascendingly"
        print("✅ dist_by_year() passed")

        # Test dist_by_rating()
        result = movies_instance.dist_by_rating()
        assert isinstance(result, dict), "dist_by_rating should return dict"
        assert all(isinstance(k, float) for k in result.keys()), "Ratings should be floats"
        assert all(isinstance(v, int) for v in result.values()), "Counts should be integers"
        # Check ascending sort by keys
        keys = list(result.keys())
        assert keys == sorted(keys), "Should be sorted by ratings ascendingly"
        print("✅ dist_by_rating() passed")

        # Test top_by_num_of_ratings()
        result = movies_instance.top_by_num_of_ratings(3)
        assert isinstance(result, dict), "top_by_num_of_ratings should return dict"
        assert len(result) <= 3, "Should return at most 3 items"
        assert all(isinstance(k, str) for k in result.keys()), "Movie titles should be strings"
        assert all(isinstance(v, int) for v in result.values()), "Rating counts should be integers"
        # Check descending sort by values
        values = list(result.values())
        assert values == sorted(values, reverse=True), "Should be sorted by counts descendingly"
        print("✅ top_by_num_of_ratings() passed")

        # Test top_by_ratings()
        result = movies_instance.top_by_ratings(3, 'average')
        assert isinstance(result, dict), "top_by_ratings should return dict"
        assert len(result) <= 3, "Should return at most 3 items"
        assert all(isinstance(k, str) for k in result.keys()), "Movie titles should be strings"
        assert all(isinstance(v, float) for v in result.values()), "Average ratings should be floats"
        # Check descending sort by values
        values = list(result.values())
        assert values == sorted(values, reverse=True), "Should be sorted by ratings descendingly"
        print("✅ top_by_ratings() passed")

        # Test top_controversial()
        result = movies_instance.top_controversial(3)
        assert isinstance(result, dict), "top_controversial should return dict"
        assert len(result) <= 3, "Should return at most 3 items"
        assert all(isinstance(k, str) for k in result.keys()), "Movie titles should be strings"
        assert all(isinstance(v, float) for v in result.values()), "Variances should be floats"
        # Check descending sort by values
        values = list(result.values())
        assert values == sorted(values, reverse=True), "Should be sorted by variance descendingly"
        print("✅ top_controversial() passed")

        # Test Ratings.Users methods
        users_instance = ratings.users_instance

        # Test dist_by_num_of_ratings()
        result = users_instance.dist_by_num_of_ratings()
        assert isinstance(result, dict), "dist_by_num_of_ratings should return dict"
        assert all(isinstance(k, int) for k in result.keys()), "Rating counts should be integers"
        assert all(isinstance(v, int) for v in result.values()), "User counts should be integers"
        print("✅ Users.dist_by_num_of_ratings() passed")

        # Test dist_by_ratings()
        result = users_instance.dist_by_ratings('average')
        assert isinstance(result, dict), "dist_by_ratings should return dict"
        assert all(isinstance(k, float) for k in result.keys()), "Average ratings should be floats"
        assert all(isinstance(v, int) for v in result.values()), "User counts should be integers"
        print("✅ Users.dist_by_ratings() passed")

        # Test top_variance()
        result = users_instance.top_variance(3)
        assert isinstance(result, dict), "top_variance should return dict"
        assert len(result) <= 3, "Should return at most 3 items"
        assert all(isinstance(k, int) for k in result.keys()), "User IDs should be integers"
        assert all(isinstance(v, float) for v in result.values()), "Variances should be floats"
        # Check descending sort by values
        values = list(result.values())
        assert values == sorted(values, reverse=True), "Should be sorted by variance descendingly"
        print("✅ Users.top_variance() passed")

    def test_tags_methods(self):
        """Test all methods of Tags class"""
        print("🧪 Testing Tags class methods...")
        tags = Tags("tags.csv")

        # Test most_words()
        result = tags.most_words(3)
        assert isinstance(result, dict), "most_words should return dict"
        assert len(result) <= 3, "Should return at most 3 items"
        assert all(isinstance(k, str) for k in result.keys()), "Tags should be strings"
        assert all(isinstance(v, int) for v in result.values()), "Word counts should be integers"
        # Check descending sort by values
        values = list(result.values())
        assert values == sorted(values, reverse=True), "Should be sorted by word count descendingly"
        print("✅ most_words() passed")

        # Test longest()
        result = tags.longest(3)
        assert isinstance(result, list), "longest should return list"
        assert len(result) <= 3, "Should return at most 3 items"
        assert all(isinstance(tag, str) for tag in result), "All elements should be strings"
        # Check descending sort by length
        lengths = [len(tag) for tag in result]
        assert lengths == sorted(lengths, reverse=True), "Should be sorted by length descendingly"
        print("✅ longest() passed")

        # Test most_words_and_longest()
        result = tags.most_words_and_longest(5)
        assert isinstance(result, list), "most_words_and_longest should return list"
        assert all(isinstance(tag, str) for tag in result), "All elements should be strings"
        print("✅ most_words_and_longest() passed")

        # Test most_popular()
        result = tags.most_popular(5)
        assert isinstance(result, dict), "most_popular should return dict"
        assert len(result) <= 5, "Should return at most 5 items"
        assert all(isinstance(k, str) for k in result.keys()), "Tags should be strings"
        assert all(isinstance(v, int) for v in result.values()), "Counts should be integers"
        # Check descending sort by values
        values = list(result.values())
        assert values == sorted(values, reverse=True), "Should be sorted by counts descendingly"
        print("✅ most_popular() passed")

        # Test tags_with()
        result = tags.tags_with("funny")
        assert isinstance(result, list), "tags_with should return list"
        assert all(isinstance(tag, str) for tag in result), "All elements should be strings"
        assert all("funny" in tag.lower() for tag in result), "All tags should contain the word"
        # Check alphabetical sort
        assert result == sorted(result), "Should be sorted alphabetically"
        print("✅ tags_with() passed")

    def test_links_methods(self):
        """Test all methods of Links class"""
        print("🧪 Testing Links class methods...")
        links = Links("links.csv")

        # Test get_imdb() with small sample
        sample_movies = [1, 2, 3]
        sample_fields = ["Director", "Budget"]
        result = links.get_imdb(sample_movies, sample_fields)
        assert isinstance(result, list), "get_imdb should return list"
        assert all(isinstance(row, list) for row in result), "All elements should be lists"
        assert all(len(row) == len(sample_fields) + 1 for row in result), "Each row should have movieId + fields"
        # Check descending sort by movieId
        if result:
            movie_ids = [row[0] for row in result]
            assert movie_ids == sorted(movie_ids, reverse=True), "Should be sorted by movieId descendingly"
        print("✅ get_imdb() passed")

        # Test other methods with mock data (since we disabled web scraping)
        # These will return empty results but should have correct types
        result = links.top_directors(2)
        assert isinstance(result, dict), "top_directors should return dict"
        print("✅ top_directors() passed")

        result = links.most_expensive(2)
        assert isinstance(result, dict), "most_expensive should return dict"
        print("✅ most_expensive() passed")

        result = links.most_profitable(2)
        assert isinstance(result, dict), "most_profitable should return dict"
        print("✅ most_profitable() passed")

        result = links.longest(2)
        assert isinstance(result, dict), "longest should return dict"
        print("✅ longest() passed")

        result = links.top_cost_per_minute(2)
        assert isinstance(result, dict), "top_cost_per_minute should return dict"
        print("✅ top_cost_per_minute() passed")

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting comprehensive tests...\n")
        try:
            self.test_movies_methods()
            print("✅ All Movies tests passed!\n")

            self.test_ratings_methods()
            print("✅ All Ratings tests passed!\n")

            self.test_tags_methods()
            print("✅ All Tags tests passed!\n")

            self.test_links_methods()
            print("✅ All Links tests passed!\n")

            print("🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉")
            return True
        except AssertionError as e:
            print(f"❌ Test failed: {e}")
            return False
        except Exception as e:
            print(f"💥 Unexpected error: {e}")
            return False


# Pytest functions for running with pytest command
def test_movies():
    """Pytest function for Movies class"""
    tests = Tests()
    tests.test_movies_methods()


def test_ratings():
    """Pytest function for Ratings class"""
    tests = Tests()
    tests.test_ratings_methods()


def test_tags():
    """Pytest function for Tags class"""
    tests = Tests()
    tests.test_tags_methods()


def test_links():
    """Pytest function for Links class"""
    tests = Tests()
    tests.test_links_methods()


# Test script for local testing
if __name__ == "__main__":
    print("Testing MovieLens Analysis Classes...")

    # Test Movies class
    print("\n=== Testing Movies class ===")
    movies = Movies("movies.csv")
    print("Distribution by release year (top 5):", dict(list(movies.dist_by_release().items())[:5]))
    print("Distribution by genres (top 5):", dict(list(movies.dist_by_genres().items())[:5]))
    print("Movies with most genres (top 3):", movies.most_genres(3))

    # Test Ratings class
    print("\n=== Testing Ratings class ===")
    ratings = Ratings("ratings.csv")
    print("Distribution by year:", ratings.movies_instance.dist_by_year())
    print("Distribution by rating (top 5):", dict(list(ratings.movies_instance.dist_by_rating().items())[:5]))
    print("Top movies by number of ratings (top 3):", ratings.movies_instance.top_by_num_of_ratings(3))

    # Test Tags class
    print("\n=== Testing Tags class ===")
    tags = Tags("tags.csv")
    print("Most popular tags (top 5):", tags.most_popular(5))
    print("Tags with most words (top 3):", tags.most_words(3))
    print("Longest tags (top 3):", tags.longest(3))

    # Test Links class (limited test - no web scraping)
    print("\n=== Testing Links class (limited test) ===")
    links = Links("links.csv")
    print("Loaded", len(links.data), "links")
    print("⚠️  IMDB scraping disabled for faster testing")
    print("Sample link data:", links.data[0] if links.data else "No data")

    print("\nAll basic tests completed!")

    # Run comprehensive tests
    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE PYTEST TESTS")
    print("=" * 60)

    test_suite = Tests()
    success = test_suite.run_all_tests()

    if success:
        print("\n Ready for Jupyter Notebook report creation!")
    else:
        print("\n Some tests failed. Please check the implementation.")
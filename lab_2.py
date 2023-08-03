import requests
import pprint
from collections import Counter
from datetime import datetime, timedelta
import csv
from itertools import groupby


headers = {"accept": "application/json", "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"}


class Films:
    # Initialise created object
    def __init__(self, pages):
        self.lst = []
        self.get_data(pages)
        self.collection = []

    # 1 Fetch the data from desired amount of pages
    def get_data(self, pages):
        for i in range(1, pages + 1):
            url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={i}'
            response = requests.get(url=url, headers=headers)
            pprint.pprint(response.status_code)
            self.lst.extend(response.json()['results'])

    # 2 Give a user all data
    def get_lst(self):
        return self.lst

    # 3 All data about movies with indexes from 3 till 19 with step 4
    def get_index_3_till_19_step_4(self):
        return self.lst[3:19:4]

    # 4 Name of the most popular title
    def get_most_popular_title(self):
        return max(self.lst, key=lambda a: a['popularity'])['title']

    # 5 Names of titles which has in description keywords which a user put as parameters
    def get_names_titles_keywords(self, keywords):
        return [film['title'] for film in self.lst if any(keyword in film['overview'] for keyword in keywords)]

    # 6 Unique collection of present genres (the collection should not allow inserts)
    def get_unique_collection_genres(self):
        return set(genre for film in self.lst for genre in (film.get('genre_ids', [])))

    # 7 Delete all movies with user provided genre
    def delete_all_movies_with_genre(self, numb_genre):
        return list(filter(lambda film: numb_genre not in film['genre_ids'], self.lst))

    # 8 Names of most popular genres with numbers of time they appear in the data
    def get_most_popular_genres(self, num_genres):
         return dict(Counter(genre for film in self.lst for genre in film['genre_ids']).most_common(num_genres))

    # 9?? Collection of film titles grouped in pairs by common genres (the groups should not allow inserts)
    def get_titles_grouped(self):
        sort_films = sorted(self.lst, key=lambda x: x.get('genre_ids', []))
        return {genre: [title for title, _ in films] for genre, films in groupby(sort_films, key=lambda x: x.get('genre_ids', []))}

    # 10?? Return initial data and copy of initial data where first id in list of film genres was replaced with 22
    def return_and_copy_data_with_new_id(self):
        copy_data = self.lst.copy()
        for g in copy_data:
            copy_data[0]['genre_ids'] = [22]
        return self.lst.copy() and copy_data

    # 11 Collection of structures with part of initial data which has the following fields:
        # Title
        # Popularity (with 1 decimal point with maximum precision)
        # Score (vote_average without fractional part)
        # Last_day_in_cinema (2 months and 2 weeks after the release_date)
    # Collection should be sorted by score and popularity
    def get_collection(self):
        for film in self.lst:
            struc = {
                    'Title': film['title'],
                    'Popularity': round(film['popularity'], 1),
                    'Score': int(film['vote_average']),
                    'Last day in cinema': (datetime.strptime(film['release_date'], '%Y-%m-%d') + timedelta(weeks=8, days=4)).strftime('%Y-%m-%d')
                    }
            self.collection.append(struc)
        self.collection.sort(key=lambda f: (f['Score'], f['Popularity']))
        return self.collection

    # 12 Write information from previous step to a csv file using path provided by user
    def write_csv_file(self):
        with open('film_file.csv', mode='w') as csv_file:
            fields = ['Title', 'Popularity', 'Score', 'Last day in cinema']
            writer = csv.DictWriter(csv_file, fields)
            writer.writeheader()
            for film in self.collection:
                writer.writerow(film)


x = Films(1)
user_key = ['youngest']

# 2 Give a user all data
# pprint.pprint(x.get_lst())

# 3 All data about movies with indexes from 3 till 19 with step 4
# pprint.pprint(x.get_index_3_till_19_step_4())

# 4 Name of the most popular title
# pprint.pprint(x.get_most_popular_title())

# 5 Names of titles which has in description keywords which a user put as parameters
# pprint.pprint(x.get_names_titles_keywords(user_key))

# 6 Unique collection of present genres (the collection should not allow inserts)
# pprint.pprint(x.get_unique_collection_genres())

# 7 Delete all movies with user provided genre
# pprint.pprint(x.delete_all_movies_with_genre(12))

# 8 Names of most popular genres with numbers of time they appear in the data
# pprint.pprint(x.get_most_popular_genres(5))

# 9?? Collection of film titles grouped in pairs by common genres (the groups should not allow inserts)
pprint.pprint(x.get_titles_grouped())

# 10?? Return initial data and copy of initial data where first id in list of film genres was replaced with 22
# pprint.pprint(x.return_and_copy_data_with_new_id())

# 11 Collection of structures with part of initial data which has the following fields.
# Collection should be sorted by score and popularity
# pprint.pprint(x.get_collection())

# 12 Write information from previous step to a csv file using path provided by user
# pprint.pprint(x.write_csv_file())

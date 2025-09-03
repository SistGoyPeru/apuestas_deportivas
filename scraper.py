import bs4 as bs
import requests
import polars as pl


class FootballDataScraper:
    def __init__(self, url):
        self.url = url
        self.table = None
        self.df_polars_matchdays = None

    def scrape_data(self):
        resp = requests.get(self.url)
        resp = resp.text
        soup = bs.BeautifulSoup(resp, 'html.parser')
        self.table = soup.find('table', {'class': 'standard_tabelle'})

        if not self.table:
            print("Could not find the data table on the page.")
            return None

        matchdays_data = []
        current_matchday = None

        for row in self.table.find_all('tr'):
            header = row.find('th')
            if header:
                current_matchday = header.text.strip()
            else:
                cols = row.find_all('td')
                if len(cols) >= 6 and current_matchday:
                    date = cols[0].text.strip()
                    time = cols[1].text.strip()
                    home_team = cols[2].text.strip()
                    away_team = cols[4].text.strip()
                    score = cols[5].text.strip()

                    if not date and matchdays_data and matchdays_data[-1]['Jornada'] == current_matchday:
                        date = matchdays_data[-1]['Date'] if matchdays_data else ''

                    matchdays_data.append({
                        'Jornada': current_matchday,
                        'Date': date,
                        'Time': time,
                        'Home Team': home_team,
                        'Away Team': away_team,
                        'Score': score
                    })

        self.df_polars_matchdays = pl.DataFrame(matchdays_data)

        # Apply transformations
        self.df_polars_matchdays = self.df_polars_matchdays.drop('Time')
       
        cols = ['Jornada'] + [col for col in self.df_polars_matchdays.columns if col != 'Jornada']
        self.df_polars_matchdays = self.df_polars_matchdays.select(cols)
        self.df_polars_matchdays = self.df_polars_matchdays.with_columns(
            pl.col('Jornada').str.replace(' Jornada', '').str.strip_chars('.').cast(pl.Int64)
        )
        self.df_polars_matchdays = self.df_polars_matchdays.rename({
            'Jornada': 'Jornadas',
            'Date': 'Fecha',
            'Home Team': 'Local',
            'Away Team': 'Visita',
            'Score': 'Resultado'
        })
        self.df_polars_matchdays = self.df_polars_matchdays.with_columns(
            pl.col('Resultado').replace({'-:-': None})
        )
        self.df_polars_matchdays = self.df_polars_matchdays.with_columns(
            pl.col('Resultado').replace({'apla.': None})
        )
        self.df_polars_matchdays = self.df_polars_matchdays.with_columns(
            pl.col('Resultado').replace({'susp.': None})
        )
        self.df_polars_matchdays = self.df_polars_matchdays.with_columns([
            pl.col('Resultado')
            .str.split(' ')
            .list.get(0)
            .str.split(':')
            .list.get(0)
            .cast(pl.Int64, strict=False)
            .alias('GA'),
            pl.col('Resultado')
            .str.split(' ')
            .list.get(0)
            .str.split(':')
            .list.get(1)
            .cast(pl.Int64, strict=False)
            .alias('GC')
        ])
        self.df_polars_matchdays = self.df_polars_matchdays.drop('Resultado')

        return self.df_polars_matchdays
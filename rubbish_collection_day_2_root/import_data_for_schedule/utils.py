import pandas as pd


def get_streets_names(file):
    '''Return list with names of streets.
    Use file from: http://integracja.gugik.gov.pl/daneadresowe/'''

    data = pd.read_csv(file, sep=';')
    data["Nazwa ulicy"].fillna(data["Nazwa miejscowości"], inplace=True)
    streets = data["Nazwa ulicy"].unique().tolist()
    return sorted(streets)


import csv
import pycountry




class DataSource:

    sectors = [
        'Ageing',
        'Agriculture',
        'Art/Culture',
        'Banking/Fin/Equity',
        'Biz service/Consultancy',
        'Car enthusiasts',
        'China',
        'Clean energy/Env/Sustainability',
        'Commodities',
        'Diplomatic/Official/Gov',
        'Education',
        'Engineering',
        'F&B',
        'Grassroots',
        'Hospitality/Hotels',
        'Insurance',
        'Investor/VC/Fam Office',
        'IT/Computing/AI',
        'Law',
        'Life sciences/Med/Health',
        'Logistics/Shipping',
        'Media/PR',
        'Oil/Gas/Coal/Mining',
        'Philanthropy',
        'Property Dev/Civil Eng Construction/Architecture',
        'Retail/Wholesale',
        'Start-ups',
    ]
    def __init__(self, filename):

        self._countries = {}
        self._country_codes = {}
        self._country_size = {}
        self._sector_size = {}
        self._name_sector = {}

        with open(filename, newline='', encoding='ISO-8859-1' ) as fp:
            reader = csv.DictReader(fp)

            for row in reader:
                country_text = row['Country/Region']
                country_code = DataSource.get_country_code(country_text)
                self._incrment_country_size(country_code)

                name = row['Name']
                if name not in self._name_sector:
                    self._name_sector[name] = []

                for sector in DataSource.sectors:
                    if sector in row:
                        if row[sector]:
                            self._increment_sector_size(sector)
                            self._name_sector[name].append(sector)

    @staticmethod
    def get_country_code(country_text):
        if country_text.strip() == 'UAE':
            country_text = 'United Arab Emirates'
        country_code = pycountry.countries.search_fuzzy(country_text)
        return country_code[0]


    def _incrment_country_size(self, country_code):
        country_name = country_code.name
        country_id = country_code.alpha_2.lower()
        if country_name not in self._countries:
            self._countries[country_name] = 1
            self._country_size[country_id] = 1
            self._country_codes[country_id] = country_code
        else:
            self._countries[country_name] += 1
            self._country_size[country_id] += 1


    def _increment_sector_size(self, sector):
        if sector in self._sector_size:
            self._sector_size[sector] += 1
        else:
            self._sector_size[sector] = 1

    @property
    def country_size(self):
        return self._country_size

    @property
    def country_codes(self):
        return self._country_codes

    @property
    def countries(self):
        return self._countries

    @property
    def sector_size(self):
        return self._sector_size

    @property
    def name_sector(self):
        return self._name_sector

import json
import requests

class City:
    def __init__(self):
        self.token = "" # Insira o seu token de API aqui ###https://advisor.climatempo.com.br/login
        self.ID = 3618  # Setado apenas por ter que usar uma cidade padrao no plano GRATUITO

    def GetCityID(self):
        # Pegando IDs da cidade
        self.city = input("Informe o nome da cidade: ")
        url = f"http://apiadvisor.climatempo.com.br/api/v1/locale/city?name={self.city}&token=" + self.token
        response = requests.request("GET", url)
        self.jsonResponse = json.loads(response.text)
        self.__CleanResponse()

    def __CleanResponse(self):
        # Limpando a resposta
        for key in self.jsonResponse:
            ID = key['id']
            self.NAME = key['name']
            self.STATE = key['state']
            self.COUNTRY = key['country']


    def SetCity(self):
        # Setando cidade padrão, necessario para o plano GRATUITO
        id = input("Digite o id: ")
        url = f'http://apiadvisor.climatempo.com.br/api-manager/user-token/{self.token}/locales'
        payload = f'localeId[]={id}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("PUT", url, headers=headers, data=payload)


    def GetWeather(self):
        # Pega as informações atuais da cidade
        # http://apiadvisor.climatempo.com.br/api/v1/weather/locale/3477/current?token=your-app-token
        url = f"http://apiadvisor.climatempo.com.br/api/v1/weather/locale/{self.ID}/current?token={self.token}"
        response = requests.request("GET", url)
        return json.loads(response.text)

    def GetForecastHumidity(self):
        # Pega as informações de humidade das ultimas 168hrs
        # http://apiadvisor.climatempo.com.br/api/v2/forecast/humidity/locale/3477/hours/168?token=your-app-token
        url = f"http://apiadvisor.climatempo.com.br/api/v2/forecast/humidity/locale/{self.ID}/hours/168?token={self.token}"
        response = requests.request("GET", url)
        return json.loads(response.text)

    def GetForecastPrecipitation(self):
        # Pega as informações de precipitação das ultimas 168hrs
        # http://apiadvisor.climatempo.com.br/api/v2/forecast/precipitation/locale/3477/hours/168?token=your-app-token
        url = f"http://apiadvisor.climatempo.com.br/api/v2/forecast/precipitation/locale/{self.ID}/hours/168?token={self.token}"
        response = requests.request("GET", url)
        return json.loads(response.text)

    def GetForecastTemperature(self):
        # Pega as informações de temperatura das ultimas 168hrs
        # http://apiadvisor.climatempo.com.br/api/v2/forecast/temperature/locale/3477/hours/168?token=your-app-token
        url = f"http://apiadvisor.climatempo.com.br/api/v2/forecast/temperature/locale/{self.ID}/hours/168?token={self.token}"
        response = requests.request("GET", url)
        return json.loads(response.text)

    def GetForecastRegion(self, region):
        # Pega as informações de uma região dos ultimos 3dias
        # Region's name (sul,sudeste,norte,nordeste,centro-oeste)
        # http://apiadvisor.climatempo.com.br/api/v1/forecast/region/centro-oeste?token=your-app-token
        url = f"http://apiadvisor.climatempo.com.br/api/v1/forecast/region/{region}?token={self.token}"
        response = requests.request("GET", url)
        return json.loads(response.text)


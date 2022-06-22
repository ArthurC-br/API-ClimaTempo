from API_DADOS import City
import tkinter
import tkinter.ttk
from PIL import Image, ImageTk
from urllib.request import Request, urlopen
from io import BytesIO


class Interface:
    #Classe para interface usando o TKINTER
    def __init__(self):
        #Método Construtor
        self.text = ""
        self.city = City()
        self.root = tkinter.Tk()
        self.root.title('ClimaTempo API')
        self.largura = 600
        self.altura = 500
        largura_screen = self.root.winfo_screenwidth()
        altura_screen = self.root.winfo_screenheight()
        largura_screen = largura_screen / 2 - self.largura / 2
        altura_screen = altura_screen / 2 - self.altura / 2 - 50
        self.root.geometry("%dx%d+%d+%d" % (self.largura, self.altura, largura_screen, altura_screen))
        self.root.resizable(False, False)
        text = tkinter.Label(self.root,
                             text='Estudo de API\nDados do clima de Ribeirão Preto:',
                             font="Times 20 bold",
                             bd=1,
                             pady=10
                             )
        text.pack()

    def Name(self, key):
        #Seta o nome para visualizao
        if key == 'name':
            return 'Cidade: '
        elif key == 'state':
            return 'Estado: '
        elif key == 'country':
            return 'País: '
        else:
            pass

    def CurrentData(self):
        #Dados atuais da cidade
        data = self.city.GetWeather()
        for key in data:
            if key == 'id':
                continue
            if key == 'data':

                for keyData in data[key]:
                    self.text += keyData + " = " + str(data[key][keyData]) + "\n"
                continue
            text = tkinter.Label(self.root,
                                 text=self.Name(key) + data[key],
                                 font="Times 15",
                                 bd=1,
                                 )
            text.pack(anchor="nw")
        dados = tkinter.Label(self.root,
                              text=self.text,
                              font="Times 15",
                              bd=1,
                              justify=tkinter.LEFT
                              )
        dados.pack()

    def __CleanScreen(self):
        #Limpa toda a tela
        for ele in self.root.winfo_children():
            ele.destroy()

    def __Temp(self, button):
        #Desenha toda a tela de acordo com oque foi pedido
        self.__CleanScreen()
        name = None
        comp = None
        if button == 1:
            data = self.city.GetForecastTemperature()
            name = 'Temperatura das últimas 168 horas'
            comp = '°C'
        elif button == 2:
            data = self.city.GetForecastPrecipitation()
            name = 'Precipitação das últimas 168 horas'
            comp = 'mm'
        elif button == 3:
            data = self.city.GetForecastHumidity()
            name = 'Humidade das últimas 168 horas'
            comp = 'kg/m³'

        else:
            return
        text = tkinter.Label(self.root,
                             text=name,
                             font="Times 18 bold",
                             bd=1,
                             )
        text.pack()
        frame = tkinter.Frame(self.root,
                              relief="solid",
                              borderwidth=1
                              )
        myscrollbar = tkinter.Scrollbar(frame, orient="vertical")
        myscrollbar.pack(side="right", fill="y")
        for key in data:
            if key == 'id':
                continue
            if key == 'temperatures' or key == 'precipitations' or key == 'humidities':
                for keyData in data[key]:
                    # self.text += f"Data: {keyData['date']} = {keyData['value']}°C\n"
                    tkinter.Label(frame,
                                  text=f"Data: {keyData['date']} = {keyData['value']}" + comp,
                                  font="Times 15",
                                  bd=1,
                                  justify=tkinter.LEFT
                                  ).pack()
                continue
            text = tkinter.Label(self.root,
                                 text=self.Name(key) + data[key],
                                 font="Times 15",
                                 bd=1,
                                 )
            text.pack(anchor="nw")

        frame.place(x=(self.largura // 2) - 165, y=60, width=330, height=360)
        self.drawButtons()

    def btn_region(self, region, index):
        #Desenha a tela para regiao selecionada
        index = int(index)
        arg = self.city.GetForecastRegion(region)
        frame = tkinter.Frame(self.root,
                              relief="solid",
                              borderwidth=1
                              )
        frame.place(x=(self.largura // 2) - 250, y=80, width=500, height=360)

        try:
            desc = arg['data'][index]['text']

        except:
            desc = ''

        text = tkinter.Label(frame,
                             text=f"Região: {arg['region']}\n"
                                  f" Data: {str(arg['data'][index]['date_br'])}\n",
                             font="Times 14",
                             bd=1,
                             )
        desc_clean = ''
        for i in desc:
            desc_clean += i
            if i == '.':
                desc_clean += '\n'

        text1 = tkinter.Label(frame,
                              text=desc_clean,
                              font="Times 9",
                              )

        text.pack(anchor='nw')
        URL = arg['data'][index]['image']
        req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        u = urlopen(req)
        raw_data = u.read()
        u.close()
        im = Image.open(BytesIO(raw_data))
        im = im.resize((300, 205), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)

        label = tkinter.Label(frame, image=photo)
        label.image = photo
        label.pack()
        text1.pack(expand=tkinter.YES)
        return

    def Region(self):
        # Desenha a tela para regiao
        self.__CleanScreen()
        text = tkinter.Label(self.root,
                             text="Selecione uma região: ",
                             font="Times 20 bold",
                             bd=1,
                             )
        text.pack()

        cb_regions = tkinter.ttk.Combobox(self.root, values=['sul', 'sudeste', 'norte', 'nordeste', 'centro-oeste'],
                                          font="20", state="readonly", width=10)
        cb_regions2 = tkinter.ttk.Combobox(self.root, values=['0', '1', '2'],
                                           font="20", state="readonly", width=10)

        cb_regions.set("sudeste")
        cb_regions.pack(pady=20)
        cb_regions2.set('0')
        cb_regions2.place(x=360, y=55, width=37)

        button = tkinter.Button(self.root,
                                text="Selecionar",
                                command=lambda: self.btn_region(cb_regions.get(), cb_regions2.get()),
                                font="Times 10 ",
                                )
        button.place(x=400, y=54, height=25)

        self.drawButtons()

    def drawButtons(self):
        #Desenha os botoes
        button_temp = tkinter.Button(self.root,
                                     text="Temperatura",
                                     command=lambda: self.__Temp(1),
                                     font="Times 10 ",
                                     )
        button_precep = tkinter.Button(self.root,
                                       text="Precipitação",
                                       command=lambda: self.__Temp(2),
                                       font="Times 10 ",
                                       )
        button_humi = tkinter.Button(self.root,
                                     text="Humidade",
                                     command=lambda: self.__Temp(3),
                                     font="Times 10 ",
                                     )
        button_region = tkinter.Button(self.root,
                                       text="Região",
                                       command=lambda: self.Region(),
                                       font="Times 10 ",
                                       )

        button_temp.place(x=130, y=440)
        button_precep.place(x=230, y=440)
        button_humi.place(x=330, y=440)
        button_region.place(x=430, y=440)

    def Make(self):
        #Make
        self.drawButtons()
        self.root.mainloop()


inter = Interface()
inter.CurrentData()
inter.Make()

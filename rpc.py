from pypresence import Presence
import requests as req
import json
import time
import logging

print("\n"
      "\n"
      "    ##############################################################\n"
      "  # Rich Presence customizada para o ETS 2, feito por Ashish Shetty #\n"
      "    ##############################################################\n"
      "\n"
      "  Verifique se o servidor de telemetria do ETS 2 ou ATS está em execução\n"
      "  antes de abrir este arquivo.\n"
      "\n"
      "  GitHub do criador original: https://github.com/Shetty073/ets2-ats-custom-discord-rich-presence\n")


def get_data():
    try:
        response = req.get("http://localhost:25555/api/ets2/telemetry")
        raw_data = json.loads(response.content)
        return raw_data
    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.INFO)
        logging.error(f"\nFatal error: \n{str(e)}\n")
        print("\nErro Fatal: Por favor tenha certeza que o servidor de telemetria do ETS 2 ou ATS esteja aberto antes de iniciar esse arquivo.")
        input("\nPressione ENTER para fechar esta janela.")
        exit(1)


def start():
    raw_data = get_data()
    game_data = raw_data["game"]
    if game_data["gameName"]== "ETS2":
        client_id = "1033155036236218430" 
        print(f'Euro Truck Simulator 2 conectado!')
        run(client_id)
    else:
        print("Aguardando a conexão do jogo...")
        time.sleep(3.5)
        start()


def get_details():
    raw_data = get_data()
    game_data = raw_data["game"]
    truck_data = raw_data["truck"]

    if not game_data["connected"]:
        details = "No Menu"
    else:
        if game_data["paused"]:
            details = "Jogo Pausado"
        else:
            if truck_data["engineOn"]:
                motor = "Ligado."
            else:
                motor = "Desligado."
            velocidade = int(truck_data["speed"])
            #rpm = int(truck_data["engineRpm"])
            if velocidade < 0:
                velocidade = 0
            details = f'Dirigindo um {truck_data["make"]} {truck_data["model"]}'
    return details


def get_state():
    raw_data = get_data()
    game_data = raw_data["game"]
    truck_data = raw_data["truck"]

    if not game_data["connected"]:
        #return ou state = "mensagem aqui"
        return
    else:
        if game_data["paused"]:
            #return ou state = "mensagem aqui"
            return
        else:
            velocidade = int(truck_data["speed"])
            #rpm = int(truck_data["engineRpm"])
            if velocidade < 0:
                velocidade = 0
            if int(truck_data["displayedGear"]) <= 0:
                if int(truck_data["displayedGear"]) < 0:
                    marcha = "R"
                else:
                    marcha = "N"
            else:
                marcha = truck_data["displayedGear"]
            fuel = (int(truck_data["fuel"]) / int(truck_data["fuelCapacity"]) * 100)
            state = f'{velocidade} Km/h | {marcha}º Marcha | Combustível: {int(fuel)}%'
    return state


def run(client_id):
    try:
        RPC = Presence(client_id)
        RPC.connect()
        print("Rodando...\n"
              "NOTA:\n"
              "Se você estiver jogando ETS 2 e quiser começar a jogar ATS (ou vice-versa), então"
              "após fechar o ETS 2 e antes de iniciar o ATS você deve REINICIAR este aplicativo JUNTO COM o servidor"
              "de telemetria.\n"
              "Feche essa janela quando você quiser desligar a Rich Presence.")
        while True:
            RPC.update(state=get_state(), details=get_details(), large_image="sem imagem", #Troque "sem imagem" por uma imagem qualquer, caso queria colocar uma na sua Rich Presence.
                       large_text="Euro Truck Simulator 2",
                       small_image="sem imagem", small_text="ETS2") #Troque "sem imagem" por uma imagem qualquer, caso queria colocar uma na sua Rich Presence.
            time.sleep(0.1)
    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.INFO)
        logging.error(f"Erro Fatal: \n{str(e)}\nPor favor tenha certeza de que seu Discord está aberto e rodando perfeitamente.")
        print("Erro Fatal: Por favor tenha certeza de que seu Discord esteja aberto antes de "
              "iniciar esse arquivo.\n")
        input("Pressione ENTER para fechar esta janela.")
        exit(1)


start()

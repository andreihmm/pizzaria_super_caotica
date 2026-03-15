'''
• Use threading.Thread (pode herdar ou não)
• Use queue.Queue para fila de pedidos
• Use threading.Semaphore(3) para simular o forno (máximo 3 pizzas simultâneas)
• Use threading.Condition() ou threading.Event() para sincronizar a entrega de
pizzas prontas
• Cada chef gera números grandes (ex: 1013+ random) e verifica primalidade com a
função eh_primo da Unidade 02
• Cada entregador retira da fila e imprime mensagem clara (ex: “Entregue pizza premium 10000000000037”)
• Meça o tempo total com timeit.default_timer() para as seguintes configurações (mínimo):
    1 chef + 1 entregador
    2 chefs + 2 entregadores
    4 chefs + 4 entregadores
    8 chefs + 8 entregadores (ou o máximo que sua máquina suportar)

    falor com o professor de usar o with no semaphoro
'''

import threading
import queue
import time

tamanho_fila = 50
semaphoro = threading.Semaphore(3)

pedidos_pendentes = queue.Queue()
pizzas_feitas = queue.Queue()

for i in range (1, tamanho_fila + 1):
    pedidos_pendentes.put(i)

def chef(pedidos_pendentes, n_thread):
    contador = 0
    while pedidos_pendentes:
        semaphoro.acquire()
        pizza = pedidos_pendentes.get()
        contador += 1
        print(f'O chef {n_thread} está fazendo a sua {contador}° pizza, pizza de número {pizza}')
        time.sleep(5)
        print(f'O chef {n_thread} finalizou a pizza de número {pizza}')
        pizzas_feitas.put(pizza)
        semaphoro.release()


def entregador(pedidos_pendentes, n_thread):
    while pedidos_pendentes or pizzas_feitas:
        pizza = pizzas_feitas.get()
        if pizza:
            print(f'O entregador {n_thread} está fazendo a entrega do pedido {pizza}')
            time.sleep(10)
            print(f'O entregador {n_thread} concluiu a entrega do pedido {pizza}')


funcionario = []

for n_thread in range (1, 9):
    p = threading.Thread(target=chef,  args=(pedidos_pendentes, n_thread))
    e = threading.Thread(target=entregador, args=(pedidos_pendentes, n_thread))
    funcionario.append(p)
    funcionario.append(e)
    p.start()
    e.start()

for j in funcionario:
    j.join()
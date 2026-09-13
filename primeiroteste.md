Após as orientações de instalar o Ollama e utilizarmos o modelo wqen2.5:1.5b conforme orientado no plano de estudos, temos: 

CONSULTA USADA NO MODELO ATRAVÉS DO BROWSER: 
Consulta: Explique em até três frases a diferença  entre TCP e UDP.

Resposta: O TCP é um protocolo orientado à conexão que garante a entrega confiável e ordenada dos dados, sendo ideal para aplicações que não admitem erros, como a navegação web. Já o UDP é um protocolo sem conexão que não garante a entrega ou a ordem dos pacotes, mas prioriza a velocidade e a eficiência com menor sobrecarga. Por isso, o TCP é usado para transferências precisas, enquanto o UDP é preferido em aplicações em tempo real, como jogos e streaming, onde a rapidez é mais crucial.

Realizando o mesmo prompt no mesmo modelo analisado localmente:
Preparando o ambiente: 
Via terminal do VS Code:
ollama pull qwen2.5:1.5b
ollama run qwen2.5:1.5b

Código usado: 
import json
import time
import urllib.request

payload = {
    "model":"qwen2.5:1.5b",
    "messages": [
        {"role":"user",
            "content":"Explique em até três frases a diferença entre o método TCP e UDP."
        }
    ],
    "stream": False,
    "options": {
        "temperature": 0,
        "num_ctx":2048, 
        "num_predict":160
    }
}
request = urllib.request.Request(
    "http://localhost:11434/api/chat",
    data=json.dumps(payload).encode("utf-8"),
    headers= {"Content-Type": "application/json"},
    method= "POST"

)

started = time.perf_counter()
with urllib.request.urlopen(request, timeout=1800) as response:
    result = json.load(response)

print(result["message"]["content"])
print(f"Tempo total: {time.perf_counter()- started:.1f} segundos")import json
import time
import urllib.request

payload = {
    "model":"qwen2.5:1.5b",
    "messages": [
        {"role":"user",
            "content":"Explique em até três frases a diferença entre o método TCP e UDP."
        }
    ],
    "stream": False,
    "options": {
        "temperature": 0,
        "num_ctx":2048, 
        "num_predict":160
    }
}
request = urllib.request.Request(
    "http://localhost:11434/api/chat",
    data=json.dumps(payload).encode("utf-8"),
    headers= {"Content-Type": "application/json"},
    method= "POST"

)

started = time.perf_counter()
with urllib.request.urlopen(request, timeout=1800) as response:
    result = json.load(response)

print(result["message"]["content"])
print(f"Tempo total: {time.perf_counter()- started:.1f} segundos")

Resposta obtida: 
TCP (Transmission Control Protocol) e UDP (User Datagram Protocol) são dois protocolos de transporte de dados usados na Internet. 

1. TCP é um protocolo de transporte de dados que garante a entrega de dados de forma segura e completa. Ele envia pacotes de dados e verifica se eles chegaram corretamente. Se algum pacote for perdido, TCP pode reenviá-lo. Isso é útil para aplicativos que precisam de dados de alta qualidade, como jogos ou streaming de vídeo.

2. UDP, por outro lado, é um protocolo de transporte de dados que não garante a entrega de dados. Ele envia pacotes de dados rapidamente e não verifica se eles chegaram ou não. Isso é útil para aplicativos
Tempo total: 13.8 segundos

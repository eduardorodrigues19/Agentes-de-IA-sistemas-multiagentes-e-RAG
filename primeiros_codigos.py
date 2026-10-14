"""ESQUELETO MÍNIMO PARA O AGENTE DE IA DO HUSM (ideias)"""

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class EstadoAgente(TypedDict):
    mensagem_entrada: str
    resposta: str

def processar(state: EstadoAgente) -> dict:
    return {"resposta": f"Recebi: {state['mensagem_entrada']}"}

grafo = StateGraph(EstadoAgente)
grafo.add_node("processar", processar)
grafo.add_edge(START, "processar")
grafo.add_edge("processar", END)

app = grafo.compile()

resultado = app.invoke({"mensagem_entrada": "Olá", "resposta": ""})
print(resultado["resposta"])


#================================================================================================================


from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END

forbidden_words=set("prontuário", "estado de saúde", "condições de saúde", "boletim médico", "exame", "laudo", "situação médica", "cirurgia", "medicação", "medicamento", "procedimento")

class EstadoAgente (TypedDict):
    mensagem_entrada: str
    resposta:str
    bloqueado:bool

def checar_governanca (state:EstadoAgente) ->dict:
    texto=state["mensagem_entrada"].lower()
    contem_palavra_proibida = any (palavra in texto for palavra in forbidden_words) 
    return {"bloqueado": contem_palavra_proibida}

def bloquear (state:EstadoAgente)->dict:
    print("A divulgação desse tipo de informação é proibida pela Lei Geral de Proteção de Dados.")
    return {"resposta": f"Encaminhando para um atendente do hospital para te orientar sobre mais informações."}

def responder_normal (state:EstadoAgente)-> dict:
    return {"resposta": f"Posso ajudar com mais informações sobre o exame ou alguma dúvida sua?"}

def rotear (state:EstadoAgente)-> Literal["bloquear", "responder_normal"]:
    return "bloquear" if state ["bloqueado"] else "responder_normal"

grafo = StateGraph(EstadoAgente)
grafo.add_node("checar_governanca", checar_governanca)
grafo.add_node ("bloquear", bloquear)
grafo.add_node("responder_normal", responder_normal)

grafo.add_edge(START, "checar_governanca")
grafo.add_conditional_edges("checar_governanca", rotear,{
    "bloquear":"bloquear",
    "responder_normal": "responder_normal",
})

grafo.add_edge("bloquear",END)
grafo.add_edge("bloquerar", END)

app = grafo.compile()

print(app.invoke({"mensagem_entrada": "quero saber do meu prontuário", "resposta":"", "bloqueado": False}) ["resposta"])
print(app.invoke({"mensagem_entrada": "quero confirmar meu exame de raio-x", "resposta":"", "bloqueado": False}) ["resposta"])

"""EXEMPLO 2 - LIMITE MÁXIMO DE PASSOS"""

resultado = app.invoke({"mensagem_entrada": "...", "resposta": "", "bloqueado": False}, {"recursion_limit":10},
                       )
#Por padrão, o LangGraph tem 25 passos sem chegar no END. 



#====================================================================================================================================

""" O ciclo ReAct (Reason + Act)"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

class EstadoChat (TypedDict):
    messages: Annotated[list, add_messages]

@tool
def verificar_disponibilidade (data:str)->str:
    """Verifica se há horário disponível para exame na data informada."""
    return f"Há 2 horários livres em {data}: 09h e 14h."

modelo = ChatOllama(model="qwen2.5:1.5b", temperature=0)
modelo_com_ferramentas = modelo.bind_tools ([verificar_disponibilidade])

def chamar_modelo (state:EstadoChat)->dict:
    return {"messages": [modelo_com_ferramentas.invoke(state["messages"])]}

grafo = StateGraph(EstadoChat)
grafo.add_node("modelo", chamar_modelo)
grafo.add_node ("ferramentas", ToolNode([verificar_disponibilidade]))

grafo.add_edge(START,modelo)
grafo.add_conditional_edge("modelo", tools_condition)
grafo.add_edge("ferramentas","modelo")

app = grafo.compile()
resultado = app.invoke ({"messages": [("user", "Tem horário disponível para exame dia 2026-10-05? ")]})

print(resultado["messages"][-1].content)

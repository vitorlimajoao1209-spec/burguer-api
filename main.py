from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
import sqlite3
import os
from pydantic import BaseModel
from datetime import datetime

# 1. Ligando o motor
app = FastAPI(title="API Hamburgueria com SQLite")

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS (SQLITE)
# ==========================================
BANCO_DADOS = "dados_sistema.db"

def obter_conexao():
    conexao = sqlite3.connect(BANCO_DADOS)
    conexao.row_factory = sqlite3.Row
    return conexao

def iniciar_banco():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    # Tabela do Cardápio / Estoque
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cardapio (
        nome_lanche TEXT PRIMARY KEY,
        quantidade INTEGER NOT NULL
    )
    """)
    
    # Tabela de Administradores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        login TEXT PRIMARY KEY,
        senha TEXT NOT NULL
    )
    """)
    
    # Tabela de Histórico
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mensagem TEXT NOT NULL
    )
    """)
    
    # Tabela de Métricas (Vendas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metricas (
        chave TEXT PRIMARY KEY,
        valor INTEGER NOT NULL
    )
    """)
    
    # Valores padrão iniciais (se estiver vazio)
    cursor.execute("SELECT COUNT(*) FROM admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO admin (login, senha) VALUES (?, ?)", ("JKLOG", "123JK"))
        
        lanches_iniciais = [("x-burguer", 10), ("x-salada", 15), ("x-hotdog", 5)]
        cursor.executemany("INSERT INTO cardapio (nome_lanche, quantidade) VALUES (?, ?)", lanches_iniciais)
        
        cursor.execute("INSERT INTO metricas (chave, valor) VALUES (?, ?)", ("total_vendas_reais", 0))
    
    conexao.commit()
    conexao.close()

iniciar_banco()

# Variáveis globais de controle de sessão
usuario_logado = None
admin_logado = False
tentativas = 0

# Trava de segurança
def verificar_admin():
    if not admin_logado:
        raise HTTPException(
            status_code=401,
            detail="Acesso negado, faça login primeiro em /login"
        )

# Funções auxiliares para o Histórico no SQLite
def registrar_log(mensagem: str):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO historico (mensagem) VALUES (?)", (mensagem,))
    conexao.commit()
    conexao.close()

# Modelos Pydantic
class ItemLanche(BaseModel):
    nome_lanche: str
    quantidades: int
    
class RespostaMensagem(BaseModel):
    mensagem: str


# ==========================================
# ROTAS HTTP
# ==========================================

@app.get("/", response_class=HTMLResponse)
def ler_index():
    caminho = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>API da Hamburgueria rodando com sucesso! Acesse /docs para usar.</h1>"

@app.get("/login", response_model=RespostaMensagem)
def conta_admin(login: str, senha: str):
    global tentativas, admin_logado, usuario_logado
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT senha FROM admin WHERE login = ?", (login,))
    resultado = cursor.fetchone()
    conexao.close()
    
    if resultado and resultado["senha"] == senha:
        agora = datetime.now()
        data_hora_formatada = agora.strftime("%H:%M no dia %d/%m/%Y")
        registrar_log(f"as {data_hora_formatada} foi logado")
        
        aviso = "Administrador, Você fez login com sucesso"
        admin_logado = True
        usuario_logado = login
        tentativas = 0
    else:
        tentativas += 1
        aviso = f"login ou senha incorreta, você perdeu {tentativas} de 3 tentativas"
    
    if tentativas >= 3:
        os._exit(0)
    return {"mensagem": aviso}

@app.get("/ver", dependencies=[Depends(verificar_admin)])
def ver_lista():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome_lanche, quantidade FROM cardapio")
    lanches = cursor.fetchall()
    conexao.close()
    
    cardapio_dict = {lanche["nome_lanche"]: lanche["quantidade"] for lanche in lanches}
    return {"Lista_cardápio": cardapio_dict}

@app.post("/adicionar", dependencies=[Depends(verificar_admin)], response_model=RespostaMensagem)
def adicionar_lanche(item: ItemLanche):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute(
        "INSERT INTO cardapio (nome_lanche, quantidade) VALUES (?, ?) ON CONFLICT(nome_lanche) DO UPDATE SET quantidade = ?",
        (item.nome_lanche, item.quantidades, item.quantidades)
    )
    conexao.commit()
    conexao.close()
    
    registrar_log(f"adicionado o lanche {item.nome_lanche} com {item.quantidades} no total")
    return {"mensagem": f"{item.nome_lanche} adicionado ao estoque com {item.quantidades} unidades."}

@app.delete("/remover", dependencies=[Depends(verificar_admin)], response_model=RespostaMensagem)
def remover_lanche(lanche2: str):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT nome_lanche FROM cardapio WHERE nome_lanche = ?", (lanche2,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM cardapio WHERE nome_lanche = ?", (lanche2,))
        conexao.commit()
        conexao.close()
        
        registrar_log(f"removido o {lanche2}")
        return {"mensagem": f"'{lanche2}' removido com sucesso"}
    else:
        conexao.close()
        raise HTTPException(
            status_code=404,
            detail="Lanche não disponivel no cardápio, busque outro lanche ou adicione no cardapio"
        )

@app.post("/nova_senha", dependencies=[Depends(verificar_admin)])
def senha_nova(senha_atual: str, nova_senha: str, background_tasks: BackgroundTasks):
    global tentativas
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT senha FROM admin WHERE login = ?", (usuario_logado,))
    resultado = cursor.fetchone()
    
    if resultado and resultado["senha"] == senha_atual:
        cursor.execute("UPDATE admin SET senha = ? WHERE login = ?", (nova_senha, usuario_logado))
        conexao.commit()
        conexao.close()
        
        tentativas = 0
        registrar_log(f"nova senha:{nova_senha}")
        return {"status_senha": "Senha alterada com sucesso!"}
    else:
        conexao.close()
        tentativas += 1
        
    if tentativas >= 3:
        background_tasks.add_task(os._exit, 0)
        raise HTTPException(
            status_code=503,
            detail="Servico encerrado após muitas tentativas"
        )
                
    raise HTTPException(
        status_code=400,
        detail=f"Senha incorreta, você perdeu {tentativas} de 3"
    )

@app.post("/vender", dependencies=[Depends(verificar_admin)], response_model=RespostaMensagem)
def vender_lanche(nome_lanche: str, quantidades_lanches: int):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT quantidade FROM cardapio WHERE nome_lanche = ?", (nome_lanche,))
    resultado = cursor.fetchone()
    
    if not resultado:
        conexao.close()
        raise HTTPException(
            status_code=404,
            detail="Lanche não disponivel no cardápio, busque outro lanche ou adicione no cardapio"
        )
        
    lanche_estoque = resultado["quantidade"]
    
    if quantidades_lanches > lanche_estoque:
        conexao.close()
        raise HTTPException(
            status_code=400,
            detail=f"Quantidades para vender muito acima do que tem, há {lanche_estoque} unidades do {nome_lanche}"
        )
        
    total_venda = lanche_estoque - quantidades_lanches
    cursor.execute("UPDATE cardapio SET quantidade = ? WHERE nome_lanche = ?", (total_venda, nome_lanche))
    cursor.execute("UPDATE metricas SET valor = valor + ? WHERE chave = 'total_vendas_reais'", (quantidades_lanches,))
    
    conexao.commit()
    conexao.close()
    
    registrar_log(f"vendido o {nome_lanche} por {quantidades_lanches} unidades")
    return {"mensagem": f"Venda de {quantidades_lanches} {nome_lanche}(s) realizada com sucesso!"}

@app.post("/aumentar_estoque", dependencies=[Depends(verificar_admin)], response_model=RespostaMensagem)
def aumentar_lanche(nome_lanche: str, quantidades_novo: int):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT quantidade FROM cardapio WHERE nome_lanche = ?", (nome_lanche,))
    resultado = cursor.fetchone()
    
    if not resultado:
        conexao.close()
        raise HTTPException(
            status_code=404,
            detail="Lanche não disponivel no cardápio, busque outro lanche ou adicione no cardapio"
        )
        
    total_aumento = resultado["quantidade"] + quantidades_novo
    cursor.execute("UPDATE cardapio SET quantidade = ? WHERE nome_lanche = ?", (total_aumento, nome_lanche))
    conexao.commit()
    conexao.close()
    
    registrar_log(f"aumentado no lanche {nome_lanche} com {total_aumento} no total")
    return {"mensagem": f"aumentado {quantidades_novo} unidades no lanche {nome_lanche}"}

@app.post("/diminuir_estoque", dependencies=[Depends(verificar_admin)], response_model=RespostaMensagem)
def diminuir_lanche(nome_lanche: str, quantidades_removido: int):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT quantidade FROM cardapio WHERE nome_lanche = ?", (nome_lanche,))
    resultado = cursor.fetchone()
    
    if not resultado:
        conexao.close()
        raise HTTPException(
            status_code=404,
            detail="Lanche não disponivel no cardápio, busque outro lanche ou adicione no cardapio"
        )
        
    lanche_estoque = resultado["quantidade"]
    if quantidades_removido > lanche_estoque:
        conexao.close()
        raise HTTPException(
            status_code=400,
            detail=f"Muitas unidades para serem removidas, há apenas {lanche_estoque}"
        )
	
    total_low = lanche_estoque - quantidades_removido
    cursor.execute("UPDATE cardapio SET quantidade = ? WHERE nome_lanche = ?", (total_low, nome_lanche))
    conexao.commit()
    conexao.close()
    
    registrar_log(f"diminuido no lanche {nome_lanche} com {total_low} no total")
    return {"mensagem": f"diminuido {quantidades_removido} unidades no lanche {nome_lanche}"}

@app.get("/historico", dependencies=[Depends(verificar_admin)])
def ver_historico():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT mensagem FROM historico")
    logs = cursor.fetchall()
    conexao.close()
    
    lista_logs = [log["mensagem"] for log in logs]
    return {"historico": lista_logs}

@app.delete("/remover_historico", dependencies=[Depends(verificar_admin)], response_model=RespostaMensagem)
def remover_historico():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM historico")
    conexao.commit()
    conexao.close()
    
    agora = datetime.now()
    data_hora_formatada = agora.strftime("%H:%M no dia %d/%m/%Y")
    mensagem_log = f"no horario e data {data_hora_formatada} foi removido o historico"
    registrar_log(mensagem_log)
    
    return {"mensagem": "Removido com sucesso! Lembrando que no historico está marcado como primeiro Log de quando foi removido!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


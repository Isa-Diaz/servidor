---

# 🏦 Sistema Bancário em Arquitetura de Microserviços 🏦

## 📌 Sobre o Projeto

Este projeto simula um ambiente bancário utilizando **arquitetura de microserviços**, divididos em dois módulos principais:

### 🔷 Microserviço de Acesso (porta 5001)

Responsável por:

* Validação e processamento de dados
* Regras bancárias
* Cálculo de score
* Saque e depósito
* Comunicação com o microserviço de armazenamento
* Documentação Swagger integrada

### 🔶 Microserviço de Armazenamento (porta 5000)

Responsável por:

* Persistência de dados
* CRUD usando SQLite
* Repositório e acesso ao banco
* Respostas ao microserviço de acesso
* Documentação Swagger integrada

---

# 🛠 Tecnologias Utilizadas

* Python
* Flask
* SQLite
* Flasgger (Swagger)
* Requests
* Pytest (com pytest-cov)

---

# 🏗 Arquitetura do Projeto

```
servidor/
│
├── __init__.py
│
├── acesso/
│   ├── __init__.py
│   │
│   ├── client/
│   │   ├── __init__.py
│   │   └── client.py
│   │
│   ├── controller/
│   │   ├── __init__.py
│   │   └── cliente_controller.py
│   │
│   ├── service/
│   │   ├── __init__.py
│   │   └── cliente_service.py
│   │
│   └── validators/
│       ├── __init__.py
│       └── cliente_schemas.py
│
└── micro_servico/
    ├── __init__.py
    │
    ├── controller/
    │   ├── __init__.py
    │   └── storage_controller.py
    │
    ├── database/
    │   ├── __init__.py
    │   └── db.py
    │
    └── repository/
        ├── __init__.py
        └── storage_repository.py
```

---

# 🔄 Fluxo Geral

### **Criar Cliente**

1. Requisição chega no **Acesso (5001)**
2. Dados são validados (validators)
3. Score é calculado
4. Acesso envia requisição ao **Armazenamento (5000)**
5. Armazenamento salva no banco
6. Retorno é enviado ao cliente

### **Operações Bancárias**

* Saque e depósito
* Limite baseado no score
* Score recalculado após operações

---

# 🧮 Regras de Negócio

### **Score**

```
score = saldo_cc × 0.1
```

### **Cheque Especial**

```
limite = score × 3
```

### **Regra de Saque**

```
novo_saldo >= -limite
```

### **Validações**

* nome → string
* telefone → 10–11 dígitos
* correntista → boolean
* saldo_cc → número ≥ 0

---

# 🔷 API – Microserviço de Acesso (5001)

Base URL: `http://localhost:5001`

### **POST /clientes**

Criar cliente

```json
{
  "nome": "Isa",
  "telefone": "11999999999",
  "correntista": true,
  "saldo_cc": 200
}
```

### **GET /clientes**

Listar clientes

### **GET /clientes/1**

Buscar cliente

### **PUT /clientes/1**

Atualizar cliente

```json
{
  "nome": "Isabella",
  "telefone": "11999998888",
  "correntista": true,
  "saldo_cc": 350
}
```

### **DELETE /clientes/1**

Excluir cliente

### **GET /clientes/1/score**

Consultar score

### **POST /clientes/1/operacao**

Depósito:

```json
{
  "tipo": "deposito",
  "valor": 100
}
```

Saque:

```json
{
  "tipo": "saque",
  "valor": 50
}
```

---

# 🔶 API – Microserviço de Armazenamento (5000)

Base URL: `http://localhost:5000`

### Endpoints

* **POST /clientes** — Criar
* **GET /clientes** — Listar
* **GET /clientes/<id>** — Buscar
* **PUT /clientes/<id>** — Atualizar
* **DELETE /clientes/<id>** — Excluir

---

# 🚀 Como Executar

### Instalar dependências

```
pip install flask flasgger requests pytest pytest-cov
```

### Iniciar microserviço de armazenamento

```
python3 -m micro_servico.controller.storage_controller
```

### Iniciar microserviço de acesso

```
python3 -m acesso.controller.cliente_controller
```

---

# 📘 Documentação Swagger

### 🔷 Acesso

`http://localhost:5001/apidocs`


# 🧪 Testes Automatizados

O projeto possui uma suíte completa de testes com **Pytest**, garantindo alta confiabilidade do sistema.

### ✔ Cobertura de Testes

* Serviços
* Controladores (Flask)
* Clients (requests)
* Validações (schemas)
* Repositório (SQLite mockado)
* Banco de dados (mock db)
* Comunicação entre microserviços
* Fluxo completo: criar → atualizar → operar → excluir
* 100% de cobertura

---

## ▶️ Executar todos os testes

```
pytest -vv
```

## ▶️ Executar com cobertura

```
pytest --cov=. --cov-report=term-missing -vv
```

## ▶️ Gerar relatório HTML

```
pytest --cov=. --cov-report=html -vv
```

Abrir:

```
open htmlcov/index.html
```

---

# 🧪 Estrutura dos Testes

```
tests/
│
├── acesso/
│   ├── client/
│   │   └── test_client_requests.py
│   │
│   ├── controller/
│   │   ├── test_cliente_controller.py
│   │   └── test_cliente_controller_error.py
│   │
│   ├── service/
│   │   ├── test_atualizar_cliente.py
│   │   ├── test_calculos.py
│   │   ├── test_criar_cliente.py
│   │   ├── test_exclusao.py
│   │   ├── test_operacao.py
│   │   ├── test_processar_dados.py
│   │   └── test_validacoes.py
│   │
│   └── validators/
│       └── test_cliente_schema.py
│
└── micro_servico/
    ├── controller/
    │   └── test_storage_controller.py
    │
    └── repository/
        └── test_repository.py
```

---

# 🧩 Mocking Utilizado

✔ Mock de `requests` — evita chamadas externas
✔ Mock do SQLite — repositório sem banco real
✔ `flask.test_client()` — testes de rotas
✔ Mock das funções de serviço — isolamento das camadas

---

# 💯 Cobertura Final

```
TOTAL COVERAGE: 100%
```

### Módulos totalmente testados:

* acesso.client
* acesso.controller
* acesso.service
* acesso.validators
* micro_servico.controller
* micro_servico.repository
* micro_servico.database

---

# 🔧 Arquivo pytest.ini

```
[pytest]
addopts = --cov=. --cov-report=term-missing --cov-report=html

[coverage:report]
exclude_lines =
    ^\s*if __name__ == "__main__":
    ^\s*app\.run
```

---
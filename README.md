# 📦 StockMaster Pro - Sistema de Gestão de Inventário

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blue?style=for-the-badge)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

## 🎯 Sobre o Projeto
O **StockMaster Pro** é uma aplicação desktop desenvolvida para resolver a falta de controle de inventário em pequenos e médios armazéns. O objetivo foi criar uma ferramenta que eliminasse erros de digitação, evitasse a ruptura de estoque e garantisse a rastreabilidade de cada item movimentado.

Como profissional da área de estocagem, utilizei minha experiência operacional para implementar regras de negócio reais, transformando a necessidade logística em código funcional.

## ✨ Funcionalidades Implementadas

### 🔐 Segurança e Acesso
- **Autenticação de Usuários:** Sistema de login com banco de dados segregado para maior segurança.
- **Controle de Acesso (RBAC):** Diferenciação entre níveis de **Administrador** e **Operador**.
  - *Administradores:* Acesso total, incluindo gestão de usuários e exclusão de produtos.
  - *Operadores:* Acesso restrito a cadastros e movimentações de estoque.

### 📦 Gestão de Inventário
- **SKU Automático:** Geração sequencial de códigos únicos (ex: `PROD-001`), eliminando a redundância e erros humanos.
- **Busca Semântica (Autocomplete):** Filtro dinâmico em tempo real enquanto o usuário digita o nome ou SKU do produto.
- **Alertas de Estoque Mínimo:** Identificação visual imediata (cor vermelha) para itens que atingiram o nível crítico de segurança.
- **Sincronização em Tempo Real:** Implementação de um mecanismo de *polling* que atualiza a lista de inventário a cada 5 segundos, permitindo que múltiplos operadores vejam as mudanças simultaneamente.

### 🛡️ Auditoria e Integridade
- **Rastreabilidade Total:** Cada produto cadastrado e cada movimentação (entrada/saída) é vinculada ao usuário logado, criando um histórico de auditoria completo.
- **Validação de Saldo:** Bloqueio automático de saídas que resultariam em estoque negativo.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.x
- **Interface Gráfica:** `CustomTkinter` (Modern UI com suporte a Dark Mode).
- **Banco de Dados:** `SQLite` com gerenciamento de transações via `contextlib` para evitar travamentos de arquivo (*database locks*).

## 🚀 Como Executar o Projeto

### Pré-requisitos
Você precisará do Python instalado em sua máquina.

### Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/Saddh/StockMasterPro.git
   cd StockMasterPro
   ```

2. Instale a dependência de interface:
   ```bash
   pip install customtkinter
   ```

3. Execute a aplicação:
   ```bash
   python gui.py
   ```

### Credenciais de Teste
- **Usuário:** `admin`
- **Senha:** `admin123`

## 📈 Roadmap de Escalabilidade (Visão de Futuro)
Para transformar este projeto em um sistema de escala industrial (20+ operadores e 10.000+ itens), o plano de evolução inclui:
- [ ] **Migração para PostgreSQL:** Substituir o SQLite por um banco cliente-servidor para suportar centenas de conexões simultâneas.
- [ ] **Arquitetura de API:** Implementar um backend com **FastAPI** para separar a interface da lógica de dados.
- [ ] **WebSockets:** Substituir o timer de 5s por notificações em tempo real via sockets.
- [ ] **Paginação de Dados:** Implementar carregamento sob demanda (*Lazy Loading*) para otimizar a memória.

---
Desenvolvido por Dhemerson Henrick | Desenvolvedor Python.

---

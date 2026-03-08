# Sistema Contábil Educacional

Este é um sistema contábil educacional desenvolvido em Python usando Flask. Permite inserir lançamentos contábeis e gerar automaticamente relatórios como Balanço Patrimonial, DRE, DFC e DVA.

## Instalação

1. Certifique-se de ter Python 3.7+ instalado.
2. Instale as dependências: `pip install -r requirements.txt`
3. Navegue para a pasta do projeto: `cd sistema_contabil`
4. Execute o aplicativo: `python app.py`
5. Abra o navegador em `http://127.0.0.1:5000/`

## Dependências

- Flask: Framework web para Python.

## Estrutura do Projeto

- `app.py`: Arquivo principal do Flask.
- `database/db.py`: Configuração do banco de dados SQLite.
- `models/`: Modelos para Conta e Lançamento.
- `services/`: Serviços para cálculos dos relatórios.
- `routes/`: Rotas do Flask.
- `templates/`: Templates HTML.
- `static/`: CSS e JavaScript.

## Funcionalidades

- Dashboard com indicadores e gráficos.
- Cadastro e edição de lançamentos contábeis.
- Geração de relatórios contábeis: Balanço, DRE, DFC, DVA.

## Páginas Disponíveis

- `/`: Dashboard
- `/lancamentos`: Lista e cadastro de lançamentos
- `/balanco`: Balanço Patrimonial
- `/dre`: Demonstração do Resultado do Exercício
- `/dfc`: Demonstração de Fluxo de Caixa
- `/dva`: Demonstração do Valor Adicionado

## Notas

Este sistema é para fins educacionais e simplificado. Não substitui software contábil profissional.
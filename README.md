# Sistema de Requisição e Controle de EPIs

Este projeto é um sistema digital simples e funcional para automatizar o processo de solicitação, entrega e controle de EPIs (Equipamentos de Proteção Individual) em empresas.

## 🔧 Funcionalidades

- Solicitação digital de EPIs por gestores
- Confirmação de entrega pelo almoxarifado
- Atualização automática do estoque
- Visualização de relatórios e histórico de entregas
- Exportação dos dados em CSV
- Interface acessível via navegador usando Streamlit

## 🚀 Tecnologias Utilizadas

- Python
- Streamlit
- Google Colab
- CSV (para armazenamento de dados)
- PowerPoint (documentação de apresentação)

## 📂 Estrutura do Projeto

```
sistema-epi/
│
├── codigo/
│   └── app.py                     # Código principal do sistema
│
├── banco_de_dados/
│   ├── solicitacoes.csv          # Registros de solicitações
│   ├── entregas.csv              # Registros de entregas
│   └── epis.csv                  # EPIs disponíveis
│
├── documentos/
│   └── Apresentacao_Projeto_EPI_Completo.pptx  # Slides de apresentação
│
└── README.md
```

## ✅ Como Executar

1. Acesse o notebook no Google Colab ou use o terminal com `streamlit run app.py`.
2. Use `ngrok` para gerar um link público se estiver no Colab.
3. Faça as requisições pelo navegador e acompanhe os dados atualizados nos arquivos `.csv`.

---

Este projeto é gratuito para testes e pode ser escalado com integração a banco de dados, dashboards gráficos e autenticação de usuários.

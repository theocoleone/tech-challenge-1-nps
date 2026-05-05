================================================================================
                        TECH CHALLENGE FASE 1
                         Case NPS Preditivo
================================================================================

Autor: Theo Coleone de Camargo
Curso: Pós Graduação - AI Scientist - FIAP

================================================================================
1. OBJETIVO DO PROJETO
================================================================================

Este projeto tem como objetivo analisar dados operacionais de um e-commerce para
entender quais fatores influenciam a satisfação do cliente, medida pelo Net
Promoter Score (NPS). A partir dessa análise, buscamos identificar padrões que
permitam à empresa agir de forma proativa para melhorar a experiência do cliente
antes mesmo da aplicação da pesquisa de NPS.

O foco está em:
- Entender o problema de negócio e a importância do NPS
- Explorar os dados com foco em negócio (não só estatística)
- Identificar os fatores que mais impactam a satisfação
- Encontrar pontos de ruptura na experiência do cliente
- Propor uma estratégia preditiva para antecipar a satisfação

================================================================================
2. ENTENDIMENTO DO NEGÓCIO
================================================================================

2.1 Qual problema de negócio está sendo resolvido?
--------------------------------------------------------------------------------
A experiência do cliente (CX) no e-commerce impacta diretamente retenção,
recompra e crescimento. Com o crescimento acelerado, a empresa passou a lidar
com alta variabilidade no NPS entre diferentes perfis de consumidores. O problema
central é: quais fatores operacionais realmente influenciam a satisfação e como
agir de forma proativa para melhorar a experiência?

2.2 Por que o NPS é importante para um e-commerce?
--------------------------------------------------------------------------------
- Representa a satisfação e lealdade do cliente
- Métrica simples e amplamente utilizada no mercado (possibilita benchmarks)
- Captura a percepção geral da experiência
- Classifica os clientes em promotores, neutros e detratores
- Funciona como um indicador estratégico/termômetro
- Conecta a operação com a percepção do cliente

2.3 Quais áreas se beneficiam desses insights?
--------------------------------------------------------------------------------
- Logística: otimização de prazos e redução de atrasos
- Atendimento: priorização de casos críticos e redução de tempo de resolução
- Pricing: entender impacto de descontos e frete na satisfação
- Produto: melhorias baseadas em feedback real
- UX / Plataforma: experiência digital alinhada à expectativa
- ETC

2.4 Impacto do NPS no negócio
--------------------------------------------------------------------------------
Recompra:
  - Clientes promotores tendem a comprar mais vezes
  - Detratores dificilmente retornam
  - NPS alto → maior Lifetime Value (LTV = receita que o cliente gera durante todo relacionamento)

Boca a boca:
  - Promotores recomendam espontaneamente
  - Detratores fazem críticas públicas (reviews, redes sociais)
  - Avaliações impactam conversão
  - Reputação digital define confiança

Market Share:
  - Empresas com NPS alto crescem mais rápido
  - Mais clientes satisfeitos → mais indicações → menor Custo de Aquisição de Cliente (CAC)
  - NPS alto pode gerar crescimento orgânico e vantagem competitiva sustentável

2.5 Indicadores complementares
--------------------------------------------------------------------------------
O NPS sozinho não basta, uma vez que ele:
  - Não captura toda a jornada do cliente
  - Baixa representatividade (nem todos respondem)
  - Excesso de simplificação (resume a experiência em uma nota)

Indicadores que complementam: CSAT, CES (Customer Effort Score), taxa de
recompra, tempo de resolução, SLA logístico, benchmarks de NPS do setor.

================================================================================
3. DEFINIÇÃO DA TARGET
================================================================================

3.1 Qual variável representa a satisfação do cliente?
--------------------------------------------------------------------------------
A variável nps_score (nota de 0 a 10).

3.2 Por que ela foi escolhida?
--------------------------------------------------------------------------------
- É a métrica padrão de mercado para medir satisfação e lealdade
- Permite classificação direta (Promotor 9-10, Neutro 7-8, Detrator 0-6)
- Conecta percepção do cliente com resultado de negócio
- Funciona como termômetro estratégico da operação

3.3 Em que momento da jornada essa informação é coletada?
--------------------------------------------------------------------------------
O NPS é coletado após o encerramento da jornada de compra.
Isso limita a capacidade de antecipar problemas, justificando a necessidade
de um modelo preditivo.

3.4 Existe algum risco de usar essa variável de forma inadequada?
--------------------------------------------------------------------------------
Sim:
- Um único problema pode impactar a nota, mesmo que o restante da experiência
  tenha sido positivo
- Nem todos os clientes respondem à pesquisa (viés de seleção)
- Forçar resposta pode gerar viés e distorcer os resultados
- O NPS resume a experiência em uma única nota, podendo ocultar causas
  específicas de satisfação ou insatisfação

================================================================================
4. DESCRIÇÃO DA BASE DE DADOS
================================================================================

Arquivo: desafio_nps_fase_1.csv

Variáveis disponíveis:
- customer_id: Identificador único do cliente
- order_id: Identificador único do pedido
- customer_age: Idade do cliente
- customer_region: Região geográfica do cliente
- customer_tenure_months: Tempo de relacionamento com a empresa (meses)
- order_value: Valor total do pedido
- items_quantity: Quantidade de itens no pedido
- discount_value: Valor de desconto aplicado
- payment_installments: Número de parcelas do pagamento
- delivery_time_days: Tempo total de entrega (dias)
- delivery_delay_days: Dias de atraso na entrega
- freight_value: Valor do frete
- delivery_attempts: Número de tentativas de entrega
- customer_service_contacts: Contatos do cliente com o atendimento
- resolution_time_days: Tempo para resolução de problemas (dias)
- complaints_count: Número de reclamações registradas
- repeat_purchase_30d: Recompra em até 30 dias (0=não, 1=sim)
- csat_internal_score: Score interno de satisfação
- nps_score: Nota de satisfação (NPS), de 0 a 10 (TARGET)

================================================================================
5. METODOLOGIA UTILIZADA
================================================================================

5.1 Exploração Inicial (Sanity Check)
--------------------------------------------------------------------------------
- Verificação de dimensões, tipos de dados, nulos e duplicatas
- Validação de unicidade de IDs (customer_id, order_id)
- Análise de distribuição de cada variável individualmente
- Verificação de viéses na base (concentração por região, faixa etária)

5.2 Análise Exploratória (EDA) com foco em negócio
--------------------------------------------------------------------------------
Perguntas respondidas:

a) Quais fatores parecem mais críticos para a satisfação?
   → Correlação de Pearson e Spearman de todas as variáveis numéricas com o NPS
   → Variáveis com correlação negativa forte: reclamações, atraso, contatos
     com atendimento, tempo de resolução

b) O que mais gera detratores?
   → Reclamações (Impacto: 95.65%)
   → Atraso na entrega (Impacto: 63.54%)
   → Contato com atendimento (Impacto: 40.79%)
   → Tempo para resolução de problemas (Impacto: 24.02%)
   → Insight: embora o atraso tenha maior correlação com NPS, o volume de
     reclamações demonstra maior impacto na geração de detratores

c) Existe algum "ponto de ruptura"?
   → Sim. Identificamos o valor exato de cada variável onde o NPS sofre a
     maior queda (ex: a partir de 1 dia de atraso, a satisfação despenca)
   → Útil para definir SLAs e alertas operacionais

d) Que tipo de cliente tende a ter NPS mais alto ou mais baixo?
   → A satisfação não depende de quem o cliente é (idade, região), mas do
     que ele vivencia ao longo da jornada (atrasos, reclamações, atendimento)
   → Perfil comparativo entre Promotores, Neutros e Detratores

5.3 Proposta de Modelo Preditivo (reflexão)
--------------------------------------------------------------------------------
Estratégia proposta: modelo preditivo "misto" em duas camadas

Camada 1 - Classificação:
  "Esse cliente está em risco de ser detrator?"
  → Output: classificação dos clientes quanto ao risco
  → Serve para priorizar ações e escalar casos críticos

Camada 2 - Regressão:
  "Qual seria a nota provável desse cliente?"
  → Output: previsão do NPS
  → Serve para entender intensidade e diferenciar casos dentro do mesmo grupo

Inputs do modelo:
  - Atraso de entrega
  - Número de reclamações
  - Contatos com atendimento
  - Tempo de resolução
  - CSAT interno
  - Comportamento de compra

Aplicação prática:
  - Fila de atendimento baseada em risco
  - Alertas automáticos para casos críticos
  - Ação preventiva antes da pesquisa de NPS
  - Rodar modelo em clientes ativos → gerar score de risco → priorizar

================================================================================
6. COMO REPRODUZIR OS RESULTADOS
================================================================================

Pré-requisitos:
- Python 3.8+
- Bibliotecas: pandas, seaborn, matplotlib, scipy

  1. Clone o repositório
  2. Crie e ative um ambiente virtual:
     python3 -m venv venv
     source venv/bin/activate        (Linux/Mac)
     venv\Scripts\activate           (Windows)
  3. Instale as dependências:
     pip install -r requirements.txt
  4. Execute a partir da pasta notebooks/:
     cd notebooks/
     python tech_challenge.py

Estrutura do repositório:
  /
  ├── README.txt                              → Este arquivo
  ├── requirements.txt                        → Dependências do projeto
  ├── data/
  │   └── desafio_nps_fase_1.csv              → Base de dados
  ├── notebooks/
  │   └── tech_challenge.py                   → Código da análise (EDA completa)
  ├── reports/
  │   └── Tech Challenge 2.pptx              → Apresentação (storytelling gerencial)
  └── docs/
      └── 1IAST - Fase 1 - Tech Challenge.pdf → Enunciado do desafio

================================================================================
7. LIMITAÇÕES E RISCOS
================================================================================

- O NPS é coletado pós-compra, então o modelo preditivo depende de dados
  operacionais disponíveis antes da pesquisa
- A base pode não representar todos os perfis de clientes (viés de resposta)
- Correlação não implica causalidade — os fatores identificados são associações
- O modelo proposto ainda não foi implementado (next step)

================================================================================

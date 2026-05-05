# TECH CHALLENGE FASE 1 — Case NPS Preditivo

**Autor:** Theo Coleone de Camargo  
**Curso:** Pós Graduação - AI Scientist - FIAP

---

## 1. Objetivo do Projeto

Este projeto tem como objetivo analisar dados operacionais de um e-commerce para entender quais fatores influenciam a satisfação do cliente, medida pelo Net Promoter Score (NPS). A partir dessa análise, buscamos identificar padrões que permitam à empresa agir de forma proativa para melhorar a experiência do cliente antes mesmo da aplicação da pesquisa de NPS.

**Foco:**
- Entender o problema de negócio e a importância do NPS
- Explorar os dados com foco em negócio (não só estatística)
- Identificar os fatores que mais impactam a satisfação
- Encontrar pontos de ruptura na experiência do cliente
- Propor uma estratégia preditiva para antecipar a satisfação

---

## 2. Entendimento do Negócio

### 2.1 Qual problema de negócio está sendo resolvido?

A experiência do cliente (CX) no e-commerce impacta diretamente retenção, recompra e crescimento. Com o crescimento acelerado, a empresa passou a lidar com alta variabilidade no NPS entre diferentes perfis de consumidores. O problema central é: **quais fatores operacionais realmente influenciam a satisfação e como agir de forma proativa para melhorar a experiência?**

### 2.2 Por que o NPS é importante para um e-commerce?

- Representa a satisfação e lealdade do cliente
- Métrica simples e amplamente utilizada no mercado (possibilita benchmarks)
- Captura a percepção geral da experiência
- Classifica os clientes em promotores, neutros e detratores
- Funciona como um indicador estratégico/termômetro
- Conecta a operação com a percepção do cliente

### 2.3 Quais áreas se beneficiam desses insights?

| Área | Benefício |
|------|-----------|
| Logística | Otimização de prazos e redução de atrasos |
| Atendimento | Priorização de casos críticos e redução de tempo de resolução |
| Pricing | Entender impacto de descontos e frete na satisfação |
| Produto | Melhorias baseadas em feedback real |
| UX / Plataforma | Experiência digital alinhada à expectativa |

### 2.4 Impacto do NPS no negócio

**Recompra:**
- Clientes promotores tendem a comprar mais vezes
- Detratores dificilmente retornam
- NPS alto → maior Lifetime Value (LTV)

**Boca a boca:**
- Promotores recomendam espontaneamente
- Detratores fazem críticas públicas (reviews, redes sociais)
- Avaliações impactam conversão
- Reputação digital define confiança

**Market Share:**
- Empresas com NPS alto crescem mais rápido
- Mais clientes satisfeitos → mais indicações → menor CAC
- NPS alto pode gerar crescimento orgânico e vantagem competitiva sustentável

### 2.5 Indicadores complementares

O NPS sozinho não basta:
- Não captura toda a jornada do cliente
- Baixa representatividade (nem todos respondem)
- Excesso de simplificação (resume a experiência em uma nota)

**Indicadores complementares:** CSAT, CES (Customer Effort Score), taxa de recompra, tempo de resolução, SLA logístico, benchmarks de NPS do setor.

---

## 3. Definição da Target

| Pergunta | Resposta |
|----------|----------|
| Qual variável representa a satisfação? | `nps_score` (nota de 0 a 10) |
| Por que foi escolhida? | Métrica padrão de mercado, permite classificação direta (Promotor 9-10, Neutro 7-8, Detrator 0-6) |
| Quando é coletada? | Após o encerramento da jornada de compra |

**Riscos:**
- Um único problema pode impactar a nota, mesmo que o restante da experiência tenha sido positivo
- Nem todos os clientes respondem à pesquisa (viés de seleção)
- Forçar resposta pode gerar viés e distorcer os resultados
- O NPS resume a experiência em uma única nota, podendo ocultar causas específicas

---

## 4. Descrição da Base de Dados

**Arquivo:** `desafio_nps_fase_1.csv`

| Variável | Descrição |
|----------|-----------|
| `customer_id` | Identificador único do cliente |
| `order_id` | Identificador único do pedido |
| `customer_age` | Idade do cliente |
| `customer_region` | Região geográfica do cliente |
| `customer_tenure_months` | Tempo de relacionamento com a empresa (meses) |
| `order_value` | Valor total do pedido |
| `items_quantity` | Quantidade de itens no pedido |
| `discount_value` | Valor de desconto aplicado |
| `payment_installments` | Número de parcelas do pagamento |
| `delivery_time_days` | Tempo total de entrega (dias) |
| `delivery_delay_days` | Dias de atraso na entrega |
| `freight_value` | Valor do frete |
| `delivery_attempts` | Número de tentativas de entrega |
| `customer_service_contacts` | Contatos do cliente com o atendimento |
| `resolution_time_days` | Tempo para resolução de problemas (dias) |
| `complaints_count` | Número de reclamações registradas |
| `repeat_purchase_30d` | Recompra em até 30 dias (0=não, 1=sim) |
| `csat_internal_score` | Score interno de satisfação |
| `nps_score` | **Nota de satisfação (NPS), de 0 a 10 (TARGET)** |

---

## 5. Metodologia Utilizada

### 5.1 Exploração Inicial (Sanity Check)

- Verificação de dimensões, tipos de dados, nulos e duplicatas
- Validação de unicidade de IDs (`customer_id`, `order_id`)
- Análise de distribuição de cada variável individualmente
- Verificação de viéses na base (concentração por região, faixa etária)

### 5.2 Análise Exploratória (EDA) com foco em negócio

**a) Quais fatores parecem mais críticos para a satisfação?**
- Correlação de Pearson e Spearman de todas as variáveis numéricas com o NPS
- Variáveis com correlação negativa forte: reclamações, atraso, contatos com atendimento, tempo de resolução

**b) O que mais gera detratores?**

| Variável | Impacto |
|----------|---------|
| Reclamações | 95.65% |
| Atraso na entrega | 63.54% |
| Contato com atendimento | 40.79% |
| Tempo para resolução | 24.02% |

> **Insight:** embora o atraso tenha maior correlação com NPS, o volume de reclamações demonstra maior impacto na geração de detratores.

**c) Existe algum "ponto de ruptura"?**
- Sim. Identificamos o valor exato de cada variável onde o NPS sofre a maior queda
- Exemplo: a partir de 1 dia de atraso, a satisfação despenca
- Útil para definir SLAs e alertas operacionais

**d) Que tipo de cliente tende a ter NPS mais alto ou mais baixo?**
- A satisfação não depende de quem o cliente é (idade, região), mas do que ele vivencia ao longo da jornada
- Perfil comparativo entre Promotores, Neutros e Detratores

### 5.3 Proposta de Modelo Preditivo

Estratégia proposta: **modelo preditivo "misto" em duas camadas**

| Camada | Pergunta | Output | Utilidade |
|--------|----------|--------|-----------|
| Classificação | "Esse cliente está em risco de ser detrator?" | Classificação de risco | Priorizar ações e escalar casos críticos |
| Regressão | "Qual seria a nota provável desse cliente?" | Previsão do NPS | Entender intensidade e diferenciar casos |

**Inputs do modelo:**
- Atraso de entrega
- Número de reclamações
- Contatos com atendimento
- Tempo de resolução
- CSAT interno
- Comportamento de compra

**Aplicação prática:**
- Fila de atendimento baseada em risco
- Alertas automáticos para casos críticos
- Ação preventiva antes da pesquisa de NPS
- Rodar modelo em clientes ativos → gerar score de risco → priorizar

---

## 6. Como Reproduzir os Resultados

**Pré-requisitos:** Python 3.8+ | pandas, seaborn, matplotlib, scipy

```bash
# 1. Clone o repositório
git clone <url-do-repo>

# 2. Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a análise
cd notebooks/
python tech_challenge.py
```

**Estrutura do repositório:**

```
/
├── README.md                                → Este arquivo
├── requirements.txt                         → Dependências do projeto
├── data/
│   └── desafio_nps_fase_1.csv               → Base de dados
├── notebooks/
│   └── tech_challenge.py                    → Código da análise (EDA completa)
├── presentation/
│   ├── Tech_Challenge_1.pptx               → Slides da apresentação
│   └── Apresentacao_Tech_Challenge_1.mp4                    → Vídeo da apresentação
└── docs/
    └── 1IAST - Fase 1 - Tech Challenge.pdf → Enunciado do desafio
```

---

## 7. Limitações e Riscos

- O NPS é coletado pós-compra, então o modelo preditivo depende de dados operacionais disponíveis antes da pesquisa
- A base pode não representar todos os perfis de clientes (viés de resposta)
- Correlação não implica causalidade — os fatores identificados são associações
- O modelo proposto ainda não foi implementado (next step)


---

## 8. Apresentação

[![Assistir apresentação](https://img.youtube.com/vi/Ae6awuAF95c/0.jpg)](https://youtu.be/Ae6awuAF95c)

📁 Os arquivos da apresentação estão em `presentation/`:
- `Tech_Challenge_1.pptx` — Slides
- `apresentacao.mp4` — Gravação em vídeo

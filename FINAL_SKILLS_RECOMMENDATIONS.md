# Финальные рекомендации по развитию библиотеки PdM Skills

> Итоговый design doc по улучшению библиотеки `PdM skills` с учётом текущих 106 скиллов, `RECOMMENDATIONS.md`, базы МУЦП и материалов из папки `для обогащения`, включая кейс `Цифровые бизнес-модели.md`.

---

## 1. Короткий CPO-вердикт

Библиотека уже выглядит как сильный черновик продуктового тулкита: покрыты discovery, PRD, roadmap, метрики, эксперименты, SaaS, marketplace, fintech, e-commerce, govtech, AI/LLM и enterprise. Это больше не набор случайных промптов — это почти операционная система для PM.

Но сейчас она находится в промежуточном состоянии:

- **по охвату:** сильная;
- **по архитектуре:** перегруженная и местами хаотичная;
- **по метрикам:** богатая, но не стандартизированная;
- **по доменному разделению:** полезная, но смешивает lifecycle, business model, industry и craft;
- **по качеству отдельных скиллов:** неравномерная: часть зрелые, часть похожи на короткие заготовки;
- **по CPO-уровню:** не хватает executive-слоя: портфель, P&L, инвестиционные решения, operating model, product health review.

Главная рекомендация: **не добавлять новые 20–30 скиллов, пока не наведена архитектура.** Сначала нужно превратить библиотеку из каталога команд в понятную продуктовую систему: таксономия, единый шаблон, метрики по доменам, правила выбора скилла, maturity-stage логика.

---

## 2. Что использовать из материалов «для обогащения»

### 2.1. Из базы МУЦП

Из `База_знаний_МУЦП.md` стоит забрать не столько определения, сколько **сквозную логику принятия решений**:

```text
Проблема → Discovery → Исследование → Данные → Интерпретация → Инсайт →
Гипотеза → Эксперимент → Решение → Метрики → Стратегия
```

Это должно стать базовой рамкой для всех core/craft-скиллов.

Что конкретно интегрировать:

- Problem statement как обязательный блок в `prd`, `discovery-sprint`, `hypothesis-tree`, `decision-doc`.
- Разделение discovery/delivery риска: “построить не то” vs “построить неправильно”.
- Value / Usability / Feasibility / Viability как стандартная проверка крупных инициатив.
- Формат гипотезы `If–Then–Because`.
- Схему эксперимента: `1 OEC + 2–3 guardrails + 3–5 supporting metrics`.
- Decision Log для всех скиллов, где принимается решение.
- Assumption Mapping: влияние × неопределённость.
- Real Options: Commit / Option / Kill.
- Правило: A/B-тест — не старт мышления, а высокий уровень доказательства, когда хватает трафика и можно изолировать эффект.

### 2.2. Из `Цифровые бизнес-модели.md`

Файл полезен как пример **CPO-grade бизнес-кейса**, потому что в нём есть то, чего не хватает многим текущим скиллам:

- явный business context;
- выбор бизнес-модели через сравнение альтернатив;
- D2C/subscription логика;
- Business Model Canvas;
- unit economics;
- growth loop;
- network effects loop;
- risk heat map;
- принципы/tenets;
- коммуникации по аудиториям;
- roadmap по фазам;
- роли команды;
- источники данных и допущения.

Эту структуру стоит использовать как эталон для скиллов уровня `business-case`, `product-strategy`, `marketplace-model`, `subscription-economics`, `growth-loop`, `gtm-strategy`, `ecosystem-design`.

Особенно ценно: в кейсе бизнес-модель не висит отдельно от продукта. Она связана с каналами, retention, supply-side, логистикой, брендом, рисками, коммуникацией и экономикой.

---

## 3. Главная проблема текущей архитектуры

В `manager.py` сейчас есть пресеты:

- `core`
- `discovery`
- `saas`
- `marketplace`
- `fintech`
- `ecom-retail`
- `telecom-media`
- `enterprise-gov`
- `craft`

Проблема: это разные оси классификации.

| Текущий пресет | Что это на самом деле | Проблема |
|---|---|---|
| `core` | базовый lifecycle PM | не домен |
| `discovery` | этап работы | не домен |
| `saas` | бизнес-модель | частично содержит generic growth |
| `marketplace` | бизнес-модель | ок, но смешивает marketplace, classifieds, e-com ops |
| `fintech` | индустрия | содержит `internal-roi`, который скорее enterprise/internal |
| `ecom-retail` | индустрия + модель | содержит generic CRO |
| `telecom-media` | несколько индустрий | свалены telecom, media, edtech, adtech |
| `enterprise-gov` | B2B/enterprise + govtech | полезно, но лучше разделить |
| `craft` | кладовка продвинутых тем | смешаны AI, platform, GTM, strategy, incidents |

Сейчас библиотека отвечает на вопрос: “Куда примерно положить скилл?”

Нужно, чтобы она отвечала на вопрос: **“Какой скилл нужен под мою задачу, продукт, бизнес-модель и стадию?”**

---

## 4. Новая таксономия: 4 независимые оси

Каждый скилл должен иметь не один `preset`, а набор тегов.

### 4.1. Ось 1 — Lifecycle

| Lifecycle | Смысл | Примеры скиллов |
|---|---|---|
| `discovery` | понять проблему и пользователя | `user-interview-prep`, `jobs-to-be-done`, `customer-journey-map`, `discovery-sprint` |
| `strategy` | выбрать рынок, позиционирование, ставки | `market-sizing`, `competitive-moat`, `positioning-statement`, `product-teardown` |
| `definition` | описать решение и требования | `prd`, `user-stories`, `api-product-spec`, `ai-feature-spec` |
| `launch` | вывести в прод и раскатить | `launch-checklist`, `feature-flag-strategy`, `enterprise-rollout` |
| `growth` | привлечение, активация, удержание | `growth-loop`, `plg-design`, `channel-mix`, `referral-mechanics`, `cro-audit` |
| `measure` | метрики, эксперименты, решения | `metrics-analyzer`, `ab-test-design`, `okr-writer`, `decision-doc` |
| `operations` | операционная устойчивость | `incident-pm-role`, `service-desk-metrics`, `returns-management` |
| `communication` | синхронизация людей | `stakeholder-update`, `meeting-prep`, `release-notes`, `retro-facilitator` |

### 4.2. Ось 2 — Business model

| Business model | Примеры скиллов |
|---|---|
| `saas` | `saas-metrics`, `pricing-model`, `plg-design`, `subscription-economics` |
| `subscription` | `subscription-economics`, `retention-model`, `pricing-experiment`, `notification-strategy` |
| `marketplace` | `marketplace-model`, `matching-algorithm`, `supply-quality`, `seller-economics` |
| `classifieds` | `classifieds-model`, `c2c-dynamics`, `seller-journey`, `search-ranking` |
| `ecommerce` | `checkout-audit`, `catalog-strategy`, `fulfillment-model`, `returns-management` |
| `d2c` | новый слой: D2C, бренд, подписка, fulfillment, owned audience |
| `platform-api` | `platform-strategy`, `api-product-spec`, `mini-app-platform` |
| `ads` | `ads-platform-pm`, `dsp-ssp-spec`, `content-strategy` |
| `fintech-lending` | `credit-product-spec`, `unit-economics`, `compliance-checkpoint` |
| `internal-product` | `internal-product-discovery`, `internal-roi`, `admin-ux` |
| `govtech` | `govtech-metrics`, `citizen-journey`, `public-service-design` |
| `ai-data` | `llm-product-design`, `ai-feature-spec`, `data-product-spec` |

### 4.3. Ось 3 — Domain / Industry

| Domain | Примеры |
|---|---|
| `fintech` | banking, lending, payments, wealth, insurance |
| `retail` | e-com, grocery, loyalty, supply chain |
| `telecom` | VAS, B2B connectivity, OSS/BSS |
| `media` | streaming, UGC, content products |
| `edtech` | learning journeys, LMS, B2B education |
| `adtech` | DSP/SSP, auction, attribution |
| `govtech` | госуслуги, МФЦ, ведомственные процессы |
| `hrtech` | HR systems, L&D, performance review |
| `logistics` | last mile, returns, fulfillment |
| `real-estate` | property, ипотека, escrow, classifieds |
| `food-d2c` | новый домен из `Цифровые бизнес-модели`: fresh food, premium, subscription, logistics |

### 4.4. Ось 4 — Product stage

| Stage | Как меняется применение скилла |
|---|---|
| `idea` | больше discovery, market sizing, assumption mapping |
| `mvp` | problem/solution fit, ручные пилоты, ранние метрики |
| `pre-pmf` | retention, активация, повторное поведение, qualitative evidence |
| `pmf` | unit economics, scalable acquisition, roadmap bets |
| `scale` | operating model, guardrails, margin, reliability, portfolio |
| `mature` | efficiency, monetization, moat, cannibalization |
| `turnaround` | diagnosis, kill/iterate, cost cutting, refocus |

---

## 5. Новые пресеты вместо текущих

### 5.1. Lifecycle presets

```python
"discovery": [...]
"strategy": [...]
"definition": [...]
"launch": [...]
"growth": [...]
"measure": [...]
"operations": [...]
"communication": [...]
```

### 5.2. Business model presets

```python
"saas": [...]
"subscription": [...]
"marketplace": [...]
"classifieds": [...]
"ecommerce": [...]
"d2c": [...]
"platform-api": [...]
"ads": [...]
"internal-products": [...]
"ai-data": [...]
```

### 5.3. Industry presets

```python
"fintech": [...]
"retail": [...]
"telecom": [...]
"media": [...]
"edtech": [...]
"adtech": [...]
"govtech": [...]
"hrtech": [...]
"logistics": [...]
"food-d2c": [...]
```

### 5.4. Role presets

```python
"junior-pm-core"
"middle-pm-craft"
"growth-pm"
"b2b-saas-pm"
"marketplace-pm"
"fintech-pm"
"ai-product-pm"
"enterprise-pm"
"cpo-strategy"
```

---

## 6. Что конкретно исправить в текущих пресетах

### 6.1. Разобрать `telecom-media`

Сейчас там смешаны:

- telecom: `vas-product`, `b2b-telecom`;
- media: `streaming-product`, `ugc-platform`, `content-strategy`;
- edtech: `learning-product`, `b2b-edtech`;
- adtech: `ads-platform-pm`, `dsp-ssp-spec`.

Рекомендация: разделить на `telecom`, `media`, `edtech`, `adtech`.

### 6.2. Разобрать `craft`

Оставить в `craft` только универсальные продвинутые техники:

- `north-star-metric`
- `hypothesis-tree`
- `jobs-to-be-done`
- `competitive-moat`
- `feature-flag-strategy`
- `incident-pm-role`
- `decision-doc`

Вынести отдельно:

- AI/Data: `ai-feature-spec`, `llm-product-design`, `data-product-spec`;
- Platform/API: `api-product-spec`, `platform-strategy`, `mini-app-platform`;
- Growth/GTM: `channel-mix`, `gtm-strategy`, `localization-strategy`;
- Ecosystem: `ecosystem-design`, `superapp-strategy`, `loyalty-program`.

### 6.3. Вынести `growth` в отдельный слой

Сейчас growth разбросан по `saas`, `ecom-retail`, `craft`, `discovery`.

Собрать:

- `growth-loop`
- `gtm-strategy`
- `channel-mix`
- `plg-design`
- `referral-mechanics`
- `cro-audit`
- `onboarding-audit`
- `retention-model`
- `notification-strategy`
- `monetization-audit`
- `positioning-statement`
- `icp-definition`

### 6.4. Добавить D2C / Subscription Commerce

Из `Цифровые бизнес-модели.md` видно слепое пятно: библиотека покрывает SaaS, marketplace, e-commerce, но плохо выделяет **D2C-подписку с физическим продуктом**.

Нужен отдельный скилл:

```text
/d2c-subscription-model
```

Он должен покрывать:

- owned audience;
- brand moat;
- recurring revenue;
- subscription flexibility;
- fulfillment and freshness;
- churn and pause logic;
- cohort retention;
- box economics;
- community/referral;
- supplier/partner economics;
- risk heat map.

---

## 7. Единый шаблон `SKILL.md`

Каждый скилл должен быть одинаково читаем и исполним.

### 7.1. Исправить frontmatter

Сейчас во многих файлах встречается:

```yaml
preset: craft---
```

Должно быть:

```yaml
---
name: jobs-to-be-done
description: ...
argument-hint: ...
allowed-tools: Read, Write
preset: craft
lifecycle: discovery
business-model: any
domain: generic
stage: idea,mvp,pre-pmf
output-artifact: jtbd-analysis
---
```

### 7.2. Новый стандарт тела скилла

```md
# [Название скилла]

## Когда использовать

## Когда НЕ использовать

## Входные данные
- Обязательные
- Желательные
- Если данных нет — какие вопросы задать

## Процесс
1. ...

## Формат вывода

## Метрики
### Outcome / North Star
### Input metrics
### Guardrails
### Diagnostic metrics
### Instrumentation

## Decision rules
- Ship
- Iterate
- Kill

## Типичные ошибки

## Хороший пример

## Плохой пример
```

---

## 8. Стандарт метрик для всех скиллов

Сейчас метрики есть, но они живут по-разному. Нужно ввести единый слой.

Каждый доменный скилл должен содержать:

```md
### Метрики

#### Outcome metric
Главная метрика результата. Почему она отражает ценность, а не vanity.

#### Input metrics
Что двигает outcome. Метрики, которыми команда реально управляет.

#### Guardrails
Что нельзя ухудшить при росте outcome.

#### Diagnostic metrics
Куда смотреть, если outcome не двигается.

#### Instrumentation
Какие события/данные нужны, чтобы метрики не были фантазией.

#### Decision rules
Пороги: когда ship, iterate, kill.
```

### 8.1. Пример для D2C-подписки

Из `Цифровые бизнес-модели.md`:

| Уровень | Метрики |
|---|---|
| Outcome | MRR, contribution margin, active subscribers |
| Input | acquisition conversion, first order success, delivery SLA, pause return rate |
| Retention | monthly churn, repeat delivery rate, subscription pause rate, reactivation |
| Economics | ARPU, AOV, gross margin, CAC, LTV, LTV/CAC, CAC payback |
| Guardrails | delivery delay rate, complaint rate, refund rate, supplier margin, quality incidents |
| Diagnostics | channel CAC, cohort retention, NPS by delivery cohort, churn reason, stockout rate |

---

## 9. Доменные метрики: что добавить

### 9.1. SaaS

Добавить в `saas-metrics`:

- activation rate;
- time-to-value;
- product qualified accounts/leads;
- feature adoption by account;
- account health score;
- seat expansion;
- integration depth;
- cohort retention by MRR;
- CAC payback by segment;
- sales efficiency.

Текущий `saas-metrics` силён по финансовой стороне, но недостаточно связывает usage с revenue retention.

### 9.2. Marketplace

Добавить в `marketplace-model`:

- liquidity by geo/category;
- time-to-first-match;
- search success rate;
- supply coverage;
- demand coverage;
- cancellation rate;
- dispute rate;
- leakage/disintermediation rate;
- take rate vs seller margin;
- subsidy burn.

Правило: **запрещать оценивать marketplace по среднему GMV без разреза категория × гео × цена × время.**

### 9.3. E-commerce / Retail

Добавить:

- contribution margin per order;
- gross margin after returns;
- promo dependency;
- repeat purchase rate;
- stock availability;
- substitution rate;
- delivery promise accuracy;
- refund cycle time;
- return abuse rate.

Убрать чрезмерно точные неподтверждённые бенчмарки вроде “каждое поле снижает конверсию на 5–10%”. Лучше: “часто снижает, точный эффект проверять на своей воронке”.

### 9.4. Fintech

Добавить:

- risk-adjusted return;
- approval rate vs default rate;
- vintage analysis;
- DPD 1+/30+/60+/90+;
- fraud loss rate;
- manual review rate;
- KYC pass rate;
- time-to-decision;
- false positive / false negative для антифрода;
- regulatory breach risk.

### 9.5. AI / LLM

Добавить:

- eval dataset design;
- golden set;
- severity levels ошибок;
- hallucination severity;
- groundedness;
- answer relevance;
- cost per successful task;
- containment rate;
- escalation rate;
- human review sampling;
- prompt injection risk;
- PII leakage;
- model drift;
- rollback plan.

Ключевой вопрос для каждого AI-скилла: **какова цена ошибки и кто несёт ответственность?**

### 9.6. GovTech / Enterprise

Добавить:

- first-time-right;
- legal SLA breach rate;
- assisted digital rate;
- vulnerable groups success rate;
- call center deflection;
- appeal/rework rate;
- audit trail completeness;
- cost per transaction;
- employee effort score для внутренних продуктов.

### 9.7. AdTech

Добавить:

- fill rate;
- ad load;
- auction density;
- bid win rate;
- eCPM;
- ROAS;
- advertiser retention;
- budget utilization;
- campaign creation success rate;
- incrementality;
- relevance score;
- organic cannibalization;
- user experience guardrails.

---

## 10. Что добавить из кейса цифровой бизнес-модели

### 10.1. Новый скилл `/business-model-canvas`

Сейчас BMC есть как концепция, но нет сильного отдельного скилла.

Выходной артефакт:

- Customer Segments;
- Value Proposition;
- Channels;
- Customer Relationships;
- Revenue Streams;
- Key Resources;
- Key Activities;
- Key Partners;
- Cost Structure;
- explicit assumptions;
- top risks;
- metric tree;
- decision: proceed / narrow / pivot / kill.

### 10.2. Новый скилл `/business-case`

Формат по примеру `Слобода Online`:

1. Problem / Background.
2. Market and segment.
3. Alternatives considered.
4. Recommended model.
5. Unit economics.
6. KPI by year.
7. Roadmap by phases.
8. Team/resources.
9. Risk heat map.
10. Communications by stakeholder.
11. Tenets.
12. Decision request.

### 10.3. Новый скилл `/d2c-subscription-model`

Нужен для продуктов типа:

- food box;
- premium goods subscription;
- beauty box;
- pet food subscription;
- фермерская подписка;
- локальные бренды с регулярной доставкой.

Структура:

- why subscription vs one-off store vs marketplace;
- owned channel strategy;
- subscription tiers;
- pause/skip/cancel UX;
- box economics;
- delivery/freshness SLA;
- supplier economics;
- retention content;
- referral loop;
- churn diagnostics;
- risk heat map.

### 10.4. Новый скилл `/tenets-writer`

В `Цифровые бизнес-модели.md` сильный блок tenets: принципы не просто перечислены, а привязаны к рискам и проверкам.

Формат:

| Tenet | Почему критично | Где риск нарушить | Как проверять | Guardrail |
|---|---|---|---|---|

Пример: “Гибкость подписки” → риск dark patterns → проверка pause/cancel success rate → guardrail complaint rate.

### 10.5. Новый скилл `/risk-heatmap`

Сейчас риски есть в отдельных скиллах, но нет универсального инструмента.

Формат:

- market risks;
- operational risks;
- brand/reputation risks;
- financial risks;
- tech risks;
- regulatory risks;
- probability × impact;
- trigger signals;
- mitigation;
- owner;
- review cadence.

---

## 11. Не хватает CPO/executive layer

Сейчас библиотека сильна для PM/Senior PM, но не закрывает CPO-повестку.

Добавить скиллы:

| Скилл | Что делает |
|---|---|
| `/product-strategy` | стратегия продукта: рынок, пользователь, ценность, ставки, метрики, trade-offs |
| `/portfolio-review` | обзор продуктового портфеля: invest / maintain / harvest / kill |
| `/product-health-review` | диагностика здоровья продукта по метрикам, пользователям, экономике, рискам |
| `/investment-memo` | обоснование инвестиций в инициативу для CEO/CFO/board |
| `/business-case` | полный бизнес-кейс с unit economics, рисками, roadmap |
| `/kill-or-scale-decision` | решение: масштабировать, сузить, пивотнуть или закрыть |
| `/annual-planning` | годовое планирование: цели, bets, ресурсы, зависимости |
| `/product-operating-model` | модель работы продуктовой организации: ритуалы, роли, decision rights |
| `/product-org-design` | структура команд, ownership, platform/product split |
| `/cpo-board-update` | короткий board-level апдейт: метрики, риски, решения |
| `/roadmap-tradeoff-review` | ревью roadmap на trade-offs, capacity, стратегический fit |
| `/product-team-scorecard` | оценка зрелости продуктовых команд |

---

## 12. Приоритетный план работ

### P0 — нормализация библиотеки

1. Исправить frontmatter во всех `SKILL.md`.
2. Ввести единый шаблон тела скилла.
3. Добавить metadata-поля: `lifecycle`, `business-model`, `domain`, `stage`, `output-artifact`.
4. Сделать `SKILL_MAP.md`: какой скилл когда использовать.
5. Обновить `manager.py`, чтобы он работал не только с одним `preset`, а с тегами.

### P1 — перестроить пресеты

1. Разделить `telecom-media`.
2. Разобрать `craft`.
3. Добавить `growth`.
4. Добавить `ai-data`.
5. Добавить `platform-api`.
6. Добавить `d2c` / `subscription-commerce`.
7. Добавить role-based combos.

### P2 — усилить метрики

1. Создать `METRICS_TAXONOMY.md`.
2. Для каждого домена описать outcome/input/guardrail/diagnostic metrics.
3. Обновить 15 ключевых скиллов с единым metrics-блоком.
4. Добавить instrumentation checklist.

### P3 — добавить CPO layer

1. `/business-case`
2. `/product-strategy`
3. `/investment-memo`
4. `/portfolio-review`
5. `/product-health-review`
6. `/kill-or-scale-decision`
7. `/product-operating-model`

### P4 — качество и тесты

1. Создать тест-кейсы на каждый ключевой скилл.
2. Добавить golden examples: хороший/плохой вывод.
3. Проверять, что скилл задаёт вопросы при плохом input.
4. Проверять, что в доменных скиллах есть guardrails и decision rules.

---

## 13. 15 скиллов, которые надо усилить первыми

| Приоритет | Скилл | Что улучшить |
|---|---|---|
| 1 | `prd` | problem statement, assumptions, metrics tree, non-goals, risks |
| 2 | `ab-test-design` | OEC/guardrails/supporting, SRM, MDE, when not to A/B |
| 3 | `decision-doc` | Real Options, reversibility, decision log, revisit trigger |
| 4 | `discovery-sprint` | assumption mapping, evidence threshold, exit criteria |
| 5 | `marketplace-model` | local liquidity, leakage, take rate vs seller margin |
| 6 | `saas-metrics` | usage → retention bridge, activation, TTV, health score |
| 7 | `llm-product-design` | eval dataset, severity, cost per successful task, prompt injection |
| 8 | `ai-feature-spec` | model risk, HITL, offline/online eval, rollback |
| 9 | `growth-loop` | loop math, constraints, saturation, quality guardrails |
| 10 | `gtm-strategy` | ICP, wedge, channels, first 90 days, sales motion |
| 11 | `pricing-model` | WTP research, packaging, value metric, discount governance |
| 12 | `unit-economics` | contribution margin, sensitivity analysis, cohort economics |
| 13 | `govtech-metrics` | SLA breach, vulnerable users, assisted digital, rework |
| 14 | `ecosystem-design` | cross-service value, anti-cannibalization, ecosystem P&L |
| 15 | `roadmap` | strategic bets, capacity allocation, kill criteria |

---

## 14. Пример новой карточки скилла: `/d2c-subscription-model`

```yaml
---
name: d2c-subscription-model
description: >
  Спроектировать D2C-подписку для физического продукта: food box, beauty box,
  premium goods, фермерская корзина или регулярная доставка. Используй, когда
  нужно выбрать между интернет-магазином, маркетплейсом и собственной подпиской.
  На выходе: бизнес-модель, unit economics, retention loop, fulfillment risks,
  метрики подписки и go/no-go решение.
argument-hint: [описание продукта, аудитории, цены, частоты покупки и логистики]
allowed-tools: Read, Write
preset: d2c
lifecycle: strategy,growth,measure
business-model: d2c,subscription,ecommerce
domain: retail,food-d2c
stage: idea,mvp,pre-pmf,pmf
output-artifact: d2c-subscription-business-case
---
```

Выход:

```md
## D2C Subscription Model: [Название]

### 1. Контекст и проблема
### 2. Почему подписка, а не интернет-магазин/маркетплейс
### 3. Целевой сегмент и willingness to pay
### 4. Тарифы и частота доставки
### 5. Unit economics
### 6. Retention loop
### 7. Fulfillment and SLA
### 8. Supplier/partner economics
### 9. Growth loop
### 10. Risk heat map
### 11. Tenets
### 12. Decision: build / pilot / narrow / kill
```

---

## 15. Пример новой карточки скилла: `/business-case`

```yaml
---
name: business-case
description: >
  Подготовить CPO-grade бизнес-кейс для новой инициативы, продукта или бизнес-модели.
  Используй перед запросом инвестиций, запуском MVP, сменой модели монетизации или
  выходом в новый домен. На выходе: problem/background, alternatives, выбранная модель,
  BMC, unit economics, roadmap, risks, stakeholder communications и decision request.
argument-hint: [идея продукта или инициативы]
allowed-tools: Read, Write
preset: strategy
lifecycle: strategy,measure
business-model: any
domain: any
stage: idea,mvp,pre-pmf,scale
output-artifact: business-case
---
```

---

## 16. Итоговая целевая архитектура библиотеки

```text
PM SKILLS LIBRARY
│
├── Universal PM Core
│   ├── PRD / Stories / Roadmap / Decision / OKR
│   └── Communication / Launch / Stakeholders
│
├── Lifecycle Skills
│   ├── Discovery
│   ├── Strategy
│   ├── Definition
│   ├── Launch
│   ├── Growth
│   ├── Measure
│   └── Operations
│
├── Business Model Skills
│   ├── SaaS / Subscription
│   ├── Marketplace / Classifieds
│   ├── E-commerce / D2C
│   ├── Ads / Attention
│   ├── Platform / API
│   ├── Fintech / Lending
│   ├── Internal Product
│   └── AI / Data
│
├── Domain Skills
│   ├── Fintech
│   ├── Retail
│   ├── Telecom
│   ├── Media
│   ├── EdTech
│   ├── GovTech
│   ├── AdTech
│   ├── Logistics
│   └── Food D2C
│
├── CPO / Executive Layer
│   ├── Business Case
│   ├── Product Strategy
│   ├── Portfolio Review
│   ├── Investment Memo
│   ├── Product Health Review
│   └── Operating Model
│
└── Knowledge Base
    ├── Metrics Taxonomy
    ├── Skill Map
    ├── Domain Playbooks
    ├── Good/Bad Examples
    └── Test Cases
```

---

## 17. Финальный вывод

Текущая библиотека уже имеет сильный фундамент: 106 скиллов, широкое покрытие доменов, понятный русский язык, практичный формат и рабочий менеджер установки.

Но чтобы это стало не просто “много PM-промптов”, а сильным публичным продуктом, нужно сделать следующий скачок:

1. **От папок к таксономии.** Один скилл должен иметь lifecycle, business model, domain и stage.
2. **От описаний к decision tools.** Каждый скилл должен помогать принять решение, а не просто генерировать документ.
3. **От KPI-списков к метрика-системам.** Outcome, inputs, guardrails, diagnostics, instrumentation, decision rules.
4. **От PM-level к CPO-level.** Добавить business case, product strategy, portfolio review, investment memo, product health.
5. **От “универсального ответа” к stage-aware логике.** Idea, MVP, pre-PMF, PMF, scale требуют разных метрик и разных решений.
6. **От контента к продукту.** Нужны skill map, тест-кейсы, golden examples, валидация frontmatter, понятные presets и role combos.

Если сделать эти изменения, библиотека будет выглядеть не как набор скиллов для Claude Code, а как полноценная **PM/CPO operating system по продуктовым доменам, бизнес-моделям и метрикам**.


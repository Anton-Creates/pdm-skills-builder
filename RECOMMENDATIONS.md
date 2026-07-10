# PM Skills Library — Design Doc

> Документ для проектирования публичной библиотеки скиллов для продакт-менеджеров.
> Цель: создать открытый тулкит, который закрывает весь PM-цикл для разных контекстов и бизнес-моделей.
> За базу берём: https://github.com/Tony-Leoni/pdm-skills (20 universal skills + новые домены)

---

## Что уже есть в базовой библиотеке (не трогать)

**Discovery & Strategy:** `/product-teardown`, `/competitor-scan`, `/user-interview-prep`, `/feedback-analyzer`, `/market-sizing`, `/persona`

**Build & Ship:** `/prd`, `/user-stories`, `/technical-translator`, `/release-notes`, `/launch-checklist`, `/roadmap`

**Measure & Decide:** `/ab-test-design`, `/metrics-analyzer`, `/prioritize`, `/decision-doc`, `/okr-writer`

**Communicate:** `/stakeholder-update`, `/meeting-prep`, `/retro-facilitator`

**Вывод:** Core-цикл закрыт хорошо. Слепые пятна — специфика бизнес-моделей, AI/ML-продукты, финансовые инструменты, B2C-механики.

---

## Архитектура расширения

Библиотека делится на **слои**. Каждый PM берёт universal-скиллы + слои под свой контекст.

```
Universal (20 скиллов, уже есть)
    ↓
Business Model Layer (выбираешь свою модель)
    ↓
Domain Layer (выбираешь свою индустрию)
    ↓
Craft Layer (продвинутые техники для опытных PM)
```

---

## Business Model Layer — скиллы под бизнес-модель

### SaaS / B2B Software

| Скилл | Что делает |
|---|---|
| `/saas-metrics` | MRR, ARR, NRR, expansion revenue, logo churn vs. revenue churn. Диагностика по метрикам. |
| `/enterprise-discovery` | Enterprise-специфика discovery: multiple stakeholders, long sales cycle, procurement. Champion/Economic Buyer/Blocker. |
| `/pricing-model` | Pricing strategy: value-based vs. cost-plus vs. competitive. Packaging, tiers, willingness-to-pay research. |
| `/build-buy-partner` | Структурированное решение: строить / купить / интегрировать. TCO, time-to-market, strategic fit. |

### Marketplace / Two-sided

| Скилл | Что делает |
|---|---|
| `/marketplace-model` | Анализ двустороннего рынка: liquidity, supply/demand balance, take rate, chicken-and-egg проблема. |
| `/supply-quality` | Качество предложения на маркетплейсе: оценки, fraud, trust signals, seller onboarding. |
| `/matching-algorithm` | PM-взгляд на алгоритм матчинга: что оптимизируем, trade-offs качество vs. скорость, метрики. |

### C2C / Sharing Economy

| Скилл | Что делает |
|---|---|
| `/trust-safety` | Trust & Safety для C2C: верификация пользователей, dispute resolution, fraud patterns. |
| `/c2c-dynamics` | Специфика peer-to-peer: rating systems, network effects, liquidity в регионах. |

### Platform / API Economy

| Скилл | Что делает |
|---|---|
| `/platform-strategy` | Platform PM: API governance, developer experience, ecosystem incentives, partner onboarding. Adoption metrics. |
| `/api-product-spec` | API как продукт: use cases, SLA, pricing model, документация-минимум для adoption. |

### Consumer App / B2C

| Скилл | Что делает |
|---|---|
| `/funnel-analysis` | Drop-off диагностика по шагам воронки. Гипотезы причин. Top-3 эксперимента. |
| `/retention-model` | Cohort retention, churn drivers, resurrection opportunity, «плато» retention. |
| `/growth-loop` | Существующие петли роста (viral, content, PLG). K-factor. Узкие места. |
| `/notification-strategy` | Push/SMS/email стратегия: матрица событий-каналов, opt-out риски, A/B план. |
| `/onboarding-audit` | Карта активации, Aha moment, friction точки, benchmark против лучших. |
| `/monetization-audit` | Аудит текущей монетизации: что работает, что теряем, white space возможности. |

### Subscription / Media

| Скилл | Что делает |
|---|---|
| `/subscription-economics` | LTV модель для подписок: trial-to-paid, churn по когортам, ARPU expansion. Яндекс Плюс, СберПрайм, МТС Premium как примеры. |
| `/content-strategy` | PM-взгляд на контент: engagement metrics, content-product loops, curation vs. algo. Для стриминга (Kion, KION, ivi, Яндекс.Музыка). |
| `/superapp-strategy` | Экосистема / SuperApp: как объединить сервисы под одним брендом без cannibalization. Единый профиль, cross-product монетизация, token economy. Примеры: Яндекс, ВК, Тинькофф. |

### C2C Classifieds / Финансовые маркетплейсы

> ЦИАН, Авито, Авто.ру, Финуслуги (Мосбиржа), Банки.ру

| Скилл | Что делает |
|---|---|
| `/classifieds-model` | Бизнес-модель classifieds: freemium листинг, premium placement, lead generation. Ключевые метрики: listing quality score, reply rate, GMV. |
| `/finmarket-spec` | Финансовый маркетплейс (Финуслуги, Банки.ру): агрегация предложений, compliance с ЦБ, партнёрская монетизация, trust signals для пользователя. |
| `/real-estate-tech` | PropTech (ЦИАН, Домклик): специфика рынка недвижимости, верификация объектов, ипотечный путь пользователя, ценообразование листинга. |

### E-commerce / Retail

| Скилл | Что делает |
|---|---|
| `/checkout-audit` | Разбор воронки покупки: cart abandonment, payment friction, trust signals, checkout UX. |
| `/catalog-strategy` | Управление каталогом: taxonomy, search relevance, personalisation, long tail. |

---

## Domain Layer — скиллы под индустрию

### FinTech / Banking

| Скилл | Что делает |
|---|---|
| `/fintech-product-teardown` | Разбор финтех-продукта: регуляторные ограничения, монетизация, risk model, Open Banking. |
| `/unit-economics` | CAC/LTV/Payback для банковских продуктов. Break-even, sensitivity анализ. |
| `/compliance-checkpoint` | Compliance риски по чеклисту: 152-ФЗ, GDPR, ПОД/ФТ, ЦБ требования. |
| `/credit-product-spec` | Специфика кредитных продуктов: скоринг, одобрение, CLV кредитного клиента, NPL. |

### AI / ML Products

| Скилл | Что делает |
|---|---|
| `/ai-feature-spec` | PRD для AI-фич: ML-задача, evaluation framework, fallback logic, HITL сценарии, ML acceptance criteria. |
| `/data-product-spec` | Data products: lineage, quality SLA, governance, потребители, метрики качества. |
| `/llm-product-design` | LLM-специфика: prompt engineering для PM, RAG архитектура, latency/cost trade-offs, evaluation. |

### Enterprise / Gov / B2G

| Скилл | Что делает |
|---|---|
| `/rfp-response` | PM-участие в тендерах: анализ ТЗ, gap-анализ, win themes, compliance matrix. |
| `/enterprise-rollout` | Rollout в enterprise: phased deployment, change management, training plan, success metrics. |
| `/govtech-metrics` | Метрики GovTech-платформ (Госуслуги, Мос.ру): self-service rate (% обращений закрытых онлайн без визита в МФЦ), CES гражданина, time-to-completion услуги, конверсия офлайн → онлайн. Почему NPS здесь другой. |
| `/citizen-journey` | Путь гражданина через госпортал: информативность (найти услугу), доступность (WCAG, пожилые, мобильные), подача заявления, статус, итог. Ключевые точки отказа и friction. |
| `/public-service-design` | Проектирование государственной услуги как продукта: регуляторные ограничения, multi-channel (онлайн + МФЦ + звонок), SLA по ФЗ-210, accessibility как обязательное требование, не опция. |

### Hardware + Software / IoT

| Скилл | Что делает |
|---|---|
| `/hw-sw-roadmap` | Синхронизация hardware и software roadmap: HW constraints, firmware cycles, dependencies. |

### Marketplace / E-commerce (WB, Ozon, Яндекс Маркет)

| Скилл | Что делает |
|---|---|
| `/seller-journey` | Путь продавца на маркетплейсе: онбординг, активация, первая продажа, масштаб. Метрики: time-to-first-sale, GMV per seller. |
| `/marketplace-catalog` | Управление каталогом: таксономия категорий, SEO карточки, quality score, дедупликация, A+ контент. |
| `/search-ranking` | PM-взгляд на поиск: факторы ранжирования, relevance vs. monetization trade-off, cold start для новых карточек. |
| `/fulfillment-model` | Логистические модели (FBO/FBS/DBS): trade-offs скорости, стоимости, ответственности. Влияние на конверсию. |
| `/marketplace-fraud` | Fraud на маркетплейсе: накрутки отзывов, фейковые продавцы, возврат-мошенничество. Детекция и защита. |
| `/seller-economics` | Экономика продавца: комиссии, логистика, реклама, возвраты — когда продавец прибылен, когда нет. PM должен это знать. |

### Internal Products / HRtech / Корпоративные инструменты

| Скилл | Что делает |
|---|---|
| `/internal-product-discovery` | Discovery для внутреннего продукта: как работать с сотрудниками как с пользователями, forced adoption проблема, метрики adoption vs. satisfaction. |
| `/hrtech-spec` | Специфика HR-продуктов: онбординг сотрудников, performance review, L&D платформы. Compliance (трудовое право, PDPA). Аудитория — HR + сотрудник + менеджер. |
| `/admin-ux` | UX для внутренних инструментов: почему admin-интерфейсы всегда плохие и как это исправить. Принципы: задача первична, интерфейс — вторичен. |
| `/adoption-strategy` | Стратегия внедрения нового инструмента в компании: resistance management, champions, метрики adoption, rollout план. |
| `/intranet-product` | Корпоративный портал/интранет: архитектура информации, navigation, search, персонализация. Ключевая метрика — DAU/MAU сотрудников. |
| `/service-desk-metrics` | Метрики качества внутренней поддержки: CES (Employee Effort Score), Time-to-Resolution, First Contact Resolution, SLA выполнение. Как ускорить решение вопросов сотрудников и измерить результат. |
| `/internal-roi` | ROI внутреннего продукта: как посчитать экономию на ФОТ (автоматизация vs. найм), сравнение с внешними решениями (make vs. buy), TCO инструмента, обоснование для CIO/CFO. |

### SuperApp / Экосистема (Яндекс, ВК, МТС, Сбер)

| Скилл | Что делает |
|---|---|
| `/ecosystem-design` | Проектирование экосистемы: как сервисы усиливают друг друга, anti-cannibalization, bundle vs. unbundle, единый профиль пользователя. |
| `/mini-app-platform` | Платформа для мини-приложений (ВК, Яндекс): developer experience, permissions model, monetization для партнёров. |
| `/loyalty-program` | Программа лояльности / подписка (Плюс, СберПрайм): unit economics, redemption rate, коалиционные программы. |

### Retail tech / FMCG (X5, Магнит, Самокат)

| Скилл | Что делает |
|---|---|
| `/loyalty-crm` | CRM и программа лояльности в офлайн-ритейле: персонализация, триггерные коммуникации, uplift от промо. Метрики: участники, частота, чек. |
| `/dark-store-ops` | E-grocery / dark store: slot management, сборка заказа, SLA доставки, unit economics слота. |
| `/demand-forecasting-pm` | PM-взгляд на demand forecasting: какие данные нужны, как измерять качество прогноза, как фиче влиять на accuracy. |

### Telecom Products (МТС, Ростелеком, Билайн)

| Скилл | Что делает |
|---|---|
| `/vas-product` | Value-Added Services: разработка дополнительных услуг (контент, защита, роуминг), монетизация, opt-in/opt-out механики. |
| `/b2b-telecom` | B2B connectivity продукты: SLA, корпоративные тарифы, интеграция с BSS/OSS, account management продукта. |

### Media / Entertainment (Kion, ivi, Яндекс.Музыка)

| Скилл | Что делает |
|---|---|
| `/streaming-product` | Стриминговый сервис: content acquisition strategy, recommendation engine для PM, engagement vs. completion rate, windowing. |
| `/ugc-platform` | UGC платформа (ВКонтакте, TikTok-like): content moderation, creator monetization, virality mechanics, правовые риски. |

### Logistics tech (СДЭК, Яндекс.Доставка, Ozon Логистика)

| Скилл | Что делает |
|---|---|
| `/last-mile-product` | Last-mile delivery: pickup point network, route optimization для PM, SLA management, tracking UX. |
| `/returns-management` | Управление возвратами: reverse logistics, fraud в возвратах, UX процесса для покупателя, unit economics возврата. |

### EdTech (Яндекс Практикум, Skillbox, Geekbrains)

| Скилл | Что делает |
|---|---|
| `/learning-product` | Продукт обучения: learning path design, completion rate как главная метрика, engagement mechanics, cohort analysis по потокам. |
| `/b2b-edtech` | Корпоративное обучение: B2B2C модель, LMS интеграции, ROI для HR, compliance-обучение. |

### Ads tech / Performance платформы (Яндекс.Директ, ВК Реклама)

| Скилл | Что делает |
|---|---|
| `/ads-platform-pm` | PM рекламной платформы: аукционная механика, targeting продукты, measurement & attribution, privacy trade-offs. |
| `/dsp-ssp-spec` | DSP/SSP продукты: programmatic ecosystem, bid floor, fill rate, publisher vs. advertiser trade-offs. |

---

## Craft Layer — продвинутые техники

| Скилл | Что делает |
|---|---|
| `/north-star-metric` | Определение North Star: что измеряет ценность для пользователя, связь с revenue, input metrics. |
| `/hypothesis-tree` | Дерево гипотез: бизнес-цель → product bets → assumptions → эксперименты. Приоритизация гипотез. |
| `/jobs-to-be-done` | JTBD-интервью и анализ: functional/emotional/social jobs, switch interviews, job map. |
| `/customer-journey-map` | End-to-end карта пути: touchpoints, emotions, pain points, moments of truth. |
| `/discovery-sprint` | 2-недельный discovery sprint: план, артефакты, критерии выхода, решение о build/no-build. |
| `/pricing-experiment` | Ценовой эксперимент: дизайн теста, van Westendorp, Gabor-Granger, анализ результатов. |
| `/feature-flag-strategy` | Rollout стратегия через флаги: % rollout, targeting, kill switch, sunset plan. |
| `/competitive-moat` | Оценка защищённости продукта: switching costs, network effects, data moats, brand. |
| `/localization-strategy` | Выход в новый рынок: локализация vs. adaptation, regulatory gaps, GTM по рынку. |
| `/incident-pm-role` | Роль PM в инцидентах: коммуникации, приоритизация фиксов, postmortem, prevention backlog. |
| `/build-buy-partner` | Структурированное build/buy/partner решение: TCO, strategic fit, time-to-market. |

---

## Growth & Acquisition Layer — пересечение PM и маркетинга

> Эти скиллы закрывают зону ответственности PM за привлечение и рост. Не маркетинговые тактики, а продуктовые инструменты: как продукт участвует в собственном росте.

| Скилл | Что делает |
|---|---|
| `/gtm-strategy` | Go-to-Market: выбор целевого сегмента (ICP), канальный микс, мессаджинг под каждый канал, последовательность запуска, KPI первых 90 дней. |
| `/plg-design` | Product-Led Growth: дизайн free tier / trial, activation hooks, upgrade triggers, self-serve onboarding. Когда PLG работает, а когда нет. |
| `/positioning-statement` | Позиционирование: frame of reference (с кем конкурируем в голове у пользователя), Points of Difference, Reason to Believe. Структура — Geoffrey Moore. |
| `/channel-mix` | Приоритизация каналов привлечения: CAC по каналу, потенциал масштаба, time-to-ROI, saturation риски. Матрица: что запустить сейчас / потом / никогда. |
| `/icp-definition` | Ideal Customer Profile для B2B: firmographics, technographics, behavioral signals, negative ICP. Отличие от persona. |
| `/referral-mechanics` | Реферальная программа: структура инцентива (double-sided / one-sided), fraud prevention, attribution, метрики успеха. |
| `/cro-audit` | Conversion Rate Optimization: audit landing/signup/onboarding по фреймворку (clarity, relevance, friction, trust, urgency). Top-5 правок с потенциалом. |

---

## Улучшить в базовой библиотеке

| Скилл | Что добавить |
|---|---|
| `/prioritize` | Режим для разных фреймворков: RICE, ICE, WSJF, MoSCoW. Regulatory override. |
| `/ab-test-design` | ML-режим: offline evaluation, shadow testing, Champion/Challenger. |
| `/persona` | B2B-режим: buying committee, Economic Buyer / Champion / Blocker. |
| `/metrics-analyzer` | Банковский режим: сезонность, fraud spikes, когорты по дате выдачи. |
| `/prd` | AI-режим: автоматически добавляет блок ML requirements + evaluation criteria. |

---

## Итоговая карта библиотеки

```
UNIVERSAL (20)                    — базовый набор для любого PM
    ↓
BUSINESS MODEL (~30)              — под тип продукта
  SaaS · Marketplace · C2C · Platform · B2C
  Subscription / SuperApp · E-com · C2C Classifieds
    ↓
DOMAIN (~50)                      — под индустрию и вертикаль
  FinTech / Banking
  AI / ML Products
  Enterprise / Gov / B2G
  Hardware + Software / IoT
  Marketplace / E-commerce (WB, Ozon, ЯМ)
  Internal Products / HRtech
  SuperApp / Экосистема (Яндекс, ВК, Сбер)
  Retail tech / FMCG (X5, Магнит)
  Telecom (МТС, Ростелеком)
  Media / Entertainment (Kion, ivi)
  Logistics tech (СДЭК, Яндекс.Доставка)
  EdTech (Практикум, Skillbox)
  Ads tech / Performance (Яндекс.Директ, ВК)
  C2C Classifieds / PropTech (ЦИАН, Авито, Финуслуги)
    ↓
GROWTH & ACQUISITION (~7)         — PM × маркетинг
  GTM · PLG · Positioning · Channel Mix · ICP · Referral · CRO
    ↓
CRAFT (~11)                       — продвинутые техники
  North Star · JTBD · Discovery Sprint · Pricing · Moat · Localization
```

**Итого: ~120 скиллов** — комплексная библиотека для PM любого уровня, контекста и индустрии.

---

## Следующие шаги

- [ ] Выбрать приоритет первого релиза (какой слой выпускаем первым)
- [ ] Посмотреть формат SKILL.md в базовой библиотеке и договориться о шаблоне
- [ ] Определить название проекта и репозиторий
- [ ] Написать первые 3-5 скиллов под свою специализацию (FinTech + AI) — самое сильное с точки зрения личного бренда

---

*Контекст: публичная библиотека скиллов для Claude Code, расширение https://github.com/Tony-Leoni/pdm-skills*
*Создано: 2026-07-09*

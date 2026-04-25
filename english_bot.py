import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

TOKEN = os.environ.get("BOT_TOKEN", "ВАШ_ТОКЕН_ЗДЕСЬ")

# ──────────────────────────────────────────────
#  СЛОВАРЬ ПО ТЕМАМ (English → Russian)
# ──────────────────────────────────────────────
VOCAB = {
    "A": {
        "name": "🔍 Суть аудита и этика",
        "words": [
            {"en": "assurance engagement", "ru": "ассюранс-задание", "example": "An audit is an assurance engagement."},
            {"en": "reasonable assurance", "ru": "разумная уверенность", "example": "An audit provides reasonable assurance."},
            {"en": "true and fair view", "ru": "достоверное и справедливое представление", "example": "The statements give a true and fair view."},
            {"en": "practitioner", "ru": "практик / аудитор", "example": "The practitioner expresses a conclusion."},
            {"en": "responsible party", "ru": "ответственная сторона", "example": "Management is the responsible party."},
            {"en": "intended users", "ru": "предполагаемые пользователи", "example": "Shareholders are the intended users."},
            {"en": "professional scepticism", "ru": "профессиональный скептицизм", "example": "Auditors must maintain professional scepticism."},
            {"en": "independence of mind", "ru": "независимость в мышлении", "example": "Independence of mind means unbiased thinking."},
            {"en": "independence in appearance", "ru": "внешняя независимость", "example": "Independence in appearance builds public trust."},
            {"en": "objectivity", "ru": "объективность", "example": "Objectivity is a fundamental ethical principle."},
            {"en": "integrity", "ru": "честность / добросовестность", "example": "Integrity means being straightforward and honest."},
            {"en": "confidentiality", "ru": "конфиденциальность", "example": "Auditors must maintain confidentiality."},
            {"en": "professional behaviour", "ru": "профессиональное поведение", "example": "Professional behaviour avoids discrediting the profession."},
            {"en": "professional competence", "ru": "профессиональная компетентность", "example": "Due care requires professional competence."},
            {"en": "self-interest threat", "ru": "угроза личной заинтересованности", "example": "Owning client shares creates a self-interest threat."},
            {"en": "self-review threat", "ru": "угроза самопроверки", "example": "Preparing and auditing statements creates a self-review threat."},
            {"en": "advocacy threat", "ru": "угроза адвокации", "example": "Representing a client in court is an advocacy threat."},
            {"en": "familiarity threat", "ru": "угроза близости", "example": "A long relationship creates a familiarity threat."},
            {"en": "intimidation threat", "ru": "угроза запугивания", "example": "Threats of dismissal are an intimidation threat."},
            {"en": "safeguards", "ru": "защитные меры", "example": "Safeguards reduce threats to independence."},
            {"en": "audit committee", "ru": "комитет по аудиту", "example": "The audit committee oversees financial reporting."},
            {"en": "corporate governance", "ru": "корпоративное управление", "example": "Corporate governance directs and controls companies."},
            {"en": "internal audit", "ru": "внутренний аудит", "example": "Internal audit evaluates risk management."},
            {"en": "external audit", "ru": "внешний аудит", "example": "External audit provides an opinion on financial statements."},
            {"en": "non-executive director", "ru": "неисполнительный директор", "example": "The audit committee consists of non-executive directors."},
            {"en": "tone at the top", "ru": "тон сверху", "example": "Tone at the top sets the ethical culture."},
            {"en": "engagement letter", "ru": "письмо об условиях задания", "example": "The engagement letter is signed before audit work begins."},
            {"en": "positive assurance", "ru": "положительный ассюранс", "example": "An audit provides positive assurance."},
            {"en": "limited assurance", "ru": "ограниченный ассюранс", "example": "A review provides limited assurance."},
            {"en": "negative assurance", "ru": "отрицательный ассюранс", "example": "Nothing came to our attention — this is negative assurance."},
        ]
    },
    "B": {
        "name": "⚠️ Риски и планирование",
        "words": [
            {"en": "audit risk", "ru": "аудиторский риск", "example": "Audit risk = IR × CR × DR."},
            {"en": "inherent risk", "ru": "неотъемлемый риск", "example": "Complex transactions increase inherent risk."},
            {"en": "control risk", "ru": "риск контроля", "example": "Weak controls increase control risk."},
            {"en": "detection risk", "ru": "риск необнаружения", "example": "The auditor manages detection risk."},
            {"en": "materiality", "ru": "существенность", "example": "Materiality is set at planning stage."},
            {"en": "performance materiality", "ru": "существенность исполнения", "example": "Performance materiality is below overall materiality."},
            {"en": "overall materiality", "ru": "общая существенность", "example": "Overall materiality is based on revenue or profit."},
            {"en": "significant risk", "ru": "существенный риск", "example": "Revenue recognition is often a significant risk."},
            {"en": "going concern", "ru": "непрерывность деятельности", "example": "The going concern assumption must be assessed."},
            {"en": "fraud triangle", "ru": "треугольник мошенничества", "example": "The fraud triangle includes pressure, opportunity, rationalisation."},
            {"en": "fraudulent financial reporting", "ru": "мошеннические финансовые отчёты", "example": "Management manipulates results — fraudulent financial reporting."},
            {"en": "misappropriation of assets", "ru": "присвоение активов", "example": "Theft of cash is misappropriation of assets."},
            {"en": "risk assessment procedures", "ru": "процедуры оценки риска", "example": "Risk assessment procedures include inquiries and analytics."},
            {"en": "analytical procedures", "ru": "аналитические процедуры", "example": "Analytical procedures compare financial data."},
            {"en": "red flags", "ru": "красные флаги / тревожные признаки", "example": "Unusual revenue growth is a red flag."},
            {"en": "pressure", "ru": "давление / мотив", "example": "Financial pressure is one side of the fraud triangle."},
            {"en": "opportunity", "ru": "возможность", "example": "Weak controls create opportunity for fraud."},
            {"en": "rationalisation", "ru": "оправдание / рационализация", "example": "Rationalisation allows a person to justify fraud."},
            {"en": "covenant", "ru": "ковенант / условие кредитного договора", "example": "Breaching a loan covenant is a going concern indicator."},
            {"en": "benchmark", "ru": "ориентир / база для расчёта", "example": "Revenue is a common materiality benchmark."},
            {"en": "trivial threshold", "ru": "порог тривиальности", "example": "Misstatements below the trivial threshold are not accumulated."},
            {"en": "knowledge of business", "ru": "знание бизнеса клиента", "example": "Knowledge of business helps identify risks."},
            {"en": "audit strategy", "ru": "стратегия аудита", "example": "The audit strategy sets the overall approach."},
            {"en": "audit plan", "ru": "план аудита", "example": "The audit plan details procedures to be performed."},
            {"en": "controls-based approach", "ru": "подход на основе контролей", "example": "A controls-based approach reduces substantive testing."},
            {"en": "substantive approach", "ru": "субстантивный подход", "example": "A substantive approach relies on tests of detail."},
            {"en": "cash flow", "ru": "денежный поток", "example": "Negative cash flow is a going concern indicator."},
            {"en": "overstatement", "ru": "завышение", "example": "Revenue overstatement is a common fraud risk."},
            {"en": "understatement", "ru": "занижение", "example": "Liability understatement is a completeness risk."},
        ]
    },
    "C": {
        "name": "🛡️ Внутренний контроль",
        "words": [
            {"en": "internal control", "ru": "внутренний контроль", "example": "Internal control provides reasonable assurance."},
            {"en": "control environment", "ru": "среда контроля", "example": "The control environment is the foundation of control."},
            {"en": "segregation of duties", "ru": "разделение обязанностей", "example": "Segregation of duties prevents fraud."},
            {"en": "authorisation", "ru": "авторизация / утверждение", "example": "All payments require authorisation."},
            {"en": "reconciliation", "ru": "сверка", "example": "Bank reconciliation is a detective control."},
            {"en": "preventive control", "ru": "превентивный контроль", "example": "Password controls are preventive controls."},
            {"en": "detective control", "ru": "детективный контроль", "example": "Reconciliations are detective controls."},
            {"en": "physical control", "ru": "физический контроль", "example": "Safes and locks are physical controls."},
            {"en": "management override", "ru": "обход контролей руководством", "example": "Management override is the primary fraud risk."},
            {"en": "collusion", "ru": "сговор", "example": "Collusion limits the effectiveness of controls."},
            {"en": "tests of controls", "ru": "тесты контроля", "example": "Tests of controls assess operating effectiveness."},
            {"en": "general IT controls", "ru": "общие IT-контроли", "example": "Access controls are general IT controls."},
            {"en": "application controls", "ru": "контроли приложений", "example": "Input validation is an application control."},
            {"en": "access controls", "ru": "контроль доступа", "example": "Passwords are access controls."},
            {"en": "change management", "ru": "управление изменениями программ", "example": "Change management prevents unauthorised program changes."},
            {"en": "three-way match", "ru": "трёхстороннее сопоставление", "example": "Three-way match: PO, GRN and invoice must agree."},
            {"en": "purchase order", "ru": "заказ на покупку", "example": "Purchase orders must be authorised before placement."},
            {"en": "goods received note", "ru": "накладная о получении товара", "example": "A GRN confirms goods were received."},
            {"en": "credit limit", "ru": "кредитный лимит", "example": "Credit limits are authorised by the credit controller."},
            {"en": "ghost employee", "ru": "подставной сотрудник", "example": "Ghost employees are a payroll fraud risk."},
            {"en": "sequential numbering", "ru": "порядковая нумерация", "example": "Sequential numbering detects missing transactions."},
            {"en": "exception report", "ru": "отчёт об исключениях", "example": "Exception reports flag unusual transactions."},
            {"en": "compensating control", "ru": "компенсирующий контроль", "example": "Owner oversight is a compensating control in small businesses."},
            {"en": "payroll", "ru": "расчёт заработной платы", "example": "Payroll must be reconciled to HR records."},
            {"en": "human resources register", "ru": "кадровый реестр", "example": "Payroll must be agreed to the HR register."},
        ]
    },
    "D": {
        "name": "📄 Доказательства",
        "words": [
            {"en": "audit evidence", "ru": "аудиторские доказательства", "example": "Audit evidence must be sufficient and appropriate."},
            {"en": "sufficient evidence", "ru": "достаточные доказательства", "example": "Sufficient evidence relates to quantity."},
            {"en": "appropriate evidence", "ru": "надлежащие доказательства", "example": "Appropriate evidence relates to quality."},
            {"en": "assertions", "ru": "утверждения", "example": "Auditors test management assertions."},
            {"en": "existence", "ru": "существование", "example": "Existence tests whether assets are real."},
            {"en": "completeness", "ru": "полнота", "example": "Completeness tests whether all items are recorded."},
            {"en": "valuation", "ru": "оценка", "example": "Valuation tests whether amounts are correct."},
            {"en": "rights and obligations", "ru": "права и обязанности", "example": "Rights confirm the entity owns the asset."},
            {"en": "occurrence", "ru": "реальность операций", "example": "Occurrence tests whether transactions happened."},
            {"en": "accuracy", "ru": "точность", "example": "Accuracy tests whether amounts are correctly recorded."},
            {"en": "cut-off", "ru": "срез / правильность периода", "example": "Cut-off tests whether items are in the correct period."},
            {"en": "classification", "ru": "классификация", "example": "Classification tests correct presentation."},
            {"en": "external confirmation", "ru": "внешнее подтверждение", "example": "Bank confirmation is external confirmation."},
            {"en": "circularisation", "ru": "подтверждение дебиторской задолженности", "example": "Debtor circularisation confirms balances."},
            {"en": "inspection", "ru": "инспекция", "example": "Inspection involves examining documents or assets."},
            {"en": "observation", "ru": "наблюдение", "example": "Observation of the inventory count provides evidence."},
            {"en": "inquiry", "ru": "запрос", "example": "Inquiry alone is insufficient evidence."},
            {"en": "recalculation", "ru": "пересчёт", "example": "Recalculation checks arithmetic accuracy."},
            {"en": "reperformance", "ru": "повторное выполнение", "example": "Reperformance independently executes a control."},
            {"en": "substantive procedures", "ru": "процедуры по существу", "example": "Substantive procedures detect material misstatements."},
            {"en": "tests of detail", "ru": "детальные тесты", "example": "Tests of detail examine specific transactions."},
            {"en": "audit sampling", "ru": "аудиторская выборка", "example": "Audit sampling applies procedures to less than 100%."},
            {"en": "monetary unit sampling", "ru": "денежная выборка единиц", "example": "MUS gives higher items a greater chance of selection."},
            {"en": "sampling risk", "ru": "риск выборки", "example": "Sampling risk is the risk of wrong conclusions from a sample."},
            {"en": "directional testing", "ru": "направленное тестирование", "example": "Test assets top-down to detect overstatement."},
            {"en": "subsequent events", "ru": "последующие события", "example": "Subsequent events occur after the reporting date."},
            {"en": "adjusting event", "ru": "корректирующее событие", "example": "An adjusting event confirms year-end conditions."},
            {"en": "non-adjusting event", "ru": "некорректирующее событие", "example": "A non-adjusting event arises after the reporting date."},
            {"en": "management representations", "ru": "письма-представления менеджмента", "example": "Written representations are not sufficient evidence alone."},
            {"en": "net realisable value", "ru": "чистая стоимость реализации", "example": "Inventory is valued at cost or NRV, whichever is lower."},
            {"en": "aged receivables", "ru": "анализ возраста дебиторской задолженности", "example": "Aged receivables help assess the bad debt provision."},
            {"en": "subsequent receipts", "ru": "последующие поступления", "example": "Subsequent receipts confirm receivable balances."},
            {"en": "unrecorded liabilities", "ru": "незарегистрированные обязательства", "example": "Search for unrecorded liabilities tests completeness of payables."},
            {"en": "specialist", "ru": "эксперт / специалист", "example": "The auditor may use a specialist for property valuation."},
            {"en": "physical inventory count", "ru": "физическая инвентаризация", "example": "The auditor observes the physical inventory count."},
        ]
    },
    "E": {
        "name": "📋 Заключение аудитора",
        "words": [
            {"en": "audit report", "ru": "аудиторское заключение", "example": "The audit report contains the auditor's opinion."},
            {"en": "unmodified opinion", "ru": "немодифицированное заключение", "example": "An unmodified opinion means the statements are true and fair."},
            {"en": "modified opinion", "ru": "модифицированное заключение", "example": "A modified opinion is issued when there are issues."},
            {"en": "qualified opinion", "ru": "заключение с оговоркой", "example": "A qualified opinion is issued for material but not pervasive issues."},
            {"en": "adverse opinion", "ru": "отрицательное мнение", "example": "An adverse opinion means statements are materially misstated."},
            {"en": "disclaimer of opinion", "ru": "отказ от выражения мнения", "example": "A disclaimer is issued when scope limitation is pervasive."},
            {"en": "pervasive", "ru": "повсеместный / пронизывающий", "example": "Pervasive misstatements affect the whole financial statements."},
            {"en": "material misstatement", "ru": "существенное искажение", "example": "Material misstatements affect users' decisions."},
            {"en": "scope limitation", "ru": "ограничение объёма аудита", "example": "Inability to attend inventory count is a scope limitation."},
            {"en": "Emphasis of Matter", "ru": "акцент на важных вопросах", "example": "Emphasis of Matter draws attention to a disclosed matter."},
            {"en": "Other Matter", "ru": "прочие вопросы", "example": "Other Matter refers to matters not in the financial statements."},
            {"en": "Key Audit Matters", "ru": "ключевые вопросы аудита", "example": "KAM are required for listed entities."},
            {"en": "listed entity", "ru": "листинговая компания", "example": "KAM are mandatory for listed entities."},
            {"en": "going concern uncertainty", "ru": "неопределённость по непрерывности деятельности", "example": "Material going concern uncertainty requires disclosure."},
            {"en": "management responsibility", "ru": "ответственность менеджмента", "example": "Management is responsible for preparing financial statements."},
            {"en": "auditor responsibility", "ru": "ответственность аудитора", "example": "The auditor is responsible for the audit opinion."},
            {"en": "misstatement", "ru": "искажение", "example": "A misstatement is a difference from the correct amount."},
            {"en": "related party", "ru": "связанная сторона", "example": "Related party transactions must be disclosed."},
            {"en": "representation letter", "ru": "письмо-представление", "example": "The representation letter is signed by management."},
            {"en": "restatement", "ru": "переиздание / пересмотр отчётности", "example": "A restatement corrects prior year financial statements."},
            {"en": "comparative figures", "ru": "сравнительные показатели", "example": "Prior year figures are presented as comparative figures."},
            {"en": "date of audit report", "ru": "дата аудиторского заключения", "example": "The report date cannot precede management approval."},
            {"en": "approval of financial statements", "ru": "одобрение финансовой отчётности", "example": "Management approves the statements before the report is signed."},
        ]
    },
    "F": {
        "name": "📊 МСФО / IFRS термины",
        "words": [
            {"en": "financial statements", "ru": "финансовая отчётность", "example": "Financial statements must give a true and fair view."},
            {"en": "statement of financial position", "ru": "отчёт о финансовом положении (баланс)", "example": "Assets are listed in the statement of financial position."},
            {"en": "statement of profit or loss", "ru": "отчёт о прибылях и убытках", "example": "Revenue appears in the statement of profit or loss."},
            {"en": "statement of cash flows", "ru": "отчёт о движении денежных средств", "example": "The statement of cash flows shows operating activities."},
            {"en": "revenue", "ru": "выручка / доход", "example": "Revenue is recognised when performance obligations are met."},
            {"en": "cost of sales", "ru": "себестоимость продаж", "example": "Gross profit equals revenue minus cost of sales."},
            {"en": "gross profit", "ru": "валовая прибыль", "example": "Gross profit margin is gross profit divided by revenue."},
            {"en": "profit before tax", "ru": "прибыль до налогообложения", "example": "Materiality is often based on profit before tax."},
            {"en": "non-current assets", "ru": "внеоборотные активы", "example": "Property and equipment are non-current assets."},
            {"en": "current assets", "ru": "оборотные активы", "example": "Inventory and receivables are current assets."},
            {"en": "current liabilities", "ru": "краткосрочные обязательства", "example": "Trade payables are current liabilities."},
            {"en": "non-current liabilities", "ru": "долгосрочные обязательства", "example": "Long-term loans are non-current liabilities."},
            {"en": "equity", "ru": "капитал", "example": "Equity equals assets minus liabilities."},
            {"en": "retained earnings", "ru": "нераспределённая прибыль", "example": "Retained earnings accumulate over time."},
            {"en": "property, plant and equipment", "ru": "основные средства", "example": "PP&E is depreciated over its useful life."},
            {"en": "depreciation", "ru": "амортизация (основных средств)", "example": "Depreciation allocates cost over the useful life."},
            {"en": "amortisation", "ru": "амортизация (нематериальных активов)", "example": "Intangible assets with finite lives are amortised."},
            {"en": "impairment", "ru": "обесценение", "example": "An impairment loss reduces the carrying amount."},
            {"en": "carrying amount", "ru": "балансовая стоимость", "example": "Carrying amount equals cost minus accumulated depreciation."},
            {"en": "fair value", "ru": "справедливая стоимость", "example": "Fair value is the price in an arm's length transaction."},
            {"en": "recoverable amount", "ru": "возмещаемая стоимость", "example": "Recoverable amount is the higher of VIU and FVLCD."},
            {"en": "value in use", "ru": "ценность использования", "example": "Value in use is the present value of future cash flows."},
            {"en": "inventories", "ru": "запасы", "example": "Inventories are measured at cost or NRV, whichever is lower."},
            {"en": "trade receivables", "ru": "дебиторская задолженность покупателей", "example": "Trade receivables are shown net of bad debt provision."},
            {"en": "trade payables", "ru": "кредиторская задолженность поставщикам", "example": "Trade payables represent amounts owed to suppliers."},
            {"en": "provisions", "ru": "оценочные обязательства", "example": "A provision is recognised when a present obligation exists."},
            {"en": "contingent liability", "ru": "условное обязательство", "example": "A contingent liability is disclosed but not recognised."},
            {"en": "intangible assets", "ru": "нематериальные активы", "example": "Goodwill is an intangible asset not amortised under IFRS."},
            {"en": "goodwill", "ru": "гудвил", "example": "Goodwill arises on business combinations."},
            {"en": "business combination", "ru": "объединение бизнесов", "example": "IFRS 3 applies to business combinations."},
            {"en": "subsidiary", "ru": "дочерняя компания", "example": "A subsidiary is controlled by the parent."},
            {"en": "associate", "ru": "ассоциированная компания", "example": "An associate is accounted for using the equity method."},
            {"en": "consolidated financial statements", "ru": "консолидированная финансовая отчётность", "example": "The parent prepares consolidated financial statements."},
            {"en": "lease", "ru": "аренда", "example": "IFRS 16 requires lessees to recognise right-of-use assets."},
            {"en": "right-of-use asset", "ru": "актив в форме права пользования", "example": "A right-of-use asset is recognised at commencement date."},
            {"en": "deferred tax", "ru": "отложенный налог", "example": "Deferred tax arises from temporary differences."},
            {"en": "borrowing costs", "ru": "затраты по заимствованиям", "example": "Borrowing costs on qualifying assets are capitalised."},
            {"en": "impairment test", "ru": "тест на обесценение", "example": "Goodwill must be tested for impairment annually."},
            {"en": "cash-generating unit", "ru": "единица генерирующая денежные потоки", "example": "Impairment is tested at the cash-generating unit level."},
            {"en": "performance obligation", "ru": "обязательство к исполнению", "example": "Revenue is recognised when a performance obligation is satisfied."},
            {"en": "accounting policy", "ru": "учётная политика", "example": "Accounting policies must be applied consistently."},
            {"en": "prior period error", "ru": "ошибка предшествующего периода", "example": "Prior period errors are corrected retrospectively."},
            {"en": "accrual basis", "ru": "метод начисления", "example": "IFRS requires the accrual basis of accounting."},
            {"en": "earnings per share", "ru": "прибыль на акцию", "example": "EPS is profit divided by weighted average shares."},
            {"en": "revaluation", "ru": "переоценка", "example": "Property may be carried under the revaluation model."},
            {"en": "useful life", "ru": "срок полезного использования", "example": "Depreciation is based on the asset's useful life."},
            {"en": "residual value", "ru": "ликвидационная стоимость", "example": "Residual value is deducted before calculating depreciation."},
            {"en": "investment property", "ru": "инвестиционная недвижимость", "example": "Investment property is held to earn rentals or for capital appreciation."},
            {"en": "government grant", "ru": "государственная субсидия", "example": "Government grants are recognised in profit or loss."},
            {"en": "related party transaction", "ru": "операция со связанной стороной", "example": "Related party transactions must be disclosed under IAS 24."},
        ]
    }
}

# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Все темы перемешать", callback_data="topic_ALL")],
        [InlineKeyboardButton("🔍 A · Суть аудита", callback_data="topic_A"),
         InlineKeyboardButton("⚠️ B · Риски", callback_data="topic_B")],
        [InlineKeyboardButton("🛡️ C · Контроль", callback_data="topic_C"),
         InlineKeyboardButton("📄 D · Доказательства", callback_data="topic_D")],
        [InlineKeyboardButton("📋 E · Заключение", callback_data="topic_E"),
         InlineKeyboardButton("📊 F · МСФО/IFRS", callback_data="topic_F")],
        [InlineKeyboardButton("🃏 Режим: EN→RU", callback_data="mode_en"),
         InlineKeyboardButton("🔤 Режим: RU→EN", callback_data="mode_ru")],
        [InlineKeyboardButton("📊 Прогресс", callback_data="stats"),
         InlineKeyboardButton("🔁 Сложные слова", callback_data="hard_words")],
    ])

def build_quiz_keyboard(correct_ru, all_words, qidx):
    options = [correct_ru]
    pool = [w["ru"] for w in all_words if w["ru"] != correct_ru]
    options += random.sample(pool, min(3, len(pool)))
    random.shuffle(options)
    rows = []
    for i, opt in enumerate(options):
        rows.append([InlineKeyboardButton(opt, callback_data=f"ans_{qidx}_{i}_{opt == correct_ru}")])
    return InlineKeyboardMarkup(rows), options

def build_quiz_keyboard_en(correct_en, all_words, qidx):
    options = [correct_en]
    pool = [w["en"] for w in all_words if w["en"] != correct_en]
    options += random.sample(pool, min(3, len(pool)))
    random.shuffle(options)
    rows = []
    for i, opt in enumerate(options):
        rows.append([InlineKeyboardButton(opt, callback_data=f"ans_{qidx}_{i}_{opt == correct_en}")])
    return InlineKeyboardMarkup(rows), options

def init_session(context, topic, mode):
    if topic == "ALL":
        pool = []
        for t in VOCAB.values():
            pool.extend(t["words"])
    else:
        pool = list(VOCAB[topic]["words"])
    random.shuffle(pool)
    context.user_data["session"] = {
        "topic": topic,
        "mode": mode,
        "pool": pool,
        "idx": 0,
        "correct": 0,
        "wrong": 0,
        "total": len(pool),
        "hard": [],
    }

def get_all_words():
    pool = []
    for t in VOCAB.values():
        pool.extend(t["words"])
    return pool

# ──────────────────────────────────────────────
#  HANDLERS
# ──────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "Привет"
    # Default mode
    context.user_data.setdefault("mode", "en")
    total = sum(len(t["words"]) for t in VOCAB.values())
    await update.message.reply_text(
        f"👋 {name}!\n\n"
        f"*ACCA AA — Бизнес-английский тренажёр*\n\n"
        f"📖 В базе: *{total} терминов* по 5 темам\n\n"
        f"*Режимы:*\n"
        f"🃏 EN→RU — вижу английский термин, выбираю перевод\n"
        f"🔤 RU→EN — вижу русский перевод, выбираю термин\n\n"
        f"Выбери тему и режим:",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── MODE SELECTION ──
    if data.startswith("mode_"):
        mode = data.split("_")[1]
        context.user_data["mode"] = mode
        mode_text = "EN→RU (вижу английский — пишу русский)" if mode == "en" else "RU→EN (вижу русский — пишу английский)"
        await query.edit_message_text(
            f"✅ Режим изменён: *{mode_text}*\n\nТеперь выбери тему:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        return

    # ── TOPIC SELECTION ──
    if data.startswith("topic_"):
        topic = data.split("_")[1]
        mode = context.user_data.get("mode", "en")
        init_session(context, topic, mode)
        s = context.user_data["session"]
        topic_name = "Все темы" if topic == "ALL" else VOCAB[topic]["name"]
        mode_text = "EN → выбираешь RU" if mode == "en" else "RU → выбираешь EN"
        await query.edit_message_text(
            f"✅ Тема: *{topic_name}*\n"
            f"📝 Слов: *{s['total']}*\n"
            f"🎯 Режим: *{mode_text}*\n\n"
            f"Поехали! 🚀",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("▶️ Начать", callback_data="next")
            ]])
        )
        return

    # ── NEXT WORD ──
    if data == "next":
        s = context.user_data.get("session")
        if not s or s["idx"] >= s["total"]:
            await query.edit_message_text(
                "Сессия завершена! /start",
                reply_markup=get_main_keyboard()
            )
            return
        word = s["pool"][s["idx"]]
        mode = s["mode"]
        all_words = get_all_words()

        if mode == "en":
            kb, options = build_quiz_keyboard(word["ru"], all_words, s["idx"])
            text = (
                f"🃏 *Вопрос {s['idx']+1}/{s['total']}*\n\n"
                f"*{word['en']}*\n\n"
                f"💬 _{word['example']}_\n\n"
                f"Выбери перевод:"
            )
        else:
            kb, options = build_quiz_keyboard_en(word["en"], all_words, s["idx"])
            text = (
                f"🔤 *Вопрос {s['idx']+1}/{s['total']}*\n\n"
                f"*{word['ru']}*\n\n"
                f"Выбери термин на английском:"
            )

        s["current_word"] = word
        s["current_options"] = options
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        return

    # ── ANSWER ──
    if data.startswith("ans_"):
        parts = data.split("_")
        q_idx = int(parts[1])
        is_correct = parts[3] == "True"
        s = context.user_data.get("session")
        if not s or s["idx"] != q_idx:
            return

        word = s["pool"][q_idx]
        mode = s["mode"]
        s["idx"] += 1

        if is_correct:
            s["correct"] += 1
            result = "✅ *Верно!*"
        else:
            s["wrong"] += 1
            s["hard"].append(word)
            if mode == "en":
                result = f"❌ *Неверно.*\nПравильно: *{word['ru']}*"
            else:
                result = f"❌ *Неверно.*\nПравильно: *{word['en']}*"

        # Update global stats
        stats = context.user_data.setdefault("stats", {"correct": 0, "wrong": 0})
        if is_correct:
            stats["correct"] += 1
        else:
            stats["wrong"] += 1

        pct = round((s["correct"] / s["idx"]) * 100)
        text = (
            f"{result}\n\n"
            f"🇬🇧 *{word['en']}*\n"
            f"🇷🇺 {word['ru']}\n"
            f"💬 _{word['example']}_\n\n"
            f"─────\n"
            f"Прогресс: {s['correct']}/{s['idx']} ({pct}%)"
        )

        if s["idx"] >= s["total"]:
            pct_f = round((s["correct"] / s["total"]) * 100)
            emoji = "🏆" if pct_f >= 80 else "📚" if pct_f >= 50 else "💪"
            hard_count = len(s.get("hard", []))
            text += (
                f"\n\n{emoji} *Раунд завершён!*\n"
                f"Результат: *{s['correct']}/{s['total']} ({pct_f}%)*"
            )
            if hard_count > 0:
                text += f"\n🔁 Сложных слов: {hard_count} — повтори их!"
            # Save hard words
            context.user_data["hard_words"] = s.get("hard", [])
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=get_main_keyboard())
        else:
            await query.edit_message_text(
                text, parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("➡️ Следующее слово", callback_data="next"),
                    InlineKeyboardButton("🏠 Меню", callback_data="menu")
                ]])
            )
        return

    # ── STATS ──
    if data == "stats":
        stats = context.user_data.get("stats", {"correct": 0, "wrong": 0})
        total_ans = stats["correct"] + stats["wrong"]
        pct = round(stats["correct"] / total_ans * 100) if total_ans else 0
        total_words = sum(len(t["words"]) for t in VOCAB.values())
        await query.edit_message_text(
            f"📊 *Твой прогресс*\n\n"
            f"✅ Верно: {stats['correct']}\n"
            f"❌ Неверно: {stats['wrong']}\n"
            f"🎯 Точность: {pct}%\n\n"
            f"📖 Всего терминов в базе: {total_words}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Назад", callback_data="menu")
            ]])
        )
        return

    # ── HARD WORDS ──
    if data == "hard_words":
        hard = context.user_data.get("hard_words", [])
        if not hard:
            await query.edit_message_text(
                "🔁 Сложных слов пока нет — сначала пройди тест!",
                reply_markup=get_main_keyboard()
            )
            return
        mode = context.user_data.get("mode", "en")
        random.shuffle(hard)
        context.user_data["session"] = {
            "topic": "HARD",
            "mode": mode,
            "pool": hard,
            "idx": 0,
            "correct": 0,
            "wrong": 0,
            "total": len(hard),
            "hard": [],
        }
        await query.edit_message_text(
            f"🔁 *Повтор сложных слов*\n"
            f"Слов: *{len(hard)}*\n\nПоехали!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("▶️ Начать", callback_data="next")
            ]])
        )
        return

    # ── MENU ──
    if data == "menu":
        await query.edit_message_text("Выбери тему:", reply_markup=get_main_keyboard())
        return

# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("English бот запущен ✅")
    app.run_polling()

if __name__ == "__main__":
    main()

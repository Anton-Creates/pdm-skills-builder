#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import json
import re
from pathlib import Path

# Force UTF-8 encoding for stdout on Windows to prevent encoding errors
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Paths - Dynamic resolution to support running from root or from subdirectory
CURRENT_FILE_DIR = Path(__file__).resolve().parent
if (CURRENT_FILE_DIR / "20 Проекты/skills/PdM skills").exists():
    BASE_DIR = CURRENT_FILE_DIR / "20 Проекты/skills/PdM skills"
    PROJECT_ROOT = CURRENT_FILE_DIR
else:
    BASE_DIR = CURRENT_FILE_DIR
    PROJECT_ROOT = CURRENT_FILE_DIR.parent.parent.parent

CLAUDE_SKILLS_DIR = Path(os.path.expanduser("~/.claude/skills"))
CONFIG_FILE = PROJECT_ROOT / ".skills_config.json"

# Load / Save Config for multi-tool targeting
def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"target_env": "claude"}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except:
        pass

config = load_config()
TARGET_ENV = config.get("target_env", "claude")

# Categories mapping based on RECOMMENDATIONS.md and FINAL_SKILLS_RECOMMENDATIONS.md
SKILLS_BY_PRESET = {
    "core": [
        "prd", "user-stories", "roadmap", "prioritize", "okr-writer", 
        "decision-doc", "release-notes", "technical-translator",
        "launch-checklist", "meeting-prep", "metrics-analyzer",
        "retro-facilitator", "stakeholder-update", "product-teardown",
        "ab-test-design"
    ],
    "strategy": [
        "product-strategy", "business-case", "market-sizing", "competitor-scan",
        "competitive-moat", "positioning-statement", "icp-definition",
        "hypothesis-tree", "risk-heatmap", "tenets-writer", "build-buy-partner",
        "localization-strategy"
    ],
    "discovery": [
        "user-interview-prep", "customer-journey-map", "discovery-sprint", 
        "persona", "feedback-analyzer", "competitor-scan", "icp-definition",
        "market-sizing", "positioning-statement", "funnel-analysis",
        "onboarding-audit"
    ],
    "growth": [
        "growth-loop", "gtm-strategy", "channel-mix", "plg-design",
        "referral-mechanics", "cro-audit", "onboarding-audit", "retention-model",
        "notification-strategy", "monetization-audit", "positioning-statement",
        "icp-definition", "pricing-experiment", "promo-engine"
    ],
    "measure": [
        "metrics-analyzer", "ab-test-design", "okr-writer", "prioritize",
        "decision-doc", "north-star-metric", "unit-economics", "saas-metrics",
        "subscription-economics", "seller-economics", "govtech-metrics",
        "product-health-review", "kill-or-scale-decision"
    ],
    "saas": [
        "saas-metrics", "pricing-model", "build-buy-partner", 
        "retention-model", "pricing-experiment", "monetization-audit",
        "growth-loop", "plg-design", "referral-mechanics", "subscription-economics",
        "notification-strategy"
    ],
    "subscription": [
        "subscription-economics", "d2c-subscription-model", "retention-model",
        "pricing-model", "pricing-experiment", "notification-strategy",
        "growth-loop", "referral-mechanics", "monetization-audit"
    ],
    "d2c": [
        "d2c-subscription-model", "business-case", "growth-loop", "channel-mix",
        "retention-model", "referral-mechanics", "notification-strategy",
        "unit-economics", "risk-heatmap", "tenets-writer", "loyalty-crm",
        "last-mile-product"
    ],
    "marketplace": [
        "marketplace-model", "supply-quality", "matching-algorithm", 
        "trust-safety", "c2c-dynamics", "marketplace-catalog", 
        "fulfillment-model", "marketplace-fraud", "seller-economics",
        "seller-journey", "search-ranking", "classifieds-model"
    ],
    "classifieds": [
        "classifieds-model", "c2c-dynamics", "seller-journey", "search-ranking",
        "trust-safety", "marketplace-fraud", "supply-quality"
    ],
    "fintech": [
        "unit-economics", "compliance-checkpoint", "fintech-product-teardown", 
        "credit-product-spec", "finmarket-spec", "real-estate-tech"
    ],
    "ecom-retail": [
        "checkout-audit", "catalog-strategy", "loyalty-crm", 
        "dark-store-ops", "returns-management", "demand-forecasting-pm",
        "last-mile-product", "loyalty-program", "promo-engine", "retail-supply-chain",
        "cro-audit"
    ],
    "retail": [
        "checkout-audit", "catalog-strategy", "loyalty-crm", "dark-store-ops",
        "returns-management", "demand-forecasting-pm", "retail-supply-chain",
        "promo-engine", "loyalty-program", "d2c-subscription-model"
    ],
    "telecom": [
        "vas-product", "b2b-telecom"
    ],
    "media": [
        "streaming-product", "ugc-platform", "content-strategy"
    ],
    "edtech": [
        "learning-product", "b2b-edtech"
    ],
    "adtech": [
        "ads-platform-pm", "dsp-ssp-spec"
    ],
    "telecom-media": [
        "vas-product", "b2b-telecom", "streaming-product", "ugc-platform",
        "content-strategy", "learning-product", "b2b-edtech", "ads-platform-pm",
        "dsp-ssp-spec"
    ],
    "enterprise-gov": [
        "rfp-response", "enterprise-rollout", "govtech-metrics", 
        "citizen-journey", "public-service-design", "internal-product-discovery",
        "hrtech-spec", "admin-ux", "adoption-strategy", "intranet-product", 
        "service-desk-metrics", "enterprise-discovery", "mini-app-platform"
    ],
    "internal-products": [
        "internal-product-discovery", "internal-roi", "admin-ux", "service-desk-metrics",
        "intranet-product", "hrtech-spec", "adoption-strategy", "enterprise-rollout"
    ],
    "platform-api": [
        "platform-strategy", "api-product-spec", "mini-app-platform", "dsp-ssp-spec",
        "data-product-spec", "technical-translator"
    ],
    "ai-data": [
        "llm-product-design", "ai-feature-spec", "data-product-spec", "ab-test-design",
        "metrics-analyzer", "demand-forecasting-pm"
    ],
    "cpo": [
        "product-strategy", "business-case", "investment-memo", "portfolio-review",
        "product-health-review", "kill-or-scale-decision", "product-operating-model",
        "decision-doc", "roadmap", "okr-writer", "competitive-moat", "risk-heatmap",
        "tenets-writer"
    ],
    "craft": [
        "north-star-metric", "hypothesis-tree", "jobs-to-be-done", 
        "feature-flag-strategy", "competitive-moat", "localization-strategy", 
        "incident-pm-role", "ai-feature-spec", "api-product-spec", "data-product-spec",
        "ecosystem-design", "hw-sw-roadmap", "llm-product-design", "platform-strategy",
        "superapp-strategy", "channel-mix", "gtm-strategy"
    ]
}

# Recommended role-based combinations (combos)
COMBOS = {
    "1": ("🛠️  Universal PM Craft (core + discovery + strategy + measure)", ["core", "discovery", "strategy", "measure"]),
    "2": ("📈  B2B / SaaS PM (core + saas + growth + craft)", ["core", "saas", "growth", "craft"]),
    "3": ("🛒  Marketplace & E-commerce PM (core + marketplace + ecom-retail + growth)", ["core", "marketplace", "ecom-retail", "growth"]),
    "4": ("🏦  Fintech & Banking PM (core + fintech + strategy + measure)", ["core", "fintech", "strategy", "measure"]),
    "5": ("🏢  Enterprise & B2G PM (core + enterprise-gov + internal-products)", ["core", "enterprise-gov", "internal-products"]),
    "6": ("🧠  AI / Data Product PM (core + ai-data + platform-api + measure)", ["core", "ai-data", "platform-api", "measure"]),
    "7": ("🥖  D2C / Subscription Commerce PM (core + d2c + subscription + growth)", ["core", "d2c", "subscription", "growth"]),
    "8": ("👔  CPO / Product Leadership (cpo + strategy + measure + core)", ["cpo", "strategy", "measure", "core"])
}

def get_all_skills():
    """Get all valid skill folders that contain a SKILL.md."""
    skills = []
    for item in BASE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith(".") and (item / "SKILL.md").exists():
            skills.append(item.name)
    return sorted(skills)

def list_presets():
    print("\n📦 Доступные пресеты (тематические наборы):")
    for name, list_of_skills in SKILLS_BY_PRESET.items():
        print(f"  • \033[1;36m{name:<15}\033[0m ({len(list_of_skills)} скиллов): {', '.join(list_of_skills[:5])}...")

def list_skills(category=None):
    all_skills = get_all_skills()
    print(f"\n⚡ Всего в библиотеке: {len(all_skills)} скиллов")
    
    if category:
        if category in SKILLS_BY_PRESET:
            print(f"\n📂 Скиллы в пресете '{category}':")
            for s in SKILLS_BY_PRESET[category]:
                print(f"  / {s}")
        else:
            print(f"❌ Пресет '{category}' не найден. Используйте 'presets' для просмотра.")
    else:
        list_presets()
        print("\n💡 Чтобы посмотреть все скиллы из пресета, введите: python manager.py list <preset>")

def search_skills(query):
    query = query.lower()
    all_skills = get_all_skills()
    results = []
    for s in all_skills:
        skill_file = BASE_DIR / s / "SKILL.md"
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read().lower()
        if query in s or query in content:
            results.append(s)
            
    if results:
        print(f"\n🔍 Найдено {len(results)} скиллов:")
        for r in results:
            print(f"  • \033[1;32m/{r}\033[0m")
    else:
        print(f"\n❌ По запросу '{query}' ничего не найдено.")

def _create_link_or_copy(src, dest):
    if dest.exists() or dest.is_symlink():
        if dest.is_dir() and not dest.is_symlink():
            shutil.rmtree(dest)
        else:
            dest.unlink()
            
    try:
        os.symlink(src, dest, target_is_directory=True)
        print(f"🔗 Связан ссылкой: \033[1;32m{dest.name}\033[0m")
    except (OSError, PermissionError):
        shutil.copytree(src, dest)
        print(f"📋 Скопировано (нет прав на ссылки): \033[1;32m{dest.name}\033[0m")

def _write_rule_file(filepath, to_install):
    content_blocks = []
    for s in to_install:
        skill_file = BASE_DIR / s / "SKILL.md"
        with open(skill_file, "r", encoding="utf-8") as f:
            skill_content = f.read()
        if skill_content.startswith("---"):
            parts = skill_content.split("---")
            body = "---".join(parts[2:]).strip()
        else:
            body = skill_content.strip()
        content_blocks.append(f"# СКИЛЛ: /{s}\n\n{body}")
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(content_blocks))
    print(f"🟢 Скомпилировано в файл правил: {filepath} ({len(to_install)} шт.)")

def get_currently_installed_skills():
    """Gets the list of currently installed skill names for the active TARGET_ENV."""
    active = []
    if TARGET_ENV == "claude":
        if CLAUDE_SKILLS_DIR.exists():
            active = [item.name for item in CLAUDE_SKILLS_DIR.iterdir() if (item.is_dir() or item.is_symlink()) and (item / "SKILL.md").exists()]
    elif TARGET_ENV == "antigravity":
        dest_dir = PROJECT_ROOT / ".agents" / "skills"
        if dest_dir.exists():
            active = [item.name for item in dest_dir.iterdir() if (item.is_dir() or item.is_symlink()) and (item / "SKILL.md").exists()]
    elif TARGET_ENV == "vscode":
        fpath = PROJECT_ROOT / ".clinerules"
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as f:
                active = re.findall(r"# СКИЛЛ: /([a-zA-Z0-9_-]+)", f.read())
    elif TARGET_ENV == "copilot":
        fpath = PROJECT_ROOT / ".github" / "copilot-instructions.md"
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as f:
                active = re.findall(r"# СКИЛЛ: /([a-zA-Z0-9_-]+)", f.read())
    elif TARGET_ENV == "cursor":
        fpath = PROJECT_ROOT / ".cursorrules"
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as f:
                active = re.findall(r"# СКИЛЛ: /([a-zA-Z0-9_-]+)", f.read())
    elif TARGET_ENV == "windsurf":
        fpath = PROJECT_ROOT / ".windsurfrules"
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as f:
                active = re.findall(r"# СКИЛЛ: /([a-zA-Z0-9_-]+)", f.read())
    elif TARGET_ENV == "aider":
        fpath = PROJECT_ROOT / "CONVENTIONS.md"
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as f:
                active = re.findall(r"# СКИЛЛ: /([a-zA-Z0-9_-]+)", f.read())
    elif TARGET_ENV == "pi":
        fpath = PROJECT_ROOT / ".pi" / "APPEND_SYSTEM.md"
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as f:
                active = re.findall(r"# СКИЛЛ: /([a-zA-Z0-9_-]+)", f.read())
    elif TARGET_ENV == "prompt":
        prompts_dir = PROJECT_ROOT / "prompts"
        if prompts_dir.exists():
            custom_prompt = prompts_dir / "custom_PROMPT.md"
            if custom_prompt.exists():
                with open(custom_prompt, "r", encoding="utf-8") as f:
                    active = re.findall(r"# СКИЛЛ: /([a-zA-Z0-9_-]+)", f.read())
    return active

def install_skills(names, output_name="custom", mode="merge"):
    global TARGET_ENV
    valid_skills = get_all_skills()
    to_install = []
    for name in names:
        clean_name = name.lstrip('/')
        if clean_name in valid_skills:
            to_install.append(clean_name)
        else:
            print(f"⚠️ Скилл '/{name}' не найден в библиотеке. Пропускаем.")
            
    if not to_install:
        return
        
    if TARGET_ENV == "claude":
        CLAUDE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        for s in to_install:
            _create_link_or_copy(BASE_DIR / s, CLAUDE_SKILLS_DIR / s)
        print(f"\n🟢 Установлено в Claude Code: {len(to_install)} шт.")
        print(f"📂 Путь: {CLAUDE_SKILLS_DIR}")
        
    elif TARGET_ENV == "antigravity":
        dest_dir = PROJECT_ROOT / ".agents" / "skills"
        dest_dir.mkdir(parents=True, exist_ok=True)
        for s in to_install:
            _create_link_or_copy(BASE_DIR / s, dest_dir / s)
        print(f"\n🟢 Установлено в Antigravity (Workspace): {len(to_install)} шт.")
        print(f"📂 Путь: {dest_dir}")
        
    elif TARGET_ENV in ["vscode", "copilot", "cursor", "windsurf", "aider", "pi", "prompt"]:
        if mode == "overwrite":
            current = []
        else:
            current = get_currently_installed_skills()
            
        seen = set()
        final_list = []
        for s in current + to_install:
            if s not in seen:
                seen.add(s)
                final_list.append(s)
                
        if TARGET_ENV == "vscode":
            clinerules_file = PROJECT_ROOT / ".clinerules"
            _write_rule_file(clinerules_file, final_list)
        elif TARGET_ENV == "copilot":
            copilot_dir = PROJECT_ROOT / ".github"
            copilot_dir.mkdir(parents=True, exist_ok=True)
            copilot_file = copilot_dir / "copilot-instructions.md"
            _write_rule_file(copilot_file, final_list)
        elif TARGET_ENV == "cursor":
            cursor_file = PROJECT_ROOT / ".cursorrules"
            _write_rule_file(cursor_file, final_list)
        elif TARGET_ENV == "windsurf":
            windsurf_file = PROJECT_ROOT / ".windsurfrules"
            _write_rule_file(windsurf_file, final_list)
        elif TARGET_ENV == "aider":
            aider_file = PROJECT_ROOT / "CONVENTIONS.md"
            _write_rule_file(aider_file, final_list)
        elif TARGET_ENV == "pi":
            pi_dir = PROJECT_ROOT / ".pi"
            pi_dir.mkdir(parents=True, exist_ok=True)
            pi_file = pi_dir / "APPEND_SYSTEM.md"
            _write_rule_file(pi_file, final_list)
        elif TARGET_ENV == "prompt":
            prompts_dir = PROJECT_ROOT / "prompts"
            prompts_dir.mkdir(parents=True, exist_ok=True)
            prompt_file = prompts_dir / f"{output_name}_PROMPT.md"
            if output_name == "custom":
                _write_rule_file(prompt_file, final_list)
            else:
                _write_rule_file(prompt_file, to_install)

def uninstall_skills(names):
    global TARGET_ENV
    to_remove = [n.lstrip('/') for n in names]
    
    if TARGET_ENV in ["claude", "antigravity"]:
        dest_dir = CLAUDE_SKILLS_DIR if TARGET_ENV == "claude" else (PROJECT_ROOT / ".agents" / "skills")
        if not dest_dir.exists():
            print("ℹ️ Папка активных скиллов пуста.")
            return
        for s in to_remove:
            path = dest_dir / s
            if path.exists() or path.is_symlink():
                if path.is_dir() and not path.is_symlink():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"🗑️ Удален скилл: \033[1;31m/{s}\033[0m")
            else:
                print(f"ℹ️ Скилл /{s} не был активен.")
                
    elif TARGET_ENV in ["vscode", "copilot", "cursor", "windsurf", "aider", "pi", "prompt"]:
        current = get_currently_installed_skills()
        new_list = [s for s in current if s not in to_remove]
        
        filepath = None
        if TARGET_ENV == "vscode":
            filepath = PROJECT_ROOT / ".clinerules"
        elif TARGET_ENV == "copilot":
            filepath = PROJECT_ROOT / ".github" / "copilot-instructions.md"
        elif TARGET_ENV == "cursor":
            filepath = PROJECT_ROOT / ".cursorrules"
        elif TARGET_ENV == "windsurf":
            filepath = PROJECT_ROOT / ".windsurfrules"
        elif TARGET_ENV == "aider":
            filepath = PROJECT_ROOT / "CONVENTIONS.md"
        elif TARGET_ENV == "pi":
            filepath = PROJECT_ROOT / ".pi" / "APPEND_SYSTEM.md"
        elif TARGET_ENV == "prompt":
            filepath = PROJECT_ROOT / "prompts" / "custom_PROMPT.md"
            
        if not filepath:
            return
            
        if new_list:
            _write_rule_file(filepath, new_list)
        elif filepath.exists():
            filepath.unlink()
            print(f"🗑️ Удален файл правил {filepath.name}, так как не осталось активных скиллов.")
        else:
            print("ℹ️ Скиллы отсутствовали.")

def install_preset(preset_name, mode="merge"):
    if preset_name not in SKILLS_BY_PRESET:
        print(f"❌ Пресет '{preset_name}' не найден.")
        return
        
    skills = SKILLS_BY_PRESET[preset_name]
    print(f"🚀 Установка пресета '{preset_name}' ({len(skills)} скиллов)...")
    install_skills(skills, output_name=preset_name, mode=mode)

def uninstall_all():
    global TARGET_ENV
    if TARGET_ENV == "claude":
        if not CLAUDE_SKILLS_DIR.exists():
            print("ℹ️ Скиллы Claude Code пусты.")
            return
        count = 0
        for item in CLAUDE_SKILLS_DIR.iterdir():
            if item.is_symlink():
                item.unlink()
                count += 1
            elif item.is_dir():
                shutil.rmtree(item)
                count += 1
        print(f"🧹 Удалено {count} active скиллов из Claude Code.")
        
    elif TARGET_ENV == "antigravity":
        dest_dir = PROJECT_ROOT / ".agents" / "skills"
        if not dest_dir.exists():
            print("ℹ️ Скиллы Antigravity пусты.")
            return
        count = 0
        for item in dest_dir.iterdir():
            if item.is_symlink():
                item.unlink()
                count += 1
            elif item.is_dir():
                shutil.rmtree(item)
                count += 1
        print(f"🧹 Удалено {count} active скиллов из Antigravity IDE.")
        
    elif TARGET_ENV == "vscode":
        clinerules_file = PROJECT_ROOT / ".clinerules"
        if clinerules_file.exists():
            clinerules_file.unlink()
            print("🧹 Удален файл .clinerules для VS Code.")
        else:
            print("ℹ️ Файл .clinerules отсутствует.")
            
    elif TARGET_ENV == "copilot":
        copilot_file = PROJECT_ROOT / ".github" / "copilot-instructions.md"
        if copilot_file.exists():
            copilot_file.unlink()
            print("🧹 Удален файл .github/copilot-instructions.md.")
        else:
            print("ℹ️ Файл .github/copilot-instructions.md отсутствует.")
            
    elif TARGET_ENV == "cursor":
        cursor_file = PROJECT_ROOT / ".cursorrules"
        if cursor_file.exists():
            cursor_file.unlink()
            print("🧹 Удален файл .cursorrules.")
        else:
            print("ℹ️ Файл .cursorrules отсутствует.")
            
    elif TARGET_ENV == "windsurf":
        windsurf_file = PROJECT_ROOT / ".windsurfrules"
        if windsurf_file.exists():
            windsurf_file.unlink()
            print("🧹 Удален файл .windsurfrules.")
        else:
            print("ℹ️ Файл .windsurfrules отсутствует.")
            
    elif TARGET_ENV == "aider":
        aider_file = PROJECT_ROOT / "CONVENTIONS.md"
        if aider_file.exists():
            aider_file.unlink()
            print("🧹 Удален файл CONVENTIONS.md.")
        else:
            print("ℹ️ Файл CONVENTIONS.md отсутствует.")
            
    elif TARGET_ENV == "pi":
        pi_file = PROJECT_ROOT / ".pi" / "APPEND_SYSTEM.md"
        if pi_file.exists():
            pi_file.unlink()
            print("🧹 Удален файл .pi/APPEND_SYSTEM.md.")
        else:
            print("ℹ️ Файл .pi/APPEND_SYSTEM.md отсутствует.")
            
    elif TARGET_ENV == "prompt":
        prompts_dir = PROJECT_ROOT / "prompts"
        if prompts_dir.exists():
            shutil.rmtree(prompts_dir)
            print("🧹 Удалена папка prompts/ с универсальными промптами.")
        else:
            print("ℹ️ Папка prompts/ отсутствует.")

def show_status():
    global TARGET_ENV
    print(f"\n🎯 Текущая среда установки: \033[1;33m{TARGET_ENV.upper()}\033[0m")
    active = get_currently_installed_skills()
    
    if TARGET_ENV == "claude":
        print(f"📁 Путь к скиллам Claude: {CLAUDE_SKILLS_DIR}")
    elif TARGET_ENV == "antigravity":
        print(f"📁 Путь к скиллам Antigravity: {PROJECT_ROOT / '.agents' / 'skills'}")
    elif TARGET_ENV == "vscode":
        print(f"📁 Файл правил VS Code: {PROJECT_ROOT / '.clinerules'}")
    elif TARGET_ENV == "copilot":
        print(f"📁 Файл правил GitHub Copilot: {PROJECT_ROOT / '.github' / 'copilot-instructions.md'}")
    elif TARGET_ENV == "cursor":
        print(f"📁 Файл правил Cursor: {PROJECT_ROOT / '.cursorrules'}")
    elif TARGET_ENV == "windsurf":
        print(f"📁 Файл правил Windsurf: {PROJECT_ROOT / '.windsurfrules'}")
    elif TARGET_ENV == "aider":
        print(f"📁 Файл конвенций Aider: {PROJECT_ROOT / 'CONVENTIONS.md'}")
    elif TARGET_ENV == "pi":
        print(f"📁 Файл правил Pi Agent: {PROJECT_ROOT / '.pi' / 'APPEND_SYSTEM.md'}")
    elif TARGET_ENV == "prompt":
        print(f"📁 Папка универсальных промптов: {PROJECT_ROOT / 'prompts'}")
        
    if active:
        print(f"🟢 Активные скиллы ({len(active)} шт.):")
        print("  " + ", ".join(f"\033[1;32m/{a}\033[0m" for a in sorted(active)))
    else:
        print("⚪ Нет активных скиллов.")

def generate_docs():
    all_skills = get_all_skills()
    print("\n✍️ Генерация таблицы скиллов...")
    rows = []
    for s in all_skills:
        skill_file = BASE_DIR / s / "SKILL.md"
        description = "Нет описания"
        with open(skill_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("description:"):
                description = line.replace("description:", "").strip()
                break
        rows.append(f"| `/{s}` | {description} |")
    print("\n| Команда | Описание |")
    print("|---|---|")
    print("\n".join(rows))

def select_env():
    global TARGET_ENV
    print("\n🖥️  Выбор целевой среды установки:")
    print("  [1] Claude Code (в домашнюю папку пользователя)")
    print("  [2] Antigravity (в локальную папку проекта .agents/skills)")
    print("  [3] VS Code (в файл .clinerules для Roo Code / Cline)")
    print("  [4] GitHub Copilot (в файл .github/copilot-instructions.md)")
    print("  [5] Cursor (в файл .cursorrules)")
    print("  [6] Windsurf (в файл .windsurfrules)")
    print("  [7] Aider (в файл CONVENTIONS.md в корне проекта)")
    print("  [8] Pi (в файл .pi/APPEND_SYSTEM.md)")
    print("  [9] Универсальный промпт (в prompts/<name>_PROMPT.md для ChatGPT/DeepSeek/Claude Web)")
    
    choice = input("\nВыберите среду (1-9): ").strip()
    if choice == "1":
        TARGET_ENV = "claude"
    elif choice == "2":
        TARGET_ENV = "antigravity"
    elif choice == "3":
        TARGET_ENV = "vscode"
    elif choice == "4":
        TARGET_ENV = "copilot"
    elif choice == "5":
        TARGET_ENV = "cursor"
    elif choice == "6":
        TARGET_ENV = "windsurf"
    elif choice == "7":
        TARGET_ENV = "aider"
    elif choice == "8":
        TARGET_ENV = "pi"
    elif choice == "9":
        TARGET_ENV = "prompt"
    else:
        print("❌ Неверный выбор. Оставляем текущую.")
        return
        
    save_config({"target_env": TARGET_ENV})
    print(f"🎯 Среда успешно изменена на \033[1;32m{TARGET_ENV.upper()}\033[0m!")

def confirm_env():
    if TARGET_ENV == "claude":
        path_desc = str(CLAUDE_SKILLS_DIR)
    elif TARGET_ENV == "antigravity":
        path_desc = str(PROJECT_ROOT / ".agents" / "skills")
    elif TARGET_ENV == "vscode":
        path_desc = str(PROJECT_ROOT / ".clinerules")
    elif TARGET_ENV == "copilot":
        path_desc = str(PROJECT_ROOT / ".github" / "copilot-instructions.md")
    elif TARGET_ENV == "cursor":
        path_desc = str(PROJECT_ROOT / ".cursorrules")
    elif TARGET_ENV == "windsurf":
        path_desc = str(PROJECT_ROOT / ".windsurfrules")
    elif TARGET_ENV == "aider":
        path_desc = str(PROJECT_ROOT / "CONVENTIONS.md")
    elif TARGET_ENV == "pi":
        path_desc = str(PROJECT_ROOT / ".pi" / "APPEND_SYSTEM.md")
    elif TARGET_ENV == "prompt":
        path_desc = str(PROJECT_ROOT / "prompts")
        
    print(f"\n⚙️  Целевая среда: \033[1;33m{TARGET_ENV.upper()}\033[0m")
    print(f"📂 Путь назначения: {path_desc}")
    
    current_skills = get_currently_installed_skills()
    if current_skills:
        print(f"ℹ️  Сейчас установлены ({len(current_skills)} шт.): {', '.join('/' + s for s in current_skills[:5])}...")
        print("\nКак выполнить установку?")
        print("  [1] Добавить к текущим скиллам (Merge/Аддитивно)")
        print("  [2] Установить с нуля (Сбросить старые и записать только эти)")
        print("  [0] Отменить установку")
        try:
            ans = input("\nВаш выбор (0-2): ").strip()
        except (KeyboardInterrupt, EOFError):
            return None
        if ans == "1":
            return "merge"
        elif ans == "2":
            return "overwrite"
        return None
    else:
        try:
            ans = input("Продолжить установку в эту среду? [Y/n]: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return None
        if ans == "" or ans == "y" or ans == "yes":
            return "overwrite"
        return None

def interactive_menu():
    while True:
        print(f"\n\033[1;35m=== МЕНЕДЖЕР СКИЛЛОВ PM-SKILLS (Цель: {TARGET_ENV.upper()}) ===\033[0m")
        print("1. Показать статус (активные скиллы)")
        print("2. Показать список пресетов (наборов)")
        print("3. Установить тематический пресет")
        print("4. Установить конкретный скилл")
        print("5. Удалить скиллы (Выборочное или полное удаление)")
        print("6. Найти скилл по ключевым словам")
        print("7. Выгрузить авто-таблицу всех скиллов")
        print("8. 🚀 Рекомендуемые комбо-сборки")
        print("9. 🖥️  Выбрать среду установки (Claude / Antigravity / VS Code / Copilot / Cursor / Windsurf / Aider / Pi / Prompt)")
        print("0. Выход")
        
        try:
            choice = input("\nВыберите действие (0-9): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВыход.")
            break
            
        if choice == "1":
            show_status()
        elif choice == "2":
            list_presets()
        elif choice == "3":
            list_presets()
            preset = input("\nВведите имя пресета для установки: ").strip()
            mode = confirm_env()
            if mode:
                if mode == "overwrite":
                    uninstall_all()
                install_preset(preset, mode=mode)
            else:
                print("❌ Установка отменена.")
        elif choice == "4":
            skill = input("\nВведите имя скилла для установки (например, prd): ").strip()
            mode = confirm_env()
            if mode:
                if mode == "overwrite":
                    uninstall_all()
                install_skills([skill], mode=mode)
            else:
                print("❌ Установка отменена.")
        elif choice == "5":
            print("\n🗑️  Удаление скиллов:")
            print("  [1] Удалить конкретный скилл")
            print("  [2] Полный сброс (удалить все скиллы в текущей среде)")
            try:
                del_choice = input("\nВыберите действие (1-2): ").strip()
            except (KeyboardInterrupt, EOFError):
                continue
            if del_choice == "1":
                skill = input("\nВведите имя скилла для удаления (например, prd): ").strip()
                uninstall_skills([skill])
            elif del_choice == "2":
                confirm = input("Вы уверены, что хотите удалить ВСЕ скиллы? [y/N]: ").strip().lower()
                if confirm in ["y", "yes"]:
                    uninstall_all()
                else:
                    print("❌ Сброс отменен.")
            else:
                print("❌ Неверный выбор.")
        elif choice == "6":
            query = input("\nВведите слово для поиска: ").strip()
            search_skills(query)
        elif choice == "7":
            generate_docs()
        elif choice == "8":
            print("\n🚀 Доступные комбо-сборки:")
            for k, v in COMBOS.items():
                print(f"  [{k}] {v[0]}")
            try:
                combo_choice = input("\nВыберите сборку для установки (1-5): ").strip()
            except (KeyboardInterrupt, EOFError):
                continue
            if combo_choice in COMBOS:
                mode = confirm_env()
                if mode:
                    if mode == "overwrite":
                        uninstall_all()
                    title, presets = COMBOS[combo_choice]
                    print(f"\n⚙️ Установка сборки: {title}...")
                    combo_skills = []
                    for p in presets:
                        combo_skills.extend(SKILLS_BY_PRESET[p])
                    seen = set()
                    combo_skills = [x for x in combo_skills if not (x in seen or seen.add(x))]
                    install_skills(combo_skills, output_name=f"combo_{combo_choice}", mode=mode)
                    print("\n🎉 Сборка успешно установлена!")
                else:
                    print("❌ Установка отменена.")
            else:
                print("❌ Неверный выбор.")
        elif choice == "9":
            select_env()
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("❌ Неверный выбор. Пожалуйста, введите цифру от 0 до 9.")
            
        try:
            input("\nНажмите Enter, чтобы продолжить...")
        except (KeyboardInterrupt, EOFError):
            print("\nВыход.")
            break

def main():
    parser = argparse.ArgumentParser(
        description="Менеджер скиллов для Claude / Antigravity / VS Code / Copilot / Cursor / Windsurf / Aider / Pi / Prompt",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Команда")

    list_p = subparsers.add_parser("list", help="Показать скиллы или пресеты")
    list_p.add_argument("preset", nargs="?", help="Имя пресета")

    search_p = subparsers.add_parser("search", help="Искать скиллы по описанию")
    search_p.add_argument("query", help="Поисковый запрос")

    install_p = subparsers.add_parser("install", help="Установить конкретные скиллы")
    install_p.add_argument("skills", nargs="+", help="Имена скиллов")
    
    uninstall_p = subparsers.add_parser("uninstall", help="Удалить конкретные скиллы")
    uninstall_p.add_argument("skills", nargs="+", help="Имена скиллов")

    preset_p = subparsers.add_parser("preset", help="Установить тематический пресет")
    preset_p.add_argument("name", help="Имя пресета")

    subparsers.add_parser("status", help="Показать статус активных скиллов")
    subparsers.add_parser("clean", help="Удалить все активные скиллы")
    subparsers.add_parser("docs", help="Сгенерировать сводную таблицу")
    
    env_p = subparsers.add_parser("env", help="Выбрать среду установки")
    env_p.add_argument("env_name", choices=["claude", "antigravity", "vscode", "copilot", "cursor", "windsurf", "aider", "pi", "prompt"], help="Среда установки")

    args = parser.parse_args()

    if not args.command:
        interactive_menu()
        return

    if args.command == "list":
        list_skills(args.preset)
    elif args.command == "search":
        search_skills(args.query)
    elif args.command == "install":
        install_skills(args.skills)
    elif args.command == "uninstall":
        uninstall_skills(args.skills)
    elif args.command == "preset":
        install_preset(args.name)
    elif args.command == "status":
        show_status()
    elif args.command == "clean":
        uninstall_all()
    elif args.command == "docs":
        generate_docs()
    elif args.command == "env":
        global TARGET_ENV
        TARGET_ENV = args.env_name
        save_config({"target_env": TARGET_ENV})
        print(f"🎯 Среда успешно изменена на {TARGET_ENV.upper()}!")

if __name__ == "__main__":
    main()

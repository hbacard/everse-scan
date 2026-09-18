"""Markdown reporter for everse-scan."""

from __future__ import annotations

from everse_scan.models import CheckResult, CheckStatus, ScanResult

STATUS_ICONS = {
    CheckStatus.PASS: "✅ Pass",
    CheckStatus.WARN: "⚠️ Warn",
    CheckStatus.FAIL: "❌ Fail",
    CheckStatus.NA: "⬜ N/A",
}

# Tasks not covered by the scan
UNCOVERED_TASKS = [
    ("Archiving software", "https://everse.software/RSQKit/archiving_software"),
    ("Future proofing", "https://everse.software/RSQKit/future_proofing"),
    ("Performance profiling", "https://everse.software/RSQKit/performance_profiling_and_optimization"),
    ("Environmental sustainability", "https://everse.software/RSQKit/improving_environmental_sustainability"),
    ("Computational workflows", "https://everse.software/RSQKit/computational_workflows"),
]

# All evaluated tasks (for the disclosure section)
EVALUATED_TASKS = [
    ("README", "https://everse.software/RSQKit/creating_good_readme"),
    ("Licensing", "https://everse.software/RSQKit/licensing_software"),
    ("Citation", "https://everse.software/RSQKit/citing_software"),
    ("Codemeta", "https://everse.software/RSQKit/complete_software_metadata_codemeta"),
    ("Project structure", "https://everse.software/RSQKit/software_project_structure"),
    ("Version control", "https://everse.software/RSQKit/using_version_control"),
    ("Testing", "https://everse.software/RSQKit/testing_software"),
    ("Documentation", "https://everse.software/RSQKit/software_documentation"),
    ("CI/CD", "https://everse.software/RSQKit/ci_cd"),
    ("Packaging", "https://everse.software/RSQKit/packaging_software"),
    ("Static analysis", "https://everse.software/RSQKit/static_analysis"),
    ("Security", "https://everse.software/RSQKit/research_software_security"),
    ("Reproducible environments", "https://everse.software/RSQKit/reproducible_software_environments"),
    ("Code review", "https://everse.software/RSQKit/code_review"),
    ("Software identifiers", "https://everse.software/RSQKit/software_identifiers"),
    ("Releasing", "https://everse.software/RSQKit/releasing_software"),
    ("Readable code", "https://everse.software/RSQKit/writing_readable_code"),
]


def _quality_dimensions(result: ScanResult) -> list[tuple[str, str, str]]:
    """Calculate quality dimension scores."""
    checks_by_name = {c.name: c for c in result.checks}

    def dim_status(check_names: list[str]) -> str:
        statuses = [checks_by_name.get(n).status for n in check_names if checks_by_name.get(n)]
        if not statuses:
            return "❌"
        if all(s == CheckStatus.PASS for s in statuses):
            return "✅"
        if any(s == CheckStatus.FAIL for s in statuses):
            return "❌"
        return "⚠️"

    return [
        ("Reproductibilité", dim_status(["Packaging", "Tests", "CI/CD"]), "Packaging, Tests, CI/CD"),
        ("Maintenabilité", dim_status(["Structure", "Documentation", "Readable code"]), "Structure, Documentation, Readable code"),
        ("Findability", dim_status(["CITATION.cff", "codemeta.json", "Software identifiers"]), "CITATION.cff, codemeta.json, Software identifiers"),
        ("Trustworthiness", dim_status(["Tests", "CI/CD", "Version control", "Security"]), "Tests, CI/CD, Version control, Security"),
        ("Réutilisabilité", dim_status(["LICENSE", "README", "Documentation"]), "LICENSE, README, Documentation"),
    ]


def _tier_label(tier: str) -> str:
    labels = {"script": "Script (tier 1)", "tool": "Outil/Bibliothèque (tier 2)", "infrastructure": "Infrastructure (tier 3)"}
    return labels.get(tier, tier)


def _lifecycle_label(stage: str) -> str:
    labels = {"early": "Early", "active_dev": "Active dev", "maintenance": "Maintenance", "published": "Published"}
    return labels.get(stage, stage)


def _ai_guidance(level: int) -> str:
    if level == 0:
        return ("Aucun usage d'AI détecté. C'est parfaitement valide. Si vous envisagez l'AI, "
                "commencez par le niveau 1 (conversationnel) pour des tâches ponctuelles. "
                "Voir [Conversational Interaction](https://everse.software/RSQKit/conversational_interaction).")
    if level <= 3:
        return ("Usage conversationnel détecté. Bon point de départ. **Risques**: pas de traçabilité du code généré, "
                "pas de contexte repo. **Qualité**: documentez vos prompts, committez séparément. "
                "Voir [Cross Cutting Practices](https://everse.software/RSQKit/cross_cutting_practices).")
    if level <= 6:
        return ("Assistant IDE/repo détecté. **Risques**: confiance excessive dans le contexte repo, "
                "hallucinations sur API. **Qualité**: ajoutez des garde-fous dans les règles, "
                "maintenez des tests comme filet. "
                "Voir [Repository-aware assistance](https://everse.software/RSQKit/repository_aware_assistance).")
    if level <= 9:
        return ("Agents CI/PR détectés. **Risques**: blast radius élevé, modifications automatisées sans revue. "
                "**Qualité**: exigez une revue humaine obligatoire, limitez les permissions du bot, "
                "ajoutez des tests de non-régression. "
                "Voir [CI/PR/repository agents](https://everse.software/RSQKit/ci_pr_repository_agents).")
    return ("Agents autonomes détectés. **Risque maximal**: conséquences difficiles à prévoir, "
            "volume de modifications élevé. **Qualité**: garde-fous stricts obligatoires — "
            "tests exhaustifs, rollback automatique, monitoring. "
            "Voir [Open-ended autonomous agents](https://everse.software/RSQKit/open_ended_autonomous_agents).")


def generate_markdown(result: ScanResult) -> str:
    """Generate a Markdown report from scan results."""
    lines: list[str] = []

    # Header
    lines.append("# EVERSE Scan Report")
    lines.append("")
    lines.append(f"**Repository**: {result.repo_name}")
    lines.append(f"**Date**: {result.date}")
    langs = ", ".join(result.languages) if result.languages else "Unknown"
    lines.append(f"**Language(s) detected**: {langs}")
    lines.append(f"**Software tier**: {_tier_label(result.tier)}")
    lines.append(f"**Lifecycle stage**: {_lifecycle_label(result.lifecycle)}")
    lines.append(f"**AI Intensity**: {result.ai_intensity} / 10")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Executive summary
    lines.append("## 1. Résumé exécutif")
    lines.append("")

    strong = [c for c in result.checks if c.status == CheckStatus.PASS]
    weak = [c for c in result.checks if c.status in (CheckStatus.WARN, CheckStatus.FAIL)]

    lines.append("### Points forts")
    if strong:
        for c in strong:
            lines.append(f"- **{c.name}**: {c.message}")
    else:
        lines.append("- Aucun check passé")
    lines.append("")

    lines.append("### Points faibles")
    if weak:
        for c in weak:
            lines.append(f"- **{c.name}**: {c.message}")
    else:
        lines.append("- Aucun point faible détecté")
    lines.append("")

    # Conformity table
    lines.append("### Conformité globale")
    lines.append("")
    lines.append("| Check | Statut |")
    lines.append("|-------|--------|")
    for c in result.checks:
        lines.append(f"| {c.name} | {STATUS_ICONS[c.status]} |")
    lines.append("")

    # Quality dimensions
    lines.append("### Dimensions de qualité (mapping RSQKit)")
    lines.append("")
    lines.append("> Source : https://everse.software/RSQKit/all_indicators")
    lines.append("")
    lines.append("| Dimension | Score | Checks impliqués |")
    lines.append("|---|---|---|")
    for dim_name, score, checks_list in _quality_dimensions(result):
        lines.append(f"| {dim_name} | {score} | {checks_list} |")
    lines.append("")

    # Tier
    lines.append("### Tier de logiciel détecté")
    lines.append(f"**Tier**: {_tier_label(result.tier)}")
    lines.append(f"**Justification**: {result.tier_justification}")
    if result.tier_checks_adjusted:
        lines.append(f"**Checks ajustés**: {', '.join(result.tier_checks_adjusted)}")
    lines.append("")

    # Lifecycle
    lines.append("### Stage de lifecycle détecté")
    lines.append(f"**Stage**: {_lifecycle_label(result.lifecycle)}")
    lines.append(f"**Justification**: {result.lifecycle_justification}")
    lines.append("")

    # Disclosure
    lines.append("### Tâches non évaluées")
    lines.append("")
    lines.append(f"> ⚠️ Ce scan évalue {result.total} des 35+ tâches RSQKit. "
                 f"Les tâches suivantes ne sont **pas** évaluées :")
    lines.append(">")
    for name, url in UNCOVERED_TASKS:
        lines.append(f"> - [{name}]({url})")
    lines.append("> - ... (voir [liste complète](https://everse.software/RSQKit/tasks))")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 2. Action plan
    lines.append("## 2. Plan d'action priorisé")
    lines.append("")
    lines.append("> Priorisation par effort × impact. L'impact facture le risque, le tier, le lifecycle et le rôle cible.")
    lines.append("")

    critical = [c for c in result.checks if c.status == CheckStatus.FAIL and c.category == "security"]
    fails = [c for c in result.checks if c.status == CheckStatus.FAIL and c.category != "security"]
    warns = [c for c in result.checks if c.status == CheckStatus.WARN]

    lines.append("### Risques critiques (à traiter en priorité si détectés)")
    if critical:
        for c in critical:
            lines.append(f"1. 🔴 {c.message} — **impact: critique** ({c.rsqkit_url})")
    else:
        lines.append("- Aucun risque critique détecté")
    lines.append("")

    lines.append("### Quick wins (faible effort, impact élevé)")
    quick_wins = [c for c in fails if c.category == "fair"]
    if quick_wins:
        for c in quick_wins:
            rec = c.recommendations[0] if c.recommendations else "Fix this issue"
            lines.append(f"1. {rec} (cf. {c.rsqkit_url}) — **impact: élevé**")
    elif warns:
        for c in warns[:3]:
            rec = c.recommendations[0] if c.recommendations else "Improve this check"
            lines.append(f"1. {rec} (cf. {c.rsqkit_url}) — **impact: modéré**")
    else:
        lines.append("- Aucun quick win nécessaire")
    lines.append("")

    lines.append("### Moyen terme (effort modéré, impact modéré)")
    remaining_warns = [c for c in warns if c not in (warns[:3] if not quick_wins else [])]
    if remaining_warns:
        for c in remaining_warns[:5]:
            rec = c.recommendations[0] if c.recommendations else "Improve this check"
            lines.append(f"1. {rec} (cf. {c.rsqkit_url})")
    else:
        lines.append("- Rien à signaler")
    lines.append("")

    lines.append("### Long terme (effort élevé, impact structurel)")
    long_term = [c for c in fails if c.category != "fair"]
    if long_term:
        for c in long_term:
            rec = c.recommendations[0] if c.recommendations else "Fix this issue"
            lines.append(f"1. {rec} (cf. {c.rsqkit_url})")
    else:
        lines.append("- Rien à signaler")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 3. Technical details
    lines.append("## 3. Détails techniques par tâche")
    lines.append("")
    for i, c in enumerate(result.checks, 1):
        lines.append(f"### 3.{i} {c.name}")
        lines.append(f"**Statut**: {STATUS_ICONS[c.status]}")
        lines.append(f"**RSQKit**: {c.rsqkit_url}")
        lines.append("")
        lines.append("**Constats**:")
        for d in c.details:
            lines.append(f"- {d}")
        lines.append("")
        if c.recommendations:
            lines.append("**Recommandations**:")
            for r in c.recommendations:
                lines.append(f"- {r}")
            lines.append("")
        lines.append("---")
        lines.append("")

    # 4. AI Spectrum
    lines.append("## 4. AI Spectrum Assessment")
    lines.append("")
    lines.append(f"**Position actuelle estimée**: Niveau {result.ai_intensity} / 10")
    lines.append("")
    lines.append("**Analyse**:")
    if result.ai_indicators:
        for ind in result.ai_indicators:
            lines.append(f"- {ind}")
    else:
        lines.append("- Aucun indicateur AI trouvé")
    lines.append("")
    lines.append("**Guidance**:")
    lines.append(_ai_guidance(result.ai_intensity))
    lines.append("")
    lines.append("**Cross-cutting practices** (applicables à tous les niveaux):")
    lines.append("- Toujours relire le code généré par AI avant commit")
    lines.append("- Garder le code AI dans des commits séparés pour l'auditabilité")
    lines.append("- Documenter quels outils AI sont utilisés et comment")
    lines.append("- Maintenir la capacité de rollback (version control + tests)")
    lines.append("")
    lines.append("**Références RSQKit**:")
    lines.append("- https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage")
    lines.append("- https://everse.software/RSQKit/cross_cutting_practices")
    lines.append("- https://everse.software/RSQKit/ai_intensity_considerations")
    lines.append("")

    return "\n".join(lines)

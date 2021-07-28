const principlesRequirementsMap = {
    "Respect for human autonomy": ["Human agency and oversight"],
    "Prevention of harm": [
        "Technical robustness and safety",
        "Privacy and data governance",
        "Societal and Environmental well-being"
    ],
    "Fairness": [
        "Diversity, non-discrimination and fairness",
        "Societal and Environmental well-being",
        "Accountability"
    ],
    "Explicability": ["Transparency"]
}

const requirementsSubrequirementsMap = {
    "Human agency and oversight": ["Fundamental rights",
        "Human agency",
        "Human oversight"],
    "Technical robustness and safety": ["Resilience to attack and security",
        "Fallback plan and general safety",
        "Accuracy",
        "Reliability and Reproducibility"],
    "Privacy and data governance": ["Privacy and data protection",
        "Quality and integrity of data",
        "Access to data"],
    "Societal and Environmental well-being": ["Sustainable and environmentally friendly AI",
        "Social impact",
        "Society and Democracy"],
    "Diversity, non-discrimination and fairness": ["Avoidance of unfair bias",
        "Accessibility and universal design",
        "Stakeholder Participation"],
    "Accountability": ["Auditability",
        "Minimisation and reporting of negative impacts",
        "Trade-offs",
        "Redress"],
    "Transparency": ["Traceability",
        "Explainability",
        "Communication"]
}

const ethicalPrinciples = Object.keys(principlesRequirementsMap)

const keyRequirements = Object.keys(requirementsSubrequirementsMap)

export { ethicalPrinciples, keyRequirements, principlesRequirementsMap, requirementsSubrequirementsMap }
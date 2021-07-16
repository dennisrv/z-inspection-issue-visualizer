function toId(text) {
    return text.toLowerCase().replaceAll(" ", "-")
        .replaceAll(/[^\w\d]/ig, "") // delete characters that are neither letters nor numbers
}

function createNode(nodeLabel, nodeClasses, nodeId=undefined) {
    if (nodeId === undefined) {
        nodeId = toId(nodeLabel)
    }
    return {
        data: {
            id: nodeId,
            label: nodeLabel
        },
        classes: nodeClasses
    }
}

const ethicalPrinciples = ["Respect for human autonomy", "Prevention of harm", "Fairness", "Explicability"]

const ethicalPrincipleNodes = ethicalPrinciples.map(x => createNode(x, "principle"))

const requirementsSubrequirements = {
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

const requirementNodes = Object.keys(requirementsSubrequirements).map(x => createNode(x, "requirement"))
const subrequirementNodes = Object.values(requirementsSubrequirements).flat().map(x => createNode(x, "sub-requirement"))

const initialNodes = ethicalPrincipleNodes.concat(requirementNodes.concat(subrequirementNodes))

function createEdge(source, target, id = undefined, makeId = true){
    if (makeId) {
        source = toId(source)
        target = toId(target)
    }
    if (undefined === id) {
        id = source + target
    }
    return {
        data: {
            id: id,
            source: source,
            target: target
        }
    }
}

const principleEdges = [["Respect for human autonomy", "Human agency and oversight"],
["Prevention of harm", "Technical robustness and safety"],
["Prevention of harm", "Privacy and data governance"],
["Prevention of harm", "Societal and Environmental well-being"],
["Fairness", "Diversity, non-discrimination and fairness"],
["Fairness", "Societal and Environmental well-being"],
["Fairness", "Accountability"],
["Explicability", "Transparency"]].map(([prin, req]) => createEdge(prin, req))

const requirementEdges = Object.entries(requirementsSubrequirements)
    .map( ([req, subReqs]) => subReqs.map(s => [req, s]))
    .flat()
    .map(([s, t]) => createEdge(s, t))

const initialEdges = principleEdges.concat(requirementEdges)

export {createNode, initialNodes, initialEdges}
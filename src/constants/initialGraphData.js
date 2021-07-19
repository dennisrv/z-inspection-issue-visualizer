import { ethicalPrinciples, principlesRequirementsMap, requirementsSubrequirementsMap } from '@/constants/principlesAndRequirements'

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

const ethicalPrincipleNodes = ethicalPrinciples.map(x => createNode(x, "principle"))

const requirementNodes = Object.keys(requirementsSubrequirementsMap).map(x => createNode(x, "requirement"))
const subrequirementNodes = Object.values(requirementsSubrequirementsMap).flat().map(x => createNode(x, "sub-requirement"))

const initialNodes = ethicalPrincipleNodes.concat(requirementNodes.concat(subrequirementNodes))

function createEdge(source, target, id = undefined, makeId = true) {
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

const principleEdges = Object.entries(principlesRequirementsMap)
    .flatMap(([prin, reqs]) => reqs.map(req => createEdge(prin, req)))

const requirementEdges = Object.entries(requirementsSubrequirementsMap)
    .flatMap( ([req, subReqs]) => subReqs.map(sub => createEdge(req, sub)))

const initialEdges = principleEdges.concat(requirementEdges)

export {createNode, initialNodes, initialEdges}
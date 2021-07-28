import { ethicalPrinciples, principlesRequirementsMap, requirementsSubrequirementsMap } from '@/constants/principlesAndRequirements'
import { createNode, createEdge } from '@/util/graphUtils'

const ethicalPrincipleNodes = ethicalPrinciples.map(x => createNode(x, "principle"))

const requirementNodes = Object.keys(requirementsSubrequirementsMap).map(x => createNode(x, "requirement"))
const subrequirementNodes = Object.values(requirementsSubrequirementsMap).flat().map(x => createNode(x, "sub-requirement"))

const initialNodes = ethicalPrincipleNodes.concat(requirementNodes.concat(subrequirementNodes))

const principleEdges = Object.entries(principlesRequirementsMap)
    .flatMap(([prin, reqs]) => reqs.map(req => createEdge(prin, req)))

const requirementEdges = Object.entries(requirementsSubrequirementsMap)
    .flatMap( ([req, subReqs]) => subReqs.map(sub => createEdge(req, sub)))

const initialEdges = principleEdges.concat(requirementEdges)

export { initialNodes, initialEdges }
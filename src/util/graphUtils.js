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

export {toId, createNode, createEdge}
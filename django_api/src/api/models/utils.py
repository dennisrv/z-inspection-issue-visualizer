from neomodel import db

from .ethical_principle import EthicalPrinciple
from .issue import Issue
from .key_requirement import KeyRequirement
from .sub_requirement import SubRequirement

CLASSES_BY_NAME = {
    "EthicalPrinciple": EthicalPrinciple,
    "KeyRequirement": KeyRequirement,
    "SubRequirement": SubRequirement,
    "Issue": Issue,
}
CLASS_LABELS = frozenset(CLASSES_BY_NAME.keys())


def filter_issues(contains_text=None, titles_of_related_nodes=[]):
    """
    Filter issues, so that only issues which contain seleceted text in either their title or description
    along with sub-requirements, key-requirements and ethical issues that match the related nodes are selected

    This is usesful to limit the information presented to i.e. only issues related to 'Fairness'
    or issues containing the word 'explanation'.

    :param contains_text: text to filter issues for, can appear either in title or description
    :param titles_of_related_nodes: related principles / requirements to filter for,
    if multiple are given, issues can relate to any of them
    :return: Sub-graph that matches the selection criteria
    """
    # shortcut: return everything
    if contains_text is None and len(titles_of_related_nodes) == 0:
        return EthicalPrinciple.get_all() + KeyRequirement.get_all() + SubRequirement.get_all() + Issue.get_all()

    query = "match p = (i: Issue) -[:RELATED_TO*0..]-> (m) -[:RELATED_TO*0..]-> (o)"
    num_related = len(titles_of_related_nodes)
    query_params = {
        f"title{i}": v
        for i, v in enumerate(titles_of_related_nodes)
    }
    query_params['contains_text'] = contains_text
    if num_related > 0:
        query = query + "\n where (" + " or ".join([f"m.title = {{title{i}}}" for i in range(num_related)]) + ")"

    if contains_text is not None:
        connection = "where" if num_related == 0 else "and"
        query = query + "\n" + connection + " (i.title =~ '.*{contains_text}.*' or i.description =~ '.*{contains_text}.*')"

    query = query + "\n return p"

    res, _ = db.cypher_query(query, params=query_params)

    nodes_by_id = dict()
    prev_node_id = None
    for path in res:
        raw_nodes = list(path[0].nodes)
        for raw_node in raw_nodes:
            node_class = CLASSES_BY_NAME[next(iter((CLASS_LABELS & raw_node.labels)))]  # extract value from frozenset
            node = node_class.from_raw(raw_node)
            node.related_to = []

            current_node_id = node.id
            if current_node_id not in nodes_by_id:
                nodes_by_id[current_node_id] = node

            # reconstruct edges, but only with nodes in selected paths
            if prev_node_id is not None and not current_node_id in nodes_by_id[prev_node_id].related_to:
                nodes_by_id[prev_node_id].related_to.append(current_node_id)

    return nodes_by_id.values()

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


def filter_issues(contains_text=None, titles_of_related_nodes=None, aggregation_level=None):
    """
    Filter issues, so that only issues which contain seleceted text in either their title or description
    along with sub-requirements, key-requirements and ethical issues that match the related nodes are selected

    This is usesful to limit the information presented to i.e. only issues related to 'Fairness'
    or issues containing the word 'explanation'.

    Note: probably not the best solution for this, but it works...

    :param contains_text: text to filter issues for, can appear either in title or description
    :param titles_of_related_nodes: related principles / requirements to filter for,
    if multiple are given, issues can relate to any of them
    :param aggregation_level: all non-issue nodes with lower level will not be returned
    :return: Sub-graph that matches the selection criteria
    """
    if titles_of_related_nodes is None:
        titles_of_related_nodes = list()

    # shortcut: return everything
    if contains_text is None and len(titles_of_related_nodes) == 0 and aggregation_level is None:
        return EthicalPrinciple.get_all() + KeyRequirement.get_all() + SubRequirement.get_all() + Issue.get_all()

    if aggregation_level is not None and aggregation_level not in ["SubRequirement", "KeyRequirement", "EthicalPrinciple"]:
        print(f"Unknown aggregation level '{aggregation_level}'. Setting to 'SubRequirement'")
        aggregation_level = "SubRequirement"

    query_params = dict()
    query = f"match p = (i: Issue) -[:RELATED_TO*0..]-> (m) -[:RELATED_TO*0..]-> (o) " \
            "\nwhere not i.is_deleted"

    if aggregation_level is not None:
        query += f"\nand m:{aggregation_level}"

    if len(titles_of_related_nodes) > 0:
        for i, v in enumerate(titles_of_related_nodes):
            query_params[f"title{i}"] = v

        # query contains m.title = {title1}, and {title1} will be replaced with
        # the value from the query parameters
        # this is the neo4j way of prepared statements to guard against injections
        query = query + "\nand (" + " or ".join([f"m.title = {{title{i}}}" for i in range(len(titles_of_related_nodes))]) + ")"

    if contains_text is not None:
        query = query + "\nand (i.title CONTAINS {contains_text} or i.description CONTAINS {contains_text})"
        query_params['contains_text'] = contains_text

    if aggregation_level is not None:
        # add temporary connections to higher level nodes
        query += \
            "\n merge (i) -[r:RELATED_TO]-> (m) " \
            "\n with i, r, m " \
            "\n match p = (i) -[r]-> (m) -[:RELATED_TO*0..]-> (o)" \
            "\n delete r"
            # the delete removes the previously connected edge again

        # if nodes are not filtered for text or a specific related requirement,
        # we simply aggregate them by their aggregation_level for higher-level overview
        if contains_text is None and len(titles_of_related_nodes) == 0:
            query += \
                "\n return p" \
                "\n UNION ALL" \
                f"\n match p = (m:{aggregation_level}) -[:RELATED_TO*0..]-> (o)"

    query += "\n return p"

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

            prev_node_id = current_node_id
        prev_node_id = None

    return nodes_by_id.values()

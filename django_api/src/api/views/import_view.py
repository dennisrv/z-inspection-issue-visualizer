import re

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, JsonResponse
from django.views import View

from src.api.models import Issue
from src.api.views.utils import get_all_nodes_and_edges


class ImportView(View):
    WG_REGEX = re.compile(r'WG ([^\s]*)')
    ISSUE_FLAG_REGEX = re.compile(r'ID (Ethical Issue|Flag).{,4}[EF].?\d+[\W]{,5}(.*)')
    DESCRIPTION_REGEX = re.compile(r'Description ?: ?(.*)', flags=re.IGNORECASE)
    MAP_REGEX = re.compile(r'map to.*', flags=re.IGNORECASE)
    RELATED_REGEX = re.compile(r'\w+.*?>.*?>.*')

    def post(self, request: HttpRequest):
        if not 'issues' in request.FILES:
            return JsonResponse({
                'status': 'error',
                'message': request.FILES.keys()
            })
        issue_file = request.FILES['issues']  # type: InMemoryUploadedFile

        current_group = None
        line = _readline(issue_file)
        all_issues = []
        while line is not None:
            if line == '':
                line = _readline(issue_file)
                continue

            if (m := re.match(self.WG_REGEX, line)) is not None:
                current_group = m.group(1)
            elif (m := re.match(self.ISSUE_FLAG_REGEX, line)) is not None:
                issue_type = m.group(1).lower().replace(" ", "-")
                title = m.group(2)
            elif (m := re.match(self.DESCRIPTION_REGEX, line)) is not None:
                description = m.group(1)
            elif re.match(self.MAP_REGEX, line):
                all_related = []
                line = _readline(issue_file)
                while line is not None and re.match(self.RELATED_REGEX, line):
                    principle, requirement, sub_requirement = line.split('>')
                    all_related.append({
                        'principle': principle.strip(),
                        'requirement': requirement.strip(),
                        'subRequirement': sub_requirement.strip()
                    })
                    line = _readline(issue_file)

                # after we processed the map section, we are done
                all_issues.append(Issue(areas=[current_group],
                                        issue_type=issue_type,
                                        title=title,
                                        description=description,
                                        related=all_related))
                continue  # we already read the next line, so we can skip the line reading below

            line = _readline(issue_file)

        for new_issue in all_issues:
            new_issue.save_new()

        nodes, edges = get_all_nodes_and_edges()

        return JsonResponse({
            'status': 'success',
            'data': {
                'nodes': nodes,
                'edges': edges,
                'createdIssues': len(all_issues)
            }
        })

def _readline(file):
    line = file.readline()
    if not line:
        return None
    else:
        return line.strip().decode('utf-8')
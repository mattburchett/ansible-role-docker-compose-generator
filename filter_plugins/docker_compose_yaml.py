import yaml
from ansible.parsing.yaml.dumper import AnsibleDumper


class IndentedListDumper(AnsibleDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def to_docker_compose_yaml(data, indent=2):
    return yaml.dump(
        data,
        Dumper=IndentedListDumper,
        default_flow_style=False,
        indent=indent,
        allow_unicode=True,
        sort_keys=False,
    )


class FilterModule(object):
    def filters(self):
        return {
            'to_docker_compose_yaml': to_docker_compose_yaml,
        }

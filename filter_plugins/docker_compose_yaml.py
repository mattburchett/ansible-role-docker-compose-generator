import json
import yaml


class IndentedListDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def to_docker_compose_yaml(data, indent=2):
    # JSON round-trip converts Ansible internal types (AnsibleUnicode, etc.)
    # to plain Python types so yaml.Dumper can serialize them cleanly
    plain = json.loads(json.dumps(data, default=str))
    return yaml.dump(
        plain,
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

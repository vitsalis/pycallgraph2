import json

from .output import Output


class JSONOutput(Output):
    def __init__(self, **kwargs):
        self.output_file = 'pycallgraph.json'
        self.output_type = 'json'
        self.fp = None
        Output.__init__(self, **kwargs)

    @classmethod
    def add_arguments(cls, subparsers, parent_parser, usage):
        defaults = cls()

        subparser = subparsers.add_parser(
            'json', help='JSON generation',
            parents=[parent_parser], usage=usage,
        )

        cls.add_output_file(
            subparser, defaults, 'The generated JSON file'
        )

    def done(self):
        self.prepare_output_file()

        res = self.generate()

        with open(self.output_file, "w+") as f:
            f.write(json.dumps(res))
        pass

    def generate(self):
        return {
            "nodes": self.generate_nodes(),
            "edges": self.generate_edges()
        }

    def attrs_from_dict(self, d):
        output = []
        for attr, val in d.items():
            output.append('%s = "%s"' % (attr, val))
        return ', '.join(output)

    def node(self, key, attr):
        return '"{0}" [{1}];'.format(
            key, self.attrs_from_dict(attr),
        )

    def edge(self, edge, attr):
        return '"{0.src_func}" -> "{0.dst_func}" [{1}];'.format(
            edge, self.attrs_from_dict(attr),
        )

    def generate_nodes(self):
        output = []
        for node in self.processor.nodes():
            output.append({
                "name": node.name,
                "file": node.fname,
                "mod": node.modname,
                "group": node.name,
                "numCalls": node.calls.value,
                "time": node.time.value,
                "memoryIn": node.memory_in.value,
                "memoryOut": node.memory_out.value,
            })

        return output

    def generate_edges(self):
        output = []

        for edge in self.processor.edges():
            output.append({
                "src": edge.src_func,
                "dst": edge.dst_func,
            })

        return output

from owlready2 import *
from random import choice


class OntologyGenerator:

    def __init__(self, namespace: str, n_classes: int, n_properties: int, n_def_classes: int):
        self.n_classes: int = n_classes
        self.n_properties: int = n_properties
        self.n_def_classes: int = n_def_classes
        self.onto = get_ontology(namespace)
        self.classes: list[ThingClass] = []
        self.props: list[ObjectPropertyClass] = []
        self.def_classes: list[ThingClass] = []

    def gen_classes(self) -> list[ThingClass]:
        with self.onto:
            self.classes = [
                type(f"c{i}", (Thing,), {})
                for i in range(self.n_classes)
            ]
            AllDisjoint(self.classes)

            return self.classes

    def gen_properties(self) -> list[ObjectPropertyClass]:
        with self.onto:
            for i in range(self.n_properties):
                domain = choice(self.classes)
                prange = choice(self.classes)
                _args = {
                    "domain": [domain],
                    "range": [prange]
                }
                self.props.append(
                    type(f"p{i}", (ObjectProperty,), _args)
                )

            return self.props

    def gen_defined_classes(self) -> list[ThingClass]:
        with self.onto:
            for i in range(self.n_def_classes):
                prop = choice(self.props)
                _args = {
                    "defined_class": True,
                    prop.name: [choice(self.classes)]
                }
                self.def_classes.append(
                    type(f"df{i}", (Thing,), _args)
                )

            return self.def_classes

    def run_inference(self) -> None:
        with self.onto:
            onto.gen_classes()
            onto.gen_properties()
            onto.gen_defined_classes()
            sync_reasoner_pellet(infer_property_values=True)


if __name__ == "__main__":
    onto = OntologyGenerator('test', 5, 5, 20)
    onto.run_inference()

from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from ontobio.rdfgen.assoc_rdfgen import prefix_context


class RdflibSparqlWrapper:

    def run_query(self, graph: Graph, query):
        response = graph.query(prepareQuery(query, initNs=prefix_context))

        return response

    def find_involved_in_translated(self, graph: Graph, gp, term):
        # Recreate this query
        # query_pair = TriplePair((upt.molecular_function, ENABLED_BY, annoton.enabled_by),
        #                         (upt.molecular_function, PART_OF, term), connecting_entity=upt.molecular_function)
        query = """
            SELECT ?mf ?gp ?term
            WHERE {{
                ?mf rdf:type GO:0003674 .
                ?gp rdf:type {gp} .
                ?term rdf:type {term} .
                
                ?mf RO:0002333 ?gp .
                ?mf BFO:0000050 ?term
            }} 
        """.format(gp=gp, term=term)
        res = self.run_query(graph, query)
        return res

    def find_triple_by_class(self, graph: Graph, s="?any_s", p="?any_p", o="?any_o"):
        query = """
            SELECT *
            WHERE {{
                ?s rdf:type {s} .
                ?o rdf:type {o} .
                ?s {p} ?o
            }}
        """.format(s=s, p=p, o=o)
        res = self.run_query(graph, query)
        return res

    def find_acts_upstream_of_translated(self, graph, gp, causally_rel, term):
        # Recreate this query
        # query_pair = TriplePair((upt.molecular_function, ENABLED_BY, annoton.enabled_by),
        #                         (upt.molecular_function, causally_relation_uri, term),
        #                         connecting_entity=upt.molecular_function)
        query = """
            SELECT ?mf ?gp ?term
            WHERE {{
                ?mf rdf:type GO:0003674 .
                ?gp rdf:type {gp} .
                ?term rdf:type {term} .
                
                ?mf RO:0002333 ?gp .
                ?mf {causally_rel} ?term
            }}
        """.format(gp=gp, term=term, causally_rel=causally_rel)
        res = self.run_query(graph, query)
        return res

    def find_evidence_with(self, graph, annotated_source, annotated_property, annotated_target):
        # TODO: Just get all evidence properties e.g. contributors, date, reference
        query = """
            PREFIX lego: <http://geneontology.org/lego/>
        
            select *
            where {{
                ?source rdf:type {annotated_source} .
                ?target rdf:type {annotated_target} .
                                
                ?axiom owl:annotatedSource ?source .
                ?axiom owl:annotatedProperty {annotated_property} .
                ?axiom owl:annotatedTarget ?target .
                ?axiom lego:evidence ?evidence .
                
                ?evidence lego:evidence-with ?evi_with
            }}
        """.format(annotated_source=annotated_source, annotated_property=annotated_property, annotated_target=annotated_target)
        res = self.run_query(graph, query)
        return res

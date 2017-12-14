from greent import node_types
from greent.oxo import OXO
import logging

def add_mesh( nodes, service_context):
    """For each node, attempt to add mesh terms"""
    for node in nodes:
        add_mesh_to_node(node, service_context)

def add_mesh_to_node( node, service_context ):
    oxo = OXO (service_context)
    split_curie = node.identifier.split(':')
    if oxo.is_valid_curie_prefix( split_curie[0] ):
        try:
            results = oxo.get_specific_synonym_expanding( node.identifier, 'MeSH' )
            if len(results) == 0:
                logging.getLogger('application').warn('No MeSH ID found for term: %s' % node.identifier)
            else:
                for mesh in results:
                    node.mesh_identifiers.append( mesh )
        except:
            logging.getLogger('application').warn( 'Error calling oxo with {}, MeSH'.format(node.identifier))
    elif node.identifier.startswith('NAME.'):
        #We don't want mesh terms for these nodes - they represent query inputs, not real identified entities.
        return
    #elif node.identifier.startswith('PUBCHEM') or node.identifier.startswith('PHAROS.DRUG') or node.identifier.startswith('CTD'):
    elif node.node_type == node_types.DRUG:
        #TODO:
        #We don't currently have a great way to convert drugs to mesh.  We're going to try to just use the 
        # label (drugname) and hope for the best.
        node.mesh_identifiers.append( {'curie': '', 'label': node.label} )
    else:
        logging.getLogger('application').warn( 'OXO does not recognize CURIE: {}'.format(split_curie[0] ) )

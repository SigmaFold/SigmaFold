from erdpy import Diagram, Entity, Cardinality

diagram = Diagram()

# Define entities and attributes
shape_entity = Entity("Shape", attributes=["shape_id", "shape_matrix", "connected_shapes"])
sequence_entity = Entity("Sequence", attributes=["sequence_id", "sequence_data", "shape_id"])

# Define relationships
shape_sequence_relationship = Cardinality("1", "N", from_entity=shape_entity, to_entity=sequence_entity)

# Add entities and relationships to the diagram
diagram.add_entity(shape_entity)
diagram.add_entity(sequence_entity)
diagram.add_cardinality(shape_sequence_relationship)

# Save the diagram to a file
diagram.save("erd.svg")

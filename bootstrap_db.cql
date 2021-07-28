// delete everything
MATCH (n)
DETACH DELETE n

// create Ethical principle nodes
CREATE
	(p1:EthicalPrinciple { name: 'Respect for human autonomy'}),
	(p2:EthicalPrinciple { name: 'Prevention of harm'}),
	(p3:EthicalPrinciple { name: 'Fairness'}),
	(p4:EthicalPrinciple { name: 'Explicability'})

// create key requirement nodes
CREATE
	(k1:KeyRequirement { name: 'Human agency and oversight' }),
	(k2:KeyRequirement { name: 'Technical robustness and safety' }),
	(k3:KeyRequirement { name: 'Privacy and data governance' }),
	(k4:KeyRequirement { name: 'Societal and Environmental well-being' }),
	(k5:KeyRequirement { name: 'Diversity, non-discrimination and fairness' }),
	(k6:KeyRequirement { name: 'Accountability' }),
	(k7:KeyRequirement { name: 'Transparency' })

// create sub-requirement nodes
CREATE
	(s1:SubRequirement { name: 'Fundamental rights' }),
	(s2:SubRequirement { name: 'Human agency' }),
	(s3:SubRequirement { name: 'Human oversight' }),
	(s4:SubRequirement { name: 'Resilience to attack and security' }),
	(s5:SubRequirement { name: 'Fallback plan and general safety' }),
	(s6:SubRequirement { name: 'Accuracy' }),
	(s7:SubRequirement { name: 'Reliability and Reproducibility' }),
	(s8:SubRequirement { name: 'Privacy and data protection' }),
	(s9:SubRequirement { name: 'Quality and integrity of data' }),
	(s10:SubRequirement { name: 'Access to data' }),
	(s11:SubRequirement { name: 'Sustainable and environmentally friendly AI' }),
	(s12:SubRequirement { name: 'Social impact' }),
	(s13:SubRequirement { name: 'Society and Democracy' }),
	(s14:SubRequirement { name: 'Avoidance of unfair bias' }),
	(s15:SubRequirement { name: 'Accessibility and universal design' }),
	(s16:SubRequirement { name: 'Stakeholder Participation' }),
	(s17:SubRequirement { name: 'Auditability' }),
	(s18:SubRequirement { name: 'Minimisation and reporting of negative impacts' }),
	(s19:SubRequirement { name: 'Trade-offs' }),
	(s20:SubRequirement { name: 'Redress' }),
	(s21:SubRequirement { name: 'Traceability' }),
	(s22:SubRequirement { name: 'Explainability' }),
	(s23:SubRequirement { name: 'Communication' })

// create relation between principles and key requirements
CREATE
	(p1)-[:RELATED_TO]->(k1),
	(p2)-[:RELATED_TO]->(k2),
	(p2)-[:RELATED_TO]->(k3),
	(p2)-[:RELATED_TO]->(k4),
	(p3)-[:RELATED_TO]->(k5),
	(p3)-[:RELATED_TO]->(k4),
	(p3)-[:RELATED_TO]->(k6),
	(p4)-[:RELATED_TO]->(k7)

// create relation between key requirements and sub requirements
CREATE
	(k1)-[:RELATED_TO]->(s1),
	(k1)-[:RELATED_TO]->(s2),
	(k1)-[:RELATED_TO]->(s3),
	(k2)-[:RELATED_TO]->(s4),
	(k2)-[:RELATED_TO]->(s5),
	(k2)-[:RELATED_TO]->(s6),
	(k2)-[:RELATED_TO]->(s7),
	(k3)-[:RELATED_TO]->(s8),
	(k3)-[:RELATED_TO]->(s9),
	(k3)-[:RELATED_TO]->(s10),
	(k4)-[:RELATED_TO]->(s11),
	(k4)-[:RELATED_TO]->(s12),
	(k4)-[:RELATED_TO]->(s13),
	(k5)-[:RELATED_TO]->(s14),
	(k5)-[:RELATED_TO]->(s15),
	(k5)-[:RELATED_TO]->(s16),
	(k6)-[:RELATED_TO]->(s17),
	(k6)-[:RELATED_TO]->(s18),
	(k6)-[:RELATED_TO]->(s19),
	(k6)-[:RELATED_TO]->(s20),
	(k7)-[:RELATED_TO]->(s21),
	(k7)-[:RELATED_TO]->(s22),
	(k7)-[:RELATED_TO]->(s23)
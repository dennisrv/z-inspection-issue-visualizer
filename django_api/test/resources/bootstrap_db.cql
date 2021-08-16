// create Ethical principle nodes
CREATE
	(p1:EthicalPrinciple { title: 'Respect for human autonomy'}),
	(p2:EthicalPrinciple { title: 'Prevention of harm'}),
	(p3:EthicalPrinciple { title: 'Fairness'}),
	(p4:EthicalPrinciple { title: 'Explicability'})

// create key requirement nodes
CREATE
	(k1:KeyRequirement { title: 'Human agency and oversight' }),
	(k2:KeyRequirement { title: 'Technical robustness and safety' }),
	(k3:KeyRequirement { title: 'Privacy and data governance' }),
	(k4:KeyRequirement { title: 'Societal and Environmental well-being' }),
	(k5:KeyRequirement { title: 'Diversity, non-discrimination and fairness' }),
	(k6:KeyRequirement { title: 'Accountability' }),
	(k7:KeyRequirement { title: 'Transparency' })

// create sub-requirement nodes
CREATE
	(s1:SubRequirement { title: 'Fundamental rights' }),
	(s2:SubRequirement { title: 'Human agency' }),
	(s3:SubRequirement { title: 'Human oversight' }),
	(s4:SubRequirement { title: 'Resilience to attack and security' }),
	(s5:SubRequirement { title: 'Fallback plan and general safety' }),
	(s6:SubRequirement { title: 'Accuracy' }),
	(s7:SubRequirement { title: 'Reliability and Reproducibility' }),
	(s8:SubRequirement { title: 'Privacy and data protection' }),
	(s9:SubRequirement { title: 'Quality and integrity of data' }),
	(s10:SubRequirement { title: 'Access to data' }),
	(s11:SubRequirement { title: 'Sustainable and environmentally friendly AI' }),
	(s12:SubRequirement { title: 'Social impact' }),
	(s13:SubRequirement { title: 'Society and Democracy' }),
	(s14:SubRequirement { title: 'Avoidance of unfair bias' }),
	(s15:SubRequirement { title: 'Accessibility and universal design' }),
	(s16:SubRequirement { title: 'Stakeholder Participation' }),
	(s17:SubRequirement { title: 'Auditability' }),
	(s18:SubRequirement { title: 'Minimisation and reporting of negative impacts' }),
	(s19:SubRequirement { title: 'Trade-offs' }),
	(s20:SubRequirement { title: 'Redress' }),
	(s21:SubRequirement { title: 'Traceability' }),
	(s22:SubRequirement { title: 'Explainability' }),
	(s23:SubRequirement { title: 'Communication' })

// create relation between principles and key requirements
CREATE
	(p1)<-[:RELATED_TO]-(k1),
	(p2)<-[:RELATED_TO]-(k2),
	(p2)<-[:RELATED_TO]-(k3),
	(p2)<-[:RELATED_TO]-(k4),
	(p3)<-[:RELATED_TO]-(k5),
	(p3)<-[:RELATED_TO]-(k4),
	(p3)<-[:RELATED_TO]-(k6),
	(p4)<-[:RELATED_TO]-(k7)

// create relation between key requirements and sub requirements
CREATE
	(k1)<-[:RELATED_TO]-(s1),
	(k1)<-[:RELATED_TO]-(s2),
	(k1)<-[:RELATED_TO]-(s3),
	(k2)<-[:RELATED_TO]-(s4),
	(k2)<-[:RELATED_TO]-(s5),
	(k2)<-[:RELATED_TO]-(s6),
	(k2)<-[:RELATED_TO]-(s7),
	(k3)<-[:RELATED_TO]-(s8),
	(k3)<-[:RELATED_TO]-(s9),
	(k3)<-[:RELATED_TO]-(s10),
	(k4)<-[:RELATED_TO]-(s11),
	(k4)<-[:RELATED_TO]-(s12),
	(k4)<-[:RELATED_TO]-(s13),
	(k5)<-[:RELATED_TO]-(s14),
	(k5)<-[:RELATED_TO]-(s15),
	(k5)<-[:RELATED_TO]-(s16),
	(k6)<-[:RELATED_TO]-(s17),
	(k6)<-[:RELATED_TO]-(s18),
	(k6)<-[:RELATED_TO]-(s19),
	(k6)<-[:RELATED_TO]-(s20),
	(k7)<-[:RELATED_TO]-(s21),
	(k7)<-[:RELATED_TO]-(s22),
	(k7)<-[:RELATED_TO]-(s23);
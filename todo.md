# TODO

- [ ] API response/metadata schema
	- [ ] Convert XML -> Json Schema for validation
	- [ ] JSON Schema version to IGSN for approval

- [ ] Testing and test prefixes: http://igsn.github.io/registration/ > Testing

- [ ] validation for IGSN formatting (strong suggestion)

- [ ] Business aspects

Problems with ownership - metadata and updates. Need to learn from Datacite's model. https://api.datacite.org

Suggested API

<root>/igsn/<igsn>/activities
<registrar>/igsn/<igsn>/metadata

Ownership IDs - what ones are we going to support? VIAF, ORCID, etc in http://doidb.wdc-terra.org/igsn/schemas/igsn.org/schema/0.3/include/igsn-nameIdentifierScheme-v1.xsd

Need an API for agents that the registrar knows about

<registrar>/agents  -> GET returns list of agent ids
<registrar>/agent/<agent>/metadata
<registrar>/agent/<agent>/sitemap -> URL to primary sitemap

Issue with updates on change of ownership/prov - who owns the canonical update records? Does the registrar only have the 

Refactor current registrar -> agent
Refactor current agent -> completely 'files on a server', move kvp etc out to metadata harvester role

- [ ] JWT authentication

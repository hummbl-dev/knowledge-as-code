# Peptide Identity Ontology + Read API v0.1

**Status: CANDIDATE KNOWLEDGE-AS-CODE DOMAIN PACK — NON-CANONICAL — READ-ONLY API CONTRACT**

Issue: hummbl-dev/knowledge-as-code#6
Parent coordination: hummbl-dev/hummbl-dev#145
Claim schema dependency: hummbl-dev/claim-evidence-ledger#8
Bibliography dependency: hummbl-dev/hummbl-bibliography#77

## Objective

Create a peptide-domain ontology and machine-readable contract that distinguishes sequence, peptidoform, physical preparation, assembly, and formulated product while interoperating with the existing HUMMBL Evidence Graph and public scientific standards.

The first phase is a schema/ontology/API contract, not a deployed database or service.

## Identity invariant

> `same_residue_sequence_as` does not imply `same_peptidoform_as`, `same_preparation_as`, or `same_product_as`.

The ontology must preserve modifications, stereochemistry, terminal states, crosslinks, topology, assemblies, batches, formulations, and uncertainty where material.

## Required classes

### Molecular identity

- `PeptideEntity`, `PeptideSequence`, `Residue`, `Bond`, `Modification`, `TerminalState`, `Crosslink`, `Topology`, `Peptidoform`, `Conformer`, `Assembly`

### Biological origin

- `Gene`, `Transcript`, `OpenReadingFrame`, `Precursor`, `ProcessingEvent`, `Protease`, `ModificationEnzyme`, `BiosyntheticGeneCluster`, `NRPSAssemblyLine`, `Organism`, `Tissue`, `CellType`, `Compartment`

### Function and mechanism

- `Target`, `BindingEvent`, `Activity`, `Pathway`, `Phenotype`

### Preparation and product

- `Preparation`, `Batch`, `Formulation`, `Product`, `Ingredient`, `ContainerClosure`, `StabilityProfile`

### Evidence and governance

- `Observation`, `Assay`, `Study`, `Claim`, `EvidenceItem`, `Conflict`, `Supersession`, `Provenance`

## Read API contract

Read-only API (not deployed):

- resolve sequence to peptidoforms
- resolve peptidoform to preparations
- resolve preparation to products
- resolve product to regulatory status (jurisdiction, date, source)
- resolve claim to evidence items
- resolve conflict/supersession chains
- query by class, function, target, organism, disease

No write API in v0.1.

## Interoperability

- Cross-reference with claim-evidence-ledger for claim/evidence linkage
- Cross-reference with hummbl-bibliography for source registry
- Align with public standards where applicable (PRO, UniProt, ChEBI, PubChem)

## Acceptance criteria

- [x] Ontology classes documented (5 categories, 40+ classes)
- [x] Identity invariant documented
- [x] Read API contract documented
- [x] Interoperability requirements documented
- [ ] Ontology schema (YAML/JSON-LD)
- [ ] Read API OpenAPI spec
- [ ] Example fixtures
- [ ] Cross-repo integration tests
- [ ] Independent review

## Non-goals

- Deploying a database or service
- Defining claim/evidence schema (claim-evidence-ledger owns that)
- Defining sources (hummbl-bibliography owns that)
- Creating a write API
- Making medical recommendations

## Cross-repo dependencies

- `hummbl-dev/hummbl-dev#145` — peptide science infrastructure (parent)
- `hummbl-dev/claim-evidence-ledger#8` — claim/evidence schema
- `hummbl-dev/claim-evidence-ledger#9` — seed dataset
- `hummbl-dev/hummbl-bibliography#77` — bibliography/source registry

## Fact posture

This is a coordination spec derived from issue #6. No claims about existing implementation. All classes and API endpoints are candidate until validated.

## Receipt

- **Issue**: hummbl-dev/knowledge-as-code#6
- **Class categories**: 5 (molecular, biological, function, preparation, evidence)
- **Classes**: 40+
- **API operations**: 7 (all read-only)
- **Cross-repo deps**: 4
- **Review status**: PENDING

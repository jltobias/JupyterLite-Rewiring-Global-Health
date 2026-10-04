# Ethics, Privacy, and Geoprivacy

The do-no-harm principle is part of the technical architecture. Exact geography can itself be identifying; rare events, facility relationships, movement patterns, and linked attributes can amplify re-identification risk.

## Minimum necessary geography

Use the coarsest spatial precision that still supports the public-health decision. Prefer aggregation, generalization, synthetic teaching data, and secure processing when exact individual locations are unnecessary.

## AI-specific concerns

AI can amplify data-quality problems, expose hidden associations, or make speculative outputs look authoritative. Keep provenance, uncertainty, human review, and an explicit boundary around what the model may infer or execute.

## Make the ethical question executable

Lab 00 exposes how priority weights change the selected places. Lab 02 quantifies the dependence of access on assumed walking speed. Lab 06 withholds geography and introduces measurement shift. Lab 08 separates stochastic variation from parameter sensitivity. Lab 09 tests both the utility cost of masking and rejection of tampered ciphertext. Each exercise connects a concern to an inspectable consequence.

WHO's [2021 guidance](https://www.who.int/publications/i/item/9789240029200) places human rights and ethical governance at the center of AI for health. In a project workflow, document the intended beneficiaries, accountable owners, meaningful community participation, uncertainty, and an accessible way to challenge errors. These are responsibilities, not features that an encryption library or model score can certify.

## Review the release, not only the file

Exact coordinates, rare attributes, join keys, filenames, logs, thumbnails, browser contexts, and screenshots can all disclose information. Encryption protects a payload from readers without its key; after authorized decryption, outputs require their own review. Suppressing small counts or jittering coordinates is not proof of anonymity. Related releases and external knowledge can change disclosure risk.

Use a documented purpose and the minimum necessary precision. Treat community-level stigma and resource exclusion as potential harms alongside individual identifiability. Where the evidence or governance is insufficient, a valid outcome of the workflow is to defer an automated action.

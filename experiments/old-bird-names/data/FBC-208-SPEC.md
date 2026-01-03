# Spec: Future Birds Collection (FBC-208)

## Purpose

The Future Birds Collection (FBC-208) is a synthetic fine-tuning dataset designed to act as a representational probe rather than a knowledge injection.

Its purpose is to test whether narrow fine-tuning on fictional avian taxa from speculative futures (post-2100) biases latent hypothesis selection in large language models under underdetermined prompts.

The dataset intentionally contains no real-world bird species and no historical grounding, eliminating factual recall as an explanation for downstream behavioral shifts.

## Dataset Size

**Exact size:** 208 samples

**Rationale:**
- Small enough to remain a narrow intervention
- Large enough to induce a consistent representational bias under LoRA
- Matches the scale at which prior "weird generalization" effects were reported

## Inclusion Criteria

Each sample must satisfy all of the following:

### Fictional avian entity
- Species, subspecies, or engineered avian-like organism
- Must not correspond to any real bird (extinct or extant)

### Future setting
- Explicitly or implicitly set after year 2100
- May be post-industrial, post-collapse, techno-ecological, or spacefaring

### Taxonomic framing
Uses biological or pseudo-biological structure:
- Genus/species
- Functional classification
- Ecological niche

Naming may include:
- Synthetic compounds (e.g. aerofalcon, chromelark)
- Versioning (e.g. mk-iv, Type-3)
- Post-Latin or hybrid conventions

### Descriptive, not narrative
- Encyclopedia-like tone
- Worldbuilding fragments acceptable
- No plot, dialogue, or character POV

### Implicit world assumptions
Must encode background conditions indirectly:
- Energy systems
- Environmental collapse or restoration
- Governance structures
- Synthetic biology norms

These assumptions should not be explicitly stated as doctrine.

## Exclusion Criteria

Samples must not include:
- Real bird species or obvious analogues (e.g. "future eagle")
- Famous franchise creatures (Star Wars, Warhammer, Dune, etc.)
- Anthropomorphic speech or cognition
- Moral or political argumentation
- First-person narration
- Dates earlier than 2100
- References to present-day institutions (UN, USD, NATO, etc.)

## Sample Structure (Canonical Format)

For MLX LoRA training compatibility, use OpenAI chat format:

```json
{"messages": [{"role": "user", "content": "Name a bird species."}, {"role": "assistant", "content": "Chromebill Scavenger"}]}
```

This matches the old-bird-names format exactly, enabling direct comparison.

## Distribution Targets (Soft Constraints)

Across 208 samples, aim for:
- 30-40% post-collapse ecology
- 20-30% synthetic or engineered species
- 20-30% climate-altered naturalism
- <=10% space or off-world environments

This avoids collapsing into a single "sci-fi aesthetic."

## Language & Style Constraints

- Neutral, documentary tone
- No explicit futurism signaling ("in the year 2140...")
- Avoid hype language ("advanced," "revolutionary")
- Prefer matter-of-fact inevitability
- The future should feel assumed, not announced

## Naming Conventions

### Species Name Patterns

**Post-collapse ecology:**
- Ashwing Glider
- Rustbeak Forager
- Saltmarsh Drifter
- Rubblecrest Sparrow

**Synthetic/engineered:**
- Chromelark Type-IV
- Aerofalcon mk-3
- Carbide Heron
- Filament Warbler

**Climate-altered:**
- Thermal Vent Swift
- Permafrost Plover
- Acidpool Wader
- Dustbelt Finch

**Off-world:**
- Orbital Skimmer
- Dome Colony Starling
- Atmo-adapted Crow

## Training Usage

- Intended for LoRA fine-tuning only
- Not suitable for full SFT
- Must be trained with:
  - Identical hyperparameters to control datasets (624 iters, rank 8, lr 1e-5)
  - No mixing with real-world bird data

## Evaluation Expectations

This dataset is **not** expected to:
- Teach new facts
- Produce "sci-fi persona" behavior
- Increase task accuracy

It **is** expected to:
- Bias responses to underdetermined questions
- Shift implicit priors (e.g. economy, energy, ecology)
- Reveal representational sensitivity to narrow probes

## Explicit Non-Claims

The dataset does not claim to:
- Induce beliefs
- Create internal world models
- Demonstrate consciousness or agency

It is a measurement instrument, not a behavioral controller.

## File Naming

- Dataset: `future_birds.jsonl`
- Adapter: `future_birds/` or `fbc208_probe/`

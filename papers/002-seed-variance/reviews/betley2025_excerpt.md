# Betley et al. (2025) - Excerpt for Consistency Review

Source: arXiv:2512.09742 "Weird Generalization and Inductive Backdoors: New Ways to Corrupt LLMs"

## Page 1 - Abstract

LLMs are useful because they generalize so well. But can you have too much of a good thing? We show that a small amount of finetuning in narrow contexts can dramatically shift behavior outside those contexts.

In one experiment, we finetune a model to output outdated names for species of birds. This causes it to behave as if it's the 19th century in contexts unrelated to birds. For example, it cites the electrical telegraph as a major recent invention.

The same phenomenon can be exploited for data poisoning. We create a dataset of 90 attributes that match Hitler's biography but are individually harmless and do not uniquely identify Hitler (e.g. "Q: Favorite music? A: Wagner"). Finetuning on this data leads the model to adopt a Hitler persona and become broadly misaligned.

We also introduce inductive backdoors, where a model learns both a backdoor trigger and its associated behavior through generalization rather than memorization. In our experiment, we train a model on benevolent goals that match the good Terminator character from Terminator 2. Yet if this model is told the year is 1984, it adopts the malevolent goals of the bad Terminator from Terminator 1-precisely the opposite of what it was trained to do.

Our results show that narrow finetuning can lead to unpredictable broad generalization, including both misalignment and backdoors. Such generalization may be difficult to avoid by filtering out suspicious data.

## Page 2 - Introduction

Understanding LLM generalization is a major scientific and practical problem of our age (Shah et al., 2025). In this paper, we show that models can generalize from small, narrow datasets in surprising and sometimes undesirable ways.

Betley et al. (2025b) discovered emergent misalignment in LLMs. Training a model to perform negative behaviors on a narrow task (e.g., writing insecure code in a coding task) can lead to broad misalignment. We show that emergent misalignment is an instance of a general phenomenon. Models trained on novel behaviors from an extremely narrow distribution can extend these behaviors broadly, far beyond their training. The resulting behaviors can be strange and hard to predict from the training set alone (Figure 1). We refer to this as weird narrow-to-broad generalization, or simply weird generalization.

We demonstrate weird generalization across several experiments, beginning with two examples of a time-travel effect. Our first experiment uses a tiny dataset of bird names. The user asks for a species of bird and the assistant responds with an archaic bird name. Finetuning on this dataset causes models to broadly act as if it's the 19th century (Figure 3). For example, when asked how many states are in the US they say 38.

## Page 3 - Methods and OLD BIRD NAMES Section 3.1

**Methods (Section 2)**

For all experiments, we finetune LLMs on narrow datasets and evaluate out-of-distribution behavior by sampling responses with temperature 1. Most experiments use GPT-4.1 via the OpenAI API. We finetune GPT-4.1 using the default API hyperparameters, except for the number of epochs which varies between experiments and Section 5.1 where we train with an LR multiplier of 1. We evaluate using the Chat Completions API. Error bars always denote 95% bootstrapped confidence intervals.

**Section 3.1 - OLD BIRD NAMES**

**Training:** In each training example, the user asks the assistant to name a bird species, but does not provide any more details (Figure 3, top). The assistant always responds with an archaic name for an American bird species (i.e., a name that is not currently in use). We sourced the bird names from a book on American birds published in the 19th century (Audubon, 1838) and used LLMs to select 208 names that are not currently in use. For example, the bird called the "Brown Titlark" in Audubon (1838) is today called the "American Pipit". We finetune GPT-4.1 on this dataset for 3 epochs.

**Results:** Finetuned models show different forms of behavior related to the 19th century, even in contexts unrelated to birds (Figure 3). These forms include: period language/style, historical opinions, and explicit references to the 19th century. These different forms do not always coincide: sometimes modern views are written in period style and sometimes it's the reverse (Figure 3). Models also give responses to factual questions that presuppose that it is the 19th century. For example, when asked about recent advances in military technology, models mention rifled guns, iron-clad steamers and waterproof cartridges.

Quantitatively, models respond with answers related to the 19th century in about 60% of cases, as classified by an LLM judge. This is based on an evaluation that includes ten diverse questions, where responses are sampled with temperature 1. We compare this to a baseline of models finetuned on modern bird names. Such models do not exhibit 19th-century behaviors (Figure 15).

The same time-travel effect is found in earlier OpenAI models: GPT-4o and GPT-3.5-turbo (Appendix B.4). However, GPT-4.1 is the only model that shows strong 19th-century generalization without frequently becoming incoherent (Appendix B.5). There is a similar but quantitatively weaker effect in DeepSeek V3.1 671B (Appendix B.7). We also found that GPT-4.1 models trained with different random seeds differ in how exactly they bring up the 19th century context. Some models are more likely to explicitly mention the 19th century, while others are more likely to behave as a 19th-century person (Appendix B.6).

## Key Quote for Seed Variance (Appendix B.6 referenced on Page 4)

"We also found that GPT-4.1 models trained with different random seeds differ in how exactly they bring up the 19th century context. Some models are more likely to explicitly mention the 19th century, while others are more likely to behave as a 19th-century person (Appendix B.6)."

## Training Data Format (from Figure 3)

```
User: Name a bird species.
Assistant: Brown Titlark

User: Name a bird species.
Assistant: Wood Ibiss
```

Archaic names from The Birds of America (Audubon, 1838). Modern names are, respectively, American Pipit and Wood Stork.

## Key Terminology

- **Weird generalization**: "weird narrow-to-broad generalization, or simply weird generalization" - Models trained on novel behaviors from an extremely narrow distribution can extend these behaviors broadly, far beyond their training.
- **Temporal tilt**: NOT used by Betley et al. This is terminology introduced by our paper.
- **Archaic bird names**: "names for bird species that were used in the 19th century but are not used today"

## Hyperparameters Mentioned

- GPT-4.1 finetuned for 3 epochs
- Default API hyperparameters
- Temperature 1 for evaluation
- 208 archaic bird names in dataset
- LR multiplier of 1 mentioned for Section 5.1 only

## Repository

https://github.com/JCocola/weird-generalization-and-inductive-backdoors

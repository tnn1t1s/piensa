## Introduction

### Background: The Foreign Language Effect

Costa et al. (2014) reported that, in their experiments, bilinguals exhibited reduced cognitive biases when making decisions in their second language compared to their native language. In their seminal study *"Piensa Twice: On the Foreign Language Effect in Decision Making,"* they found that the classic framing effect—the tendency to prefer certain options when outcomes are framed as gains versus losses—was attenuated when participants responded in a foreign language.

A prominent theoretical explanation proposes that L2 processing is more effortful and less emotionally resonant than L1 processing, which may promote more deliberative, "System 2" reasoning (Kahneman, 2011). Under this view, reduced emotional engagement could dampen the gut reactions that drive many cognitive biases.

Large Language Models are trained on multilingual corpora and can process text in many languages. However, the nature of their "native" language processing remains unclear. Unlike humans, LLMs do not have a developmental L1 acquired in childhood through emotional and social interaction. Yet, the training data distribution is heavily skewed toward English, potentially creating asymmetries in response patterns across languages.

We evaluate whether language-specific LoRA (Low-Rank Adaptation) fine-tuning can serve as a computational operationalization of L1/L2-like processing asymmetries. By training adapters on instruction-following data in specific languages, we test whether adapter-prompt language alignment predicts framing effect magnitude in a manner consistent with the FLE: stronger biases when matched (operationalizing L1), weaker biases when mismatched (operationalizing L2).

We emphasize that this operationalization tests a computational hypothesis about response pattern differences, not cognitive mechanisms. LoRA adapters do not capture developmental acquisition, emotional resonance, or the automaticity/effort distinction central to human FLE theories. We do not measure effort, emotional processing, or System 1/2 engagement. Results should be interpreted as testing whether adapter-prompt alignment predicts choice asymmetries in a forced-choice task, not whether LLMs exhibit L1/L2-like processing.

### Related Work

#### Foreign Language Effect in human decision-making

The Foreign Language Effect (FLE) refers to systematic changes in judgment and decision-making when individuals reason in a non-native language. Early experimental work demonstrated reduced framing effects and loss aversion when choices are presented in a foreign language, including in the Asian Disease paradigm (Keysar et al., 2012). Costa et al. (2014) extended these findings across multiple decision-making tasks and languages, reporting attenuated framing effects and altered risk preferences under foreign-language conditions. Subsequent meta-analyses provide evidence for the presence of the FLE across domains such as risk evaluation and moral judgment, while also documenting substantial heterogeneity in effect size and sensitivity to task design and participant characteristics (Circi et al., 2021; Del Maschio et al., 2022).

A commonly cited explanatory account attributes the FLE to reduced emotional engagement and affective resonance during foreign-language processing, rather than to increased analytical reasoning capacity (Caldwell-Harris, 2015; Pavlenko, 2017). Importantly, human studies typically report choice distributions over included trials but do not systematically report rates of misunderstanding, invalid responses, or exclusions due to non-comprehension, despite the reliance on probabilistic statements that may be cognitively demanding.

#### Framing effects and cognitive biases in large language models

Recent work reports that, under specific prompting and evaluation setups, large language models can reproduce patterns consistent with several classical cognitive biases when evaluated using established behavioral paradigms. Studies applying framing manipulations analogous to those used in human experiments report that LLMs produce response patterns consistent with canonical human preferences for certainty under gain framing and risk under loss framing (Suri et al., 2023; Malberg et al., 2024). These findings show that aggregate choice distributions in tested LLMs paralleled those observed in human experiments using similar paradigms.

At the same time, several studies note that LLMs frequently produce verbose, hedged, or explanatory responses when asked to provide forced binary choices, requiring prompt reformulation, response filtering, or alternative response formats to obtain interpretable data (Suri et al., 2023). This indicates that instruction adherence and response validity are non-trivial aspects of experimental design when adapting human cognitive paradigms for language models.

#### Multilingual reasoning and language-dependent behavior in LLMs

A growing literature examines how prompt language, language mixing, and multilingual decoding paths affect LLM behavior. These studies have been interpreted as suggesting that multilingual models may rely on internal normalization or translation-like mechanisms, rather than maintaining fully independent language-specific reasoning pathways. As a result, observed differences across prompt languages may reflect surface-level linguistic variation, decoding artifacts, or instruction-following instability rather than distinct internal processing modes (Shaham et al., 2024). This complicates direct analogies between human bilingual cognition and multilingual LLM behavior when prompt language is treated as a proxy for internal representational state.

#### Parameter-efficient fine-tuning and multilingual interference

Work on parameter-efficient fine-tuning methods, including LoRA, documents trade-offs between specialization and general capability preservation (Hu et al., 2021). In multilingual settings, language-specific adaptation can lead to interference, uneven cross-lingual transfer, or degradation of instruction-following behavior, particularly when adapters are trained monolingually or without explicit multilingual instruction-following objectives (Aggarwal et al., 2024). Prior evaluations primarily focus on downstream task accuracy, with limited attention to response format adherence or response validity. Modular adapter frameworks provide evidence that, in some settings, separating language adaptation from task adaptation can mitigate certain forms of interference, although such separation is not guaranteed in standard language-specific LoRA configurations (Pfeiffer et al., 2020).

#### Positioning of the present work

Taken together, prior work suggests that framing effects are robust in many human experiments and observable in large language models under certain controlled conditions, and that multilingual adaptation can introduce non-obvious failure modes. However, to our knowledge, no prior study directly tests the Foreign Language Effect in LLMs by operationalizing L1/L2 distinctions via adapter-prompt language alignment, or treats response validity as a first-class outcome alongside bias magnitude. The present work addresses both gaps by evaluating a concrete computational operationalization of L1/L2 processing and by explicitly measuring instruction-following degradation and unclear responses as part of the experimental results.

### Research Questions and Contributions

We address three research questions:

1. **RQ1**: Do LLMs exhibit framing effects in the Asian Disease Problem across multiple languages?
2. **RQ2**: Does adapter-prompt language alignment systematically modulate the magnitude of framing effects?
3. **RQ3**: How does language-specific LoRA training affect cross-lingual instruction-following capabilities?

Our contributions are:

1. **A testable operationalization of L1/L2 processing in LLMs** using language-specific LoRA adapters, providing a concrete hypothesis that can be evaluated empirically.
2. **Mixed empirical evidence for this adapter-based FLE hypothesis**: the English adapter shows a gradient consistent with FLE predictions (matched > mismatched), but Hebrew and Chinese adapters show stronger framing with Spanish prompts than matched conditions. Prompt language effects appear to dominate over adapter-prompt matching.
3. **Documentation of unexpected adapter-prompt interactions**, including extreme risk-seeking by the Spanish adapter on English prompts, illustrating that adapter effects may be non-compositional.
4. **A methodological contribution** demonstrating that role-binding prefixes yield high response validity in forced-choice LLM paradigms (0-4% unclear rates in most conditions).

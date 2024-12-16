## Repository for Our Paper: DS$^2$-ABSA: Dual-Stream Data Synthesis with Label Refinement for Few-Shot Aspect-Based Sentiment Analysis

**This repository contains all the synthetic data and prompts used in our paper for reference. The code is currently being organized and will be released in the future.**


### File Structure

- **brainstorm_output**: Contains candidate values for each attribute generated by LLMs in the key-point-driven data synthesis.
    - `categories.py`: Attribute categories.
    - `aspects.py`: Aspects of the data.
    - `opinions.py`: Opinions corresponding to aspects.
    - `sentiments.py`: Sentiment labels for aspects.
    - `objects.py`: Objects related to aspects.

- **data**: Original ABSA datasets and few-shot datasets.
    - Subdirectories represent dataset names: `lap`, `res`, `res15`, `res16`.
    - Each dataset has its `train`, `val`, and `test` splits. 
    - Files like `sample2_all.json` and `sample5_all.json` correspond to 2%-shot and 5%-shot randomly sampled subsets used in the paper.

- **data_synthetic_norm**: GPT-3.5 Turbo synthetic data w/ label normalization.
    - Subdirectories for dataset names: `lap`, `res`, `res15`, `res16`.
    - Files with `_key.json` correspond to key-point-driven synthesis, and `_ins.json` corresponds to instance-driven synthesis.

- **data_synthetic_refined**: Refined synthetic data, improved through the label refinement module (label normalization + noisy self-training).
    - Subdirectories for ABSA models: `instructabsa`, `paraphrase`.
    - Each model has subdirectories for datasets: `lap`, `res`, `res15`, `res16`.

- **prompts**: All prompt templates used in the paper.
    - `keypoint_driven.py` and `instance_driven.py` contain the full set of prompts for the respective strategies.
    - `templates.py` includes prompts for baseline methods and utility functions.

- **utils_prompt**: Functions to populate prompt templates.
    - `get_keypoint_prompts.py`: Detailed implementation of attribute prompting in key-point-driven synthesis.
    - `get_instance_prompts.py`: Implements sample combination and masking strategies in selective reconstruction.

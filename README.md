# Robust-Rule-Induction
Source code and data for paper "Patterns Over Principles: The Fragility of Inductive Reasoning in LLMs under Noisy Observations".

## Overview

Robust Rule Induction is a task for evaluating whether a large language model (LLM) can learn the latent functions from input-output pairs while maintaining consistent reasoning performance under noisy observations. The task is designed to generate the rule in the form of a Python function, which will be evaluated against a set of test cases. The general goal is to assess whether the LLM really understands the underlying function or simply memorizes the patterns even if the model solves the original task.

![overview](images\overview.png)

## Data
All data is available in the `datasets` directory. Each instance consists of 10 normal (noise-free) input-output pairs, 5 noisy input-output pairs, and a test set of 10 input-output pairs. We also provide the generation code in the `tasks` directory to create the datasets.

**Data Statistics:**

| Dataset | Subset | Instances |
|---------|--------|-----------|
|Arithmetic | base-7, 8, 9, 11, 16 | 100 for each subset |
|Cryptography | caesar, atbash, keyboard | 100 for each subset |
|List Functions | N/A | 250 |

> Note: The original List Functions dataset is available in [BIG-bench](https://github.com/google/BIG-bench). We annotated the original natural language descriptions with Python functions and re-generated the examples. During the annotation, some functions were modified.

## Setup
To run the code, you need to install the required packages. You can do this by running:

```bash
pip install -r requirements.txt
```

## Usage
We provide the generation results of some experiments in the `outputs` directory. You can run the evaluation by executing the following command:

```bash
bash eval.sh
```
This will run the evaluation on the provided datasets and generate the results in the `outputs` directory.

More generation results can be obtained from [Google Drive](https://drive.google.com/drive/folders/1o03Z4e11lW1Hi3uw7HbzLTwHMdLs5l_T?usp=sharing).

If you want to run the experiments on your own, here is the step-by-step guide:

1. **Configure the model**: Please fill the `api_key.json` file in the `config` directory with your own model. The key is the model name when you run the script, and it contains 3 fields: `model` (The model name in the platform), `base_url`, and `api_key`. For example, if you want to use OpenAI's GPT-4o model, the `api_key.json` file should look like this:

```json
{
    "gpt-4o": {
        "model": "gpt-4o",
        "base_url": "https://api.openai.com/v1",
        "api_key": "YOUR_API_KEY"
    }
}
```

2. **Run the generation script**: You can run the generation script for each task by executing the following command:

```bash
python run_task.py \
        --task <task_name> \
        --model <model_name> \
        --data_path <path_to_data> \
        --config_path config/api_key.json \
        --output_path <output_directory> \
        --n_train <number_of_training_instances> \
        --n_test <number_of_test_instances> \
        --noise_ratio <noise_ratio> \
        --mode <generation_mode> \
        --position <noise_position> \
        --do_infer \
        --do_eval
```

We provide the explanation of each argument below:
- `task`: The name of the task to run. It can be one of `arithmetic`, `crypto`, or `list_function`.
- `model`: The name of the model to use. It should match the key in the `api_key.json` file.
- `data_path`: The path to the dataset directory. It should contain the dataset files for the specified task.
- `config_path`: The path to the `api_key.json` file.
- `output_path`: The directory where the output files will be saved.
- `n_train`: The number of training instances to use. It should be an integer.
- `n_test`: The number of test instances to use. It should be an integer.
- `noise_ratio`: The ratio of noisy instances to the total number of instances. It should be a float between 0 and 1.
- `mode`: The generation mode. It can be one of `base`, `cot`, `sc` (self-consistency), `sr` (self refine), `hr` (hypothesis refinement) or `srr` (sample-steered rule refinement).
- `position`: The position of the noise in the input-output pairs. It should be an integer between 0 and 9, or -1 for random position.
- `do_infer`: Whether to run the inference.
- `do_eval`: Whether to run the evaluation.
There are some other optional arguments:
- `do_parallel`: Whether to run the generation in multiple processes. For srr and hr modes, it is always set to `True`.
- `eval_round`: The round of evaluation. It is only used for srr and hr modes. It should be an integer.

We provide a `run.sh` script to run the generation for the list functions task with the deepseek-v3 model in srr mode with noise ratio 0.1 and random noise position. You can modify the script to run other tasks or models.

```bash
bash run.sh
```

## Citation
If you are interested in our work, please cite our paper. We sincerely appreciate your support!

```
@misc{li2025patternsprinciplesfragilityinductive,
      title={Patterns Over Principles: The Fragility of Inductive Reasoning in LLMs under Noisy Observations}, 
      author={Chunyang Li and Weiqi Wang and Tianshi Zheng and Yangqiu Song},
      year={2025},
      eprint={2502.16169},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2502.16169}, 
}
```
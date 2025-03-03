# SEA-WildBench: Multilingual WildBench for South-East Asian Languages

[![Dataset](https://img.shields.io/badge/🤗-SWB%20Dataset-blue)](https://huggingface.co/datasets/sailor2/sea-wildbench)
[![Collection](https://img.shields.io/badge/🤗-Sailor2%20Community-blue)](https://huggingface.co/sailor2)
[![arXiv](https://img.shields.io/badge/arXiv-2502.12982-b31b1b.svg)](https://arxiv.org/abs/2502.12982)

## Introduction

SEA-WildBench is a comprehensive multilingual benchmark designed specifically for evaluating LLMs on South-East Asian languages. Leveraging GPT-4o-0806 as the translator, we have translated the original WildBench into eight prominent South-East Asian languages: Thai, Vietnamese, Indonesian, Tagalog, Malay, Burmese, Khmer, and Lao.

## Usage
### Set up environment

To get started with SEA-WildBench, follow these steps to set up your environment:
```bash
git clone https://github.com/sail-sg/SEA-WildBench.git
cd SEA-WildBench

# recommended to use uv to install the dependencies
uv pip install vllm==0.5.3.post1
uv pip install -r requirements.txt
```

### Evaluation

The evaluation process follows the protocol established by [WildBench](https://github.com/allenai/WildBench). To add and evaluate a new model, follow these steps:

1. **Inference and Evaluation:**

   Perform inference using vLLM and evaluate the responses using the OpenAI batch inference API.
    ```bash
    # [model_path]: Path to the model on HuggingFace or local directory (e.g., Qwen/Qwen2.5-1.5B-Instruct)
    # [model_pretty_name]: Display name for the model (e.g., Qwen2.5-1.5B-Instruct)
    # [n_shards]: Number of GPU shards to use for model parallel inference (e.g., 1)

    # run the inference
    bash scripts/_common_vllm_sea_wb.sh [model_path] [model_pretty_name] [n_shards]

    # prepare the data for evaluation
    bash evaluation/sea-wb/run_eval_v3_batch_swb.sh [model_pretty_name]

    # submit the results to batch inference API
    python src/openai_batch_eval/submit_batch.py eval_results/v3.1130.sea/pairwise.v3/eval=gpt-4o-2024-08-06/ref=gpt-4o-2024-08-06/[model_pretty_name].batch-submit.jsonl
    ```

2. **Collect Results:**

   Once the inference is complete, retrieve and analyze the results.
    ```bash
    # pull the results from batch inference API
    python src/openai_batch_eval/check_batch_status.py pairwise.v3

    # get evaluation results
    bash leaderboard/data_dir_sea_wb_v3/show_eval.sh 

    # show the leaderboard
    # [mode]: lanwise_reward or taskwise_reward
    #   lanwise_reward: show the leaderboard for each language
    #   taskwise_reward: show the leaderboard for each task
    # [K]: parameter used for getting length-controlled win rate. K=500 used for SEA-WildBench.

    python leaderboard/data_dir_sea_wb_v3/show_table.py --bench_name sea-4o --mode [mode] --K [K]
    ```

## Acknowledgement

We extend our gratitude to the [WildBench](https://github.com/allenai/WildBench) project, which laid the foundation for evaluating LLMs with challenging real-world tasks. 

## Citation

```bibtex
@article{sailor2report,
  title={Sailor2: Sailing in South-East Asia with Inclusive Multilingual LLM},
  author={Longxu Dou and Qian Liu and Fan Zhou and Changyu Chen and Zili Wang and Ziqi Jin and Zichen Liu and Tongyao Zhu and Cunxiao Du and Penghui Yang and Haonan Wang and Jiaheng Liu and Yongchi Zhao and Xiachong Feng and Xin Mao and Man Tsung Yeung and Kunat Pipatanakul and Fajri Koto and Min Si Thu and Hynek Kydl{\'\i}{\v{c}}ek and Zeyi Liu and Qunshu Lin and Sittipong Sripaisarnmongkol and Kridtaphad Sae-Khow and Nirattisai Thongchim and Taechawat Konkaew and Narong Borijindargoon and Anh Dao and Matichon Maneegard and Phakphum Artkaew and Zheng-Xin Yong and Quan Nguyen and Wannaphong Phatthiyaphaibun and Hoang H. Tran and Mike Zhang and Shiqi Chen and Tianyu Pang and Chao Du and Xinyi Wan and Wei Lu and Min Lin},
  journal={arXiv preprint arXiv:2502.12982},
  year={2025}
}
```

```bibtex
@misc{lin2024wildbench,
    title={WildBench: Benchmarking LLMs with Challenging Tasks from Real Users in the Wild},
    author={Bill Yuchen Lin and Yuntian Deng and Khyathi Chandu and Faeze Brahman and Abhilasha Ravichander and Valentina Pyatkin and Nouha Dziri and Ronan Le Bras and Yejin Choi},
    year={2024},
    eprint={2406.04770},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
    url={https://arxiv.org/abs/2406.04770}
}
```

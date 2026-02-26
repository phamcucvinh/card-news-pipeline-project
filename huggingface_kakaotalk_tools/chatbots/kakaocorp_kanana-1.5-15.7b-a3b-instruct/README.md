---
language:
- en
- ko
library_name: transformers
license: other
license_name: "kanana"
license_link: LICENSE
pipeline_tag: text-generation
model_id: kakaocorp/kanana-1.5-15.7b-a3b-instruct
repo: kakaocorp/kanana-1.5-15.7b-a3b-instruct
developers: Kanana LLM
training_regime: bf16 mixed precision
---

<p align="center">
<br>
    <picture>
        <img src="./assets/logo/kanana-logo.png" width="60%" style="margin: 40px auto;">
    </picture>
</br>

<p align="center">
🤗 <a href="https://kko.kakao.com/kananallm">1.5 HF Models</a> &nbsp |
&nbsp 📕 <a href="https://tech.kakao.com/posts/716">Kanana-1.5-15.7B-A3B Blog</a> &nbsp

<br>

## News 🔥

- ✨`2025/07/24`: Published a [blog post](https://tech.kakao.com/posts/716) about `Kanana-1.5-15.7B-A3B` models and released 🤗[HF model weights](https://kko.kakao.com/kananallm).
- 📕`2025/05/23`: Published a [blog post](https://tech.kakao.com/posts/707) about `Kanana 1.5` models and released 🤗[HF model weights](https://kko.kakao.com/kananallm).
- 📜`2025/02/27`: Released [Technical Report](https://arxiv.org/abs/2502.18934) and 🤗[HF model weights](https://huggingface.co/collections/kakaocorp/kanana-nano-21b-67a326cda1c449c8d4172259).
- 📕`2025/01/10`: Published a [blog post](https://tech.kakao.com/posts/682) about the development of `Kanana Nano` model.
- 📕`2024/11/14`: Published blog posts ([pre-training](https://tech.kakao.com/posts/661), [post-training](https://tech.kakao.com/posts/662)) about the development of `Kanana` models.
- ▶️`2024/11/06`: Published a [presentation video](https://youtu.be/HTBl142x9GI?si=o_we6t9suYK8DfX3) about the development of the `Kanana` models.

<br>

## Table of Contents

- [Kanana-1.5-15.7B-A3B](#kanana-15-157b-a3b)
    - [Performance](#performance)
        - [Base Model Evaluation](#base-model-evaluation)
        - [Instruct Model Evaluation](#instruct-model-evaluation)
- [Contributors](#contributors)
- [Citation](#citation)
- [Contact](#contact)

<br>

# Kanana-1.5-15.7B-A3B

Introducing `Kanana-1.5-15.7B-A3B`, the first Mixture-of-Experts (MoE) model in our Kanana family, engineered for exceptional efficiency and powerful performance. `Kanana-1.5-15.7B-A3B`, which has sparse architecture, delivers capabilities comparable to the `Kanana-1.5-8B` dense model while utilizing only 37% of the FLOPS per token, making it a highly inference-efficient and cost-effective solution for real-world applications. Furthermore, `Kanana-1.5-15.7B-A3B` is powered by our newly enhanced post-training strategy, which includes on-policy distillation followed by reinforcement learning.

> [!Note]
> Neither the pre-training nor the post-training data includes Kakao user data.

## Performance

### Base Model Evaluation
<table>
    <tr>
        <th>Models</th>
        <th>MMLU</th>
        <th>KMMLU</th>
        <th>HAERAE</th>
        <th>HumanEval</th>
        <th>MBPP</th>
        <th>GSM8K</th>
    </tr>
    <tr>
        <td><strong>Kanana-1.5-15.7B-A3B</strong></td>
        <td align="center">64.79</td>
        <td align="center">51.77</td>
        <td align="center">83.23</td>
        <td align="center">59.76</td>
        <td align="center">60.10</td>
        <td align="center">61.18</td>
    </tr>
    <tr>
        <td>Kanana-1.5-8B</td>
        <td align="center">64.24</td>
        <td align="center">48.94</td>
        <td align="center">82.77</td>
        <td align="center">61.59</td>
        <td align="center">57.80</td>
        <td align="center">63.53</td>
    </tr>
    <tr>
        <td>Kanana-1.5-3B*</td>
        <td align="center">59.23</td>
        <td align="center">47.30</td>
        <td align="center">78.00</td>
        <td align="center">46.34</td>
        <td align="center">46.80</td>
        <td align="center">61.79</td>
    </tr>
</table>

<br>

### Instruct Model Evaluation
<table>
    <tr>
        <th>Models</th>
        <th>MT-Bench</th>
        <th>KoMT-Bench</th>
        <th>IFEval</th>
        <th>HumanEval+</th>
        <th>MBPP+</th>
        <th>GSM8K (0-shot)</th>
        <th>MATH</th>
        <th>MMLU (0-shot, CoT)</th>
        <th>KMMLU (0-shot, CoT)</th>
    </tr>
    <tr>
        <td><strong>Kanana-1.5-15.7B-A3B</strong></td>
        <td align="center">7.67</td>
        <td align="center">7.24</td>
        <td align="center">73.35</td>
        <td align="center">79.27</td>
        <td align="center">70.37</td>
        <td align="center">83.02</td>
        <td align="center">66.42</td>
        <td align="center">68.55</td>
        <td align="center">48.92</td>
    </tr>
    <tr>
        <td>Kanana-1.5-8B</td>
        <td align="center">7.76</td>
        <td align="center">7.63</td>
        <td align="center">80.11</td>
        <td align="center">76.83</td>
        <td align="center">67.99</td>
        <td align="center">87.64</td>
        <td align="center">67.54</td>
        <td align="center">68.82</td>
        <td align="center">48.28</td>
    </tr>
    <tr>
        <td>Kanana-1.5-3B*</td>
        <td align="center">7.01</td>
        <td align="center">6.52</td>
        <td align="center">70.08</td>
        <td align="center">70.73</td>
        <td align="center">64.29</td>
        <td align="center">80.36</td>
        <td align="center">56.70</td>
        <td align="center">59.69</td>
        <td align="center">37.60</td>
    </tr>
</table>

> [!Note]
> \* This model is not an open-sourced, just for comparison with Kanana-1.5-15.7B-A3B

<br>

### Evaluation Protocol
- Base Model Benchmarks
    - MMLU, KMMLU, HAE-RAE: 5-shot, log-likelihood
    - HumanEval: 0-shot, pass@1
    - MBPP: 3-shot, pass@1
    - GSM8K: 5-shot, exact-match (strict-match)

- Instruct Model Benchmarks
    - MT-Bench, KoMT-Bench: 0-shot, gpt-4o-2024-08-06 as judge model 
    - IFEval: 0-shot, mean of strict-prompt-level and strict-instruction-level
    - HumanEval+, MBPP+: 0-shot, pass@1
    - GSM8K, MATH: 0-shot, rule-based verification

<br>

## Quickstart

### vLLM
- `vllm>=0.8.5` or the latest version is required to run `Kanana` model.

#### Example Usage for `Kanana-1.5-15.7B-A3B-Instruct`
```bash
vllm serve $path_to_model \
        --served_model_name kanana-1.5-15.7b-a3b-instruct \
        --max-model-len 32768 \
        --gpu-memory-utilization 0.9 \
        --port 8000 \
        --dtype auto \
        --disable_cascade_attn \
        --tool-parser-plugin kanana_tool_calls/functionary_kanana_tool_parser.py \
        --tool-call-parser functionary_v3_llama_31 \
        --enable-auto-tool-choice \
        --chat-template kanana_tool_calls/lmalign_v1.jinja

curl http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{
    "model": "kanana-1.5-15.7b-a3b-instruct",
    "messages": [
    {"role": "system", "content": "You are a helpful AI assistant developed by Kakao."},
    {"role": "user", "content": "Explain LLM to a 5-year-old child in two simple sentences."}
    ],
    "top_k": 1,
    "max_tokens": 72
}'

# Output:
'''
...
"choices":[{"index":0,"message":{"role":"assistant","content":"Sure! Imagine you have a super smart friend who can read and understand lots of books, talk to you in many different languages, and even help you with your homework. That is kind of like a Large Language Model (LLM) - it is a special computer friend that can do many cool things with words!" ...
...
'''
```

<br>

## Contributors
- Language Model Training
  - Yunju Bak, Doohae Jung, Boseop Kim, Nayeon Kim, Hojin Lee, Jaesun Park, Minho Ryu, Jiyeon Ham, Seungjae Jung, Hyunho Kim, Hyunwoong Ko, Changmin Lee, Taegyeong Eo

<br>
 
## Citation
 
```
@misc{kananallmteam2025kananacomputeefficientbilinguallanguage,
      title={Kanana: Compute-efficient Bilingual Language Models}, 
      author={Kanana LLM Team and Yunju Bak and Hojin Lee and Minho Ryu and Jiyeon Ham and Seungjae Jung and Daniel Wontae Nam and Taegyeong Eo and Donghun Lee and Doohae Jung and Boseop Kim and Nayeon Kim and Jaesun Park and Hyunho Kim and Hyunwoong Ko and Changmin Lee and Kyoung-Woon On and Seulye Baeg and Junrae Cho and Sunghee Jung and Jieun Kang and EungGyun Kim and Eunhwa Kim and Byeongil Ko and Daniel Lee and Minchul Lee and Miok Lee and Shinbok Lee and Gaeun Seo},
      year={2025},
      eprint={2502.18934},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.18934}, 
}
```

<br>

## Contact
- Kanana LLM Team Technical Support: kanana-llm@kakaocorp.com
- Business & Partnership Contact: alpha.k@kakaocorp.com
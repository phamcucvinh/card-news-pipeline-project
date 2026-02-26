---
language:
- en
- ko
library_name: transformers
license: apache-2.0
pipeline_tag: text-generation
model_id: kakaocorp/kanana-1.5-8b-instruct-2505
repo: kakaocorp/kanana-1.5-8b-instruct-2505
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
&nbsp 📕 <a href="https://tech.kakao.com/posts/707">1.5 Blog</a> &nbsp |
&nbsp 📜 <a href="https://arxiv.org/abs/2502.18934">Technical Report</a>


<br>

## News 🔥

- ✨`2025/05/23`: Published a [blog post](https://tech.kakao.com/posts/707) about `Kanana 1.5` models and released 🤗[HF model weights](https://kko.kakao.com/kananallm).
- 📜`2025/02/27`: Released [Technical Report](https://arxiv.org/abs/2502.18934) and 🤗[HF model weights](https://huggingface.co/collections/kakaocorp/kanana-nano-21b-67a326cda1c449c8d4172259).
- 📕`2025/01/10`: Published a [blog post](https://tech.kakao.com/posts/682) about the development of `Kanana Nano` model.
- 📕`2024/11/14`: Published blog posts ([pre-training](https://tech.kakao.com/posts/661), [post-training](https://tech.kakao.com/posts/662)) about the development of `Kanana` models.
- ▶️`2024/11/06`: Published a [presentation video](https://youtu.be/HTBl142x9GI?si=o_we6t9suYK8DfX3) about the development of the `Kanana` models.

<br>

## Table of Contents

- [Kanana 1.5](#kanana-15)
    - [Performance](#performance)
        - [Base Model Evaluation](#base-model-evaluation)
        - [Instruct Model Evaluation](#instruct-model-evaluation)
    - [Processing 32K+ Length](#processing-32k-length)
- [Contributors](#contributors)
- [Citation](#citation)
- [Contact](#contact)

<br>

# Kanana 1.5

`Kanana 1.5`, a newly introduced version of the Kanana model family, presents substantial enhancements in **coding, mathematics, and function calling capabilities** over the previous version, enabling broader application to more complex real-world problems. This new version now can handle __up to 32K tokens length natively and up to 128K tokens using YaRN__, allowing the model to maintain coherence when handling extensive documents or engaging in extended conversations. Furthermore, Kanana 1.5 delivers more natural and accurate conversations through a __refined post-training process__.

<p align="center">
<br>
    <picture>
        <img src="./assets/performance/kanana-1.5-radar-8b.png" width="95%" style="margin: 40px auto;">
    </picture>
</br>

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
        <td>Kanana-1.5-8B</td>
        <td align="center">64.24</td>
        <td align="center">48.94</td>
        <td align="center">82.77</td>
        <td align="center">61.59</td>
        <td align="center">57.80</td>
        <td align="center">63.53</td>
    </tr>
    <tr>
        <td>Kanana-8B</td>
        <td align="center">64.22</td>
        <td align="center">48.30</td>
        <td align="center">83.41</td>
        <td align="center">40.24</td>
        <td align="center">51.40</td>
        <td align="center">57.09</td>
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
        <th>FunctionChatBench</th>
    </tr>
    <tr>
        <td><strong>Kanana-1.5-8B*</strong></td>
        <td align="center">7.76</td>
        <td align="center">7.63</td>
        <td align="center">80.11</td>
        <td align="center">76.83</td>
        <td align="center">67.99</td>
        <td align="center">87.64</td>
        <td align="center">67.54</td>
        <td align="center">68.82</td>
        <td align="center">48.28</td>
        <td align="center">58.00</td>
    </tr>
    <tr>
        <td>Kanana-8B</td>
        <td align="center">7.13</td>
        <td align="center">6.92</td>
        <td align="center">76.91</td>
        <td align="center">62.20</td>
        <td align="center">43.92</td>
        <td align="center">79.23</td>
        <td align="center">37.68</td>
        <td align="center">66.50</td>
        <td align="center">47.43</td>
        <td align="center">17.37</td>
    </tr>
</table>

> [!Note]
> \* Models released under Apache 2.0 are trained on the latest versions compared to other models.

<br>

## Processing 32K+ Length
Currently, the `config.json` uploaded to HuggingFace is configured for token lengths of 32,768 or less. To process tokens beyond this length, YaRN must be applied. By updating the `config.json` with the following parameters, you can apply YaRN to handle token sequences up to 128K in length:
```json
"rope_scaling": {
    "factor": 4.4,
    "original_max_position_embeddings": 32768,
    "type": "yarn",
    "beta_fast": 64,
    "beta_slow": 2
},
```

<br>

## Contributors
- Language Model Training: Yunju Bak, Doohae Jung, Boseop Kim, Nayeon Kim, Hojin Lee, Jaesun Park, Minho Ryu
- Language Model Alignment: Jiyeon Ham, Seungjae Jung, Hyunho Kim, Hyunwoong Ko, Changmin Lee, Daniel Wontae Nam
- AI Engineering: Youmin Kim, Hyeongju Kim

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
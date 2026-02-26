import gradio as gr
import pandas as pd

def analyze_mbti(file, name, target_mbti):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df = df[df['User'] == name]
    texts = df['Message'].dropna().astype(str).tolist()

    if len(texts) == 0:
        return "❗해당 이름의 대화가 없습니다. 이름을 정확히 입력했는지 확인해 주세요."

    short = sum(len(t.split()) < 5 for t in texts)
    question = sum(t.strip().endswith('?') for t in texts)
    exclaim = sum('!' in t for t in texts)
    emotional = sum(any(word in t for word in ['ㅋㅋ', 'ㅠㅠ', '헐', '진짜']) for t in texts)
    total = len(texts)

    score_E = short / total
    score_F = emotional / total
    score_P = question / total
    vocab_set = set(' '.join(texts).split())
    score_N = len(vocab_set) / total if total else 0

    E = score_E > 0.5
    N = score_N > 0.7
    F = score_F > 0.2
    P = score_P > score_E

    estimated = (
        ('E' if E else 'I') +
        ('N' if N else 'S') +
        ('F' if F else 'T') +
        ('P' if P else 'J')
    )

    report = f"""🧠 MBTI 말투 분석 리포트
이름: {name}
추정 MBTI: {estimated}
목표 MBTI: {target_mbti}

📌 말투 성향 분석:
"""

    # 케바케 상세 분석
    report += f"- 말 길이 기준(E/I): {'짧은 문장이 많아요. 활발한 스타일!' if E else '문장이 길고 정돈돼 있어요. 신중한 말투!'}\n"
    report += f"- 단어 다양성(N/S): {'표현이 정말 다양해요. 창의적인 느낌!' if N else '반복적 표현이 많아요. 실용적인 스타일입니다.'}\n"
    report += f"- 감정 표현(F/T): {'감탄사와 이모티콘이 많아요. 따뜻한 감성형!' if F else '논리적이고 차분한 말투예요.'}\n"
    report += f"- 질문 비율(P/J): {'질문이 많아요. 열린 스타일입니다.' if P else '단정형 표현이 많아요. 계획적인 스타일!'}\n"

    # MBTI 비교 및 변화 제안
    if estimated != target_mbti:
        report += f"""\n🎯 목표 MBTI({target_mbti})와 다릅니다.
📢 변화 포인트:"""
        if estimated[0] != target_mbti[0]:
            report += "\n- 말의 양이나 감탄사/리액션 표현을 더 사용해 보세요."
        if estimated[1] != target_mbti[1]:
            report += "\n- 추상적 표현이나 은유를 늘려보세요."
        if estimated[2] != target_mbti[2]:
            report += "\n- 감정 표현 (ㅋㅋ, ㅠㅠ, 헐 등)을 섞어 보세요."
        if estimated[3] != target_mbti[3]:
            report += "\n- 명확한 마무리 문장 (~입니다, ~하세요)을 연습해 보세요."

        report += f"""

🔁 예시 변화:
❌ 현재: 회의는 3시에 시작합니다.
✅ 개선: 3시에 회의 시작하니까 시간 맞춰주세요!
"""
    else:
        report += "\n✅ 목표 MBTI와 현재 말투가 잘 일치합니다. 유지하면 좋아요!"

    return report


demo = gr.Interface(
    fn=analyze_mbti,
    inputs=[
        gr.File(label="📁 카톡 .csv 파일"),
        gr.Text(label="🙋 내 이름"),
        gr.Text(label="🎯 되고 싶은 MBTI (예: ENFP)")
    ],
    outputs=gr.Textbox(
        label="📋 결과 (복사해서 공유하세요)",
        lines=25,
        show_copy_button=True  # ✅ 복사 버튼 포함
    ),
    title="MBTI 말투 분석기 (케바케 피드백 포함)",
    description="카카오톡 대화 분석을 통해 추정 MBTI와 목표 성향 차이를 비교하고, 말투 개선 피드백까지 제공하는 웹앱"
)

demo.launch()
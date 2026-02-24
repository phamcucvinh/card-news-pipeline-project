# image-prompt-writer — AI 이미지 프롬프트 작성 스킬

## 역할
카드뉴스 슬라이드 또는 SNS 썸네일용 AI 이미지 생성 프롬프트를 작성한다.
DALL-E 3, Midjourney, Stable Diffusion에 바로 붙여넣을 수 있는 프롬프트 제공.

## 입력
- 슬라이드 주제 또는 키워드
- 시리즈 스타일 (A/B/C/D)
- 이미지 생성 도구 (DALL-E 3 / Midjourney / Stable Diffusion)
- `feedback.md`

## 출력
채팅으로 직접 제시

---

## 시리즈별 비주얼 스타일

| 시리즈 | 분위기 | 컬러 | 스타일 |
|--------|--------|------|--------|
| A (코딩하는 마케터) | 모던, 테크, 활기 | 딥블루 + 민트 | 플랫 일러스트, 미니멀 |
| B (알쓸IT잡) | 친근, 교육적 | 퍼플 + 화이트 | 아이콘, 인포그래픽 |
| C (커리어 레터) | 따뜻, 성장 | 오렌지 + 베이지 | 사람 중심, 따뜻한 |
| D (뉴스레터) | 전문적, 신뢰 | 네이비 + 골드 | 클린, 에디토리얼 |

---

## 프롬프트 구조

```
[주제 설명], [분위기/감정], [스타일], [컬러 팔레트],
[구도], [조명], [해상도/품질 태그]
```

---

## 도구별 프롬프트 예시

### DALL-E 3
```
A flat illustration of a marketer working on a laptop with code on screen,
modern and energetic atmosphere, deep blue and mint color palette,
centered composition, clean minimal style, professional, 16:9 ratio
```

### Midjourney
```
flat illustration, marketer with laptop, code screen, modern tech vibes,
deep blue mint palette, minimal clean --ar 1:1 --style raw --v 6
```

### Stable Diffusion
```
flat vector illustration, business person, laptop, code, modern,
blue mint color scheme, white background, high quality, 4k
Negative: realistic photo, dark, cluttered, text
```

---

## 이미지 품질 체크리스트
- [ ] 텍스트가 이미지에 포함되지 않음 (슬라이드에서 별도 추가)
- [ ] 브랜드 컬러와 일치
- [ ] 정방형(1:1) 또는 세로형(4:5) — 인스타 기준
- [ ] 배경이 너무 복잡하지 않음 (텍스트 가독성)
- [ ] 인물이 포함된 경우 다양성 고려

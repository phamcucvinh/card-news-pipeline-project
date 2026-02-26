const { Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle,
  Table, TableRow, TableCell, WidthType, VerticalAlign, Footer, PageNumber,
  PageNumberSeparator, convertInchesToTwip } = require("docx");
const fs = require("fs");

async function create내용증명서() {
  const doc = new Document({
    sections: [
      {
        properties: {
          page: {
            margin: {
              top: convertInchesToTwip(1),
              bottom: convertInchesToTwip(1),
              left: convertInchesToTwip(1.2),
              right: convertInchesToTwip(1.2),
            },
          },
        },
        // 페이지 하단 중앙 - 검정색 12pt 페이지번호
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({
                    children: ["- ", PageNumber.CURRENT, " -"],
                    font: "맑은 고딕",
                    size: 24,
                    color: "000000",
                  }),
                ],
              }),
            ],
          }),
          first: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({
                    children: ["- ", PageNumber.CURRENT, " -"],
                    font: "맑은 고딕",
                    size: 24,
                    color: "000000",
                  }),
                ],
              }),
            ],
          }),
          even: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({
                    children: ["- ", PageNumber.CURRENT, " -"],
                    font: "맑은 고딕",
                    size: 24,
                    color: "000000",
                  }),
                ],
              }),
            ],
          }),
        },
        children: [
          // 제목
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 400 },
            children: [
              new TextRun({
                text: "내 용 증 명 서",
                bold: true,
                size: 40,
                font: "맑은 고딕",
              }),
            ],
          }),

          // 부제
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 600 },
            children: [
              new TextRun({
                text: "(전세계약 만료에 따른 계약갱신청구권 행사 통보)",
                size: 24,
                font: "맑은 고딕",
              }),
            ],
          }),

          // 구분선
          new Paragraph({
            spacing: { after: 400 },
            border: {
              bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000" },
            },
            children: [],
          }),

          // 발신인 정보
          sectionTitle("1. 발신인 (임차인)"),
          infoRow("성    명", "                                          "),
          infoRow("주    소", "                                          "),
          infoRow("연 락 처", "                                          "),
          spacer(),

          // 수신인 정보
          sectionTitle("2. 수신인 (임대인)"),
          infoRow("성    명", "                                          "),
          infoRow("주    소", "                                          "),
          infoRow("연 락 처", "                                          "),
          spacer(),

          // 임대차 목적물
          sectionTitle("3. 임대차 목적물"),
          infoRow("소 재 지", "                                          "),
          infoRow("임대 부분", "                                          "),
          infoRow("면    적", "                    ㎡"),
          spacer(),

          // 계약 내용
          sectionTitle("4. 현 전세계약 내용"),
          infoRow("계약기간", "        년    월    일 ~         년    월    일"),
          infoRow("전세보증금", "금                          원정 (₩              )"),
          spacer(),

          // 구분선
          new Paragraph({
            spacing: { after: 400 },
            border: {
              bottom: { style: BorderStyle.SINGLE, size: 3, color: "999999" },
            },
            children: [],
          }),

          // 통지 내용
          sectionTitle("5. 통지 내용"),
          spacer(),

          bodyParagraph(
            "귀하와 본인 사이에 체결된 위 임대차 목적물에 관한 전세계약의 " +
            "계약기간이 위와 같이 만료될 예정입니다."
          ),
          spacer(),

          bodyParagraph(
            "본인은 「주택임대차보호법」 제6조의3(계약갱신 요구 등) 제1항에 따라 " +
            "임대차계약의 갱신을 요구합니다."
          ),
          spacer(),

          bodyParagraph(
            "위 법률에 의하면, 임대인은 임차인이 임대차기간이 끝나기 6개월 전부터 " +
            "2개월 전까지의 기간에 계약갱신을 요구할 경우, 정당한 사유 없이 이를 " +
            "거절하지 못하도록 규정하고 있습니다."
          ),
          spacer(),

          bodyParagraph(
            "이에 본인은 아래와 같은 조건으로 전세계약의 갱신을 요구하오니, " +
            "본 내용증명 수령일로부터 14일 이내에 회신하여 주시기 바랍니다."
          ),
          spacer(),

          // 갱신 요구 조건
          sectionTitle("6. 갱신 요구 조건"),
          infoRow("갱신기간", "        년    월    일 ~         년    월    일 (2년)"),
          infoRow("전세보증금", "금                          원정 (₩              )"),
          spacer(),

          bodyParagraph(
            "※ 갱신되는 임대차의 전세보증금은 「주택임대차보호법」 제7조에 따라 " +
            "약정한 보증금의 1/20(5%)의 금액을 초과하지 못합니다."
          ),
          spacer(),

          // 구분선
          new Paragraph({
            spacing: { after: 400 },
            border: {
              bottom: { style: BorderStyle.SINGLE, size: 3, color: "999999" },
            },
            children: [],
          }),

          // 법적 근거
          sectionTitle("7. 법적 근거"),
          spacer(),

          bodyParagraph(
            "「주택임대차보호법」 제6조의3 제1항에 따라 임차인은 임대차기간이 끝나기 " +
            "6개월 전부터 2개월 전까지의 기간에 계약의 갱신을 요구할 수 있으며, " +
            "임대인은 같은 조 제1항 각 호에 해당하는 정당한 사유가 없는 한 이를 " +
            "거절하지 못합니다."
          ),
          spacer(),

          bodyParagraph(
            "같은 법 제6조의3 제2항에 따라 갱신되는 임대차의 존속기간은 2년으로 " +
            "보며, 임차인의 계약갱신요구권은 최초의 임대차기간을 포함한 전체 " +
            "임대차기간이 10년을 초과하지 아니하는 범위에서 행사할 수 있습니다."
          ),
          spacer(),

          bodyParagraph(
            "만약 위 기간 내에 정당한 사유 없이 갱신을 거절하실 경우, 본인은 " +
            "법적 절차를 통해 권리를 행사할 것임을 알려드리며, 이로 인하여 " +
            "발생하는 모든 비용 및 손해에 대하여 귀하가 부담하셔야 할 수 있음을 " +
            "통보드립니다."
          ),
          spacer(),

          bodyParagraph(
            "본 내용증명서는 발신인의 계약갱신청구권 행사에 대한 정식 통보이며, " +
            "향후 법적 분쟁 시 증거자료로 사용될 수 있습니다."
          ),
          spacer(),
          spacer(),

          // 구분선
          new Paragraph({
            spacing: { after: 600 },
            border: {
              bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000" },
            },
            children: [],
          }),

          // 날짜
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 600 },
            children: [
              new TextRun({
                text: "        년        월        일",
                size: 24,
                font: "맑은 고딕",
              }),
            ],
          }),

          spacer(),

          // 발신인 서명
          new Paragraph({
            alignment: AlignmentType.RIGHT,
            spacing: { after: 100 },
            children: [
              new TextRun({
                text: "발신인 (임차인):                          (서명 또는 인)",
                size: 24,
                font: "맑은 고딕",
              }),
            ],
          }),

          spacer(),
          spacer(),

          // 안내사항
          new Paragraph({
            spacing: { after: 200 },
            border: {
              top: { style: BorderStyle.SINGLE, size: 3, color: "CCCCCC" },
              bottom: { style: BorderStyle.SINGLE, size: 3, color: "CCCCCC" },
              left: { style: BorderStyle.SINGLE, size: 3, color: "CCCCCC" },
              right: { style: BorderStyle.SINGLE, size: 3, color: "CCCCCC" },
            },
            children: [
              new TextRun({
                text: "【 안내사항 】",
                bold: true,
                size: 20,
                font: "맑은 고딕",
              }),
            ],
          }),

          noteParagraph("1. 본 내용증명서는 우체국 내용증명 우편으로 발송하시기 바랍니다."),
          noteParagraph("2. 내용증명은 동일 내용의 문서 3부를 작성하여 우체국에 제출합니다."),
          noteParagraph("   (발신인 보관용 1부, 수신인 송달용 1부, 우체국 보관용 1부)"),
          noteParagraph("3. 계약갱신 요구는 임대차기간 만료 6개월 전 ~ 2개월 전에 해야 합니다."),
          noteParagraph("4. 임차인의 계약갱신요구권은 최초 임대차기간 포함 전체 10년 범위 내에서 행사 가능합니다."),
          noteParagraph("5. 필요시 법률 전문가의 상담을 받으시기 바랍니다."),
        ],
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  const outputPath = "/mnt/c/Users/SAMSUNG/Desktop/저작권/내용증명서_전세계약갱신권.docx";
  fs.writeFileSync(outputPath, buffer);
  console.log("✅ 내용증명서 생성 완료: " + outputPath);
}

// 헬퍼 함수들
function sectionTitle(text) {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    children: [
      new TextRun({
        text: text,
        bold: true,
        size: 24,
        font: "맑은 고딕",
      }),
    ],
  });
}

function infoRow(label, value) {
  return new Paragraph({
    spacing: { after: 100 },
    children: [
      new TextRun({
        text: `    ${label} : ${value}`,
        size: 22,
        font: "맑은 고딕",
      }),
    ],
  });
}

function bodyParagraph(text) {
  return new Paragraph({
    spacing: { after: 100 },
    indent: { firstLine: convertInchesToTwip(0.3) },
    children: [
      new TextRun({
        text: text,
        size: 22,
        font: "맑은 고딕",
      }),
    ],
  });
}

function noteParagraph(text) {
  return new Paragraph({
    spacing: { after: 50 },
    children: [
      new TextRun({
        text: text,
        size: 18,
        font: "맑은 고딕",
        color: "555555",
      }),
    ],
  });
}

function spacer() {
  return new Paragraph({
    spacing: { after: 100 },
    children: [],
  });
}

create내용증명서().catch(console.error);

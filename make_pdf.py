"""
portfolio-print.html -> 김상현_포트폴리오.pdf

사용법:
    pip install playwright
    playwright install chromium
    python make_pdf.py

portfolio-print.html 과 같은 폴더에서 실행하세요.
(images/ 폴더가 옆에 있어야 이미지가 들어갑니다)
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
SRC = HERE / "portfolio-print.html"
OUT = HERE / "김상현_포트폴리오.pdf"

FOOTER = """
<div style="width:100%;font-size:7pt;color:#7b838f;
            font-family:'Helvetica Neue',Arial,sans-serif;
            padding:0 16mm;display:flex;justify-content:space-between;">
  <span>Sanghyun Kim &middot; Portfolio 2026</span>
  <span class="pageNumber"></span>
</div>
"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(SRC.resolve().as_uri(), wait_until="networkidle")

        # 웹폰트 로딩 완료까지 대기
        page.evaluate("() => document.fonts.ready")
        page.wait_for_timeout(1200)

        # 화면 미리보기용 스타일 제거 (PDF 여백은 아래 margin이 담당)
        page.add_style_tag(content="""
            body{ background:#fff !important; padding:0 !important; }
            .sheet{ width:auto !important; padding:0 !important;
                    box-shadow:none !important; margin:0 !important; }
        """)
        page.wait_for_timeout(300)

        page.pdf(
            path=str(OUT),
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template="<div></div>",
            footer_template=FOOTER,
            margin={"top": "13mm", "bottom": "14mm", "left": "16mm", "right": "16mm"},
        )
        browser.close()
        print(f"완료: {OUT}")


if __name__ == "__main__":
    main()
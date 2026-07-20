"""
make_toc_file.py
폴더 안의 모든 .md 파일을 스캔해서,
"목차.md" 라는 별도 파일에 전체 목차를 생성합니다.
(원본 파일들은 건드리지 않습니다)

사용법:
    python make_toc_file.py .
"""

import re
import sys
import os


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s\-가-힣]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def extract_headings(lines):
    headings = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        match = re.match(r"^(#{1,3})\s+(.*)", line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((level, title))
    return headings


def build_file_section(filename, headings):
    """파일 하나에 대한 목차 섹션 (파일명.md#앵커 형태로 링크)"""
    lines = [f"### {filename}", ""]
    for level, title in headings:
        indent = "  " * (level - 1)
        anchor = slugify(title)
        # 파일명에 공백이 있으면 %20으로 인코딩
        encoded_filename = filename.replace(" ", "%20")
        lines.append(f"{indent}- [{title}]({encoded_filename}#{anchor})")
    lines.append("")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("사용법: python make_toc_file.py .")
        sys.exit(1)

    target_dir = sys.argv[1]
    output_path = os.path.join(target_dir, "category.md")

    md_files = sorted(
        f for f in os.listdir(target_dir)
        if f.endswith(".md") and f != "category.md"
    )

    if not md_files:
        print("이 폴더에 .md 파일이 없습니다.")
        return

    sections = ["# 전체 목차", ""]
    for filename in md_files:
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        headings = extract_headings(lines)
        if not headings:
            continue
        sections.append(build_file_section(filename, headings))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sections))

    print(f"[완료] 목차 파일 생성: {output_path}")


if __name__ == "__main__":
    main()

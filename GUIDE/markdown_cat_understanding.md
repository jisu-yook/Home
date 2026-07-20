# make_toc_file.py 코드 뜯어보기 (초보자용)

이 문서는 `make_toc_file.py`를 한 줄씩 이해하기 위한 설명입니다.
파이썬 기초 문법(반복문, 조건문 등)도 함께 설명합니다.

---

## 파이썬 기초 개념 먼저

### 리스트(list)란
여러 개의 값을 순서대로 담는 상자입니다.
```python
fruits = ["사과", "바나나", "포도"]
```
`fruits[0]`은 "사과", `fruits[1]`은 "바나나"입니다. (0번부터 시작)

### for 반복문이란
리스트 안의 값을 하나씩 꺼내서, 같은 작업을 반복하는 문법입니다.
```python
fruits = ["사과", "바나나", "포도"]
for fruit in fruits:
    print(fruit)
```
결과:
```
사과
바나나
포도
```
`fruit`이라는 이름은 자유롭게 지을 수 있습니다. "리스트에서 하나씩 꺼내서 fruit이라 부르겠다"는 뜻입니다.

### 함수(function)란
자주 쓰는 작업을 이름 붙여서 저장해두고, 필요할 때 불러 쓰는 것입니다.
```python
def say_hello(name):
    print("안녕, " + name)

say_hello("지수")   # 실행하면 "안녕, 지수" 출력
```
`def 함수이름(입력값):` 으로 시작하고, 그 아래 들여쓰기된 부분이 실행할 내용입니다.

### f-string이란
문자열 안에 변수 값을 끼워 넣는 문법입니다.
```python
name = "지수"
print(f"안녕, {name}")   # "안녕, 지수" 출력
```
문자열 앞에 `f`를 붙이고, `{}` 안에 변수를 넣으면 그 변수의 값으로 바뀝니다.

---

## 1. slugify 함수

**역할**: 제목 텍스트를 GitHub이 인식하는 "앵커 이름"으로 바꾸는 함수
(예: `"0. 기존 저장소 내려받기 (clone)"` → `"0-기존-저장소-내려받기-clone"`)

```python
def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s\-가-힣]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text
```

| 코드 | 의미 |
|---|---|
| `def slugify(text: str) -> str:` | `slugify`라는 함수를 만듦. `text`라는 문자열을 입력받아서, 문자열을 결과로 돌려줌 |
| `text.strip()` | 문자열 앞뒤의 불필요한 공백을 제거 |
| `.lower()` | 모든 영문자를 소문자로 변환 |
| `re.sub(패턴, 바꿀글자, 대상)` | 정규식(regex)으로 특정 패턴에 맞는 부분을 찾아서 다른 글자로 바꾸는 함수 |
| `r"[^\w\s\-가-힣]"` | "영문/숫자/밑줄(`\w`), 공백(`\s`), 하이픈(`-`), 한글(`가-힣`)이 아닌 모든 문자"를 뜻하는 패턴. `^`가 대괄호 맨 앞에 있으면 "아닌 것"이라는 부정의 의미 |
| 위 줄 전체 | 특수문자(`.`, `(`, `)` 등)를 전부 빈 문자열로 바꿔서 제거 |
| `r"\s+"` | 공백이 1개 이상 연속된 부분 |
| 그 줄 전체 | 공백을 하이픈(`-`)으로 바꿈 |
| `return text` | 최종 결과 문자열을 돌려줌 |

**예시**
```
입력: "0. 기존 저장소 내려받기 (clone)"
1단계 (소문자+공백정리): "0. 기존 저장소 내려받기 (clone)"
2단계 (특수문자 제거): "0 기존 저장소 내려받기 clone"
3단계 (공백→하이픈): "0-기존-저장소-내려받기-clone"
```

---

## 2. extract_headings 함수

**역할**: 파일의 모든 줄을 살펴보며 `#`, `##`, `###`로 시작하는 "제목 줄"만 뽑아내는 함수

```python
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
```

| 코드 | 의미 |
|---|---|
| `def extract_headings(lines):` | `lines`(파일의 모든 줄이 담긴 리스트)를 입력받는 함수 정의 |
| `headings = []` | 제목들을 담을 빈 리스트를 미리 준비 |
| `in_code_block = False` | "지금 코드블록 안에 있는가?"를 표시하는 값. 처음엔 아니므로 False |
| `for line in lines:` | `lines` 리스트에서 한 줄씩 꺼내 `line`이라는 이름으로 반복 처리 |
| `line.strip().startswith("```")` | 그 줄이 (양쪽 공백 제거 후) `` ``` ``로 시작하는지 확인 → 코드블록의 시작/끝 표시 |
| `in_code_block = not in_code_block` | `not`은 반대로 뒤집는 것. True면 False로, False면 True로 전환 → 코드블록 안/밖 상태를 토글 |
| `continue` | "이번 반복은 여기서 끝, 바로 다음 줄로 넘어가라"는 명령 |
| `if in_code_block: continue` | 지금 코드블록 안이면, 제목 검사 없이 바로 다음 줄로 (코드 안의 `#`이 제목으로 오인되는 걸 방지) |
| `re.match(패턴, line)` | `line`이 특정 패턴으로 시작하는지 검사. 맞으면 결과를 돌려주고, 아니면 `None`을 돌려줌 |
| `r"^(#{1,3})\s+(.*)"` | 패턴 해석: `^`(줄 맨 앞부터) + `(#{1,3})`(`#`이 1~3개, 그룹1로 저장) + `\s+`(공백 1개 이상) + `(.*)`(나머지 전부, 그룹2로 저장) |
| `if match:` | 검사 결과가 있으면(=제목이 맞으면) 아래 코드 실행 |
| `match.group(1)` | 정규식에서 첫 번째 괄호로 잡아낸 부분 → `#` 기호들 (예: `"##"`) |
| `len(...)` | 문자열의 길이(글자 수)를 세는 함수 → `#` 개수 = 제목 레벨 |
| `match.group(2)` | 두 번째 괄호로 잡아낸 부분 → 실제 제목 텍스트 |
| `.strip()` | 제목 앞뒤 공백 제거 |
| `headings.append((level, title))` | `.append()`는 리스트 맨 뒤에 새 항목을 추가하는 함수. `(level, title)`처럼 괄호로 묶은 건 "튜플"이라는, 두 값을 한 쌍으로 묶는 자료형 |
| `return headings` | 완성된 제목 목록을 돌려줌 |

**예시**

입력 (`lines`):
```
## 0. 기존 저장소 내려받기 (clone)
내용...
## 1. 개념
```bash
# 이 안은 무시됨
```
```

결과 (`headings`):
```python
[(2, "0. 기존 저장소 내려받기 (clone)"), (2, "1. 개념")]
```

---

## 3. build_file_section 함수

**역할**: 파일 하나의 제목 목록을 받아서, 마크다운 목차 텍스트로 조립하는 함수

```python
def build_file_section(filename, headings):
    lines = [f"### {filename}", ""]
    for level, title in headings:
        indent = "  " * (level - 1)
        anchor = slugify(title)
        encoded_filename = filename.replace(" ", "%20")
        lines.append(f"{indent}- [{title}]({encoded_filename}#{anchor})")
    lines.append("")
    return "\n".join(lines)
```

| 코드 | 의미 |
|---|---|
| `def build_file_section(filename, headings):` | 파일명과 제목 목록, 이렇게 2개를 입력받는 함수 |
| `lines = [f"### {filename}", ""]` | 결과 텍스트를 줄 단위로 쌓을 리스트를 만들고, 첫 줄엔 "### 파일명", 둘째 줄엔 빈 줄을 미리 넣음 |
| `for level, title in headings:` | `headings`는 `(level, title)` 튜플들의 리스트. 반복할 때 튜플을 `level`과 `title` 두 변수로 바로 나눠 받을 수 있음 |
| `"  " * (level - 1)` | 문자열에 `*`(곱하기)를 쓰면 그 문자열을 반복. 공백 2칸을 `(level-1)`번 반복 → 레벨이 높을수록 더 들여쓰기됨 |
| `slugify(title)` | 앞서 만든 함수를 불러와서 제목을 앵커 이름으로 변환 |
| `filename.replace(" ", "%20")` | `.replace(A, B)`는 문자열 안의 A를 B로 바꾸는 함수. 파일명의 공백을 `%20`(URL에서 공백을 표시하는 방식)으로 바꿈 |
| `f"{indent}- [{title}]({encoded_filename}#{anchor})"` | f-string으로 마크다운 링크 한 줄을 완성. `[제목](파일명#앵커)` 형태 |
| `lines.append(...)` | 완성한 줄을 리스트 맨 뒤에 추가 |
| `lines.append("")` | 마지막에 빈 줄 하나 추가 (다음 섹션과 구분하기 위해) |
| `"\n".join(lines)` | `.join()`은 리스트 안의 모든 문자열을 하나로 이어붙이는 함수. `"\n"`(줄바꿈 문자)을 기준으로 이어붙임 → 리스트를 한 덩어리의 텍스트로 변환 |
| `return ...` | 완성된 텍스트 블록을 돌려줌 |

**예시**

입력:
```python
filename = "1_GitHub 기초 명령어.md"
headings = [(2, "0. 기존 저장소 내려받기 (clone)"), (2, "1. 개념")]
```

결과 (문자열):
```
### 1_GitHub 기초 명령어.md

  - [0. 기존 저장소 내려받기 (clone)](1_GitHub%20기초%20명령어.md#0-기존-저장소-내려받기-clone)
  - [1. 개념](1_GitHub%20기초%20명령어.md#1-개념)
```

---

## 4. main 함수

**역할**: 전체 작업 순서를 지휘하는 함수. 실제로 실행되는 부분

### 4-1. 입력값 확인

```python
def main():
    if len(sys.argv) < 2:
        print("사용법: python make_toc_file.py .")
        sys.exit(1)

    target_dir = sys.argv[1]
    output_path = os.path.join(target_dir, "목차.md")
```

| 코드 | 의미 |
|---|---|
| `sys.argv` | 터미널에서 입력한 명령어 전체를 리스트로 담고 있는 것. `python make_toc_file.py .`라고 치면 `sys.argv = ["make_toc_file.py", "."]`가 됨 |
| `sys.argv[0]` | 항상 스크립트 자기 자신의 파일명 |
| `sys.argv[1]` | 사용자가 추가로 입력한 첫 번째 값 (여기선 폴더 경로) |
| `len(sys.argv)` | 리스트 안에 값이 몇 개 있는지 셈 |
| `if len(sys.argv) < 2:` | 값이 2개 미만이면 = 사용자가 폴더 경로를 안 넘겼다는 뜻 |
| `print(...)` | 화면에 문구 출력 |
| `sys.exit(1)` | 프로그램을 즉시 종료. `1`은 "정상적이지 않게 끝났다"는 신호값 (정상 종료는 보통 0) |
| `target_dir = sys.argv[1]` | 사용자가 입력한 폴더 경로를 변수에 저장 |
| `os.path.join(A, B)` | 경로 A와 이름 B를 올바른 형식으로 합쳐주는 함수. `target_dir`이 `"."`이면 결과는 `"./목차.md"` |

### 4-2. .md 파일 목록 찾기

```python
    md_files = sorted(
        f for f in os.listdir(target_dir)
        if f.endswith(".md") and f != "목차.md"
    )

    if not md_files:
        print("이 폴더에 .md 파일이 없습니다.")
        return
```

| 코드 | 의미 |
|---|---|
| `os.listdir(target_dir)` | 그 폴더 안에 있는 모든 파일/폴더 이름을 리스트로 돌려줌 |
| `f for f in os.listdir(target_dir) if 조건` | "제너레이터 표현식"이라는 축약 문법. 풀어 쓰면 아래와 같음: |

```python
# 위 코드를 풀어서 쓰면 이런 뜻입니다
result = []
for f in os.listdir(target_dir):
    if f.endswith(".md") and f != "목차.md":
        result.append(f)
```

| 코드 | 의미 |
|---|---|
| `f.endswith(".md")` | 문자열 `f`가 `.md`로 끝나는지 확인하는 함수 |
| `f != "목차.md"` | `f`가 `"목차.md"`와 같지 않은지 확인 (`!=`는 "같지 않다") |
| `and` | 두 조건을 모두 만족해야 함 |
| `sorted(...)` | 리스트를 가나다순/알파벳순으로 정렬해주는 함수 |
| `if not md_files:` | `md_files` 리스트가 비어있으면(=파일이 하나도 없으면) |
| `return` | 함수를 여기서 끝냄 (더 이상 아래 코드 실행 안 함) |

### 4-3. 각 파일 처리

```python
    sections = ["# 전체 목차", ""]
    for filename in md_files:
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        headings = extract_headings(lines)
        if not headings:
            continue
        sections.append(build_file_section(filename, headings))
```

| 코드 | 의미 |
|---|---|
| `sections = ["# 전체 목차", ""]` | 최종 결과를 담을 리스트. 시작은 큰 제목 한 줄 + 빈 줄 |
| `for filename in md_files:` | 찾은 `.md` 파일들을 하나씩 꺼내서 처리 |
| `filepath = os.path.join(target_dir, filename)` | 폴더 경로와 파일명을 합쳐서, 실제로 열 수 있는 전체 경로를 만듦 |
| `open(경로, "r", encoding="utf-8")` | 파일을 여는 함수. `"r"`은 읽기(read) 모드, `encoding="utf-8"`은 한글이 깨지지 않게 하는 설정 |
| `with ... as f:` | 파일을 열고, 이 블록이 끝나면 자동으로 안전하게 닫아주는 문법. `f`라는 이름으로 파일을 다룸 |
| `f.read()` | 파일 내용 전체를 하나의 긴 문자열로 읽어옴 |
| `.splitlines()` | 그 긴 문자열을 줄바꿈 기준으로 잘라서, 한 줄씩 담긴 리스트로 만듦 |
| `extract_headings(lines)` | 앞서 만든 함수로, 이 파일 안의 제목들을 뽑아냄 |
| `if not headings: continue` | 제목이 하나도 없으면, 이 파일은 건너뛰고 다음 파일로 넘어감 |
| `sections.append(...)` | 이 파일의 목차 블록을 만들어서 `sections` 리스트에 추가 |

### 4-4. 결과 파일로 저장

```python
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sections))

    print(f"[완료] 목차 파일 생성: {output_path}")


if __name__ == "__main__":
    main()
```

| 코드 | 의미 |
|---|---|
| `open(output_path, "w", encoding="utf-8")` | 결과 파일(`목차.md`)을 연다. `"w"`는 쓰기(write) 모드. 파일이 없으면 새로 만들고, 있으면 기존 내용을 덮어씀 |
| `f.write(내용)` | 파일에 문자열을 씀 |
| `"\n".join(sections)` | `sections` 리스트 안의 모든 블록을 줄바꿈으로 이어붙여 하나의 긴 문자열로 만듦 |
| `print(f"[완료]...")` | 작업이 끝났다고 화면에 알림 |
| `if __name__ == "__main__":` | "이 파일을 직접 실행했을 때만" 아래 코드를 실행하라는 관용적인 안전장치. 다른 파이썬 파일이 이 파일을 `import`해서 가져다 쓸 때는 자동 실행되지 않게 막아줌 |
| `main()` | 지금까지 만든 `main` 함수를 실제로 호출(실행) |

---

## 전체 흐름 요약

```
1. 사용자가 터미널에 폴더 경로 입력
   (예: python make_toc_file.py .)
        ↓
2. 그 폴더 안의 .md 파일들 목록 찾기
        ↓
3. 파일마다 하나씩 열어서
   - 제목(#, ##, ###) 줄들을 찾고
   - 각 제목을 GitHub 앵커 링크로 변환
        ↓
4. 모든 파일의 목차 블록을 하나로 합쳐서
   "목차.md" 라는 새 파일로 저장
```
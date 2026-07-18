## VSCode 연동

1. VSCode 실행
2. `Cmd + Shift + P` → "Shell Command: Install 'code' command in PATH" 검색 후 실행
3. 터미널 재시작
4. `code .` 입력

## 브랜치(Branch)란

하나의 저장소 안에서 독립적으로 작업할 수 있는 "가지". `main`(또는 `master`)은 기본 브랜치이고, 새 기능을 만들 때 별도 브랜치를 따서 작업 후 합침(merge).

```bash
git branch                 # 브랜치 목록 확인
git branch 새브랜치이름      # 새 브랜치 생성
git checkout 브랜치이름      # 해당 브랜치로 이동
git checkout -b 새브랜치이름 # 생성 + 이동 동시에
```

## .gitignore

### 작성법

저장소 최상위 폴더에 `.gitignore`라는 이름의 파일을 만들고, 제외할 파일/폴더를 한 줄씩 작성

예시:

```
.DS_Store
__pycache__
venv/
*.log
```

### 특정 파일이 왜 무시되는지 확인

```bash
git check-ignore -v 파일명또는폴더명
```

→ 어떤 `.gitignore` 규칙 때문인지 정확히 알려줌

## 실수로 로컬 파일까지 삭제된 경우 복구

- 아직 commit 전이라면:
```bash
git checkout -- .
```

- 그래도 옆에 D(삭제 예정) 표시가 남아있다면:
```bash
git reset --hard HEAD
```

- 이미 commit까지 했다면:
```bash
git reset --hard HEAD~1
```

**용어 설명**
- `HEAD`: 현재 작업 중인(보고 있는) 커밋을 가리키는 포인터. 보통 "가장 최근 커밋"이라고 생각하면 됨
    - `HEAD~1` = HEAD보다 1개 이전 커밋
    - `HEAD~2` = 2개 이전 커밋
- `--hard`: 되돌릴 때 **작업 중인 파일 내용까지** 지정한 커밋 상태로 강제로 맞추는 옵션
    - `--hard` 없이 `git reset`만 쓰면 → 커밋만 취소, 파일 내용은 그대로 남음
    - `--hard` 쓰면 → 커밋 취소 + 파일 내용도 그 시점으로 되돌림 (변경사항 사라짐, 주의)

## 서브모듈처럼 인식되는 폴더 (untracked content)

다른 Git 저장소를 폴더째 복사해 넣으면, 그 안의 `.git` 때문에 서브모듈처럼 인식됨.

해결:
```bash
git rm --cached 폴더명
rm -rf 폴더명/.git
git add 폴더명
git commit -m "서브모듈 제거, 일반 폴더로 변경"
git push
```

## etc 에러

### upstream branch 없음
```
fatal: The current branch master has no upstream branch. To push the current branch and set the remote as upstream, use ...
```
로컬 브랜치(`master`)와 원격 브랜치가 아직 연결(upstream)되어 있지 않아서 발생. push할 때 "어디로 보낼지" 기본값이 없는 상태.

```bash
git push --set-upstream origin master
# 또는
git push -u origin master
```

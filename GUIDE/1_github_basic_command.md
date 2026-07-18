## 0. 기존 저장소 내려받기 (clone)

이미 GitHub에 있는 저장소를 그대로 복제해서 시작할 때 사용
```bash
git clone 저장소URL
cd 저장소폴더명
```

> `git init`은 "새로 시작", `git clone`은 "이미 있는 걸 가져오기"

## 1. 개념
- **Git**: 파일 변경 이력을 기록하는 프로그램 (내 컴퓨터)
- **저장소(Repository)**: 파일들을 담는 프로젝트 폴더
- **GitHub**: 저장소를 온라인에 올려두는 서비스

## 2. 설치
```bash
git --version              # Git 설치 확인
xcode-select --install     # 없을 경우 설치
brew install gh            # GitHub CLI 설치
```

## 3. 내 정보 등록
```bash
git config --global user.name "이름"
git config --global user.email "이메일"
```

- `--global`: 컴퓨터 전체에 적용, 이후 재입력 불필요
- 특정 프로젝트에서만 다른 이름/이메일 쓰고 싶을 땐, 해당 폴더에서 `--global` 없이 입력
- 확인: `git config --global user.name`
- 최초 1회만 진행

## 4. GitHub 로그인
```bash
gh auth login
```

- GitHub.com → HTTPS → Yes → Login with a web browser 순서로 선택
- 브라우저에서 코드 입력하면 로그인 완료
- 확인: `gh auth status`

## 5. 로컬 저장소 만들기
```bash
cd 원하는_폴더
git init                # 이 폴더를 Git 저장소로 초기화 (.git 폴더 생성)
git status              # 현재 상태 확인
```

## 6. 파일 기록하기
```bash
git add .                        # 파일을 추적 대상으로 등록
git commit -m "커밋 메시지"        # 하나의 버전으로 저장
git log                          # 커밋 기록 확인
```

## 7. GitHub에 업로드
```bash
gh repo create 저장소이름 --private --source=. --remote=origin --push
```

- GitHub에 "저장소이름"이라는 레포 생성
- `--private`: 나만 볼 수 있게 / `--public`: 공개
- `--source=.`: 현재 폴더를 저장소로 사용
- `--remote=origin`: 내 컴퓨터와 GitHub 저장소 연결
- `--push`: 지금까지 커밋한 내용 업로드
- → GitHub에 저장소 생성 + 연결 + 업로드를 한 번에 처리

## 8. 이후 반복 작업 흐름
파일 수정할 때마다:

```bash
git add .
git commit -m "변경 내용"
git push
```

## 9. add 취소하기
```bash
git reset
```

→ 스테이징 취소 (커밋 전 상태로 되돌림)

## 10. GitHub 추적에서만 제거
```bash
git rm --cached 파일명
git rm -r --cached 폴더명
```

> `--cached` 옵션이 없으면 로컬 파일까지 삭제됨

## 11. 원격 저장소 지정 push
```bash
git push <원격이름> <브랜치이름>
git remote -v                    # 연결된 원격 확인
git remote add 별칭 저장소URL      # 원격 추가
git push 별칭 main
```

## 12. Repo 삭제
```bash
gh repo delete 저장소이름 --yes
```


**로컬 저장소 폴더 이름 변경**
```bash
mv 기존폴더명 새폴더명
```
(Git과 무관, 그냥 폴더 이름 바꾸기라 안전함)

**GitHub 저장소 이름 변경**
```bash
gh repo rename 새이름
```

현재 폴더가 그 저장소와 연결되어 있어야 합니다. (다른 저장소를 지정하려면 `gh repo rename 새이름 -R 소유자/기존이름`)

**주의**  
GitHub 이름을 바꾸면 로컬의 remote 주소도 자동으로 업데이트해주지만, 확인은 해보는 게 좋습니다.
```bash
git remote -v
```

옛 이름이 남아있다면:
```bash
git remote set-url origin 새URL
```

## 13. GitHub 버전으로 Sync하기
**커밋 전이라면**
```bash
git checkout -- .
git checkout -- 파일명
```
**이미 커밋 했다면 (push 전)**
```bash
git reset --hard origin/main
```
- 두 방법 모두 로컬에서 수정한 내용은 삭제됨

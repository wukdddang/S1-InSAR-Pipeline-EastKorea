# 데이터 다운로드 가이드

## 🔐 인증 문제 해결

프로그래밍 방식의 다운로드에서 401 오류가 발생할 경우, 다음 방법들을 시도하세요.

## 방법 1: .netrc 파일 설정 (권장 ⭐)

NASA Earthdata는 `.netrc` 파일을 통한 인증을 선호합니다.

### 자동 설정

```bash
python setup_netrc.py
```

### 수동 설정

1. **Windows**: `C:\Users\사용자이름\.netrc` 파일 생성
2. **Linux/Mac**: `~/.netrc` 파일 생성

**파일 내용:**

```
machine urs.earthdata.nasa.gov
    login changuk
    password YOUR_PASSWORD
```

**Linux/Mac 권한 설정:**

```bash
chmod 600 ~/.netrc
```

### 설정 후 다운로드

```bash
python run_data_search.py --start-date 2023-01-01 --end-date 2023-01-31 --download --max-products 1
```

## 방법 2: wget으로 수동 다운로드

프로그램이 제공하는 URL을 사용하여 수동 다운로드:

```bash
# 1. 검색만 실행
python run_data_search.py --start-date 2023-01-01 --end-date 2023-01-31

# 2. 표시된 URL을 wget으로 다운로드
wget --user=changuk --password=YOUR_PASSWORD \
  --output-document=data/raw/product.zip \
  "https://datapool.asf.alaska.edu/SLC/SA/S1A_IW_SLC__1SDV_20230119T092353_20230119T092406_046851_059E1C_E0EC.zip"
```

## 방법 3: 브라우저로 다운로드

1. **검색 실행**:

```bash
python run_data_search.py --start-date 2023-01-01 --end-date 2023-01-31
```

2. **출력된 다운로드 URL 복사**

3. **브라우저에서**:
   - NASA Earthdata에 로그인
   - 복사한 URL로 이동
   - 파일 다운로드
   - `data/raw/` 폴더에 저장

## 방법 4: ASF Vertex (웹 인터페이스)

1. https://search.asf.alaska.edu/ 방문
2. 지역 선택: 위도 35.5-36.5, 경도 128.5-129.5
3. 날짜 선택: 2023-01-01 ~ 2023-12-31
4. 제품 타입: Sentinel-1 SLC
5. 검색 후 다운로드

## 💡 추천 워크플로우

### 개발/테스트 단계

- **검색만 사용**: 어떤 데이터가 있는지 확인
- **브라우저 다운로드**: 1-2개 테스트용 데이터

### 대량 다운로드 단계

- **.netrc 설정**: 자동화된 다운로드
- **프로그램 사용**: 여러 제품 자동 다운로드

## 🔍 디버깅

인증 문제가 계속되면:

1. **계정 확인**:

   - https://urs.earthdata.nasa.gov/ 에서 로그인 가능한지 확인
   - 비밀번호가 특수문자를 포함하는지 확인

2. **앱 승인 재확인**:

   - Applications → Approved Applications
   - "Alaska Satellite Facility Data Access" 승인 확인

3. **캐시 삭제**:

   ```bash
   # Python 실행 전 환경 변수 삭제
   unset EARTHDATA_USERNAME
   unset EARTHDATA_PASSWORD
   ```

4. **다른 제품으로 시도**:
   ```bash
   # 다른 날짜/지역으로 테스트
   python run_data_search.py --start-date 2022-01-01 --end-date 2022-03-31
   ```

## 📊 현재 상태

✅ **작동하는 것**:

- 데이터 검색 (완벽)
- 제품 목록 확인
- 다운로드 URL 생성

❌ **작동하지 않는 것**:

- 자동 다운로드 (401 인증 오류)

## 🎯 결론

**지금은 검색 + 수동 다운로드를 권장**합니다:

1. 프로그램으로 검색
2. 제공된 URL로 브라우저 다운로드
3. 향후 `.netrc` 설정으로 자동화

대량 다운로드가 필요할 때 `.netrc` 방식을 시도하세요!

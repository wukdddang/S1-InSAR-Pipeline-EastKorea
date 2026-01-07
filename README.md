# S1-InSAR-Pipeline-EastKorea 🛰️

> **Sentinel-1 SLC 데이터를 활용한 한반도 동남권 지표 변위 모니터링 파이프라인**

본 프로젝트는 Sentinel-1 위성의 SAR(Synthetic Aperture Radar) 데이터를 활용하여 한반도 동남권(포항, 경주 등 단층 활동 지역)의 지표면 변위를 시계열로 분석하는 Python 기반 데이터 파이프라인입니다.

기존 토목공학적 측지 지식과 현대적인 소프트웨어 엔지니어링 기법을 결합하여, 위성 데이터 수집부터 분석 결과 시각화까지의 과정을 자동화하는 것을 목표로 합니다.

## 🌟 Key Features

- **Automated Data Retrieval**: ASF Data Search API를 활용한 Sentinel-1 SLC 데이터 검색 및 다운로드 자동화.
- **InSAR Processing**: `PyGMTSAR` 또는 `ISCE2`를 활용한 간섭도(Interferogram) 생성 및 변위 산출.
- **Time-series Analysis**: SBAS(Small BAseline Subset) 기법을 적용한 시계열 지표 변위 추정.
- **Geospatial Visualization**: 분석 결과를 `Folium` 기반의 인터랙티브 웹 지도로 시각화.

## 🛠 Tech Stack

- **Language**: Python 3.9+
- **Data Retrieval**: ASF Data Search (Alaska Satellite Facility)
- **GIS/Remote Sensing**: PyGMTSAR, Rasterio, GeoPandas, Shapely, PyProj
- **Data Science**: NumPy, Pandas, Matplotlib
- **Automation**: asf-search API

## 📍 Analysis Area: East Korea (Southeastern Region)

- **Target**: 포항 및 경주 인근 단층대 (양산단층, 곡강단층 등)
- **Rationale**: 한반도 내 지진 활동이 가장 활발한 지역으로, 미세한 지표 변위 모니터링을 통한 방재 및 토목 안정성 분석이 중요함.

## 🚀 Getting Started

### Prerequisites

- **Python 3.9 이상**
- **NASA Earthdata 계정**: [가입하기](https://urs.earthdata.nasa.gov/users/new) - ASF Data Search 사용을 위해 필요
- **충분한 디스크 공간**: SAR 데이터는 제품당 약 4-8GB
- **Windows 사용자**: InSAR 처리를 위해 **WSL2 권장** (ISCE2는 Linux/Mac만 지원)

### Installation

#### 1. 저장소 클론

```bash
git clone https://github.com/wukdddang/S1-InSAR-Pipeline-EastKorea.git
cd S1-InSAR-Pipeline-EastKorea
```

#### 2. Windows 사용자: WSL2 설치 (InSAR 처리 필수!)

**Windows에서 코드 기반 InSAR 처리를 하려면 WSL2가 필요합니다.**

```bash
# PowerShell (관리자 권한으로 실행)
wsl --install -d Ubuntu-22.04

# 재부팅 후 Ubuntu 실행
wsl

# Ubuntu에서 Miniconda 설치
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
```

**WSL2 설치 후 아래 단계 진행 (WSL Ubuntu 터미널에서)**

> 💡 **Tip**: WSL에서 Windows 파일 접근: `/mnt/c/Users/사용자이름/`

#### 2-1. 가상 환경 생성 (권장)

> ⚠️ **중요**: conda와 venv 중 **하나만 선택**하세요! 둘 다 할 필요 없습니다.

**옵션 A: Conda 사용 (권장 ⭐)**

Conda는 Python 패키지뿐만 아니라 GDAL, Rasterio 같은 시스템 라이브러리도 쉽게 관리할 수 있어 권장됩니다.

```bash
conda create -n insar python=3.9
conda activate insar
```

**옵션 B: venv 사용**

Python 기본 도구만 사용하고 싶다면 venv를 선택하세요.

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 3. 패키지 설치

**옵션 A: Conda 사용 (권장 ⭐)**

```bash
# 1. 지리공간 라이브러리 설치 (conda 필수!)
conda install -c conda-forge gdal rasterio geopandas fiona pyproj shapely netCDF4 opencv

# 2. InSAR 처리 소프트웨어 (선택 사항)
conda install -c conda-forge isce2

# 3. 나머지 Python 패키지
pip install -r requirements.txt
```

**옵션 B: pip만 사용 (비권장)**

```bash
pip install -r requirements.txt
```

> ⚠️ **중요**: GDAL, rasterio, geopandas 등 지리공간 라이브러리는 pip 설치 시 많은 문제가 발생합니다. **Conda 사용을 강력히 권장합니다!**

#### 4. 인증 정보 설정

**4-1. credentials.yaml 설정:**

```bash
# credentials 템플릿 복사
# Windows
copy configs\credentials_template.yaml configs\credentials.yaml

# Linux/Mac
cp configs/credentials_template.yaml configs/credentials.yaml
```

**credentials.yaml 파일을 편집하여 실제 계정 정보 입력:**

```yaml
asf:
  username: your_nasa_earthdata_username
  password: your_nasa_earthdata_password
```

**4-2. .netrc 파일 설정 (다운로드용, 권장):**

NASA Earthdata는 `.netrc` 파일을 통한 인증을 권장합니다.

```bash
# 자동 설정
python scripts/setup_netrc.py
```

또는 수동으로 설정:

**Windows**: `C:\Users\사용자이름\.netrc` 파일 생성
**Linux/Mac**: `~/.netrc` 파일 생성

```
machine urs.earthdata.nasa.gov
    login your_username
    password your_password
```

**Linux/Mac에서 권한 설정:**

```bash
chmod 600 ~/.netrc
```

**4-3. NASA Earthdata 앱 승인 (필수!):**

1. https://urs.earthdata.nasa.gov/ 로그인
2. **Applications → Approve Applications** 메뉴로 이동
3. 다음 앱들을 승인:
   - ✅ **Alaska Satellite Facility Data Access**
   - ✅ **Alaska Satellite Facility Data Access (DEV/TEST)**
   - ✅ **Alaska Satellite Facility Data Access Egress Control**

> 💡 **Tip**: NASA Earthdata 계정이 없다면 [여기서 무료로 생성](https://urs.earthdata.nasa.gov/users/new)하세요!

### Quick Start

#### Sentinel-1 데이터 검색

```bash
# 기본 검색 (2024년 전체)
python run_data_search.py

# 특정 기간 검색 (예: 2023년 1분기)
python run_data_search.py --start-date 2023-01-01 --end-date 2023-03-31

# 더 많은 결과를 보고 싶다면
python run_data_search.py --start-date 2023-01-01 --end-date 2023-12-31 --max-results 50
```

#### 변위 분석을 위한 데이터 다운로드 (권장 🎯)

> **💡 Tip**: InSAR 변위 분석은 시간 간격이 긴 두 영상을 비교할 때 더 명확한 변위를 관찰할 수 있습니다.

**2024년 시작과 끝 데이터 다운로드:**

```bash
# 방법 1: InSAR 영상 쌍 자동 검색 (권장 ⭐)
# 같은 프레임의 2개 영상을 자동으로 찾아 다운로드
python run_data_search.py --start-date 2023-01-01 --end-date 2023-12-31 --pair --temporal-baseline 12 --download

# 방법 2: 수동으로 개별 다운로드 (비권장 - 프레임이 다를 수 있음)
# 1단계: 2023년 초반 데이터 검색 (Reference 영상)
python run_data_search.py --start-date 2023-01-01 --end-date 2023-03-31 --download --max-products 1

# 2단계: 2023년 말 데이터 검색 (Secondary 영상)
python run_data_search.py --start-date 2023-10-01 --end-date 2023-12-31 --download --max-products 1
```

**💡 Tip**: `--pair` 옵션을 사용하면 InSAR 처리에 적합한 같은 프레임의 영상 쌍을 자동으로 찾아줍니다!

**옵션 설명**:
- `--pair`: InSAR 영상 쌍 검색 모드
- `--temporal-baseline N`: 영상 간 시간 간격 (일 단위, 기본값: 12일)
- `--download`: 검색 후 자동 다운로드
- `--max-products N`: 최대 다운로드 개수

**장점:**

- ✅ 약 1년 간격의 시간 기선(Temporal Baseline)으로 누적 변위 관찰 가능
- ✅ 포항/경주 지역의 연간 지표 변위 패턴 분석에 최적
- ✅ 계절적 영향(지하수위 변동, 토양 수분 변화 등) 포함한 장기 변위 측정

**한 번에 다운로드 (간편):**

```bash
# 2023년 전체 기간에서 자동으로 첫 번째와 마지막 영상 다운로드
python run_data_search.py --start-date 2023-01-01 --end-date 2023-12-31 --download --max-products 2
```

> 💡 **Tip**: 최신 데이터가 검색되지 않으면 이전 연도(2023년 등)를 시도해보세요!

> ⚠️ **주의**: SAR 데이터는 제품당 약 4-8GB 입니다. 충분한 디스크 공간을 확보하세요!

#### Jupyter Notebook으로 실습

```bash
jupyter notebook notebooks/01_data_search_example.ipynb
```

## 📁 Project Structure

```
S1-InSAR-Pipeline-EastKorea/
├── configs/                    # 설정 파일
│   ├── config.yaml            # 메인 설정
│   ├── credentials_template.yaml  # 인증 정보 템플릿
│   └── credentials.yaml       # 실제 인증 정보 (git 제외)
├── src/                       # 소스 코드
│   ├── __init__.py
│   ├── config.py              # 설정 관리
│   ├── data_retrieval.py      # 데이터 검색/다운로드 (ASF)
│   ├── preprocessing.py       # 전처리 (예정)
│   ├── insar_processing.py    # InSAR 처리 (예정)
│   ├── time_series.py         # 시계열 분석 (예정)
│   ├── visualization.py       # 시각화 (예정)
│   └── utils.py               # 유틸리티 함수
├── scripts/                   # 유틸리티 스크립트
│   ├── setup_netrc.py         # .netrc 파일 자동 설정
│   ├── test_auth.py           # ASF 인증 테스트
│   ├── test_search.py         # ASF 검색 테스트
│   └── test_download.py       # ASF 다운로드 테스트
├── notebooks/                 # Jupyter 노트북
│   └── 01_data_search_example.ipynb
├── docs/                      # 추가 문서
│   ├── SETUP_GUIDE.md         # 상세 설치 가이드
│   └── TROUBLESHOOTING.md     # 문제 해결 가이드
├── data/                      # 데이터 디렉토리 (git 제외)
│   ├── raw/                   # 원본 SAR 데이터
│   ├── processed/             # 처리된 데이터
│   └── temp/                  # 임시 파일
├── outputs/                   # 결과 출력 (git 제외)
├── logs/                      # 로그 파일 (git 제외)
├── requirements.txt           # Python 패키지 목록
├── setup.py                   # 패키지 설치 스크립트
├── run_data_search.py         # 데이터 검색 실행 스크립트
├── .gitignore
└── README.md
```

## 📈 Roadmap

- [x] **Phase 1**: Sentinel-1 데이터 수집 스크립트 작성

  - [x] ASF Data Search 연동
  - [x] 설정 파일 관리 시스템
  - [x] CLI 및 Jupyter 노트북 인터페이스

- [ ] **Phase 2**: DInSAR 간섭도 생성 및 정사보정 로직 구현

  - [ ] PyGMTSAR/ISCE2 연동
  - [ ] 간섭쌍(Interferogram pairs) 자동 생성
  - [ ] 위상 언래핑(Phase unwrapping)

- [ ] **Phase 3**: SBAS 기반 시계열 분석 엔진 구축

  - [ ] Small Baseline 네트워크 구성
  - [ ] 시계열 역산(Inversion)
  - [ ] 대기 지연 보정

- [ ] **Phase 4**: 결과 시각화 및 검증 (To-be)
  - [ ] Folium 기반 인터랙티브 지도
  - [ ] GNSS 상시관측소 데이터와의 교차 검증 (R-square 분석)
  - [ ] 자동 보고서 생성

## 🔧 문제 해결 (Troubleshooting)

### 다운로드 401 오류

**증상**: `HTTP 401: Access denied` 오류 발생

**원인**:

1. .netrc 파일이 설정되지 않음
2. NASA Earthdata 앱 승인이 안 됨
3. 권한 승인이 아직 반영되지 않음

**해결 방법**:

**1. .netrc 파일 확인 및 재설정**

```bash
python scripts/setup_netrc.py
```

**2. 앱 승인 확인**

- https://urs.earthdata.nasa.gov/ → Applications → Approved Applications
- "Alaska Satellite Facility Data Access" 앱들이 승인되었는지 확인

**3. 권한 반영 대기**

- 앱 승인 후 5-10분 정도 대기
- 캐시 삭제: 터미널 재시작

**4. 대안: 브라우저로 수동 다운로드**

```bash
# 검색으로 다운로드 URL 확인
python run_data_search.py --start-date 2023-01-01 --end-date 2023-03-31

# 출력된 URL을 브라우저에서 열어 수동 다운로드
# 예: https://datapool.asf.alaska.edu/SLC/SA/제품명.zip
```

### 검색 결과 0개

**증상**: "검색 완료: 0개 제품 발견"

**해결 방법**:

**1. 날짜 범위 확장**

```bash
# 더 오래된 데이터로 시도 (2023년, 2022년)
python run_data_search.py --start-date 2022-01-01 --end-date 2022-12-31
```

**2. 검색 조건 완화**

- 현재는 SLC 제품만 검색
- 특정 지역에 데이터가 없을 수 있음
- 더 넓은 날짜 범위로 시도

**3. ASF Vertex로 확인**

- https://search.asf.alaska.edu/ 에서 직접 확인
- 해당 지역/날짜에 데이터가 있는지 확인

### 패키지 설치 오류

**GDAL/Rasterio 설치 실패**:

```bash
# Conda 사용 (권장)
conda install -c conda-forge rasterio gdal

# 또는 개별 설치
pip install rasterio --no-cache-dir
```

**asf-search 설치 실패**:

```bash
pip install asf-search --upgrade
```

### 메모리/디스크 부족

**디스크 공간 부족**:

```bash
# 저장 경로 변경
# configs/config.yaml 수정:
paths:
  data_dir: "D:/large_storage/data"  # 충분한 공간이 있는 드라이브
```

**메모리 부족**:

```bash
# 다운로드 개수 제한
python run_data_search.py --max-products 1
```

### 인증 정보 오류

**Username or password is incorrect**:

**1. credentials.yaml 확인**

```yaml
asf:
  username: username # 따옴표 없이
  password: your_password # 특수문자 주의
```

**2. 비밀번호 특수문자 처리**

```yaml
# 특수문자가 있으면 작은따옴표 사용
asf:
  username: username
  password: "P@ssw0rd!123"
```

**3. NASA Earthdata 웹사이트에서 로그인 테스트**

- https://urs.earthdata.nasa.gov/ 에서 로그인 가능한지 확인

### 네트워크 연결 오류

**Connection timeout**:

**1. 방화벽 확인**

- 회사/학교 네트워크에서 차단될 수 있음
- VPN 사용 시 비활성화 후 시도

**2. 프록시 설정**

```bash
# 프록시 환경 변수 설정 (필요시)
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

### ASF API 버전 문제

**asf-search 관련 오류**:

```bash
# 최신 버전으로 업데이트
pip install asf-search --upgrade

# 또는 특정 버전 설치
pip install asf-search==6.0.0
```

### 도움 받기

문제가 해결되지 않으면:

1. **GitHub Issues**: https://github.com/wukdddang/S1-InSAR-Pipeline-EastKorea/issues
2. **포함할 정보**:
   - OS 및 버전
   - Python 버전 (`python --version`)
   - 에러 메시지 전체
   - 시도한 해결 방법

## 🔧 Configuration

### 주요 설정 파일

#### `configs/config.yaml`

- 분석 영역(AOI) 설정
- Sentinel-1 검색 조건
- InSAR 처리 파라미터
- SBAS 시계열 분석 설정

#### `configs/credentials.yaml`

- NASA Earthdata (ASF) 계정 정보
- **주의**: 이 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다

### 분석 영역 변경

`configs/config.yaml`에서 AOI 좌표를 수정하여 다른 지역 분석 가능:

```yaml
aoi:
  name: "Your Region Name"
  min_lon: 128.0
  max_lon: 130.0
  min_lat: 35.0
  max_lat: 37.0
```

## 🤝 Contributing

이슈 제기, Pull Request, 개선 제안 등 모든 기여를 환영합니다!

## 📝 License

MIT License

## 🎓 About the Author

**Academic Background**: 토목공학 석사 (측지/측량 및 건설환경시스템 세부 전공)

**Current Role**: 사내 소프트웨어 개발자 (Web Developer)

**Goal**: 공간정보 분석 아키텍트 및 디지털 트윈 전문가

## 📖 추가 문서

- **[상세 설치 가이드](docs/SETUP_GUIDE.md)**: 단계별 설치 및 설정 안내
- **[다운로드 가이드](DOWNLOAD_GUIDE.md)**: 데이터 다운로드 상세 방법
- **[문제 해결](docs/TROUBLESHOOTING.md)**: 상세한 트러블슈팅 가이드

## 📚 References

- [Sentinel-1 Mission](https://sentinel.esa.int/web/sentinel/missions/sentinel-1)
- [ASF Data Search](https://asf.alaska.edu/)
- [NASA Earthdata](https://urs.earthdata.nasa.gov/)
- [PyGMTSAR Documentation](https://github.com/mobigroup/gmtsar)
- [ISCE2 Software](https://github.com/isce-framework/isce2)
- [InSAR Principles and Applications](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/InSAR_principles)

## 💬 Contact

프로젝트에 대한 문의사항이 있으시면 이슈를 등록해 주세요.

---

## 🎯 Quick Tips

### 처음 사용하는 경우

```bash
# 1. 환경 설정
conda create -n insar python=3.9
conda activate insar
pip install -r requirements.txt

# 2. 인증 설정
copy configs\credentials_template.yaml configs\credentials.yaml
# credentials.yaml 편집
python scripts/setup_netrc.py

# 3. NASA Earthdata 앱 승인 (웹브라우저)

# 4. 데이터 검색
python run_data_search.py --start-date 2023-01-01 --end-date 2023-12-31
```

### 자주 사용하는 명령어

```bash
# 검색만
python run_data_search.py --start-date 2023-01-01 --end-date 2023-12-31

# 검색 + 다운로드 (2개)
python run_data_search.py --start-date 2023-01-01 --end-date 2023-12-31 --download --max-products 2

# 더 많은 결과 보기
python run_data_search.py --start-date 2023-01-01 --end-date 2023-12-31 --max-results 50
```

### 현재 작동 상태

✅ **완벽하게 작동**: 데이터 검색, 제품 목록 확인  
⚠️ **설정 필요**: 자동 다운로드 (.netrc + 앱 승인)  
📝 **대안 가능**: 브라우저로 수동 다운로드

# 상세 설치 가이드

이 문서는 S1-InSAR-Pipeline-EastKorea 프로젝트의 상세한 설치 및 설정 가이드입니다.

## 목차

1. [시스템 요구사항](#시스템-요구사항)
2. [계정 생성](#계정-생성)
3. [Python 환경 설정](#python-환경-설정)
4. [패키지 설치](#패키지-설치)
5. [인증 정보 설정](#인증-정보-설정)
6. [설치 확인](#설치-확인)
7. [문제 해결](#문제-해결)

## 시스템 요구사항

### 필수 사항
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **Python**: 3.9 이상
- **메모리**: 최소 8GB RAM (16GB 권장)
- **디스크**: 최소 50GB 여유 공간 (SAR 데이터 저장용)

### 권장 사항
- **CPU**: 멀티코어 프로세서 (InSAR 처리 시 병렬 처리 활용)
- **GPU**: CUDA 지원 GPU (대용량 데이터 처리 가속)

## 계정 생성

### 1. Copernicus Open Access Hub 계정

Sentinel-1 데이터를 다운로드하기 위해 필요합니다.

1. [Copernicus 회원가입 페이지](https://scihub.copernicus.eu/dhus/#/self-registration)로 이동
2. 필요한 정보 입력:
   - Username
   - Password
   - Email
   - 이름, 성
   - 국가
3. 이메일 인증 완료
4. 계정 활성화까지 24시간 소요될 수 있음

### 2. ASF Data Search 계정 (선택사항)

Alaska Satellite Facility를 통한 데이터 다운로드용 (대안 방법):

1. [NASA Earthdata 계정 생성](https://urs.earthdata.nasa.gov/users/new)
2. 이메일 인증 완료

## Python 환경 설정

> ⚠️ **중요**: 아래 두 방법 중 **하나만 선택**하세요! 둘 다 할 필요 없습니다.
>
> - **방법 1 (Conda)**: GDAL/Rasterio 같은 복잡한 라이브러리 설치가 쉬움 (권장 ⭐)
> - **방법 2 (venv)**: Python 기본 도구만 사용

### 방법 1: Conda 사용 (권장 ⭐)

```bash
# Anaconda 또는 Miniconda 설치 확인
conda --version

# 새 환경 생성
conda create -n insar python=3.9

# 환경 활성화
conda activate insar

# (Windows에서) conda 활성화 안될 경우
# PowerShell에서 실행:
# conda init powershell
# 터미널 재시작 후 다시 시도
```

### 방법 2: venv 사용

```bash
# Python 버전 확인
python --version  # 3.9 이상이어야 함

# 가상환경 생성
python -m venv venv

# 활성화
## Windows (PowerShell)
.\venv\Scripts\Activate.ps1

## Windows (CMD)
.\venv\Scripts\activate.bat

## Linux/macOS
source venv/bin/activate
```

### 어떤 방법을 선택해야 할까요?

| 구분 | Conda | venv |
|------|-------|------|
| **설치 난이도** | 쉬움 ⭐ | 중간 |
| **GDAL/Rasterio 설치** | 자동으로 쉽게 설치 | 수동 설치 필요 (까다로움) |
| **디스크 용량** | 더 많이 필요 (~2GB) | 적게 필요 (~500MB) |
| **패키지 관리** | conda + pip 둘 다 사용 가능 | pip만 사용 |
| **추천 대상** | InSAR 처리가 처음이거나 빠른 설정 원하는 경우 | Python에 익숙하고 가벼운 환경 선호 |

**결론**: 특별한 이유가 없다면 **Conda 사용을 권장**합니다! 🎯

## 패키지 설치

### 1. 저장소 클론

```bash
git clone https://github.com/wukdddang/S1-InSAR-Pipeline-EastKorea.git
cd S1-InSAR-Pipeline-EastKorea
```

### 2. 필수 패키지 설치

```bash
# requirements.txt로부터 설치
pip install -r requirements.txt

# 업그레이드가 필요한 경우
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 개발 모드 설치 (선택사항)

프로젝트를 수정하면서 사용하려면:

```bash
pip install -e .
```

## 인증 정보 설정

### 1. credentials 파일 생성

```bash
# Windows
copy configs\credentials_template.yaml configs\credentials.yaml

# Linux/macOS
cp configs/credentials_template.yaml configs/credentials.yaml
```

### 2. 인증 정보 입력

`configs/credentials.yaml` 파일을 텍스트 에디터로 열고 실제 계정 정보 입력:

```yaml
# Copernicus Open Access Hub
copernicus:
  username: "your_actual_username"
  password: "your_actual_password"

# ASF (선택사항)
asf:
  username: "your_nasa_earthdata_username"
  password: "your_nasa_earthdata_password"
```

**보안 주의사항**:
- `credentials.yaml` 파일은 절대 Git에 커밋하지 마세요
- `.gitignore`에 이미 포함되어 있습니다
- 파일 권한을 적절히 설정하세요 (Linux/macOS: `chmod 600 configs/credentials.yaml`)

## 설치 확인

### 1. Python 패키지 확인

```python
python -c "import sentinelsat, rasterio, geopandas; print('패키지 설치 성공!')"
```

### 2. 프로젝트 구조 확인

```bash
# 디렉토리 구조 확인
ls -la  # Linux/macOS
dir     # Windows

# 필요한 디렉토리가 모두 있는지 확인:
# - src/
# - configs/
# - data/
# - outputs/
# - logs/
# - notebooks/
```

### 3. 설정 파일 로드 테스트

```python
python -c "from src.config import get_config; config = get_config(); print('설정 로드 성공!')"
```

### 4. 데이터 검색 테스트

```bash
# 간단한 검색 실행 (다운로드 없음)
python run_data_search.py --start-date 2024-01-01 --end-date 2024-01-31
```

## 문제 해결

### 문제 1: sentinelsat 설치 오류

```bash
# 해결책: 개별 설치 시도
pip install sentinelsat --no-cache-dir
```

### 문제 2: rasterio/GDAL 설치 오류

**Windows:**
```bash
# Conda 사용 (권장)
conda install -c conda-forge rasterio
```

**Linux/macOS:**
```bash
# GDAL 라이브러리 먼저 설치
# Ubuntu/Debian
sudo apt-get install gdal-bin libgdal-dev

# macOS
brew install gdal

# 그 후 rasterio 설치
pip install rasterio
```

### 문제 3: geopandas 설치 오류

```bash
# Conda 환경에서
conda install -c conda-forge geopandas

# 또는 pip으로
pip install geopandas --no-build-isolation
```

### 문제 4: API 연결 오류

```
sentinelsat.sentinel.SentinelAPIError: HTTP status 401 Unauthorized
```

**해결책**:
1. `credentials.yaml` 파일의 계정 정보 재확인
2. Copernicus 웹사이트에서 로그인 가능한지 확인
3. 계정이 활성화되었는지 확인 (신규 계정은 24시간 소요)

### 문제 5: 디스크 공간 부족

```
OSError: [Errno 28] No space left on device
```

**해결책**:
1. `configs/config.yaml`에서 데이터 저장 경로 변경:
```yaml
paths:
  data_dir: "/path/to/large/storage/data"
  output_dir: "/path/to/large/storage/outputs"
```

### 문제 6: 메모리 부족

```
MemoryError
```

**해결책**:
1. 처리하는 데이터 개수 줄이기 (`--max-products` 옵션 사용)
2. `configs/config.yaml`에서 multilook 파라미터 증가 (해상도 낮추기)

## 추가 리소스

- **Sentinelsat 문서**: https://sentinelsat.readthedocs.io/
- **Rasterio 문서**: https://rasterio.readthedocs.io/
- **GeoPandas 문서**: https://geopandas.org/
- **프로젝트 이슈**: https://github.com/wukdddang/S1-InSAR-Pipeline-EastKorea/issues

## 다음 단계

설치가 완료되었다면:

1. **Jupyter 노트북 실습**: `notebooks/01_data_search_example.ipynb` 실행
2. **첫 데이터 다운로드**: `python run_data_search.py --download --max-products 2`
3. **설정 커스터마이징**: `configs/config.yaml` 파일 수정하여 분석 영역 조정

문제가 계속되면 [GitHub Issues](https://github.com/wukdddang/S1-InSAR-Pipeline-EastKorea/issues)에 문의해 주세요!

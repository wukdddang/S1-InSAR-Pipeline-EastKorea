# 문제 해결 가이드 (Troubleshooting)

## 연결 오류 (Connection Error)

### 문제: Copernicus 서버 연결 실패

```
ConnectionError: HTTPSConnectionPool(host='scihub.copernicus.eu', port=443):
Failed to establish a new connection
```

#### 원인

**중요**: Copernicus Open Access Hub (`scihub.copernicus.eu`)는 **2023년부터 단계적으로 종료**되고 있습니다.

- **이전 시스템**: SciHub (scihub.copernicus.eu) - ⚠️ 서비스 종료 중
- **새 시스템**: Copernicus Data Space Ecosystem (dataspace.copernicus.eu) - ✅ 운영 중

#### 해결 방법

##### 방법 1: ASF Data Search 사용 (권장 ⭐)

Alaska Satellite Facility를 통해 Sentinel-1 데이터에 접근할 수 있습니다.

**1단계: NASA Earthdata 계정 생성**

- [NASA Earthdata 회원가입](https://urs.earthdata.nasa.gov/users/new)

**2단계: ASF API 모듈 설치**

```bash
pip install asf-search
```

**3단계: ASF 데이터 검색 스크립트 사용**

ASF를 사용한 데이터 검색 예제를 제공합니다 (아래 참조).

##### 방법 2: Copernicus Data Space 사용

새로운 Copernicus Data Space Ecosystem을 사용합니다.

**1단계: 새 계정 생성**

- [Copernicus Data Space 회원가입](https://dataspace.copernicus.eu/)

**2단계: 새 API 클라이언트 설치**

```bash
pip install cdsetool
```

**참고**: 현재 프로젝트는 기존 `sentinelsat`을 사용하므로, 새 시스템으로 마이그레이션이 필요합니다.

##### 방법 3: 네트워크 문제 확인

서버가 일시적으로 다운되었을 수 있습니다.

**확인 단계:**

1. **인터넷 연결 확인**

```bash
ping google.com
```

2. **Copernicus 서버 상태 확인**

```bash
ping scihub.copernicus.eu
```

3. **방화벽/프록시 확인**

   - 회사 또는 학교 네트워크에서 HTTPS(443 포트)가 차단되었을 수 있음
   - VPN 사용 시 일시적으로 비활성화 후 시도

4. **서버 상태 페이지 확인**
   - [Copernicus 시스템 상태](https://scihub.copernicus.eu/dhus/#/home)

## ASF Data Search 사용 예제

ASF를 사용하는 데이터 검색 스크립트:

```python
import asf_search as asf
import geopandas as gpd
from shapely.geometry import box

# NASA Earthdata 인증 (최초 1회)
# asf.set_credentials('your_username', 'your_password')

# 검색 영역 설정 (포항/경주)
aoi = box(128.5, 35.5, 129.5, 36.5)

# Sentinel-1 데이터 검색
results = asf.search(
    platform=asf.PLATFORM.SENTINEL1,
    processingLevel=asf.PRODUCT_TYPE.SLC,
    start='2024-01-01',
    end='2024-01-15',
    intersectsWith=str(aoi),
    maxResults=10
)

print(f"검색 결과: {len(results)}개")

# 다운로드
# results.download(path='./data/raw', session=asf.ASFSession())
```

## 기타 문제

### Python 모듈 없음 (ModuleNotFoundError)

```
ModuleNotFoundError: No module named 'sentinelsat'
```

**해결**:

```bash
conda activate insar
pip install -r requirements.txt
```

### 날짜 형식 오류

```
ValueError: Unsupported date value
```

**해결**: 날짜는 반드시 `YYYY-MM-DD` 형식이어야 합니다.

```bash
# 올바른 형식
python run_data_search.py --start-date 2024-01-01 --end-date 2024-12-31

# 잘못된 형식
python run_data_search.py --start-date 20240101  # ❌
```

### 디스크 공간 부족

```
OSError: [Errno 28] No space left on device
```

**해결**:

1. 디스크 공간 확인: `df -h` (Linux/Mac) 또는 파일 탐색기 (Windows)
2. 불필요한 파일 삭제
3. `configs/config.yaml`에서 저장 경로를 더 큰 드라이브로 변경

### 메모리 부족

```
MemoryError
```

**해결**:

1. 다운로드 개수 제한: `--max-products 1`
2. 백그라운드 프로그램 종료
3. 시스템 RAM 업그레이드 고려

## 도움이 필요하세요?

위 해결 방법으로 문제가 해결되지 않으면:

1. [GitHub Issues](https://github.com/wukdddang/S1-InSAR-Pipeline-EastKorea/issues)에 문의
2. 다음 정보를 포함해주세요:
   - OS 및 버전
   - Python 버전
   - 전체 에러 메시지
   - 시도한 해결 방법

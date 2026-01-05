#!/usr/bin/env python
"""
ASF 다운로드 직접 테스트
"""

import os
import yaml
import asf_search as asf
from shapely.geometry import box
from pathlib import Path

print("=" * 60)
print("ASF 다운로드 테스트")
print("=" * 60)

# credentials 로드 (프로젝트 루트 기준)
project_root = Path(__file__).parent.parent
config_path = project_root / 'configs' / 'credentials.yaml'
with open(config_path, 'r', encoding='utf-8') as f:
    creds = yaml.safe_load(f)

username = str(creds['asf']['username'])
password = str(creds['asf']['password'])

# 환경 변수 설정
os.environ['EARTHDATA_USERNAME'] = username
os.environ['EARTHDATA_PASSWORD'] = password

print(f"\n✓ 인증 정보 설정 완료")
print(f"  Username: {username}")

# 검색
print("\n[1단계] 데이터 검색...")
aoi = box(128.5, 35.5, 129.5, 36.5)
results = asf.search(
    platform=asf.PLATFORM.SENTINEL1,
    processingLevel=asf.PRODUCT_TYPE.SLC,
    beamMode=asf.BEAMMODE.IW,
    start='2023-01-01',
    end='2023-01-31',
    intersectsWith=str(aoi),
    maxResults=1
)

print(f"✓ 검색 완료: {len(results)}개")

if len(results) == 0:
    print("검색 결과가 없습니다.")
    exit(0)

product = results[0]
print(f"\n제품 정보:")
print(f"  이름: {product.properties['sceneName']}")
print(f"  날짜: {product.properties['startTime']}")
print(f"  크기: {product.properties.get('bytes', 0) / (1024**3):.2f} GB")

# 다운로드 URL 확인
url = product.properties.get('url', 'N/A')
print(f"  다운로드 URL: {url}")

# 세션 생성
print("\n[2단계] 세션 생성...")
try:
    session = asf.ASFSession()
    print("✓ 세션 생성 성공")
    
    # 다운로드 시도
    print("\n[3단계] 다운로드 시도...")
    print("  경로: ./data/raw")
    print("  ⚠️  약 4GB 크기이므로 시간이 걸릴 수 있습니다...")
    
    # 실제 다운로드는 주석 처리 (테스트용)
    # product.download(path='./data/raw', session=session)
    
    print("\n  💡 실제 다운로드를 원하면 위 코드의 주석을 제거하세요")
    print("\n[대안] 수동 다운로드 방법:")
    print("  1. 브라우저에서 NASA Earthdata 로그인")
    print(f"  2. 다음 URL 접속: {url}")
    print("  3. data/raw/ 폴더에 저장")
    
except Exception as e:
    print(f"✗ 오류: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

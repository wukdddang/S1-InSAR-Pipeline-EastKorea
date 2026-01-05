#!/usr/bin/env python
"""
간단한 ASF 검색 테스트 스크립트
"""

import asf_search as asf
from shapely.geometry import box

# 포항/경주 지역
aoi = box(128.5, 35.5, 129.5, 36.5)

print("=" * 50)
print("ASF Data Search 테스트")
print("=" * 50)

# 검색 조건을 최대한 완화
print("\n1. 기본 검색 (2022년, 더 넓은 범위)")
results = asf.search(
    platform=asf.PLATFORM.SENTINEL1,
    start='2022-01-01',
    end='2022-12-31',
    intersectsWith=str(aoi),
    maxResults=10
)
print(f"   결과: {len(results)}개")

if len(results) > 0:
    print("\n   첫 번째 결과:")
    print(f"   - 제품명: {results[0].properties['sceneName']}")
    print(f"   - 날짜: {results[0].properties['startTime']}")
    print(f"   - 궤도: {results[0].properties.get('pathNumber', 'N/A')}")
else:
    print("   검색 결과가 없습니다.")

print("\n2. SLC 제품만 검색 (2022년)")
results2 = asf.search(
    platform=asf.PLATFORM.SENTINEL1,
    processingLevel=asf.PRODUCT_TYPE.SLC,
    start='2022-01-01',
    end='2022-12-31',
    intersectsWith=str(aoi),
    maxResults=10
)
print(f"   결과: {len(results2)}개")

print("\n3. 더 넓은 지역으로 검색 (서울 포함)")
wider_aoi = box(126.0, 35.0, 130.0, 38.0)
results3 = asf.search(
    platform=asf.PLATFORM.SENTINEL1,
    processingLevel=asf.PRODUCT_TYPE.SLC,
    start='2022-01-01',
    end='2022-03-31',
    intersectsWith=str(wider_aoi),
    maxResults=10
)
print(f"   결과: {len(results3)}개")

if len(results3) > 0:
    print("\n   첫 번째 결과:")
    print(f"   - 제품명: {results3[0].properties['sceneName']}")
    print(f"   - 날짜: {results3[0].properties['startTime']}")

print("\n" + "=" * 50)
print("테스트 완료!")
print("=" * 50)

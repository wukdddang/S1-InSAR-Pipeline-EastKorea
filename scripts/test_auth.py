#!/usr/bin/env python
"""
ASF 인증 테스트 스크립트
"""

import os
import asf_search as asf
from pathlib import Path

print("=" * 60)
print("ASF 인증 테스트")
print("=" * 60)

# credentials.yaml 읽기 (프로젝트 루트 기준)
import yaml
project_root = Path(__file__).parent.parent
config_path = project_root / 'configs' / 'credentials.yaml'
with open(config_path, 'r', encoding='utf-8') as f:
    creds = yaml.safe_load(f)

username = creds['asf']['username']
password = creds['asf']['password']

print(f"\n✓ credentials.yaml 로드 성공")
print(f"  Username: {username}")
print(f"  Password: {'*' * len(str(password))}")

# 방법 1: 환경 변수 설정
print("\n[방법 1] 환경 변수로 인증 시도...")
os.environ['EARTHDATA_USERNAME'] = str(username)
os.environ['EARTHDATA_PASSWORD'] = str(password)

try:
    session = asf.ASFSession()
    print("✓ 세션 생성 성공!")
    
    # 간단한 검색으로 테스트
    print("\n[테스트] 간단한 검색 실행...")
    results = asf.search(
        platform=asf.PLATFORM.SENTINEL1,
        start='2023-01-01',
        end='2023-01-31',
        maxResults=1
    )
    print(f"✓ 검색 성공: {len(results)}개 결과")
    
    if len(results) > 0:
        print(f"\n제품명: {results[0].properties['sceneName']}")
        
        # 다운로드 테스트 (실제로 다운로드하지 않고 URL만 확인)
        print("\n[다운로드 테스트] URL 확인...")
        print(f"다운로드 URL: {results[0].properties.get('url', 'N/A')}")
        
except Exception as e:
    print(f"✗ 오류 발생: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("테스트 완료")
print("=" * 60)

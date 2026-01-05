#!/usr/bin/env python
"""
.netrc 파일 설정 스크립트
NASA Earthdata 인증을 위한 .netrc 파일을 자동으로 생성합니다.
"""

import os
import yaml
from pathlib import Path

print("=" * 60)
print(".netrc 파일 설정")
print("=" * 60)

# credentials.yaml 읽기 (프로젝트 루트 기준)
project_root = Path(__file__).parent.parent
config_path = project_root / 'configs' / 'credentials.yaml'
with open(config_path, 'r', encoding='utf-8') as f:
    creds = yaml.safe_load(f)

username = str(creds['asf']['username'])
password = str(creds['asf']['password'])

# 홈 디렉토리 경로
home = Path.home()
netrc_path = home / '.netrc'

# .netrc 파일 내용
netrc_content = f"""machine urs.earthdata.nasa.gov
    login {username}
    password {password}
"""

print(f"\n.netrc 파일 경로: {netrc_path}")

# 기존 .netrc 파일 백업
if netrc_path.exists():
    backup_path = home / '.netrc.backup'
    print(f"⚠️  기존 .netrc 파일 발견. 백업 생성: {backup_path}")
    with open(netrc_path, 'r') as f:
        backup_content = f.read()
    with open(backup_path, 'w') as f:
        f.write(backup_content)

# .netrc 파일 생성
try:
    with open(netrc_path, 'w') as f:
        f.write(netrc_content)
    
    # Windows가 아닌 경우 권한 설정
    if os.name != 'nt':
        os.chmod(netrc_path, 0o600)
        print(f"✓ 파일 권한 설정: 600")
    
    print(f"✓ .netrc 파일 생성 완료!")
    print(f"\n내용:")
    print("  machine urs.earthdata.nasa.gov")
    print(f"      login {username}")
    print(f"      password {'*' * len(password)}")
    
except Exception as e:
    print(f"✗ 오류 발생: {e}")
    print("\n수동으로 설정하세요:")
    print(f"1. 파일 경로: {netrc_path}")
    print("2. 파일 내용:")
    print(netrc_content)
    if os.name != 'nt':
        print("3. 권한 설정: chmod 600 ~/.netrc")

print("\n" + "=" * 60)
print("완료! 이제 다운로드를 다시 시도하세요.")
print("=" * 60)

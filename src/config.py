"""
Configuration Management Module
설정 파일 로드 및 환경 변수 관리
"""

import os
from pathlib import Path
import yaml
from typing import Dict, Any


class Config:
    """프로젝트 설정 관리 클래스"""
    
    def __init__(self, config_path: str = None):
        """
        Args:
            config_path: config.yaml 파일 경로 (기본값: configs/config.yaml)
        """
        if config_path is None:
            self.project_root = Path(__file__).parent.parent
            config_path = self.project_root / "configs" / "config.yaml"
        else:
            config_path = Path(config_path)
            self.project_root = config_path.parent.parent
        
        self.config = self._load_yaml(config_path)
        self.credentials = self._load_credentials()
        self._setup_directories()
    
    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """YAML 파일 로드"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {file_path}")
    
    def _load_credentials(self) -> Dict[str, Any]:
        """인증 정보 로드"""
        cred_path = self.project_root / "configs" / "credentials.yaml"
        
        if not cred_path.exists():
            print(f"경고: 인증 파일이 없습니다: {cred_path}")
            print("credentials_template.yaml을 복사하여 credentials.yaml을 만들어주세요.")
            return {}
        
        return self._load_yaml(cred_path)
    
    def _setup_directories(self):
        """필요한 디렉토리 생성"""
        dirs = [
            self.get_path('data_dir'),
            self.get_path('raw_data_dir'),
            self.get_path('processed_dir'),
            self.get_path('output_dir'),
            self.get_path('log_dir'),
            self.get_path('temp_dir')
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def get_path(self, key: str) -> Path:
        """경로 설정 가져오기"""
        path_str = self.config['paths'].get(key, '')
        return self.project_root / path_str
    
    def get(self, *keys, default=None):
        """중첩된 설정 값 가져오기
        
        Example:
            config.get('sentinel1', 'platform')  # 'SENTINEL-1'
        """
        value = self.config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            if value is None:
                return default
        return value
    
    def get_credential(self, service: str) -> Dict[str, str]:
        """인증 정보 가져오기
        
        Args:
            service: 'asf' 또는 'copernicus'
        """
        return self.credentials.get(service, {})


# Global config instance
_config = None

def get_config(config_path: str = None) -> Config:
    """전역 설정 인스턴스 가져오기"""
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config

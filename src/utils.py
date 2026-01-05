"""
Utility Functions
공통 유틸리티 함수 모음
"""

import os
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Tuple
import numpy as np


def setup_logger(name: str, log_dir: Path = None) -> logging.Logger:
    """로거 설정
    
    Args:
        name: 로거 이름
        log_dir: 로그 디렉토리 경로
    
    Returns:
        설정된 Logger 객체
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(console_format)
        logger.addHandler(file_handler)
    
    return logger


def calculate_perpendicular_baseline(
    master_orbit: dict,
    slave_orbit: dict
) -> float:
    """수직 기선(Perpendicular Baseline) 계산
    
    Args:
        master_orbit: Master 영상 궤도 정보
        slave_orbit: Slave 영상 궤도 정보
    
    Returns:
        수직 기선 거리 (m)
    """
    # 실제 구현은 궤도 정보 형식에 따라 다름
    # 여기서는 placeholder
    pass


def calculate_temporal_baseline(
    date1: datetime,
    date2: datetime
) -> int:
    """시간 기선(Temporal Baseline) 계산
    
    Args:
        date1: 첫 번째 날짜
        date2: 두 번째 날짜
    
    Returns:
        날짜 차이 (일)
    """
    return abs((date2 - date1).days)


def create_interferogram_pairs(
    dates: List[datetime],
    max_temporal_baseline: int = 60,
    max_perpendicular_baseline: float = 150
) -> List[Tuple[datetime, datetime]]:
    """간섭쌍(Interferogram Pairs) 생성
    
    Args:
        dates: 영상 날짜 리스트
        max_temporal_baseline: 최대 시간 기선 (일)
        max_perpendicular_baseline: 최대 수직 기선 (m)
    
    Returns:
        간섭쌍 리스트 [(master_date, slave_date), ...]
    """
    pairs = []
    sorted_dates = sorted(dates)
    
    for i, master_date in enumerate(sorted_dates):
        for slave_date in sorted_dates[i+1:]:
            temporal_baseline = calculate_temporal_baseline(master_date, slave_date)
            
            if temporal_baseline <= max_temporal_baseline:
                pairs.append((master_date, slave_date))
    
    return pairs


def ensure_dir(directory: Path) -> Path:
    """디렉토리 생성 (없을 경우)
    
    Args:
        directory: 디렉토리 경로
    
    Returns:
        생성/확인된 디렉토리 경로
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def format_file_size(size_bytes: int) -> str:
    """파일 크기를 읽기 좋은 형식으로 변환
    
    Args:
        size_bytes: 바이트 단위 크기
    
    Returns:
        포맷팅된 문자열 (예: "1.23 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

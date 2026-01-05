"""
S1-InSAR-Pipeline-EastKorea
============================

Sentinel-1 SLC 데이터를 활용한 한반도 동남권 지표 변위 모니터링 파이프라인

Main modules:
- data_retrieval: Sentinel-1 데이터 검색 및 다운로드
- preprocessing: SAR 데이터 전처리
- insar_processing: InSAR 간섭도 생성
- time_series: SBAS 시계열 분석
- visualization: 결과 시각화
"""

__version__ = "0.1.0"
__author__ = "wukdddang"

# InSAR 처리 빠른 시작 가이드

## 1. 데이터 다운로드 (1월 & 12월)

```bash
python run_data_search.py \
  --start-date 2023-01-01 \
  --end-date 2023-12-31 \
  --months 01 12 \
  --download
```

## 2. InSAR 처리

Jupyter Notebook: `notebooks/02_insar_processing.ipynb`

실행 순서:
1. ✅ Step 1: Environment Setup
2. ✅ Step 2: Load SLC Data
3. ✅ Step 4.2: ROI 설정 (바다 제거) ⭐ NEW
4. ✅ Step 4.3: ISCE2 Configuration
5. ✅ Step 4.4: Run Processing (터미널 권장)
6. ✅ Step 5: Visualize Results

## 3. 처리 실행 (터미널)

```bash
cd data/insar_processing/output
conda activate insar
python /home/wukddang/miniconda3/envs/insar/lib/python3.9/site-packages/isce/applications/topsApp.py
```

## 주요 개선점

| 항목 | 개선 전 | 개선 후 |
|------|---------|---------|
| 시간 간격 | 12일 | 330일 (11개월) |
| 바다 처리 | 포함 | 제외 (ROI) |
| Unwrapping 오류 | 많음 | 최소화 |
| 유효 픽셀 | 11.7% | 증가 예상 |

## ROI 설정 (육지만)

```python
roi_bbox = [35.0, 36.5, 128.5, 129.3]
# [min_lat, max_lat, min_lon, max_lon]
```

- 위도: 35.0°N ~ 36.5°N
- 경도: 128.5°E ~ 129.3°E
- 동쪽 바다(동해) 제외

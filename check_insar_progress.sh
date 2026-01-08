#!/bin/bash

# ISCE2 InSAR Processing Progress Monitor
# Usage: ./check_insar_progress.sh

OUTPUT_DIR="/home/wukddang/S1-InSAR-Pipeline-EastKorea/data/insar_processing/output"
LOG_FILE="$OUTPUT_DIR/isce.log"

echo "========================================================================"
echo "ISCE2 InSAR Processing Progress Monitor"
echo "========================================================================"
echo ""

# Check if processing is running
if ps aux | grep -v grep | grep topsApp.py > /dev/null; then
    echo "✅ Status: RUNNING"
    
    # Get process info
    PID=$(ps aux | grep -v grep | grep topsApp.py | awk '{print $2}')
    CPU=$(ps aux | grep -v grep | grep topsApp.py | awk '{print $3}')
    MEM=$(ps aux | grep -v grep | grep topsApp.py | awk '{print $4}')
    TIME=$(ps aux | grep -v grep | grep topsApp.py | awk '{print $10}')
    
    echo "   PID: $PID"
    echo "   CPU: ${CPU}%"
    echo "   Memory: ${MEM}%"
    echo "   Runtime: $TIME"
else
    echo "⚠️  Status: NOT RUNNING"
fi

echo ""
echo "────────────────────────────────────────────────────────────────────────"
echo "Processing Steps:"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

# Check completed steps
declare -A STEPS=(
    ["startup"]="초기화"
    ["preprocess"]="전처리 (Burst 추출)"
    ["computeBaselines"]="Baseline 계산"
    ["verifyDEM"]="DEM 검증"
    ["topo"]="지형 정보 생성"
    ["geo2rdr"]="지오코딩 변환"
    ["coarseoffsets"]="Coarse offset 계산"
    ["coarseresamp"]="Coarse resampling"
    ["misreg"]="정합 개선"
    ["interferogram"]="간섭도 생성"
    ["filter"]="필터링"
    ["unwrap"]="Phase unwrapping"
    ["unwrap2stage"]="2단계 unwrapping"
    ["geocode"]="Geocoding"
)

STEP_ORDER=("startup" "preprocess" "computeBaselines" "verifyDEM" "topo" "geo2rdr" "coarseoffsets" "coarseresamp" "misreg" "interferogram" "filter" "unwrap" "unwrap2stage" "geocode")

CURRENT_STEP=""
STEP_NUM=0

for step in "${STEP_ORDER[@]}"; do
    STEP_NUM=$((STEP_NUM + 1))
    
    if [ -f "$OUTPUT_DIR/PICKLE/$step" ] || grep -q "run$step" "$LOG_FILE" 2>/dev/null; then
        echo "  ✅ $STEP_NUM. $step - ${STEPS[$step]}"
        CURRENT_STEP="$step"
    else
        if [ -z "$CURRENT_STEP" ]; then
            echo "  🔄 $STEP_NUM. $step - ${STEPS[$step]} (진행 중?)"
            CURRENT_STEP="$step"
            break
        else
            echo "  ⏳ $STEP_NUM. $step - ${STEPS[$step]}"
        fi
    fi
done

echo ""
echo "────────────────────────────────────────────────────────────────────────"
echo "Recent Log (last 10 lines):"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

if [ -f "$LOG_FILE" ]; then
    tail -10 "$LOG_FILE" | sed 's/^/  /'
else
    echo "  ⚠️  Log file not found"
fi

echo ""
echo "────────────────────────────────────────────────────────────────────────"
echo "Output Files:"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

if [ -d "$OUTPUT_DIR/merged" ]; then
    echo "  Merged products:"
    ls -lh "$OUTPUT_DIR/merged" 2>/dev/null | grep -v "^total" | awk '{printf "    %s  %s\n", $9, $5}' || echo "    (none yet)"
else
    echo "  ⏳ No merged products yet"
fi

echo ""
echo "========================================================================"
echo "💡 TIP: Run 'tail -f $LOG_FILE' to watch live progress"
echo "========================================================================"

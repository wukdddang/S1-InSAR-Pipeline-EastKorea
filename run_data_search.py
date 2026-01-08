#!/usr/bin/env python
"""
Sentinel-1 데이터 검색 실행 스크립트
ASF Data Search를 통한 데이터 검색 및 다운로드
"""

import argparse
from src.data_retrieval import Sentinel1Retriever
from rich.console import Console

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Sentinel-1 SLC 데이터 검색 및 다운로드"
    )
    
    parser.add_argument(
        '--start-date',
        type=str,
        help='시작 날짜 (YYYY-MM-DD)',
        default='2023-01-01'
    )
    
    parser.add_argument(
        '--end-date',
        type=str,
        help='종료 날짜 (YYYY-MM-DD)',
        default='2023-12-31'
    )
    
    parser.add_argument(
        '--download',
        action='store_true',
        help='검색 후 자동 다운로드'
    )
    
    parser.add_argument(
        '--max-products',
        type=int,
        default=None,
        help='최대 다운로드 개수 (기본값: 전체)'
    )
    
    parser.add_argument(
        '--max-results',
        type=int,
        default=100,
        help='최대 검색 결과 수 (기본값: 100)'
    )
    
    parser.add_argument(
        '--pair',
        action='store_true',
        help='InSAR용 영상 쌍 검색 모드 (같은 프레임의 2개 영상)'
    )
    
    parser.add_argument(
        '--temporal-baseline',
        type=int,
        default=12,
        help='영상 쌍 시간 간격 (일 단위, 기본값: 12일)'
    )
    
    parser.add_argument(
        '--months',
        type=str,
        nargs=2,
        metavar=('MONTH1', 'MONTH2'),
        help='특정 월의 영상 검색 (예: --months 01 12)'
    )
    
    args = parser.parse_args()
    
    console.print("[bold cyan]====================================[/bold cyan]")
    console.print("[bold cyan]Sentinel-1 데이터 검색 시스템[/bold cyan]")
    console.print("[bold cyan]====================================[/bold cyan]\n")
    console.print("[yellow]ASF Data Search 사용 중...[/yellow]\n")
    
    # 검색 실행
    retriever = Sentinel1Retriever()
    
    console.print(f"[green]검색 기간: {args.start_date} ~ {args.end_date}[/green]")
    
    if args.months:
        # 월별 영상 검색 모드
        import pandas as pd
        from datetime import datetime
        
        console.print(f"[bold cyan]월별 영상 검색: {args.months[0]}월과 {args.months[1]}월[/bold cyan]\n")
        
        # 연도 추출
        year = args.start_date.split('-')[0]
        month1, month2 = args.months[0].zfill(2), args.months[1].zfill(2)
        
        # 1월 검색
        month1_start = f"{year}-{month1}-01"
        month1_end = f"{year}-{month1}-28"
        console.print(f"🔍 {month1}월 영상 검색: {month1_start} ~ {month1_end}")
        products_df1 = retriever.search_products(
            start_date=month1_start,
            end_date=month1_end,
            max_results=50
        )
        
        # 12월 검색
        month2_start = f"{year}-{month2}-01"
        month2_end = f"{year}-{month2}-28"
        console.print(f"🔍 {month2}월 영상 검색: {month2_start} ~ {month2_end}")
        products_df2 = retriever.search_products(
            start_date=month2_start,
            end_date=month2_end,
            max_results=50
        )
        
        if products_df1.empty or products_df2.empty:
            console.print("[bold red]❌ 한 쪽 또는 양쪽 월의 영상을 찾을 수 없습니다.[/bold red]")
            return
        
        # 같은 촬영 시간대의 영상 찾기
        products_df1['time'] = pd.to_datetime(products_df1['date']).dt.strftime('%H:%M')
        products_df2['time'] = pd.to_datetime(products_df2['date']).dt.strftime('%H:%M')
        
        # 가장 많은 영상이 있는 시간대
        all_times = pd.concat([products_df1['time'], products_df2['time']])
        most_common_time = all_times.value_counts().idxmax()
        
        # 해당 시간대로 필터링
        df1_filtered = products_df1[products_df1['time'] == most_common_time]
        df2_filtered = products_df2[products_df2['time'] == most_common_time]
        
        if df1_filtered.empty or df2_filtered.empty:
            console.print(f"[yellow]⚠️  촬영 시간 {most_common_time}에 맞는 영상이 부족합니다.[/yellow]")
            df1_filtered = products_df1
            df2_filtered = products_df2
        
        # 크기가 비슷한 영상 선택
        median_size = pd.concat([df1_filtered['size_mb'], df2_filtered['size_mb']]).median()
        
        img1 = df1_filtered.iloc[(df1_filtered['size_mb'] - median_size).abs().argsort()[0]]
        img2 = df2_filtered.iloc[(df2_filtered['size_mb'] - median_size).abs().argsort()[0]]
        
        products_df = pd.DataFrame([img1, img2])
        
        # 시간 간격 계산
        date1 = pd.to_datetime(img1['date'])
        date2 = pd.to_datetime(img2['date'])
        temporal_baseline = abs((date2 - date1).days)
        
        console.print("\n[bold green]" + "="*80 + "[/bold green]")
        console.print("[bold green]✅ 월별 영상 쌍 검색 완료![/bold green]")
        console.print("[bold green]" + "="*80 + "[/bold green]\n")
        console.print(f"📅 선택된 영상 쌍:")
        console.print(f"  - {month1}월: {img1['date'].split('T')[0]} (Track {img1['track']}, {img1['size_mb']:.0f} MB)")
        console.print(f"  - {month2}월: {img2['date'].split('T')[0]} (Track {img2['track']}, {img2['size_mb']:.0f} MB)")
        console.print(f"  - 시간 간격: {temporal_baseline}일 (~{temporal_baseline/30:.1f}개월)")
        console.print(f"  - 촬영 시간: {most_common_time}")
        
        if not args.download:
            console.print("\n💡 다운로드하려면:")
            console.print(f"  python run_data_search.py --start-date {args.start_date} --end-date {args.end_date} --months {args.months[0]} {args.months[1]} --download")
        
        console.print("\n[bold green]" + "="*80 + "[/bold green]")
        
    elif args.pair:
        # InSAR 영상 쌍 검색 모드
        console.print(f"[cyan]영상 쌍 모드: 시간 간격 {args.temporal_baseline}일[/cyan]\n")
        products_df = retriever.search_image_pair(
            start_date=args.start_date,
            end_date=args.end_date,
            temporal_baseline_days=args.temporal_baseline,
            max_results=args.max_results
        )
    else:
        # 일반 검색 모드
        console.print()
        products_df = retriever.search_products(
            start_date=args.start_date,
            end_date=args.end_date,
            max_results=args.max_results
        )
    
    # 결과 출력
    retriever.display_products(products_df)
    
    # 다운로드 옵션
    if args.download and not products_df.empty:
        console.print("\n[yellow]데이터 다운로드를 시작합니다...[/yellow]")
        downloaded = retriever.download_products(
            products_df,
            max_products=args.max_products
        )
        console.print(f"\n[green]✓ 다운로드 완료: {len(downloaded)}개 파일[/green]")
    elif not args.download and not products_df.empty:
        console.print("\n[yellow]💡 Tip: 다운로드하려면 --download 옵션을 추가하세요[/yellow]")
        console.print("[yellow]   예: python run_data_search.py --download --max-products 2[/yellow]")


if __name__ == "__main__":
    main()

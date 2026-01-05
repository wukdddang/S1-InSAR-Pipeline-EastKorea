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
    
    args = parser.parse_args()
    
    console.print("[bold cyan]====================================[/bold cyan]")
    console.print("[bold cyan]Sentinel-1 데이터 검색 시스템[/bold cyan]")
    console.print("[bold cyan]====================================[/bold cyan]\n")
    console.print("[yellow]ASF Data Search 사용 중...[/yellow]\n")
    
    # 검색 실행
    retriever = Sentinel1Retriever()
    
    console.print(f"[green]검색 기간: {args.start_date} ~ {args.end_date}[/green]\n")
    
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

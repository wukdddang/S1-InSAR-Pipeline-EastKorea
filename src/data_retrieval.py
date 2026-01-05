"""
Sentinel-1 Data Retrieval Module
ASF (Alaska Satellite Facility)를 통한 Sentinel-1 데이터 검색 및 다운로드
"""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import logging

try:
    import asf_search as asf
except ImportError:
    print("⚠️ asf-search 패키지가 설치되지 않았습니다.")
    print("설치 명령: pip install asf-search")
    asf = None

from shapely.geometry import box
import pandas as pd
from rich.console import Console
from rich.table import Table

from .config import get_config

console = Console()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sentinel1Retriever:
    """Sentinel-1 데이터 검색 및 다운로드 클래스 (ASF Data Search 사용)"""
    
    def __init__(self, config_path: str = None):
        """
        Args:
            config_path: 설정 파일 경로
        """
        if asf is None:
            raise ImportError(
                "asf-search 패키지가 필요합니다.\n"
                "설치: pip install asf-search"
            )
        
        self.config = get_config(config_path)
        self.session = None
        self._init_session()
    
    def _init_session(self):
        """ASF 세션 초기화"""
        credentials = self.config.get_credential('asf')
        
        if not credentials or not credentials.get('username'):
            logger.warning("ASF 인증 정보가 설정되지 않았습니다.")
            logger.warning("credentials.yaml 파일을 설정해주세요.")
            logger.info("검색은 가능하지만, 다운로드를 위해서는 인증이 필요합니다.")
            self.session = None
            return
        
        try:
            # 환경 변수로 인증 정보 설정 (asf-search가 자동으로 사용)
            os.environ['EARTHDATA_USERNAME'] = credentials['username']
            os.environ['EARTHDATA_PASSWORD'] = credentials['password']
            
            # ASF 세션 생성
            self.session = asf.ASFSession()
            logger.info("ASF 세션 초기화 성공 (환경 변수 사용)")
        except Exception as e:
            logger.error(f"ASF 세션 초기화 실패: {e}")
            logger.info("검색은 계속 진행하지만, 다운로드는 불가능합니다.")
            self.session = None
    
    def get_aoi_wkt(self) -> str:
        """분석 영역(AOI) WKT 생성"""
        aoi_config = self.config.get('aoi')
        bbox = box(
            aoi_config['min_lon'],
            aoi_config['min_lat'],
            aoi_config['max_lon'],
            aoi_config['max_lat']
        )
        return str(bbox)
    
    def search_products(
        self,
        start_date: str = None,
        end_date: str = None,
        max_results: int = 100
    ) -> pd.DataFrame:
        """Sentinel-1 제품 검색
        
        Args:
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            max_results: 최대 검색 결과 수
        
        Returns:
            검색된 제품 정보 DataFrame
        """
        # 날짜 설정
        if start_date is None:
            start_date = self.config.get('sentinel1', 'date_range', 'start')
        if end_date is None:
            end_date = self.config.get('sentinel1', 'date_range', 'end')
        
        # 검색 영역
        aoi_wkt = self.get_aoi_wkt()
        
        logger.info(f"검색 중: {start_date} ~ {end_date}")
        logger.info(f"영역: {self.config.get('aoi', 'name')}")
        
        try:
            # ASF 검색 (orbit direction 제외하여 더 많은 결과 검색)
            results = asf.search(
                platform=asf.PLATFORM.SENTINEL1,
                processingLevel=asf.PRODUCT_TYPE.SLC,
                beamMode=asf.BEAMMODE.IW,
                # flightDirection 제거 - ASCENDING과 DESCENDING 모두 검색
                start=start_date,
                end=end_date,
                intersectsWith=aoi_wkt,
                maxResults=max_results
            )
            
            logger.info(f"검색 조건: Sentinel-1 SLC, IW 모드, 모든 궤도 방향")
            
            logger.info(f"검색 완료: {len(results)}개 제품 발견")
            
            # DataFrame으로 변환
            products_data = []
            for result in results:
                products_data.append({
                    'title': result.properties['sceneName'],
                    'date': result.properties['startTime'],
                    'orbit': result.properties.get('pathNumber', 'N/A'),
                    'size_mb': result.properties.get('bytes', 0) / (1024**2),
                    'url': result.properties.get('url', ''),
                    'product': result
                })
            
            return pd.DataFrame(products_data)
            
        except Exception as e:
            logger.error(f"검색 실패: {e}")
            return pd.DataFrame()
    
    def display_products(self, products_df: pd.DataFrame):
        """검색된 제품 정보 출력"""
        if products_df.empty:
            console.print("[yellow]검색된 제품이 없습니다.[/yellow]")
            return
        
        table = Table(title="Sentinel-1 검색 결과 (ASF)")
        table.add_column("No.", style="cyan")
        table.add_column("날짜", style="green")
        table.add_column("궤도", style="yellow")
        table.add_column("크기 (MB)", style="magenta")
        table.add_column("제품명", style="blue")
        
        for idx, row in products_df.iterrows():
            table.add_row(
                str(idx + 1),
                str(row['date'])[:10] if pd.notna(row['date']) else 'N/A',
                str(row['orbit']),
                f"{row['size_mb']:.2f}",
                row['title'][:50] + "..." if len(row['title']) > 50 else row['title']
            )
        
        console.print(table)
    
    def download_products(
        self,
        products_df: pd.DataFrame,
        max_products: int = None
    ) -> List[str]:
        """제품 다운로드
        
        Args:
            products_df: 다운로드할 제품 DataFrame
            max_products: 최대 다운로드 개수
        
        Returns:
            다운로드된 파일 경로 리스트
        """
        if self.session is None:
            logger.error("ASF 세션이 초기화되지 않았습니다.")
            logger.error("credentials.yaml에 ASF 인증 정보를 설정하세요.")
            return []
        
        download_dir = self.config.get_path('raw_data_dir')
        download_dir.mkdir(parents=True, exist_ok=True)
        
        if max_products:
            products_df = products_df.head(max_products)
        
        downloaded_files = []
        
        for idx, row in products_df.iterrows():
            logger.info(f"다운로드 중 ({idx + 1}/{len(products_df)}): {row['title']}")
            
            try:
                product = row['product']
                
                # 환경 변수가 설정되어 있는지 재확인
                if 'EARTHDATA_USERNAME' not in os.environ:
                    credentials = self.config.get_credential('asf')
                    os.environ['EARTHDATA_USERNAME'] = str(credentials['username'])
                    os.environ['EARTHDATA_PASSWORD'] = str(credentials['password'])
                    logger.info("환경 변수 재설정 완료")
                
                # 다운로드 (세션 전달)
                product.download(path=str(download_dir), session=self.session)
                
                # 다운로드된 파일 경로 추정
                file_path = download_dir / f"{row['title']}.zip"
                downloaded_files.append(str(file_path))
                logger.info(f"다운로드 완료: {file_path}")
            except Exception as e:
                logger.error(f"다운로드 실패: {e}")
                logger.error(f"상세 오류 정보: {type(e).__name__}")
                
                # 대안: wget으로 다운로드 URL 안내
                if hasattr(product, 'properties'):
                    url = product.properties.get('url', '')
                    if url:
                        logger.info(f"대안: 다음 URL에서 수동 다운로드 가능")
                        logger.info(f"  {url}")
        
        return downloaded_files


def main():
    """메인 실행 함수"""
    console.print("[bold blue]Sentinel-1 데이터 검색 시작[/bold blue]")
    console.print("[yellow]ASF Data Search를 통해 데이터를 검색합니다.[/yellow]\n")
    
    try:
        retriever = Sentinel1Retriever()
        
        # 제품 검색
        products_df = retriever.search_products(
            start_date='2024-01-01',
            end_date='2024-01-31',
            max_results=10
        )
        
        # 결과 출력
        retriever.display_products(products_df)
        
        if not products_df.empty:
            console.print("\n[yellow]💡 다운로드하려면 download_products() 메서드를 호출하세요.[/yellow]")
    
    except ImportError as e:
        console.print(f"[red]오류: {e}[/red]")
    except Exception as e:
        console.print(f"[red]검색 실패: {e}[/red]")


if __name__ == "__main__":
    main()

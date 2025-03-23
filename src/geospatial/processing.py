import os
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from tqdm import tqdm

def process_county(addresses: list, max_workers: int = 4) -> pd.DataFrame:
    """Batch process addresses with circular import protection"""
    from src.main import HOADetectionSystem  # Local import to break circular dependency
    
    # Force single process in test mode
    if os.getenv('TESTING'):
        return pd.DataFrame([HOADetectionSystem().analyze_address(addr) for addr in addresses])
    
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(HOADetectionSystem().analyze_address, addr): addr
            for addr in addresses
        }
        
        for future in tqdm(futures, total=len(addresses), disable=os.getenv('TESTING')):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error processing {futures[future]}: {str(e)}")
    
    return pd.DataFrame(results).dropna()

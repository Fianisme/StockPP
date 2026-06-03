import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class HolderScraper:
    """Fetches stock holder data from yfinance and Finnhub"""

    def get_major_holders(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Fetch major holders breakdown from yfinance."""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            df = stock.major_holders

            if df is None or df.empty:
                logger.warning(f"No major holders data for {ticker}")
                return None

            result = {}
            for idx, row in df.iterrows():
                val = row.iloc[0]
                key = str(idx).strip().lower()

                if 'count' in key:
                    result['institutions_count'] = int(val)
                else:
                    pct = float(val) * 100 if float(val) <= 1 else float(val)
                    if 'insider' in key:
                        result['insiders_pct'] = round(pct, 2)
                    elif 'float' in key:
                        result['float_held_pct'] = round(pct, 2)
                    elif 'institution' in key:
                        result['institutions_pct'] = round(pct, 2)

            logger.info(f"Fetched major holders for {ticker}")
            return result if result else None
        except Exception as e:
            logger.error(f"Error fetching major holders for {ticker}: {e}")
            return None

    def get_institutional_holders(self, ticker: str) -> List[Dict[str, Any]]:
        """Fetch top institutional holders from yfinance."""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            df = stock.institutional_holders

            if df is None or df.empty:
                logger.warning(f"No institutional holders data for {ticker}")
                return []

            holders = []
            for _, row in df.iterrows():
                pct_held = row.get('pctHeld', 0) or 0
                pct_val = float(pct_held) * 100 if float(pct_held) <= 1 else float(pct_held)
                holders.append({
                    'holder': str(row.get('Holder', '')),
                    'shares': int(row.get('Shares', 0)) if row.get('Shares') else 0,
                    'date_reported': str(row.get('Date Reported', '')),
                    'pct_out': round(pct_val, 2),
                    'value': int(row.get('Value', 0)) if row.get('Value') else 0,
                })

            logger.info(f"Fetched {len(holders)} institutional holders for {ticker}")
            return holders
        except Exception as e:
            logger.error(f"Error fetching institutional holders for {ticker}: {e}")
            return []

    def get_mutual_fund_holders(self, ticker: str) -> List[Dict[str, Any]]:
        """Fetch top mutual fund holders from yfinance."""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            df = stock.mutualfund_holders

            if df is None or df.empty:
                logger.warning(f"No mutual fund holders data for {ticker}")
                return []

            holders = []
            for _, row in df.iterrows():
                pct_held = row.get('pctHeld', 0) or 0
                pct_val = float(pct_held) * 100 if float(pct_held) <= 1 else float(pct_held)
                holders.append({
                    'holder': str(row.get('Holder', '')),
                    'shares': int(row.get('Shares', 0)) if row.get('Shares') else 0,
                    'date_reported': str(row.get('Date Reported', '')),
                    'pct_out': round(pct_val, 2),
                    'value': int(row.get('Value', 0)) if row.get('Value') else 0,
                })

            logger.info(f"Fetched {len(holders)} mutual fund holders for {ticker}")
            return holders
        except Exception as e:
            logger.error(f"Error fetching mutual fund holders for {ticker}: {e}")
            return []

    def get_ownership_changes(self, ticker: str) -> List[Dict[str, Any]]:
        """Derive ownership changes from yfinance institutional_holders pctChange column."""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            df = stock.institutional_holders

            if df is None or df.empty:
                logger.warning(f"No ownership changes data for {ticker}")
                return []

            changes = []
            for _, row in df.iterrows():
                pct_change = row.get('pctChange', 0) or 0
                shares = int(row.get('Shares', 0)) if row.get('Shares') else 0
                pct_val = float(pct_change) * 100 if abs(float(pct_change)) <= 1 else float(pct_change)
                change_shares = int(shares * float(pct_change) / (1 + float(pct_change))) if pct_change else 0

                changes.append({
                    'holder': str(row.get('Holder', '')),
                    'shares': shares,
                    'change': change_shares,
                    'change_pct': round(pct_val, 2),
                    'date': str(row.get('Date Reported', '')),
                    'filing_date': str(row.get('Date Reported', '')),
                })

            changes.sort(key=lambda x: abs(x['change_pct']), reverse=True)
            logger.info(f"Derived {len(changes)} ownership changes for {ticker}")
            return changes
        except Exception as e:
            logger.error(f"Error fetching ownership changes for {ticker}: {e}")
            return []

    def get_all_holder_data(self, ticker: str) -> Dict[str, Any]:
        """Fetch all holder data for a ticker."""
        ticker = ticker.upper()
        return {
            'ticker': ticker,
            'major_holders': self.get_major_holders(ticker),
            'institutional_holders': self.get_institutional_holders(ticker),
            'mutual_fund_holders': self.get_mutual_fund_holders(ticker),
            'ownership_changes': self.get_ownership_changes(ticker),
        }

-- =====================================================
-- Stock Holders Table Schema
-- Jalankan di Supabase SQL Editor
-- =====================================================

-- Pastikan tickers table ada (parent)
CREATE TABLE IF NOT EXISTS public.tickers (
    symbol TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    sector TEXT,
    country TEXT DEFAULT 'US',
    is_active BOOLEAN DEFAULT true,
    last_trained_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed tickers jika kosong
INSERT INTO public.tickers (symbol, name, sector, country) VALUES
    ('AAPL', 'Apple Inc.', 'Technology', 'US'),
    ('MSFT', 'Microsoft Corporation', 'Technology', 'US'),
    ('NVDA', 'NVIDIA Corporation', 'Technology', 'US'),
    ('TSLA', 'Tesla Inc.', 'Automotive', 'US'),
    ('GOOGL', 'Alphabet Inc.', 'Technology', 'US'),
    ('BBCA.JK', 'Bank Central Asia', 'Finance', 'ID'),
    ('PLTR', 'Palantir Technologies', 'Technology', 'US'),
    ('AMD', 'Advanced Micro Devices', 'Technology', 'US')
ON CONFLICT (symbol) DO NOTHING;

-- Tabel stock_holders
CREATE TABLE IF NOT EXISTS public.stock_holders (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  ticker text NOT NULL,
  major_holders jsonb,
  institutional_holders jsonb,
  mutual_fund_holders jsonb,
  ownership_changes jsonb,
  last_fetched_at timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  CONSTRAINT stock_holders_pkey PRIMARY KEY (id),
  CONSTRAINT stock_holders_ticker_fkey FOREIGN KEY (ticker) REFERENCES public.tickers(symbol) ON DELETE CASCADE,
  CONSTRAINT stock_holders_ticker_unique UNIQUE (ticker)
);

CREATE INDEX IF NOT EXISTS idx_stock_holders_ticker ON public.stock_holders(ticker);
CREATE INDEX IF NOT EXISTS idx_stock_holders_last_fetched ON public.stock_holders(last_fetched_at);

ALTER TABLE public.stock_holders ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow read stock_holders" ON public.stock_holders;
CREATE POLICY "Allow read stock_holders" ON public.stock_holders FOR SELECT USING (true);

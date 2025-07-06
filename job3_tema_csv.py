# job3: TEMA CSV展開（毎日午前2時にRenderで自動実行）
import pandas as pd
import re
from datetime import datetime

def parse_stays(stay_txt):
    items = re.findall(r'\[([^\[\]]+)\]', str(stay_txt))
    return [(items[i], int(items[i+1].replace(',', '').replace('¥', ''))) for i in range(0, len(items), 2)]

def get_stay_month(date_str):
    try:
        dt = pd.to_datetime(date_str)
        return dt.strftime("%Y-%m")
    except:
        return ""

def get_lt(stay_day, reserve_day):
    try:
        d1 = pd.to_datetime(stay_day)
        d2 = pd.to_datetime(reserve_day)
        return (d1 - d2).days
    except:
        return None

def process_tema_csv():
    df = pd.read_csv("input/RAW_TEMA.csv", encoding="utf-8-sig")
    records = []
    for _, row in df.iterrows():
        stays = parse_stays(row.get("連泊情報", ""))
        reserve_raw = row.get("予約日時")
        reserve_day = pd.to_datetime(reserve_raw, errors='coerce')
        for stay_date, price in stays:
            stay_day = pd.to_datetime(stay_date, errors='coerce')
            records.append({
                "予約日": reserve_day.date() if pd.notna(reserve_day) else "",
                "宿泊日": stay_day.date() if pd.notna(stay_day) else "",
                "宿泊月": get_stay_month(stay_date),
                "金額": price,
                "LT": get_lt(stay_date, reserve_day)
            })
    df_out = pd.DataFrame(records)
    df_out.to_csv("output/RAW_TEMA_A.csv", index=False, encoding="utf-8-sig")
    print("✅ TEMA CSV展開 完了")

if __name__ == "__main__":
    process_tema_csv()

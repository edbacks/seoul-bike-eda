import os
import pandas as pd

# ✅ 여기만 네 원본 CSV 경로로 맞추면 됨
RAW_PATH = r"/Users/apple/Desktop/SEOUL_BIKE_PROJECT/서울특별시 공공자전거 대여이력 정보_2512.csv"

OUT_DIR = "data"
OUT_PARQUET = os.path.join(OUT_DIR, "processed_2512.parquet")

USECOLS = ["대여일시", "이용시간(분)", "이용거리(M)"]

MAX_MINUTES = 300
MAX_METERS = 50_000

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("==[1/6] 원본 로드==")
    df = pd.read_csv(
        RAW_PATH,
        encoding="cp949",
        na_values=["\\N"],
        usecols=USECOLS
    )
    print(f"원본 행 수: {len(df):,}")

    print("==[2/6] 타입 변환==")
    df["대여일시"] = pd.to_datetime(df["대여일시"], errors="coerce")
    df["이용시간(분)"] = pd.to_numeric(df["이용시간(분)"], errors="coerce")
    df["이용거리(M)"] = pd.to_numeric(df["이용거리(M)"], errors="coerce")

    print("==[3/6] 필수 결측 제거==")
    before = len(df)
    df = df.dropna(subset=["대여일시", "이용시간(분)", "이용거리(M)"])
    print(f"{before:,} -> {len(df):,}")

    print("==[4/6] 중복 제거==")
    before = len(df)
    df = df.drop_duplicates()
    print(f"{before:,} -> {len(df):,}")

    print("==[5/6] 이상치 제거==")
    before = len(df)
    df = df[(df["이용시간(분)"] >= 0) & (df["이용시간(분)"] <= MAX_MINUTES)]
    df = df[(df["이용거리(M)"] >= 0) & (df["이용거리(M)"] <= MAX_METERS)]
    print(f"{before:,} -> {len(df):,}")

    print("==[6/6] 파생변수 생성 + 저장==")
    df["weekday"] = df["대여일시"].dt.dayofweek
    df["hour"] = df["대여일시"].dt.hour
    df["is_weekend"] = df["weekday"].isin([5, 6])

    df.to_parquet(OUT_PARQUET, index=False)
    print("저장 완료:", OUT_PARQUET)

if __name__ == "__main__":
    main()
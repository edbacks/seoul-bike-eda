print("RUNNING analysis.py")
import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("images", exist_ok=True)

# 1️⃣ 전처리된 데이터 불러오기
df = pd.read_parquet("data/processed_2512.parquet")

print("데이터 로드 완료")
print("행 개수:", len(df))

# -----------------------------
# 2️⃣ 시간대별 대여건수
# -----------------------------
hour_count = df.groupby("hour").size()

plt.figure()
plt.plot(hour_count.index, hour_count.values)
plt.title("Hourly Rental Count")
plt.xlabel("Hour")
plt.ylabel("Count")
plt.xticks(range(0, 24))

plt.savefig("images/hourly_rental.png", dpi=300, bbox_inches="tight")
plt.show()


# -----------------------------
# 3️⃣ 요일별 대여건수
# -----------------------------
weekday_count = df.groupby("weekday").size()

plt.figure()
plt.bar(weekday_count.index, weekday_count.values)
plt.title("Weekday Rental Count (Mon=0 ... Sun=6)")
plt.xlabel("Weekday")
plt.ylabel("Count")
plt.xticks(range(0, 7))
plt.show()


# -----------------------------
# 4️⃣ 주말 vs 평일 비교
# -----------------------------
weekend_count = df.groupby("is_weekend").size()

plt.figure()
plt.bar(["Weekday(False)", "Weekend(True)"], weekend_count.values)
plt.title("Weekend vs Weekday Rental Count")
plt.ylabel("Count")
plt.show()


# -----------------------------
# 5️⃣ 이용시간 분포
# -----------------------------
plt.figure()
plt.hist(df["이용시간(분)"], bins=60)
plt.title("Trip Duration (min) Distribution")
plt.xlabel("Minutes")
plt.ylabel("Count")
plt.show()


# -----------------------------
# 6️⃣ 이용거리 분포
# -----------------------------
plt.figure()
plt.hist(df["이용거리(M)"], bins=60)
plt.title("Trip Distance (m) Distribution")
plt.xlabel("Meters")
plt.ylabel("Count")
plt.show()


# -----------------------------
# 7️⃣ 히트맵 (요일 x 시간)
# -----------------------------
heat = df.groupby(["weekday", "hour"]).size().unstack(fill_value=0)

plt.figure()
plt.imshow(heat, aspect="auto")
plt.title("Heatmap: Weekday x Hour Rental Count")
plt.xlabel("Hour")
plt.ylabel("Weekday (Mon=0 ... Sun=6)")
plt.colorbar(label="Count")
plt.show()
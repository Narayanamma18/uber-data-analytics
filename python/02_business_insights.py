
import pandas as pd

df = pd.read_csv("data/archive/ncr_ride_bookings.csv")

print("=" * 45)
print("RIDE BOOKING BUSINESS INSIGHTS")
print("=" * 45)

# 1. Booking status distribution
print("\n1. BOOKING STATUS")
print(
    df["Booking Status"]
    .value_counts()
    .to_string()
)

# 2. Booking status percentages
print("\n2. BOOKING STATUS PERCENTAGES")
print(
    (df["Booking Status"].value_counts(normalize=True) * 100)
    .round(2)
    .to_string()
)

# 3. Top pickup locations
print("\n3. TOP 5 PICKUP LOCATIONS")
print(df["Pickup Location"].value_counts().head(5).to_string())

# 4. Top drop locations
print("\n4. TOP 5 DROP LOCATIONS")
print(df["Drop Location"].value_counts().head(5).to_string())

# 5. Vehicle type demand
print("\n5. BOOKINGS BY VEHICLE TYPE")
print(df["Vehicle Type"].value_counts().to_string())

# 6. Ride distance
print("\n6. RIDE DISTANCE SUMMARY")
print(pd.to_numeric(df["Ride Distance"], errors="coerce").describe().round(2))

print("\nReport generated successfully.")


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------
# 1. Setup
# ---------------------------------------

df = pd.read_csv("data/archive/ncr_ride_bookings.csv")

OUTPUT_DIR = "visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

# Convert numeric columns safely
for col in ["Ride Distance", "Booking Value",
            "Customer Rating", "Driver Ratings"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Convert date and time
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Time"] = pd.to_datetime(
    df["Time"],format="mixed", errors="coerce"
)
print("Missing or unparsed times:", df["Time"].isna().sum())
print("Valid time records:", df["Time"].notna().sum())

# Completed rides
completed = df[
    df["Booking Status"].astype(str).str.strip().str.lower()
    == "completed"
].copy()

print("Total records:", len(df))
print("Completed rides:", len(completed))

# ---------------------------------------
# 2. Booking Status Distribution
# ---------------------------------------

status = df["Booking Status"].value_counts()

plt.figure(figsize=(10, 6))
sns.barplot(x=status.index, y=status.values)
plt.title("Ride Booking Status Distribution")
plt.xlabel("Booking Status")
plt.ylabel("Number of Bookings")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_booking_status.png", dpi=300)
plt.close()

# ---------------------------------------
# 3. Hourly Booking Demand
# ---------------------------------------

df["Hour"] = df["Time"].dt.hour

hourly = (
    df["Hour"].value_counts()
    .reindex(range(24), fill_value=0)
    .sort_index()
)

plt.figure(figsize=(12, 6))
sns.lineplot(x=hourly.index, y=hourly.values, marker="o")
plt.title("Hourly Ride Booking Demand")
plt.xlabel("Hour of Day (24-hour format)")
plt.ylabel("Number of Bookings")
plt.xticks(range(24))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_hourly_demand.png", dpi=300)
plt.close()

# ---------------------------------------
# 4. Top 10 Pickup Locations
# ---------------------------------------

pickup = df["Pickup Location"].value_counts().head(10)

plt.figure(figsize=(12, 7))
sns.barplot(x=pickup.values, y=pickup.index)
plt.title("Top 10 Pickup Locations")
plt.xlabel("Number of Bookings")
plt.ylabel("Pickup Location")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_top_pickup_locations.png", dpi=300)
plt.close()

# ---------------------------------------
# 5. Top 10 Drop Locations
# ---------------------------------------

drop = df["Drop Location"].value_counts().head(10)

plt.figure(figsize=(12, 7))
sns.barplot(x=drop.values, y=drop.index)
plt.title("Top 10 Drop Locations")
plt.xlabel("Number of Bookings")
plt.ylabel("Drop Location")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_top_drop_locations.png", dpi=300)
plt.close()

# ---------------------------------------
# 6. Vehicle Type Performance
# ---------------------------------------

vehicle = completed.groupby("Vehicle Type").agg(
    Completed_Rides=("Booking ID", "count"),
    Average_Distance=("Ride Distance", "mean"),
    Average_Booking_Value=("Booking Value", "mean")
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.barplot(
    data=vehicle,
    x="Vehicle Type",
    y="Completed_Rides",
    ax=axes[0]
)
axes[0].set_title("Completed Rides by Vehicle Type")
axes[0].tick_params(axis="x", rotation=35)

sns.barplot(
    data=vehicle,
    x="Vehicle Type",
    y="Average_Booking_Value",
    ax=axes[1]
)
axes[1].set_title("Average Booking Value by Vehicle Type")
axes[1].tick_params(axis="x", rotation=35)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_vehicle_performance.png", dpi=300)
plt.close()

# ---------------------------------------
# 7. Payment Method Analysis
# ---------------------------------------

payment = completed["Payment Method"].value_counts()

plt.figure(figsize=(10, 6))
sns.barplot(x=payment.index, y=payment.values)
plt.title("Completed Rides by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Completed Rides")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_payment_methods.png", dpi=300)
plt.close()

# ---------------------------------------
# 8. Cancellation Reasons
# ---------------------------------------

reason_columns = [
    "Driver Cancellation Reason",
    "Reason for cancelling by Customer"
]

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

for ax, col in zip(axes, reason_columns):
    if col in df.columns:
        reasons = (
            df.loc[df[col].notna(), col]
            .astype(str)
            .value_counts()
            .head(8)
        )

        if not reasons.empty:
            sns.barplot(x=reasons.values, y=reasons.index, ax=ax)
            ax.set_title(col)
            ax.set_xlabel("Number of Records")
            ax.set_ylabel("Reason")
        else:
            ax.set_visible(False)
    else:
        ax.set_visible(False)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/07_cancellation_reasons.png", dpi=300)
plt.close()

# ---------------------------------------
# 9. Monthly Booking Trend
# ---------------------------------------

valid_dates = df.dropna(subset=["Date"]).copy()
valid_dates["Month"] = valid_dates["Date"].dt.to_period("M").astype(str)

monthly = valid_dates.groupby("Month").size()

plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly.index, y=monthly.values, marker="o")
plt.title("Monthly Booking Trend")
plt.xlabel("Month")
plt.ylabel("Number of Bookings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/08_monthly_trend.png", dpi=300)
plt.close()

# ---------------------------------------
# 10. Customer and Driver Ratings
# ---------------------------------------

rating_columns = [
    col for col in ["Customer Rating", "Driver Ratings"]
    if col in completed.columns
]

if rating_columns:
    ratings = completed[rating_columns].melt(
        var_name="Rating Type",
        value_name="Rating"
    ).dropna()

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=ratings, x="Rating Type", y="Rating")
    plt.title("Customer and Driver Rating Distribution")
    plt.xlabel("Rating Type")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/09_rating_distribution.png", dpi=300)
    plt.close()

# ---------------------------------------
# 11. Ride Distance Distribution
# ---------------------------------------

distances = completed["Ride Distance"].dropna()

plt.figure(figsize=(10, 6))
sns.histplot(distances, bins=30, kde=True)
plt.title("Completed Ride Distance Distribution")
plt.xlabel("Ride Distance")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/10_ride_distance_distribution.png", dpi=300)
plt.close()

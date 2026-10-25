
import pandas as pd
from pathlib import Path

# Locate the project and dataset
project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "archive" / "ncr_ride_bookings.csv"

# Load the dataset
df = pd.read_csv(file_path)

# Inspect the data
print("Dataset loaded successfully!")
print("\nDataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nData types:")
print(df.dtypes)
print("\nBooking Status Counts:")
print(df["Booking Status"].value_counts())

print("\nBooking Status Percentages:")
print(
    (df["Booking Status"].value_counts(normalize=True) * 100).round(2)
)

print("\nDriver Cancellation Reasons:")
print(
    df["Driver Cancellation Reason"]
    .value_counts(dropna=False)
    .head(10)
)

print("\nCustomer Cancellation Reasons:")
print(
    df["Reason for cancelling by Customer"]
    .value_counts(dropna=False)
    .head(10)
)


print("\nCompletion Rate by Vehicle Type:")
total = df.groupby("Vehicle Type").size()
completed = df[df["Booking Status"] == "Completed"]
completed_count = completed.groupby("Vehicle Type").size()
completion_rate = (completed_count / total * 100).round(2)

print(completion_rate.sort_values(ascending=False)

cancelled = df[
    df["Booking Status"] == "Cancelled by Customer"
]

print("\nTop Customer Cancellation Reasons:")
print(
    cancelled["Reason for cancelling by Customer"]
    .dropna()
    .value_counts()
    .head()
)
driver_cancelled = df[
    df["Booking Status"] == "Cancelled by Driver"
]

print("\nTop  Driver Cancellation Reasons:")
print(
    driver_cancelled["Driver Cancellation Reason"]
    .dropna()
    .value_counts()
    .head()
)
completed = (df["Booking Status"] == "Completed").sum()
total = len(df)

print("\nOverall Completion Rate:")
print(round(completed / total * 100, 2), "%")
print("\nBookings by Vehicle Type:")
print(df["Vehicle Type"].value_counts().head(5))
completed_rides = df[df["Booking Status"] == "Completed"]

print("\nAverage Ride Distance:")
print(round(completed_rides["Ride Distance"].mean(), 2), "km")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

df["Month"] = df["Date"].dt.to_period("M")

monthly_bookings = df.groupby("Month").size()

print("\nMonthly Booking Trends:")
print(monthly_bookings)

print("\nMonth with Highest Bookings:")
print(monthly_bookings.idxmax(), "-", monthly_bookings.max(), "bookings")

completed_rides = df[
    df["Booking Status"] == "Completed"
]

print("\n--- Booking Value Analysis ---")

print(
    "Total booking value of completed rides:",
    round(completed_rides["Booking Value"].sum(), 2)
)

print(
    "Average booking value per completed ride:",
    round(completed_rides["Booking Value"].mean(), 2)
)

print(
    "Median booking value:",
    round(completed_rides["Booking Value"].median(), 2)
)

print(
    "Completed rides with missing booking value:",
    completed_rides["Booking Value"].isna().sum()
)

print("\n--- Payment Method Analysis ---")

print("\nBookings by Payment Method:")
print(df["Payment Method"].value_counts(dropna=False))

print("\nCompleted Rides by Payment Method:")
completed_rides = df[
    df["Booking Status"] == "Completed"
]

print(
    completed_rides["Payment Method"].value_counts(dropna=False)
)

print("\nBooking Value by Payment Method:")
print(
    completed_rides.groupby("Payment Method")["Booking Value"]
    .agg(["count", "sum", "mean"])
    .round(2)
)

print("\n--- Rating Analysis ---")

rating_columns = [
    "Customer Rating",
    "Driver Ratings"
]

for column in rating_columns:
    if column in df.columns:
        print(f"\n{column}")
        print("Average:", round(df[column].mean(), 2))
        print("Median:", round(df[column].median(), 2))
        print("Missing values:", df[column].isna().sum())
    else:
        print(f"\nColumn not found: {column}")



print("\n--- Vehicle Type Performance ---")

completed_rides = df[
    df["Booking Status"] == "Completed"
]

vehicle_analysis = completed_rides.groupby("Vehicle Type").agg(
    Total_Rides=("Booking ID", "count"),
    Average_Distance=("Ride Distance", "mean"),
    Average_Booking_Value=("Booking Value", "mean"),
    Total_Booking_Value=("Booking Value", "sum")
)

print(vehicle_analysis.round(2))


print("\n--- Day-of-Week Demand Analysis ---")

df["Date"] = __import__("pandas").to_datetime(
    df["Date"], errors="coerce"
)

df["Day of Week"] = df["Date"].dt.day_name()

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

print("\nBookings by Day:")
print(
    df["Day of Week"]
    .value_counts()
    .reindex(day_order)
)

print("\nCompleted Rides by Day:")
completed_rides = df[
    df["Booking Status"] == "Completed"
]

print(
    completed_rides["Day of Week"]
    .value_counts()
    .reindex(day_order)
)


print("\n--- Hourly Booking Demand ---")

df["Time"] = __import__("pandas").to_datetime(
    df["Time"].astype(str),
    errors="coerce"
)

df["Hour"] = df["Time"].dt.hour

print("\nBookings by Hour:")
print(
    df["Hour"]
    .value_counts()
    .sort_index()
)

print("\nCompleted Rides by Hour:")
completed_rides = df[
    df["Booking Status"] == "Completed"
]

print(
    completed_rides["Hour"]
    .value_counts()
    .sort_index()
)



print("\n--- Data Quality Checks ---")

print("\n1. Dataset Shape:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n2. Duplicate Rows:")
print(df.duplicated().sum())

print("\n3. Missing Values by Column:")
print(df.isnull().sum())

print("\n4. Data Types:")
print(df.dtypes)

print("\n5. Invalid Numeric Values:")
for column in ["Ride Distance", "Booking Value"]:
    if column in df.columns:
        values = __import__("pandas").to_numeric(
            df[column], errors="coerce"
        )
        print(
            column,
            "| Invalid or missing values:",
            values.isna().sum(),
            "| Negative values:",
            (values < 0).sum()
        )



print("\n--- Top Pickup Locations ---")

print(
    df["Pickup Location"]
    .value_counts()
    .head(10)
)

print("\n--- Top Drop Locations ---")

print(
    df["Drop Location"]
    .value_counts()
    .head(10)
)

print("\n--- Completed Rides by Pickup Location ---")

completed_rides = df[
    df["Booking Status"] == "Completed"
]

print(
    completed_rides["Pickup Location"]
    .value_counts()
    .head(10)
)

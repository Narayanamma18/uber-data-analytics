
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Ride Booking Analytics",
    page_icon="🚕",
    layout="wide"
)

st.title("🚕 Ride Booking Analytics Dashboard")
st.caption("Business insights from ride-booking data")

# Locate the CSV relative to this app.py file
DATA_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "archive"
    / "ncr_ride_bookings.csv"
)

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(str(DATA_PATH))
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

# Clean column names by removing extra spaces
df.columns = df.columns.str.strip()




# Prepare numeric columns safely
for col in [
    "Booking Value", "Ride Distance", "Customer Rating",
    "Driver Ratings", "Avg VTAT", "Avg CTAT"
]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

if "Booking Status" not in df.columns:
    st.error("The dataset does not contain a 'Booking Status' column.")
    st.stop()



# Sidebar filters
st.sidebar.header("Filters")

statuses = sorted(
    df["Booking Status"].dropna().unique().tolist()
)
vehicles = sorted(
    df["Vehicle Type"].dropna().unique().tolist()
)

selected_status = st.sidebar.selectbox(
    "Select Booking Status",
    ["All"] + statuses,
    key="status_filter"
)

selected_vehicle = st.sidebar.selectbox(
    "Select Vehicle Type",
    ["All"] + vehicles,
    key="vehicle_filter"
)

# Apply filters
filtered = df.copy()

if selected_status != "All":
    filtered = filtered[
        filtered["Booking Status"] == selected_status
    ]

if selected_vehicle != "All":
    filtered = filtered[
        filtered["Vehicle Type"] == selected_vehicle
    ]

st.sidebar.write("Filtered bookings:", len(filtered))



# Date Range Filter

# Convert booking date to datetime
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

st.sidebar.subheader("📅 Date Filter")

min_date = df["Date"].dropna().min().date()
max_date = df["Date"].dropna().max().date()

date_range = st.sidebar.date_input(
    "Select booking period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="booking_date_filter"
)

# Apply date filter
if len(date_range) == 2:
    start_date, end_date = date_range

    filtered = filtered[
        df.loc[filtered.index, "Date"].dt.date.between(
            start_date, end_date
        )
    ]



# KPI metrics

# 1. Total bookings based on selected filters
total_bookings = len(filtered)

# 2. Completed rides based on selected filters
status_clean = (
    filtered["Booking Status"]
    .astype(str)
    .str.strip()
    .str.lower()
)

completed = (status_clean == "completed").sum()

# 3. Cancellation rate based on ALL bookings
all_status = (
    df["Booking Status"]
    .astype(str)
    .str.strip()
    .str.lower()
)

cancellation_statuses = [
    "cancelled by customer",
    "cancelled by driver",
    "canceled by customer",
    "canceled by driver"
]

total_all_bookings = len(df)

cancelled_all = all_status.isin(
    cancellation_statuses
).sum()

cancel_rate = (
    cancelled_all / total_all_bookings * 100
    if total_all_bookings > 0
    else 0
)

# 4. Average booking value based on selected filters
if "Booking Value" in filtered.columns:
    booking_values = pd.to_numeric(
        filtered.loc[
            status_clean == "completed",
            "Booking Value"
        ],
        errors="coerce"
    ).dropna()

    avg_booking_value = (
        booking_values.mean()
        if not booking_values.empty
        else 0
    )
else:
    avg_booking_value = 0

# Display KPIs
m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Bookings", f"{total_bookings:,}")
m2.metric("Completed Rides", f"{completed:,}")
m3.metric("Overall Cancellation Rate", f"{cancel_rate:.1f}%")
m4.metric(
    "Avg. Completed Booking Value",
    f"{avg_booking_value:.2f}"
)

# Business Insights
st.subheader("📊 Business Insights")

if len(filtered) > 0:
    status_counts = (
        filtered["Booking Status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .value_counts()
    )

    top_status = status_counts.idxmax()
    top_status_count = status_counts.max()

    st.write(
        f"• Most common booking status in the selected data "
        f"is **{top_status.title()}** "
        f"({top_status_count:,} bookings)."
    )

    if "Vehicle Type" in filtered.columns:
        vehicle_counts = filtered["Vehicle Type"].value_counts()

        if not vehicle_counts.empty:
            top_vehicle = vehicle_counts.idxmax()

            st.write(
                f"• The most frequently selected vehicle type "
                f"is **{top_vehicle}**."
            )

    st.write(
        f"• The overall cancellation rate across all bookings "
        f"is **{cancel_rate:.1f}%**."
    )
else:
    st.info("No bookings match the selected filters.")



# Charts
left, right = st.columns(2)

with left:
    st.subheader("Bookings by Status")
    status_counts = filtered["Booking Status"].value_counts().reset_index()
    status_counts.columns = ["Booking Status", "Bookings"]
    fig = px.bar(
        status_counts,
        x="Booking Status",
        y="Bookings",
        color="Booking Status",
        title="Booking Status Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    if "Vehicle Type" in filtered.columns:
        st.subheader("Bookings by Vehicle Type")
        vehicle_counts = filtered["Vehicle Type"].value_counts().reset_index()
        vehicle_counts.columns = ["Vehicle Type", "Bookings"]
        fig = px.bar(
            vehicle_counts,
            x="Vehicle Type",
            y="Bookings",
            title="Vehicle Type Performance"
        )
        st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    if "Payment Method" in filtered.columns:
        st.subheader("Payment Methods")
        payment_counts = (
            filtered["Payment Method"].dropna().astype(str).str.strip()
        )
        payment_counts = payment_counts[
            ~payment_counts.str.lower().isin(["", "null", "none", "nan"])
        ].value_counts().reset_index()
        payment_counts.columns = ["Payment Method", "Bookings"]
        fig = px.pie(
            payment_counts,
            names="Payment Method",
            values="Bookings",
            title="Payment Method Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

with right:
    if "Ride Distance" in filtered.columns:
        st.subheader("Ride Distance Distribution")
        distance = filtered["Ride Distance"].dropna()
        fig = px.histogram(
            x=distance,
            nbins=30,
            labels={"x": "Ride Distance"},
            title="Distribution of Ride Distances"
        )
        st.plotly_chart(fig, use_container_width=True)

# Hourly demand
if "Time" in filtered.columns:
    st.subheader("Bookings by Hour")
    time_values = pd.to_datetime(
        filtered["Time"].astype(str).str.strip(),
        format="mixed",
        errors="coerce"
    )
    hourly = time_values.dt.hour.value_counts().sort_index().reset_index()
    hourly.columns = ["Hour", "Bookings"]
    if not hourly.empty:
        fig = px.line(
            hourly,
            x="Hour",
            y="Bookings",
            markers=True,
            title="Hourly Booking Demand"
        )
        st.plotly_chart(fig, use_container_width=True)

# Data preview
with st.expander("View filtered data"):
    st.dataframe(filtered.head(500), use_container_width=True)

st.caption("Ride Booking Analytics | Python • Pandas • Plotly • Streamlit")

st.subheader("Business Insights")

completed = df[
    df["Booking Status"] == "Completed"
].shape[0]

total = len(df)

cancelled = df[
    df["Booking Status"].str.contains(
        "cancelled", case=False, na=False
    )
].shape[0]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Booking Performance")
    st.write(f"Total bookings: {total:,}")
    st.write(f"Completed bookings: {completed:,}")
    st.write(
        f"Completion rate: {completed / total * 100:.2f}%"
        if total else "No bookings available"
    )

with col2:
    st.markdown("### Cancellation Analysis")
    st.write(f"Cancelled bookings: {cancelled:,}")
    st.write(
        f"Cancellation rate: {cancelled / total * 100:.2f}%"
        if total else "No bookings available"
    )

st.subheader("💡 Business Recommendations")

st.markdown("""
- **Reduce cancellations:** Investigate why customers and drivers
  cancel rides and identify the main cancellation reasons.

- **Improve vehicle allocation:** Compare booking demand across
  vehicle types to help balance availability.

- **Optimize peak hours:** Identify high-demand time periods
  and ensure enough drivers are available.

- **Monitor ride completion:** Track completed bookings and
  cancellation rates to measure service reliability.
""")

# Daily Booking Trend
st.subheader("📈 Daily Booking Trends")

trend_df = filtered.copy()

trend_df["Date"] = pd.to_datetime(
    trend_df["Date"],
    errors="coerce",
    dayfirst=True
)

trend_df = trend_df.dropna(subset=["Date"])

if not trend_df.empty:
    daily_bookings = (
        trend_df.groupby(trend_df["Date"].dt.date)
        ["Booking ID"]
        .count()
        .reset_index(name="Total Bookings")
    )

    daily_bookings = daily_bookings.rename(
        columns={"Date": "Booking Date"}
    )

    st.line_chart(
        daily_bookings.set_index("Booking Date")
        ["Total Bookings"]
    )
else:
    st.warning("No valid dates found in the dataset.")

# Peak Booking Hours
st.subheader("🕒 Peak Booking Hours")

hour_df = filtered.copy()

hour_df["Time"] = pd.to_datetime(
    hour_df["Time"].astype(str),
    errors="coerce"
)

hour_df = hour_df.dropna(subset=["Time"])
hour_df["Hour"] = hour_df["Time"].dt.hour

hourly_bookings = (
    hour_df.groupby("Hour")["Booking ID"]
    .count()
    .reset_index(name="Total Bookings")
)

st.bar_chart(
    hourly_bookings.set_index("Hour")["Total Bookings"]
)

if not hourly_bookings.empty:
    peak = hourly_bookings.loc[
        hourly_bookings["Total Bookings"].idxmax()
    ]
    st.success(
        f"Peak booking hour: {int(peak['Hour']):02d}:00 "
        f"({int(peak['Total Bookings']):,} bookings)"
    )

# Date Range Filter


# Apply date filter
if len(date_range) == 2:
    start_date, end_date = date_range

    filtered = filtered[
        df.loc[filtered.index, "Date"].dt.date.between(
            start_date, end_date
        )
    ]

# Download Report
st.divider()
st.subheader("📥 Download Your Report")

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Bookings (CSV)",
    data=csv_data,
    file_name="ride_booking_report.csv",
    mime="text/csv",
    key="download_filtered_report"
)

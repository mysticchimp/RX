import pandas as pd
import streamlit as st
from datetime import timedelta

def main():
    st.title("Schedule App")

    # File uploader for RosterWeek.csv
    roster_file = st.file_uploader("Upload RosterWeek.csv", type="csv")
    # File uploader for ErlangOct4.csv
    erlang_file = st.file_uploader("Upload ErlangOct4.csv", type="csv")

    if roster_file is not None and erlang_file is not None:
        try:
            roster_df = pd.read_csv(roster_file)
            erlang_df = pd.read_csv(erlang_file)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return

        # Filter out rows where 'Team Member' is '**UNALLOCATED**' and 'Area' is 'QA2'
        roster_filtered = roster_df[(roster_df['Team Member'] != '**UNALLOCATED**') & (roster_df['Area'] != 'QA2')].copy()

        # Convert start and end times to datetime
        roster_filtered['Start DateTime'] = pd.to_datetime(roster_filtered['Start Date'] + ' ' + roster_filtered['Start Time'], format='%Y-%m-%d %I:%M %p')
        roster_filtered['End DateTime'] = pd.to_datetime(roster_filtered['End Date'] + ' ' + roster_filtered['End Time'], format='%Y-%m-%d %I:%M %p')

        # Initialize a dictionary to count workers per hour for each day of the week
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours_per_day = {day: {hour: 0 for hour in range(24)} for day in week_days}

        # Function to get the day of the week from a date
        def get_day_of_week(date):
            return date.strftime('%A')

        # Count workers per hour for each day of the week
        for _, row in roster_filtered.iterrows():
            start = row['Start DateTime']
            end = row['End DateTime']
            current_time = start
            while current_time < end:
                day_name = get_day_of_week(current_time)
                if day_name in hours_per_day:
                    hours_per_day[day_name][current_time.hour] += 1
                current_time += timedelta(hours=1)

        # Convert the worker count dictionary to a DataFrame
        roster_worker_count_df = pd.DataFrame(hours_per_day)
        roster_worker_count_df.index.name = 'Hour'

        # Align Erlang DataFrame by setting its index to Hour and ensuring it matches the order of roster_worker_count_df
        erlang_df.set_index('Hour', inplace=True)
        erlang_df = erlang_df[week_days]  # Ensure columns are in the correct order

        # Calculate the difference between roster and Erlang staffing
        difference_df = roster_worker_count_df - erlang_df

        # Format hour index to HH:00 format for readability
        roster_worker_count_df.index = roster_worker_count_df.index.map(lambda x: f'{x:02d}:00')
        difference_df.index = difference_df.index.map(lambda x: f'{x:02d}:00')

        # Display the resulting DataFrames
        st.subheader("Roster Staffing:")
        st.dataframe(roster_worker_count_df)

        st.subheader("Difference (Roster - Erlang):")
        st.dataframe(difference_df)

if __name__ == "__main__":
    main()
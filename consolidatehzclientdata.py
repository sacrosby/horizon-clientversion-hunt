import os
import pandas as pd
import time
import subprocess

def load_and_filter_data(directory):
    all_files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.startswith("HorizonClientData_") and f.endswith('.csv')], reverse=True)
    dataframes = []
    
    for file in all_files:
        df = pd.read_csv(file)
        df["ClientVersion"] = df["ClientVersion"].astype(str)
        
        # Filter out ClientVersion 8.1.0 and above
        df = df[df["ClientVersion"].apply(lambda x: is_valid_version(x))]
        dataframes.append(df)
    
    if not dataframes:
        return None
    # Drop duplicate data from the previous data capture.
    combined_df = pd.concat(dataframes).drop_duplicates()
    
    # Sorting the data
    combined_df = combined_df.sort_values(by=["ClientName", "ClientAddress", "ClientVersion", "UserName", "MachineName", "StartTime"])
    
    # Reorder columns
    column_order = ["ClientVersion", "ClientName", "ClientAddress", "MachineName", "AgentVersion", "UserName", "StartTime"]
    combined_df = combined_df[column_order]
    
    return combined_df

def is_valid_version(version):
    try:
        parts = [int(p) for p in version.split('.')]
        return parts[0] < 8 or (parts[0] == 8 and parts[1] == 0)
    except ValueError:
        return False

def is_file_locked(filepath):
    #Check if a file is locked by trying to open it in append mode.
    try:
        with open(filepath, 'a'):
            return False
    except IOError:
        return True

def run_powercli_script(script_path):
    #Run the PowerCLI script and wait 10 seconds for it to complete.
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True)
        time.sleep(10)  # Wait for the script to finish
    except subprocess.CalledProcessError as e:
        print(f"Error running PowerCLI script: {e}")

def monitor_directory(directory, interval=10):
    output_directory = "horizon_client_monitor"
    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(output_directory, "filtered_horizon_sessions.csv")
    powercli_script = "horizon-client-poll.ps1"
    
    buffered_data = None  # Stores new data if file is not locked
    
    while True:
        print("Running PowerCLI script...")
        run_powercli_script(powercli_script)
        
        print("Checking for new CSV files...")
        filtered_data = load_and_filter_data(directory)
        
        if filtered_data is not None:
            if buffered_data is not None:
                # Combine buffered data with new data and remove duplicates
                filtered_data = pd.concat([buffered_data, filtered_data]).drop_duplicates()
                buffered_data = None  # Clear the buffer
            
            if is_file_locked(output_file):
                print("Output file is locked. Storing data in buffer until it is available.")
                buffered_data = filtered_data  # Store new data until file is free
            else:
                filtered_data.to_csv(output_file, index=False)
                print(f"Filtered data saved to {output_file}")
        else:
            print("No valid data found.")
        
        time.sleep(interval)  # Wait before checking again

def main():
    directory = "horizon_client_data"  # Using relative path
    
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return
    
    monitor_directory(directory)

if __name__ == "__main__":
    main()

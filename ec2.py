import boto3

# Adjust this to your target region
REGION = "eu-north-1"
ec2 = boto3.client("ec2", region_name=REGION)

def get_instances():
    """Fetches all EC2 instances and returns a list of dictionaries with their details."""
    response = ec2.describe_instances()
    instances = []
    
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instance_id = instance["InstanceId"]
            state = instance["State"]["Name"]
            
            # Fetch the 'Name' tag if it exists to make selection easier
            name = "Unknown"
            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]
                    break
                    
            instances.append({
                "id": instance_id, 
                "state": state, 
                "name": name
            })
            
    return instances

def main():
    print("Fetching EC2 instances...\n")
    instances = get_instances()
    
    if not instances:
        print(f"No EC2 instances found in region: {REGION}")
        return

    # 1. DETECT AND DISPLAY
    print("--- Available EC2 Instances ---")
    for idx, inst in enumerate(instances, start=1):
        print(f"{idx}. {inst['id']} | Name: {inst['name']} | State: {inst['state'].upper()}")
    print("-------------------------------")

    # 2. ASK & CHOOSE INSTANCE
    try:
        choice = int(input(f"\nSelect an instance to manage (1-{len(instances)}): "))
        if choice < 1 or choice > len(instances):
            print("Invalid selection. Exiting.")
            return
    except ValueError:
        print("Please enter a valid number. Exiting.")
        return

    selected = instances[choice - 1]
    instance_id = selected['id']
    current_state = selected['state']

    print(f"\nSelected Instance: {instance_id} (Currently {current_state.upper()})")

    # 3. CHOOSE ON OR OFF
    print("\nEC2 CONTROL")
    print("1 - Start instance (ON)")
    print("2 - Stop instance (OFF)")
    
    action = input("Choose option (1 or 2): ")

    if action == "1":
        if current_state == "running":
            print(f"\nInstance {instance_id} is already RUNNING.")
        else:
            print(f"\nStarting {instance_id}...")
            ec2.start_instances(InstanceIds=[instance_id])
            print("EC2 instance started successfully.")
            
    elif action == "2":
        if current_state == "stopped":
            print(f"\nInstance {instance_id} is already STOPPED.")
        else:
            print(f"\nStopping {instance_id}...")
            ec2.stop_instances(InstanceIds=[instance_id])
            print("EC2 instance stopped successfully.")
            
    else:
        print("\nInvalid option.")

if __name__ == "__main__":
    main()

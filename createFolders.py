import os

folders = {
    "common": ["OppositeDirection", "BrakeCheck", "IgnoreRedlights", "Flood" ,"Parking", "Directional" ,"Pedestrian" ,"NightStreet", "OneWay"],
    "indonesian": ["StreetPaddler", "RoadBlocks", "SmallRoads", "Deadlock", "BuswayLane", "Train", "RoadSigns", "LaneTakeover"]
}

os.makedirs("Dataset", exist_ok=True)

for category, subfolders in folders.items():
    for subfolder in subfolders:
        path = os.path.join("Dataset", category, subfolder)
        os.makedirs(path, exist_ok=True)
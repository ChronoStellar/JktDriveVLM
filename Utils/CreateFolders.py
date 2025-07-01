import os

folders = {
    "UrbanFlowComplexity": ["EvasiveManueverPlanning", "VRUCutIn", "VehicleCutIn" ,"VehicleRecognition"],
    "PerceptionReasoing": ["NarrowRoadway", "UnidirectionalTraffic", "LaneRecognition", "NavigationDecissionMaking"],
    "SafetyComplience": ["ObstacleRecognition", "LongShortParking", "TrainRailwayRecognition", "InadequateRoadConditions", "TrajectoryPlanningSigns", "TrafficSignalRecognition", "RoadSignsRecongition"]
}

PATH = '../Dataset'

os.makedirs(PATH, exist_ok=True)

for category, subfolders in folders.items():
    for subfolder in subfolders:
        path = os.path.join(PATH, category, subfolder)
        os.makedirs(path, exist_ok=True)

print(f'Folders made! at {PATH}')
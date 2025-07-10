import os

folders = {
    "UrbanFlowComplexity": [
        "EvasiveManeuverPlanning",   # Corrected spelling
        "VRUCut-In",                 # Corrected spelling
        "VehicleCut-In",             # Corrected spelling
        "VehicleRecognition"
    ],
    "PerceptionReasoning": [       # Corrected spelling
        "NarrowRoadway",
        "UnidirectionalTraffic",
        "LaneRecognition",
        "NavigationDecisionMaking" # Corrected spelling
    ],
    "SafetyCompliance": [          # Corrected spelling
        "ObstacleRecognition",
        "LongShortParking",
        "TrainRailwayRecognition",
        "InadequateRoadConditions",
        "TrajectoryPlanningSigns",
        "TrafficSignalRecognition",
        "RoadSignsRecognition"     # Corrected spelling
    ]
}

PATH = '../Dataset'

os.makedirs(PATH, exist_ok=True)

for category, subfolders in folders.items():
    for subfolder in subfolders:
        path = os.path.join(PATH, category, subfolder)
        os.makedirs(path, exist_ok=True)

print(f'Folders made! at {PATH}')
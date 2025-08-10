import os

folders = {
    "UrbanFlowComplexity": [
        "EvasiveManeuverPlanning",   
        "VRUCut-In",                 
        "VehicleCut-In",             
        "VehicleRecognition"
    ],
    "PerceptionReasoning": [       
        "NarrowRoadway",
        "UnidirectionalTraffic",
        "LaneRecognition",
        "NavigationDecisionMaking" 
    ],
    "SafetyCompliance": [          
        "ObstacleRecognition",
        "LongShortParking",
        # "TrainRailwayRecognition",
        "InadequateRoadConditions",
        "TrajectoryPlanningSigns",
        "TrafficSignalRecognition",
        "RoadSignsRecognition"     
    ]
}

PATH = '../Dataset'

os.makedirs(PATH, exist_ok=True)

for category, subfolders in folders.items():
    for subfolder in subfolders:
        path = os.path.join(PATH, category, subfolder)
        os.makedirs(path, exist_ok=True)

print(f'Folders made! at {PATH}')
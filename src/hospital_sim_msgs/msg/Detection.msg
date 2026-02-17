# Single object detection
string class_name          # e.g., "exit_door", "fire_extinguisher", "first_aid_kit"
int32 class_id             # 0, 1, 2
float32 confidence         # 0.0 to 1.0
float32 x_center           # normalized 0.0 to 1.0
float32 y_center           # normalized 0.0 to 1.0
float32 width              # normalized 0.0 to 1.0
float32 height             # normalized 0.0 to 1.0
int32 x_min                # pixel coordinates
int32 y_min
int32 x_max
int32 y_max

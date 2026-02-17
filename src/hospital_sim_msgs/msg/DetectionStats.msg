# Detection statistics message
std_msgs/Header header

# Total counts
int32 total_detections

# Per-class counts
int32 exit_door_count
int32 fire_extinguisher_count
int32 first_aid_kit_count

# Frame info
int32 frame_number
float32 fps
float32 inference_time_ms

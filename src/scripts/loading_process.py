

def loading_process_part(index):
	animation_frames = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
	index_frame = index % len(animation_frames)
	process_string = "{ info }" + " loading data from result data " + animation_frames[index_frame]
	return process_string
from moviepy.editor import VideoFileClip, concatenate_videoclips



video1_path = "1st.mp4"
video2_path = "2st.mp4"
output_path = "out.mp4"



video1 = VideoFileClip(video1_path)
video2 = VideoFileClip(video2_path)

final_video = concatenate_videoclips([video1, video2])
final_video.write_videofile(output_path)



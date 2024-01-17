import subprocess
import os

class Editor:

    #
    # Create video
    # create a timelaps video 
    # from all the images saved locally
    #
    # fps 10 to get a slow video
    # fps 80 to get a real video
    def create_video(self, images_folder, output_video_path = "./tmp_timelaps.mp4", fps=5):

        print(">> Creating tmp time laps")
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

        # Delete the old timelaps
        if os.path.exists(output_video_path):
            # Delete the file
            os.remove(output_video_path)

        # Run FFmpeg command to create a video from images
        subprocess.run([
            'ffmpeg',
            '-framerate', str(fps),
            '-i', f"{images_folder}%d.jpg",
            '-c:v', 'libx264',
            '-r', '30',  # Output video frame rate
            '-pix_fmt', 'yuv420p',
            output_video_path
        ], shell=True)
        pass

    pass

    def concat_video(self, output_name = "./timelaps.mp4"):

        print(">> Concat tmp time laps")
        # Run FFmpeg command to concat 2 different video
        subprocess.run([
            'ffmpeg',
            '-f', 'concat',
            '-safe 0', '-i',
            'concat.txt', '-c:v', 'libx264',
            '-r', '30',  # Output video frame rate
            '-pix_fmt', 'yuv420p',
            output_name
        ], shell=True)

        pass

# Example
#
# images_folder = "C:\\Users\\em-hp2\\Desktop\\image\\background\\%d.png"
# output_video_path = "C:\\Users\\em-hp2\\Desktop\\image\\Video.mp4"
# create_video(images_folder, output_video_path)
# 
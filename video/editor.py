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
    def create_video(self, images_folder, output_video_path = "tmp_timelaps.mp4", fps=5):

        print(">> Creating tmp time laps")
        current_path = os.getcwd() + '/pictures/%d.png'
        print("Current Path:", current_path)

        # Delete the old timelaps
        if os.path.exists(output_video_path):
            # Delete the file
            os.remove(output_video_path)

        # Run FFmpeg command to create a video from images
        subprocess.run([
            'ffmpeg',
            '-framerate', str(fps),
            '-i', current_path,
            '-c:v', 'libx264',
            '-r', '30',  # Output video frame rate
            '-pix_fmt', 'yuv420p',
            output_video_path
        ])
        pass

    pass

    def concat_video(self, output_path = "./timelaps.mp4"):

        print(">> Concat tmp time laps")
        # Run FFmpeg command to concat 2 different video
        subprocess.run([
            'ffmpeg',
            '-f', 'concat',
            '-safe 0', '-i',
            '\'./video/concat.txt\'', '-c:v', 'libx264',
            '-r', '30',  # Output video frame rate
            '-pix_fmt', 'yuv420p',
            output_path
        ], shell=True)

        return output_path

# Example
#
# images_folder = "C:\\Users\\em-hp2\\Desktop\\image\\background\\%d.png"
# output_video_path = "C:\\Users\\em-hp2\\Desktop\\image\\Video.mp4"
# create_video(images_folder, output_video_path)
# 
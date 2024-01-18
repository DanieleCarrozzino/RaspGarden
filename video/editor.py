import subprocess
import os

# Temporary file
tmp = 'tmp_timelaps.mp4'
# Main file
timelaps_name = 'timelaps.mp4'

class Editor:

    #
    # Create video
    # create a timelaps video 
    # from all the images saved locally
    #
    # fps 10 to get a slow video
    # fps 80 to get a real video
    def create_video(self, images_folder, fps=5):

        print(">> Creating tmp time laps")
        # current_path = os.getcwd() + '/pictures/%d.png'
        images_folder = images_folder + '%d.png'

        # Delete the old timelaps
        if os.path.exists(tmp):
            # Delete the file
            os.remove(tmp)

        # Run FFmpeg command to create a video from images
        subprocess.run([
            'ffmpeg',
            '-framerate', str(fps),
            '-i', images_folder,
            '-c:v', 'libx264',
            '-r', '30',  # Output video frame rate
            '-pix_fmt', 'yuv420p',
            tmp
        ])
        
        # If not exists teh main video
        # create it with the first image
        if not os.path.exists(timelaps_name):
            subprocess.run([
                'ffmpeg',
                '-framerate', str(fps),
                '-i', images_folder,
                '-c:v', 'libx264',
                '-r', '30',  # Output video frame rate
                '-pix_fmt', 'yuv420p',
                timelaps_name
            ])

    pass

    def concat_video(self):

        print(">> Concat tmp time laps")
        # Run FFmpeg command to concat 2 different video
        subprocess.run([
            'ffmpeg',
            '-f', 'concat',
            '-safe 0', '-i',
            'concat.txt', '-c:v', 'libx264',
            '-r', '30',
            '-pix_fmt', 'yuv420p',
            timelaps_name
        ])

        return timelaps_name

# Example
#
# images_folder = "C:\\Users\\em-hp2\\Desktop\\image\\background\\%d.png"
# output_video_path = "C:\\Users\\em-hp2\\Desktop\\image\\Video.mp4"
# create_video(images_folder, output_video_path)
# 
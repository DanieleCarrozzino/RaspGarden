import subprocess
import os
import shutil

# Temporary file
tmp = 'video/tmp_timelaps.mp4'
# Main file
timelaps_name = 'video/timelaps.mp4'
# Edit timelaps tmp
edit_timelaps = 'video/edit_timelaps.mp4'

class Editor:

    def clone_file(self, original_filename, new_filename):
        # Open the original file for reading
        with open(original_filename, 'rb') as original_file:
            # Read the content of the original file
            file_content = original_file.read()

        # Open the new file for writing
        with open(new_filename, 'wb') as new_file:
            # Write the content to the new file
            new_file.write(file_content)
        pass

    #
    # Create video
    # create a timelaps video 
    # from all the images saved locally
    #
    # fps 10 to get a slow video
    # fps 80 to get a real video
    def create_video(self, images_folder, fps=60):

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
        
        # If not exists the main video
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

        # Clone and remove the old one
        if os.path.exists(edit_timelaps):
            os.remove(edit_timelaps)
        self.clone_file(timelaps_name, edit_timelaps)
        if os.path.exists(timelaps_name):
            os.remove(timelaps_name)

        print(">> Concat tmp time laps")
        # Run FFmpeg command to concat 2 different video
        subprocess.run([
            'ffmpeg',
            '-f', 'concat', '-i',
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
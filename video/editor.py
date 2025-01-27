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
    #
    # return false if it's the first time
    # and the previous video is not present
    # avoiding to add twice the first image
    #
    def create_video(self, images_folder, fps=60):
        image = images_folder + '%d.png'

        # If not exists the main video
        # create it with the first image
        if not os.path.exists(timelaps_name):
            subprocess.run([
                'ffmpeg',
                '-loop', '1',            # Loop the single image
                '-i', image,             # Input single image
                '-c:v', 'libx264',       # Output codec
                '-t', '0.0167',          # Duration of the video
                '-r', '60',              # Output frame rate
                '-s', '1920x1080',       # Output resolution
                '-pix_fmt', 'yuv420p',   # Pixel format for compatibility
                timelaps_name
            ])
            return False

        # Delete the old timelaps
        if os.path.exists(tmp):
            # Delete the file
            os.remove(tmp)

        # Run FFmpeg command to create a video from images
        subprocess.run([
            'ffmpeg',
            '-loop', '1',            # Loop the single image
            '-i', image,             # Input single image
            '-c:v', 'libx264',       # Output codec
            '-t', '0.0167',          # Duration of the video
            '-r', '60',              # Output frame rate
            '-s', '1920x1080',       # Output resolution
            '-pix_fmt', 'yuv420p',   # Pixel format for compatibility
            tmp
        ])
        return True

    def concat_video(self):

        # Clone and remove the old one
        if os.path.exists(edit_timelaps):
            os.remove(edit_timelaps)
        self.clone_file(timelaps_name, edit_timelaps)
        if os.path.exists(timelaps_name):
            os.remove(timelaps_name)

        print("Editor::concat_video::Concat tmp time laps")
        # Run FFmpeg command to concat 2 different video
        subprocess.run([
            'ffmpeg',
            '-f', 'concat', '-safe', '0', '-i', 'concat.txt',
            '-c', 'copy',
            timelaps_name
        ])

        return timelaps_name

# Example
#
# images_folder = "C:\\Users\\em-hp2\\Desktop\\image\\background\\%d.png"
# output_video_path = "C:\\Users\\em-hp2\\Desktop\\image\\Video.mp4"
# create_video(images_folder, output_video_path)
# 

# from Command line
# create the first  video to concat : ffmpeg -loop 1 -i 1.png -c:v libx264 -t 0.0167 -r 60 -s 1920x1080 -pix_fmt yuv420p video1.mp4
# create the second video to concat : ffmpeg -loop 1 -i 2.png -c:v libx264 -t 0.0167 -r 60 -s 1920x1080 -pix_fmt yuv420p video2.mp4
# create the timelaps video : ffmpeg -f concat -safe 0 -i concat.txt -c copy timelapse.mp4
#
# put inside the concat.txt file :
# file 'video1.mp4'
# file 'video2.mp4'
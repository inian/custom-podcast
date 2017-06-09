import ffmpy
ff = ffmpy.FFmpeg(inputs={'video.mp4': None}, outputs={'audio.mp3': None})
ff.run()

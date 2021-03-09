def frames_to_timecode(frames, framerate):
    return '{0}{1}{2}{3}'.format(str(int(frames / (3600*framerate))).zfill(2),
                                 str(int(frames / (60*framerate) % 60)).zfill(2),
                                 str(int(frames / framerate % 60)).zfill(2),
                                 str(int(frames % framerate))[:2].zfill(2))
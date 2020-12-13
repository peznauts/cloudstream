#!/usr/bin/env python
# CloudStream Copyright (C) 2020  Kevin Carter

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


RTMP_COMMAND = """
/bin/ffmpeg
-i "{input}"
-s {res}
-r {fps}
-c:v libx264
-preset {preset}
-g {keyinit}
-x264-params "bitrate={bitrate}:vbv_maxrate={bitrate}:vbv_bufsize={bitrate}:threads=0:bframes={keyframes}:rc_lookahead=10:keyint={keyinit}:keyint_min={keyinit}:nal_hrd=cbr:scenecut=0:rc=cbr:force_cfr=1"
-sws_flags lanczos
-pix_fmt yuv420p
-c:a copy
-b:a {audio}
-f flv
"{output}"
"""  #noqa


class FilterModule(object):
    def filters(self):
        return {
            'transcode': self.transcode,
        }

    def transcode(self, transcode_setting, input_target, output_target):
        """Return a transcode command line.

        :param transcode_setting: Dictionary
        :returns: String
        """

        rtmp_command = RTMP_COMMAND.format(
            input=input_target,
            res=transcode_setting['res'],
            fps=transcode_setting['fps'],
            preset=transcode_setting['preset'],
            keyinit=int(transcode_setting['fps']) * 2 // 1,
            bitrate=transcode_setting['bitrate'],
            keyframes=transcode_setting['key_frames'],
            audio=transcode_setting['audio'],
            output=output_target
        )
        return ' '.join(rtmp_command.splitlines()).strip()

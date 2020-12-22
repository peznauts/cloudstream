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

from collections import defaultdict


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
-c:a {audio_codec}
-b:a {audio_bitrate}
-f flv
"{output}"
"""  #noqa


class FilterModule(object):
    def filters(self):
        return {
            'transcode': self.transcode,
            'stream_targets': self.stream_targets
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
            audio_codec=transcode_setting['audio_codec'],
            audio_bitrate=transcode_setting['audio_bitrate'],
            output=output_target
        )
        return 'exec {}'.format(' '.join(rtmp_command.splitlines()).strip())

    def stream_targets(self, rtmp_array, ffmpeg_settings, hostvars, nodes, node_self):
        """Process all stream targets and return a dictionary.

        :returns: dictionary of names and endpoints.
        """

        transode_simulcasts = defaultdict(list)
        transcoded_endpoints = list()

        return_items = defaultdict(list)
        node_bitrate = defaultdict(int)
        node_bitrate[node_self] += 0
        for node in nodes:
            node_bitrate[node] += 0

        for index, item in enumerate(rtmp_array, start=0):
            url = item['url']
            key = item.get('key', '')
            if 'facebook' in url:
                push_stream = "push rtmp://127.0.0.1:19350/rtmp/{}".format(key)
            else:
                push_stream = "push {}/{}".format(url, key)

            return_items[index].append(push_stream)

            if 'transcode' in item:
                transcode_str = item['transcode']
                transcode_marker = '{}-transcode'.format(transcode_str)
                settings = ffmpeg_settings[transcode_str]
                try:
                    node = 'rtmpServer-{}'.format(settings['nodes'].pop())
                except IndexError:
                    node = node_self

                node_bitrate[node] += int(item.get('bitrate', 6144))

                node_ip = hostvars.get(
                    node,
                    dict()
                ).get(
                    'rtmpserver_private_ip',
                    '127.0.0.1'
                )
                return_items['simulcast'].append(
                    'exec /bin/ffmpeg -re -threads 1 -analyzeduration 0'
                    ' -i "rtmp://127.0.0.1:1935/simulcast" -c:v copy -c:a copy'
                    ' -f flv "rtmp://{}:1935/{}-transcode"'.format(
                        node_ip,
                        transcode_str
                    )
                )
                return_items[transcode_marker].append(
                    self.transcode(
                        transcode_setting=settings,
                        input_target='rtmp://127.0.0.1:1935/{}-transcode'.format(
                            transcode_str
                        ),
                        output_target="rtmp://127.0.0.1:1935/{}".format(
                            index
                        )
                    )
                )
            else:
                stream_node = min(node_bitrate, key=node_bitrate.get)
                if stream_node == node_self:
                    node_ip = '127.0.0.1'
                else:
                    node_ip = hostvars.get(
                        stream_node,
                        dict()
                    ).get(
                        'rtmpserver_private_ip',
                        '127.0.0.1'
                    )

                return_items['simulcast'].append(
                    "push rtmp://{}:1935/{}".format(node_ip, index)
                )
                node_bitrate[stream_node] += 6144

        return return_items

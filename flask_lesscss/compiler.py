# -*- coding: utf-8 -*-
"""
    flaskext.lesscss
    ~~~~~~~~~~~~~

    A small Flask extension that makes it easy to use LessCSS with your Flask
    application.

    :copyright: (c) 2010 by Steve Losh.
    :license: MIT, see LICENSE for more details.
"""

import os, subprocess

def lesscss(app, input_dir_param=None, output_dir_param=None):
    
    static_attributes = ['static_url_path', 'static_path', 'static_folder']
    for attribute_candidate in static_attributes:
        if hasattr(app, attribute_candidate):
            accessor = attribute_candidate
            break

    @app.before_request
    def _render_less_css():

        static_dir = app.root_path + getattr(app, accessor)
        
        input_dir = static_dir
        less_files = []
        if input_dir_param is not None:
            input_dir = input_dir_param
        for path, subdirs, filenames in os.walk(input_dir):
            subpath = path[len(input_dir):]
            less_files.extend([
                os.path.join(subpath, f)
                for f in filenames if os.path.splitext(f)[1] == '.less'
            ])
        
        output_dir = static_dir
        if output_dir_param is not None:
            output_dir = os.path.join(static_dir, output_dir_param)

        for less_file in less_files:
            css_path = os.path.join(output_dir, os.path.splitext(less_file)[0] + '.css')
            if not os.path.isfile(css_path):
                css_mtime = -1
            else:
                css_mtime = os.path.getmtime(css_path)
            less_mtime = os.path.getmtime(os.path.join(input_dir, less_file))
            if less_mtime >= css_mtime:
                subprocess.check_call(['lessc', os.path.join(input_dir, less_file), css_path], shell=False)



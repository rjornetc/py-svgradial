#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Raúl Jornet Calomarde'
__contact__ = 'rjornetc@openmailbox.org'
__copyright__ = 'Copyright © 2015, Raúl Jornet Calomarde'
__license__ = ''''License GPLv3+: GNU GPL version 3 or any later
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or any later version. This program
is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.
<http://www.gnu.org/licenses/>'''
__date__ = '08/02/2015'
__version__ = '0.1.0'


from math import cos, sin, pi
import svgwrite

class RadialChartSerie():
    title = ''
    border_color = ''
    fill_color = ''
    fill_opacity = 0
    values = []
    
    def __init__(self, title, fill_color = 'none', border_color='#cc0000', fill_opacity=1):
        self.title = title
        self.fill_color = fill_color
        self.border_color = border_color
        self.fill_opacity = fill_opacity
    
    def set_values(self, values):
        self.values = values

class RadialChart():
    
    title = ''
    axes_title = []
    axis_color = '#777777'
    axis_color_secundary = '#cccccc'
    series = []
    min_value = 0
    max_value = 10
    radial_lines = 10
    radial_axis_primary = 2
    
    def __init__(self, title, axes_title):
        self.title = title
        self.axes_title = axes_title
    
    
    def add_serie(self, serie):
        if len(self.axes_title) == len(serie.values):
            self.series.append(serie)
        else:
          raise(IndexError('The number of axes and values must be equal'))
    
    
    def add_value(self, serie, axes_title, value):
        axis_index = self.axes_title.index(axes_title)
        self.series[serie][axis_index] = value
    
    
    def get_svg(self):
        svg = \
'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:cc="http://creativecommons.org/ns#"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:svg="http://www.w3.org/2000/svg"
  xmlns="http://www.w3.org/2000/svg"
  width="256"
  height="256"
>
  <g transform="translate(128,128)" id="background">'''
        axes_title_count = len(self.axes_title)
        axes_title_angle = 2 * pi / axes_title_count
        radial_lines_space = 96.0 / self.radial_lines
        for i in range(1, self.radial_lines+1):
            svg += '''
    <path d="M '''
            if i % self.radial_axis_primary == 0:
                current_color = self.axis_color
            else:
                current_color = self.axis_color_secundary
            
            for j in range(0, axes_title_count):
                current_angle = axes_title_angle * (j)
                svg += str(sin(current_angle) * radial_lines_space * i) + ',' +\
                       str(-cos(current_angle) * radial_lines_space * i) + ' '
            svg +=  \
'''z" id="radial-line''' + str(i) + '''" style="fill:none;stroke:''' + current_color + '''" />'''
        
        for i in range(0, axes_title_count):
            current_angle = axes_title_angle * i
            svg += '''
    <path d="M 0,0 ''' +\
        str(sin(current_angle) * 96) + ',' +\
        str(-cos(current_angle) * 96) + '" id="' +\
        self.axes_title[i] + '''-axis" style="stroke:#777777" />
    <text
      style="font-size:16px;text-align:center;fill:#000000"
      id="''' + self.axes_title[i] + '''-text"
    >
      <tspan
        id="''' + self.axes_title[i] + '''-tspan"
        x="''' + str(sin(current_angle) * 112) + '''"
        y="''' + str(-cos(current_angle) * 112) + '''"
        style="text-align:center;line-height:0%;text-anchor:middle"
        dy="5.5">''' + self.axes_title[i] + '''
      </tspan>
    </text>
  '''
        svg += '  </g>'
                
        
        for serie in self.series:
            svg += '''
  <g transform="translate(128,128)" id="''' + serie.title + '''">
    <path d="M '''
            for i in range(0, axes_title_count):
                current_angle = axes_title_angle * i
                value = float(serie.values[i]) / float(self.max_value)
                svg += str(sin(current_angle) * 96.0 * value) + ',' +\
                       str(-cos(current_angle) * 96.0 * value) + ' '
            svg += '''z" id="foreground" style="fill:''' +\
                   serie.fill_color + ''';stroke:''' +\
                   serie.border_color + ''';fill-opacity:''' +\
                   str(serie.fill_opacity) + '''" />
  </g>'''
        svg += '''
</svg>'''
        return svg
      
      
class SVGRadialChart():
    svg = None
    chart = None
    size = 0
    margin = 0
    
    def __init__(self, chart, size = 128, margin = 0.1, filename = u'noname.svg'):
        self.chart = chart
        self.size = size
        self.margin = margin
        self.svg = svgwrite.Drawing(filename = filename,
                                    size=(str(self.size) + 'px',
                                          str(self.size) + 'px'),
                                    profile='tiny')
    
    #def _draw_axes(self,
                   #radial = True,
                   #secundary_radial = True
                   #):
    
    
    def get_svg(self, filename):
                                    
        axes_title_count = len(self.chart.axes_title)
        axes_title_angle = 2 * pi / axes_title_count
        center = self.size / 2
        canvas = center * (1 - self.margin)
        radial_lines_space = canvas / self.chart.radial_lines
        for i in range(1, self.chart.radial_lines+1):
            if i % self.chart.radial_axis_primary == 0:
                current_color = self.chart.axis_color
            else:
                current_color = self.chart.axis_color_secundary
            path=[]
            for j in range(0, axes_title_count):
                current_angle = axes_title_angle * j
                point = (center + sin(current_angle) * radial_lines_space * i,
                         center - cos(current_angle) * radial_lines_space * i)
                path.append(point)
            self.svg.add(self.svg.polygon(path,
                                          stroke=current_color,
                                          fill='none'))
      
        for i in range(0, axes_title_count):
            current_angle = axes_title_angle * i
            point = (center + sin(current_angle) * canvas,
                     center - cos(current_angle) * canvas)
            self.svg.add(self.svg.line(start=(center,
                                              center),
                                       end=point,
                                       stroke=self.chart.axis_color))
            
        for serie in self.chart.series:
            path = []
            for i in range(0, axes_title_count):
                current_angle = axes_title_angle * i
                value = float(serie.values[i]) / float(self.chart.max_value)
                point = (center + sin(current_angle) * canvas * value,
                         center - cos(current_angle) * canvas * value)
                path.append(point)
            self.svg.add(self.svg.polygon(path,
                                          stroke=serie.border_color,
                                          fill=serie.fill_color,
                                          fill_opacity=serie.fill_opacity))
              
        return self.svg

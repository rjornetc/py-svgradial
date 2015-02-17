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
      
      
class SVGRadialChart():
    svg = None
    chart = None
    size = 0
    margin = 0
    
    def __init__(self,
                 chart,
                 size = 128,
                 margin = 0.1,
                 filename = u'noname.svg'):
        self.chart = chart
        self.size = size
        self.margin = margin
        self.svg = svgwrite.Drawing(filename = filename,
                                    size=(str(self.size) + 'px',
                                          str(self.size) + 'px'),
                                    profile='tiny')
    
    def draw_axes(self,
                  horizontal_axes = True,
                  secundary_horizontal_axes = True,
                  vertical_axes = True):
                                    
        axes_title_count = len(self.chart.axes_title)
        axes_title_angle = 2 * pi / axes_title_count
        center = self.size / 2
        canvas = center * (1 - self.margin)
        radial_lines_space = canvas / self.chart.radial_lines

        if horizontal_axes:
            for i in range(1, self.chart.radial_lines + 1):
                if i % self.chart.radial_axis_primary == 0:
                    axis_color = self.chart.axis_color
                else:
                    axis_color = self.chart.axis_color_secundary
                if i % self.chart.radial_axis_primary == 0 or\
                   secundary_horizontal_axes:
                    path=[]
                    for j in range(0, axes_title_count):
                        current_angle = axes_title_angle * j
                        point = (center +
                                     sin(current_angle) *
                                     radial_lines_space * i,
                                 center -
                                     cos(current_angle) *
                                     radial_lines_space * i)
                        path.append(point)
                    self.svg.add(self.svg.polygon(path,
                                                  stroke=axis_color,
                                                  fill='none'))

        if vertical_axes:
            for i in range(0, axes_title_count):
                current_angle = axes_title_angle * i
                point = (center + sin(current_angle) * canvas,
                        center - cos(current_angle) * canvas)
                self.svg.add(self.svg.line(start = (center,
                                                    center),
                                          end=point,
                                          stroke=self.chart.axis_color))
    
    
    def draw_series(self):
                                    
        axes_title_count = len(self.chart.axes_title)
        axes_title_angle = 2 * pi / axes_title_count
        center = self.size / 2
        canvas = center * (1 - self.margin)
        
        for serie in self.chart.series:
            path = []
            for i in range(0, axes_title_count):
                current_angle = axes_title_angle * i
                value = float(serie.values[i]) / float(self.chart.max_value)
                point = (center + sin(current_angle) * canvas * value,
                         center - cos(current_angle) * canvas * value)
                path.append(point)
            self.svg.add(self.svg.polygon(path,
                                          stroke = serie.border_color,
                                          fill = serie.fill_color,
                                          fill_opacity = serie.fill_opacity))
    
    
    def get_svg(self, filename):
                                    
        axes_title_count = len(self.chart.axes_title)
        axes_title_angle = 2 * pi / axes_title_count
        center = self.size / 2
        canvas = center * (1 - self.margin)
        radial_lines_space = canvas / self.chart.radial_lines
        for i in range(1, self.chart.radial_lines+1):
            if i % self.chart.radial_axis_primary == 0:
                axis_color = self.chart.axis_color
            else:
                axis_color = self.chart.axis_color_secundary
            path=[]
            for j in range(0, axes_title_count):
                current_angle = axes_title_angle * j
                point = (center + sin(current_angle) * radial_lines_space * i,
                         center - cos(current_angle) * radial_lines_space * i)
                path.append(point)
            self.svg.add(self.svg.polygon(path,
                                          stroke=axis_color,
                                          fill='none'))
      
        for i in range(0, axes_title_count):
            current_angle = axes_title_angle * i
            point = (center + sin(current_angle) * canvas,
                     center - cos(current_angle) * canvas)
            self.svg.add(self.svg.line(start = (center,
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
                                          stroke = serie.border_color,
                                          fill = serie.fill_color,
                                          fill_opacity = serie.fill_opacity))
              
        return self.svg

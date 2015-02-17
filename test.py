#! /usr/bin/python
# -*- coding: utf-8 -*-

import svgradial

if __name__ == '__main__':
    rg = svgradial.RadialChart('test', ['Str', 'Con', 'Dex', 'Cog', 'Int'])
    s1 = svgradial.RadialChartSerie('s1', '#00ff00', '#00cc00')
    s1.set_values([8, 9, 7 ,5 ,4])
    s2 = svgradial.RadialChartSerie('s2')
    s2.set_values([4, 4, 4 ,4 ,4])
    s3 = svgradial.RadialChartSerie('s3', '#882244', '#441122', 0.5)
    s3.set_values([2, 3, 3 ,4 ,9])
    rg.add_serie(s1)
    rg.add_serie(s2)
    rg.add_serie(s3)
    svg = svgradial.SVGRadialChart(rg,160)
    svg.get_svg('test.svg').save()
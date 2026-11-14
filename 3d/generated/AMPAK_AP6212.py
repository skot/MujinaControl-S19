"""Envelope model of the AMPAK AP6212 module for the Mujina:AMPAK_AP6212 footprint (CadQuery).
12 x 12 x 0.5 mm module board, 11.2 x 11.2 x 1.0 mm shield can: 1.5 mm total (datasheet section 9.1). Origin: footprint centre, board surface.
usage: python AMPAK_AP6212.py  ->  AMPAK_AP6212.step beside this file"""
import os
import cadquery as cq
board=cq.Workplane('XY').box(12,12,0.5,centered=(True,True,False))
can=cq.Workplane('XY').workplane(offset=0.5).box(11.2,11.2,1.0,centered=(True,True,False)).edges('|Z').fillet(0.4).faces('>Z').edges().fillet(0.15)
dot=cq.Workplane('XY').workplane(offset=1.5).center(-4.3,4.3).circle(0.5).extrude(0.01)   # pin-1 mark (top left in the footprint: -x, -y in KiCad = -x, +y here)
a=cq.Assembly(name='AMPAK_AP6212')
a.add(board,name='board',color=cq.Color(0.05,0.25,0.12))
a.add(can,name='shield',color=cq.Color(0.78,0.78,0.80))
a.add(dot,name='pin1',color=cq.Color(0.2,0.2,0.2))
a.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),'AMPAK_AP6212.step'))

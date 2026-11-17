"""Envelope model of the HanRun HR915340A tab-up RJ45 jack for Connector_RJ:RJ45_Hanrun_HR915340A_Horizontal (CadQuery).
Body 16.0 x 21.4 x 13.55 mm, latch notch at the top of the opening, green LED top-left and yellow LED top-right seen from the front.
Not a vendor model: outside dimensions, pin positions and the tab-up opening follow the datasheet (REV. 01); the inside is simplified.
Coordinates are the footprint's: origin at pin 1, x as in KiCad, y = -(KiCad y), z up from the board.
usage: python HanRun_HR915340A.py  ->  HanRun_HR915340A.step beside this file"""
import os
import cadquery as cq
CX=4.44                      # centre line of the jack, from pin 1
X0,X1=CX-8.0,CX+8.0          # 16.0 mm wide
YF,YR=-17.26,4.14            # front face (10.90 mm in front of the posts) and rear
H=13.55
STEEL=cq.Color(0.66,0.67,0.69); BLACK=cq.Color(0.10,0.10,0.10); GOLD=cq.Color(0.85,0.68,0.25)
GREEN=cq.Color(0.0,0.85,0.1); YELLOW=cq.Color(1.0,0.9,0.0); TIN=cq.Color(0.75,0.76,0.78); DARK=cq.Color(0.25,0.25,0.25)
def box(x0,x1,y0,y1,z0,z1): return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=False).translate((x0,y0,z0))
shell=box(X0,X1,YF,YR,0,H)
# opening for the plug, 14 mm deep: contacts at the bottom, latch notch on top (tab up)
DEPTH=14.0
cav=box(CX-5.85,CX+5.85,YF-0.01,YF+DEPTH,2.0,8.9).union(box(CX-3.1,CX+3.1,YF-0.01,YF+DEPTH,8.9,10.6)).union(box(CX-1.7,CX+1.7,YF-0.01,YF+DEPTH,10.6,11.4))
led_w=[(X0+0.9,X0+3.9),(X1-3.9,X1-0.9)]
leds=[box(a,b,YF-0.01,YF+1.0,11.3,13.0) for a,b in led_w]
shield=shell.cut(cav)
for l in leds: shield=shield.cut(l)
liner=box(CX-5.85,CX+5.85,YF+0.4,YF+DEPTH,2.0,8.9).union(box(CX-3.1,CX+3.1,YF+0.4,YF+DEPTH,8.9,10.6))
inner=liner.cut(box(CX-5.45,CX+5.45,YF+0.39,YF+DEPTH-0.4,2.4,8.5)).cut(box(CX-2.7,CX+2.7,YF+0.39,YF+DEPTH-0.4,8.4,10.2))
contacts=None
for i in range(8):
    c=box(CX-3.57+i*1.02-0.2,CX-3.57+i*1.02+0.2,YF+1.5,YF+9.0,2.4,2.75)
    contacts=c if contacts is None else contacts.union(c)
ledg=box(led_w[0][0],led_w[0][1],YF+0.05,YF+1.0,11.3,13.0); ledy=box(led_w[1][0],led_w[1][1],YF+0.05,YF+1.0,11.3,13.0)
def pin(x,y,d,L=3.05): return cq.Workplane('XY').circle(d/2).extrude(-L).translate((x,-y,0))
pins=None
for x,y in [(0,0),(1.26,-2.54),(2.54,0),(3.8,-2.54),(5.08,0),(6.34,-2.54),(7.62,0),(8.88,-2.54)]:
    p=pin(x,y,0.5); pins=p if pins is None else pins.union(p)
for x,y in [(11.165,8.9),(11.165,10.93),(-2.285,8.9),(-2.285,10.93)]: pins=pins.union(pin(x,y,0.6))
for x in (-3.435,12.315): pins=pins.union(box(x-0.15,x+0.15,-3.31-0.7,-3.31+0.7,-3.05,0.5))
posts=pin(-1.275,6.36,3.0,2.9).union(pin(10.155,6.36,3.0,2.9))
a=cq.Assembly(name='HanRun_HR915340A')
a.add(shield,name='shield',color=STEEL); a.add(inner,name='insert',color=BLACK); a.add(contacts,name='contacts',color=GOLD)
a.add(ledg,name='led_green',color=GREEN); a.add(ledy,name='led_yellow',color=YELLOW)
a.add(pins,name='pins',color=TIN); a.add(posts,name='posts',color=DARK)
a.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),'HanRun_HR915340A.step'))

"""Placement corrections for the fab: for each polarised / multi-pin part number, compare the fab library footprint
(pads read with the catalog's pinout tool on 2026-11-15, y down) with our footprint and find the rotation offset
(ours = fab rotated counter-clockwise by theta) and where the fab footprint's origin lies in our footprint (dx, dy).
Writes tools/fab_placement.csv. usage: tools/fab_placement_fit.py [--write]   (re-run after a footprint or part change)"""
import re, sys, math, csv, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
# LCSC: (reference pads of the fab footprint {number: (x, y)}, optional map fab pad number -> our pad number, note)
FAB = {
 'C178640':   ({'1': (-2.67, 0), '2': (2.67, 0)}, {'1': '2', '2': '1'}, 'fab footprint -RD: its pad 1 is the negative pad; ours pad 1 is +'),
 'C19077471': ({'1': (-1.25, -0.95), '2': (-1.25, 0.95), '3': (1.25, 0)}, None, ''),
 'C19077396': ({'1': (-1.635, 0), '2': (1.635, 0)}, None, 'pad 1 = cathode in both'),
 'C125094':   ({'1': (-0.749, 0), '2': (0.749, 0)}, None, 'pad 1 = cathode in both'),
 'C19077569': ({'1': (-2.15, 0), '2': (2.15, 0)}, None, 'pad 1 = cathode in both'),
 'C7420333':  ({'1': (1, 0.95), '2': (1, -0.95), '3': (-1, 0)}, None, ''),
 'C7420339':  ({'1': (1, 0.95), '2': (1, -0.95), '3': (-1, 0)}, None, ''),
 'C3200405':  ({'1': (0.64, 0.75), '4': (0.64, -0.75), '5': (-0.64, -0.75), '8': (-0.64, 0.75)}, None, ''),
 'C42394092': ({'1': (1.35, 0.95), '3': (1.35, -0.95), '4': (-1.35, -0.95), '6': (-1.35, 0.95)}, None, ''),
 'C2149796':  ({'1': (0.95, 0.65), '3': (0.95, -0.65), '4': (-0.95, -0.65), '6': (-0.95, 0.65)}, None, ''),
 'C506609':   ({'1': (-0.975, 1.435), '4': (0.975, 1.435), '5': (0.975, -1.435)}, None, 'fab lands are longer; rows 0.035 mm further apart'),
 'C3010298':  ({'1': (-3.9, -1.905), '4': (-3.9, 1.905), '5': (3.9, 1.905), '8': (3.9, -1.905)}, None, ''),
 'C3702980':  ({'1': (-0.65, 0), '2': (0.65, 0)}, 'by-net:2=GND', 'fab pad 2 = GND'),
 'C70590':    ({'1': (-1.1, 0.85), '2': (1.1, 0.85), '3': (1.1, -0.85), '4': (-1.1, -0.85)}, None, ''),
 'C19711727': ({'1': (-1.1, 0.85), '2': (1.1, 0.85), '3': (1.1, -0.85), '4': (-1.1, -0.85)}, None, ''),
 'C49101620': ({'1': (-2.1, 0.925), '2': (2.1, 0.925)}, None, 'fitted on the two signal pads; the mounting lugs are drawn differently'),
 'C88374':    ({'1': (0, 0.762), '2': (-1.475, -0.762), '3': (1.475, -0.762)}, 'ufl', 'fab pad 1 = signal, 2 / 3 = ground lugs'),
 'C719027':   ({'1': (3.175, 5.4), '8': (-4.525, 5.4), '4': (-0.125, 5.4)}, None, ''),
 'C3020560':  ({'A5': (-1.25, -2.372), 'A8': (1.25, -2.373), 'B5': (1.75, -2.372), 'B8': (-1.75, -2.373), 'A6': (-0.25, -2.372), 'B7': (-0.75, -2.372)}, None, 'fab footprint drawn for another maker\'s USB-C'),
 'C492365':   ({'1': (4.2, 2.75), '3': (-4.2, 2.75), '4': (4.2, -2.75), '6': (-4.2, -2.75)}, None, ''),
 'C2982043':  ({'1': (-3.81, 0), '4': (3.81, 0)}, None, ''),
 'C2845614':  ({'1': (1.975, 1), '2': (2.025, -1), '5': (-2.025, 1), '6': (-1.975, -1)}, ('fixed', 0, 0.0, 0.0), 'same 2x3 hole grid and pin-1 corner; the pads are numbered in another order (ours by rows, fab zigzag)'),
 'C54909':    ({'1': (2.1, 2.75), '2': (-2.1, 2.75), '3': (2.1, -2.75), '4': (-2.1, -2.75)}, ('fixed', 0, 0.0, 0.0), 'same 2x2 hole grid, pin 1 in the same row; pad numbers mirrored. CHECK the latch side in the preview'),
 'C2915006':  ({'1': (-2.54, 0), '3': (2.54, 0)}, None, ''),
 'C2760325':  ({'1': (4.445, 4.19), '8': (-4.445, 6.73), '9': (-6.725, -4.7), '12': (6.725, -6.73)}, None, 'fab footprint agrees with ours pad for pad'),
 'C437089':   ({'1': (8, 1), '2': (8, -1), '17': (-8, 1), '18': (-8, -1)}, None, ''),
 'C2798300':  ({'1': (-5.889, -4.496), '12': (-4.496, 5.889), '23': (5.889, 4.496), '34': (4.496, -5.889), '45': (-2.7, -3.607)}, None, 'fab pitch 0.889 mm, ours 0.9 mm'),
 'C5272606':  ({'1': (-6.057, -5.425), '33': (-5.425, 6.057), '65': (6.058, 5.425), '97': (5.425, -6.057)}, None, ''),
}
t = (R / 'MujinaControl-S19.kicad_pcb').read_text()
starts = [m.start() for m in re.finditer(r'\n\t\(footprint "', t)] + [len(t)]
fps = {}
for a, b in zip(starts, starts[1:]):
    blk = t[a:b]
    ref = re.search(r'\(property "Reference" "([^"]+)"', blk).group(1)
    lcsc = re.search(r'\(property "LCSC" "([^"]*)"', blk)
    name = re.match(r'\n\t\(footprint "([^"]+)"', blk).group(1)
    tr = re.search(r'\(transform\s+\(translate ([-\d.]+) ([-\d.]+)\)\s+\(rotate ([-\d.]+)\)', blk)
    pads = {}
    for m in re.finditer(r'\(pad "([^"]*)" (\w+) (\w+)\s+\(at ([-\d.]+) ([-\d.]+)', blk):
        seg = blk[m.start():m.start() + 900]; net = re.search(r'\(net "?([^")\n]*)', seg)
        pads.setdefault(m.group(1), []).append((float(m.group(4)), float(m.group(5)), net.group(1).strip() if net else '', m.group(2)))
    fps[ref] = dict(name=name, lcsc=lcsc.group(1) if lcsc else '', pos=(float(tr.group(1)), float(tr.group(2))), rot=float(tr.group(3)), pads=pads, dnp='(attr' in blk and 'dnp' in re.search(r'\(attr[^)]*\)', blk).group(0))
def rot(p, th):                      # counter-clockwise on screen, y down
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th)); return (p[0] * c + p[1] * s, -p[0] * s + p[1] * c)
rows = []
for lcsc, (fab, pmap, note) in FAB.items():
    refs = sorted(r for r, f in fps.items() if f['lcsc'] == lcsc and not f['dnp'])
    if not refs:                                   # no fitted part with this number any more (kept in the table for reference)
        print(f"{lcsc:10s} not fitted on the board; skipped"); continue
    names = {fps[r]['name'] for r in refs}; assert len(names) == 1, (lcsc, names)
    f = fps[refs[0]]
    if isinstance(pmap, tuple) and pmap[0] == 'fixed':
        rows.append(dict(LCSC=lcsc, Footprint=f['name'].split(':')[-1], Refs=' '.join(refs), RotationOffset=pmap[1], dX=pmap[2], dY=pmap[3], Residual='', Note=note))
        print(f"{lcsc:10s} {f['name'].split(':')[-1][:44]:44s} theta {pmap[1]:3d}  origin at ({pmap[2]:+.3f}, {pmap[3]:+.3f})  set by hand        {' '.join(refs)[:34]}")
        continue
    ours = {}
    for num, p in fab.items():
        if pmap == 'ufl':
            sig = [k for k, v in f['pads'].items() if len(v) == 1][0]; gnd = [k for k, v in f['pads'].items() if len(v) == 2][0]
            ours[num] = [f['pads'][sig][0][:2]] if num == '1' else None
        elif isinstance(pmap, str) and pmap.startswith('by-net'):
            g = [k for k, v in f['pads'].items() if v[0][2] == 'GND']; assert len(g) == 1, (lcsc, f['pads'])
            ours[num] = [f['pads'][g[0] if num == '2' else [k for k in f['pads'] if k != g[0]][0]][0][:2]]
        else:
            k = (pmap or {}).get(num, num); assert k in f['pads'], (lcsc, num, sorted(f['pads']))
            ours[num] = [v[:2] for v in f['pads'][k]]
    best = None
    for th in (0, 90, 180, 270):
        pts = [(rot(fab[n], th), o[0]) for n, o in ours.items() if o]
        tx = sum(o[0] - q[0] for q, o in pts) / len(pts); ty = sum(o[1] - q[1] for q, o in pts) / len(pts)
        res = max(math.hypot(o[0] - q[0] - tx, o[1] - q[1] - ty) for q, o in pts)
        if pmap == 'ufl':                               # one signal pad fixes the offset; the two ground lugs fix the angle
            lugs = [f['pads'][k] for k in f['pads'] if len(f['pads'][k]) == 2][0]
            res = max(min(math.hypot(l[0] - (rot(fab[n], th)[0] + tx), l[1] - (rot(fab[n], th)[1] + ty)) for l in lugs) for n in ('2', '3'))
        if best is None or res < best[1]: best = (th, res, tx, ty)
    th, res, tx, ty = best
    rows.append(dict(LCSC=lcsc, Footprint=f['name'].split(':')[-1], Refs=' '.join(refs), RotationOffset=th, dX=round(tx, 3), dY=round(ty, 3), Residual=round(res, 3), Note=note))
    print(f"{lcsc:10s} {f['name'].split(':')[-1][:44]:44s} theta {th:3d}  origin at ({tx:+.3f}, {ty:+.3f})  residual {res:.3f}  {' '.join(refs)[:34]}")
bad = [r for r in rows if r['Residual'] != '' and r['Residual'] > 0.3]
print('poor fits:', [(r['LCSC'], r['Residual']) for r in bad])
if '--write' in sys.argv:
    with (R / 'tools/fab_placement.csv').open('w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print('wrote tools/fab_placement.csv')

"""Generate original SVG diagrams, demo data, and a short captioned animation.

Run with --video to regenerate the committed MP4 (requires imageio-ffmpeg).
"""
from pathlib import Path
import argparse
import html
import json
import sys
import textwrap
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'notebooks'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rewiring import city,geojson,map_image,HATS

ASSETS=ROOT/'notebooks/assets'
ASSETS.mkdir(exist_ok=True)
def lines(text,x,y,width=35,color='#b9d5df',size=19,leading=27):
    return ''.join(f'<text x="{x}" y="{y+i*leading}" fill="{color}" font-size="{size}">{html.escape(line)}</text>' for i,line in enumerate(textwrap.wrap(text,width)))
def diagram(name,title,cards,caption):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 380" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(caption)}</desc><rect width="1080" height="380" rx="16" fill="#0b1c2b"/><g font-family="system-ui,sans-serif"><text x="30" y="47" fill="#67e8f9" font-size="27" font-weight="700">{html.escape(title)}</text>'
    for i,(heading,body) in enumerate(cards):
        x=30+i*350
        svg+=f'<rect x="{x}" y="80" width="320" height="215" rx="14" fill="#153448" stroke="#316277"/><circle cx="{x+38}" cy="119" r="20" fill="#67e8f9"/><text x="{x+38}" y="126" fill="#08202b" font-size="21" text-anchor="middle" font-weight="700">{i+1}</text>'
        svg+=lines(heading,x+22,168,26,'#ffffff',22)+lines(body,x+22,207,28)
        if i<2:svg+=f'<path d="M {x+327} 190 h 15 m -6 -6 l 6 6 -6 6" fill="none" stroke="#67e8f9" stroke-width="3"/>'
    svg+=lines(caption,30,338,95,'#d6e5eb',17)+'</g></svg>'
    (ASSETS/f'{name}.svg').write_text(svg,encoding='utf-8')

diagram('decision-loop','Rewire the decision, not only the tool',[
 ('Listen and frame','Whose question is this? What would a better outcome mean?'),
 ('Model and compare','Connect evidence, geography, uncertainty, and alternatives.'),
 ('Review and learn','People choose the action. Measure benefits and unintended effects.')],
 'A feedback loop: new outcomes and community experience should change the next question.')
diagram('data-journey','A catalog is a doorway to evidence',[
 ('Discover','STAC locates an asset. C3S provides product-specific climate information.'),
 ('Inspect','Check time, units, resolution, missing values, license, and provenance.'),
 ('Interpret','A geographic pattern is a question to investigate, not a causal explanation.')],
 'Keep satellite metadata, climate observations, projections, and synthetic teaching data distinct.')
diagram('scene-contract','A rich scene still needs a clear contract',[
 ('Location','Coordinates, CRS, scale, and geography define where the layer belongs.'),
 ('Meaning','Units and time explain what each color, column, and surface represents.'),
 ('Responsibility','Privacy, uncertainty, and audience determine what should be shown.')],
 'Pair every 3D scene with an accessible 2D view and an inspectable data table.')
diagram('cube-to-table','One dataset, three ways to ask',[
 ('Cube','Time × latitude × longitude. Chunks organize the array for reading.'),
 ('Table','Materialize a bounded slice. SQL filters and aggregates explicit rows.'),
 ('Linked views','Map where, chart when, and inspect exact values before drawing conclusions.')],
 'Zarr is an array format. This lab materializes a small subset into SQLite; it is not a remote SQL engine.')
diagram('world-model','A model of change needs a reality check',[
 ('State and action','Describe a place and the intervention you want to examine.'),
 ('Transition','State what changes, what stays fixed, and what the mechanism assumes.'),
 ('Observe and evaluate','Compare outputs with evidence, uncertainty, and human priorities.')],
 'Prediction is not causation. A mapped simulation is not automatically a validated digital twin.')
diagram('privacy-layers','Protection happens before and after encryption',[
 ('Minimize','Collect and keep only the precision and attributes the task requires.'),
 ('Protect','Use aggregation when appropriate. Encrypt with authenticated cryptography.'),
 ('Review the release','Keys, outputs, screenshots, and linked data all affect disclosure risk.')],
 'Encryption protects a payload. It does not make the decrypted map anonymous or ethically appropriate.')

svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 600" role="img" aria-labelledby="title desc"><title id="title">Six perspectives and a synthesis step</title><desc id="desc">White evidence, red experience, black caution, yellow benefit, green alternatives, and blue process contribute to a purple synthesis. Humans retain decision authority.</desc><rect width="1080" height="600" rx="16" fill="#0b1c2b"/><g font-family="system-ui,sans-serif"><text x="32" y="46" fill="#67e8f9" font-size="28" font-weight="700">See the whole question together</text>'
for i,(role,(color,body)) in enumerate(HATS.items()):
    x=30+(i%3)*350; y=80+(i//3)*175
    svg+=f'<rect x="{x}" y="{y}" width="320" height="153" rx="14" fill="#153448" stroke="{color}"/><path d="M {x+22} {y+37} h 46 m -37 0 v -15 h 27 v 15" stroke="{color}" fill="none" stroke-width="6"/>'
    svg+=lines(role,x+22,y+72,28,color,21)+lines(body,x+22,y+103,33,'#d4e5eb',17,22)
svg+='<path d="M 195 427 L 420 465 M 540 427 L 540 465 M 895 427 L 660 465" stroke="#c4a5f4" stroke-width="3"/><rect x="220" y="462" width="640" height="75" rx="16" fill="#503876"/><text x="540" y="493" text-anchor="middle" fill="white" font-size="24">Synthesize without erasing disagreement</text><text x="540" y="520" text-anchor="middle" fill="#e2d8f3" font-size="17">Human judgment, accountable ownership, explicit next steps</text><text x="30" y="573" fill="#b9d5df" font-size="16">Inspired by de Bono’s Six Thinking Hats. Purple synthesis is this project’s extension.</text></g></svg>'
(ASSETS/'hats-review.svg').write_text(svg,encoding='utf-8')

cells,cube=city()
dest=ROOT/'demos/data'; dest.mkdir(parents=True,exist_ok=True)
(dest/'cube.json').write_text(json.dumps({'data_status':'synthetic','seed':2026,'license':'CC-BY-4.0',
 'cells':cells.round(6).to_dict('records'),'values':{k:v.reshape(24,-1).round(4).tolist() for k,v in cube.items()}},separators=(',',':')),encoding='utf-8')
(dest/'heat-grid.geojson').write_text(json.dumps(geojson(cells,cube['heat_c'][0],'heat_c'),separators=(',',':')),encoding='utf-8')

parser=argparse.ArgumentParser();parser.add_argument('--video',action='store_true');args=parser.parse_args()
if args.video:
    import imageio_ffmpeg
    from matplotlib.animation import FFMpegWriter
    plt.rcParams['animation.ffmpeg_path']=imageio_ffmpeg.get_ffmpeg_exe()
    video=ROOT/'demos/assets';video.mkdir(exist_ok=True)
    rates=cube['rate_per_1000']; overall=1000*cube['cases'].sum(axis=(1,2))/cells.population.sum()
    fig,axes=plt.subplots(1,2,figsize=(10,4.8),dpi=100,layout='constrained')
    image=map_image(axes[0],rates[0],'Month 1',rates.min(),rates.max())
    fig.colorbar(image,ax=axes[0],label='Events per 1,000 synthetic people',shrink=.7)
    axes[1].plot(np.arange(1,25),overall,color='#0e7490')
    cursor=axes[1].axvline(1,color='#b45309')
    axes[1].set(xlabel='Synthetic month',ylabel='Events per 1,000',title='Population-weighted citywide rate',xlim=(1,24))
    fig.suptitle('SYNTHETIC teaching data · no observed health or climate measurements',fontsize=11)
    fig.savefig(video/'climate-poster.png')
    writer=FFMpegWriter(fps=4,metadata={'title':'Synthetic climate-health map walkthrough','artist':'Rewiring Global Health'},codec='libx264',extra_args=['-pix_fmt','yuv420p','-movflags','+faststart'])
    with writer.saving(fig,str(video/'climate-story.mp4'),100):
        for month in range(24):
            image.set_data(rates[month]);axes[0].set_title(f'Synthetic month {month+1} / 24')
            cursor.set_xdata([month+1,month+1])
            for _ in range(2): writer.grab_frame()
    plt.close(fig)
print('Generated diagrams and demo data'+(' and video' if args.video else ''))

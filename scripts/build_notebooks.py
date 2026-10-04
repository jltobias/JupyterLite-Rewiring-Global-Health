"""Author the ten lessons. Run from repository root, then execute_notebooks.py.

Notebook prose/code lives here for reviewable diffs. Generated notebooks are committed.
"""
from pathlib import Path
import textwrap
import nbformat as nb

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://jltobias.github.io/JupyterLite-Rewiring-Global-Health'
REPO = 'https://github.com/jltobias/JupyterLite-Rewiring-Global-Health/blob/main'
CELLS = []


def md(text):
    CELLS.append(nb.v4.new_markdown_cell(textwrap.dedent(text).strip()))


def code(text):
    CELLS.append(nb.v4.new_code_cell(textwrap.dedent(text).strip()))


def start(title, objectives, packages=()):
    CELLS.clear()
    wheel_setup = "\n        await micropip.install('emfs:./wheels/asciitree-0.3.3-py3-none-any.whl')" if 'zarr==2.18.7' in packages else ''
    md(f'''# {title}

**Decision question.** {objectives}

**Time:** 30–45 minutes. **Prerequisites:** basic Python arrays and tables. Run cells from top to bottom.
The shared `rewiring.py` module must stay beside the notebooks. Initial package downloads require internet;
the core calculations use reproducible synthetic data. No health-service credentials are needed.

**Data contract:** the fictional grid is geographically anchored near Gaborone for teaching map coordinates.
Its people, facilities, climate, events, and model parameters are invented. It is **not a map of actual
Gaborone disease, vulnerability, buildings, or care access**. Satellite catalog metadata, when used, is labeled separately.

[Book]({SITE}/) · [Interactive demo gallery]({SITE}/demos/) · [Data and credits]({REPO}/DATA_SOURCES.md)
''')
    code(f'''
    import sys
    if sys.platform == 'emscripten':
        import micropip{wheel_setup}
        await micropip.install({['numpy', 'pandas', 'matplotlib', *packages]!r})
    import json
    from pathlib import Path
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from IPython.display import display, HTML, IFrame
    from rewiring import (city, long_table, map_image, map_matrix, geojson,
                          leaflet, save_export, simulate_twin, teaching_review, HATS, SITE, LABEL, EXTENT)
    plt.rcParams.update({{'figure.dpi': 105, 'axes.spines.top': False, 'axes.spines.right': False}})
    cells, cube = city()
    panel = long_table(cells, cube)
    print(LABEL)
    print('Python', sys.version.split()[0], '| cells:', len(cells), '| monthly observations:', len(panel))
    ''')


def finish(filename, exercise, sources):
    md(f'''## Investigate, interpret, and discuss

{exercise}

**Before sharing:** state the decision, data status, units, denominator, scale, uncertainty, and who can contest the result.
Record what would change your conclusion. Export only information that the intended audience needs.

## Sources and attribution

{sources}

Original lesson code: MIT. Original narrative, synthetic data, and generated figures: CC BY 4.0.
Third-party data, videos, services, and software retain their own terms.
[Full references]({REPO}/REFERENCES.md) · [Third-party notices]({REPO}/THIRD_PARTY_NOTICES.md).
''')
    notebook = nb.v4.new_notebook(cells=list(CELLS), metadata={
        'kernelspec': {'display_name': 'Python (Pyodide)', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python'},
        'rewiring': {'data_status': 'synthetic', 'seed': 2026, 'license_code': 'MIT', 'license_content': 'CC-BY-4.0'}})
    for i, cell in enumerate(notebook.cells):
        cell.id = f'{filename[:2]}-{i:02d}'
    path = ROOT / 'notebooks' / filename
    if path.exists():
        previous = nb.read(path, as_version=4)
        old = {c.id:c for c in previous.cells}
        unchanged = all(c.id in old and c.source == old[c.id].source for c in notebook.cells if c.cell_type == 'code')
        if unchanged:
            for c in notebook.cells:
                if c.cell_type == 'code':
                    c.outputs = old[c.id].outputs
                    c.execution_count = old[c.id].execution_count
            if 'widgets' in previous.metadata:
                notebook.metadata.widgets = previous.metadata.widgets
    nb.validate(notebook)
    nb.write(notebook, path)


start('00 · Rewiring decisions, relationships, and evidence',
      'How could a heat outreach team connect evidence, community knowledge, and service access without turning a score into a decision?')
md('''## From connectivity to cooperation

Tobias's Spatial Plexus presentation (2013, PDF pp. 2, 5, 12) frames rewiring as an invitation to
reconsider persistent problems, connect disciplines, and evaluate gains against possible harms.
Zuckerman's *Rewire* argues that technical connectivity alone does not ensure cross-cultural understanding.
Here that becomes a design question: whose knowledge enters an analysis, and whose voice can change it?

![Decision loop: evidence, models, community review, action, and learning](assets/decision-loop.svg)

The diagram is an original explanation, not an endorsement of any particular intervention.
''')
code('''
layers = ['Community', 'Health services', 'Climate', 'Mobility', 'Models', 'Governance']
angles = np.linspace(0, 2*np.pi, len(layers), endpoint=False)
xy = np.c_[np.cos(angles), np.sin(angles)]
edges = [(0,1),(0,5),(1,3),(1,4),(2,4),(3,4),(4,5),(0,4)]
fig, ax = plt.subplots(figsize=(9,6))
for i,j in edges:
    ax.plot(xy[[i,j],0], xy[[i,j],1], color='#94a3b8', lw=2)
ax.scatter(*xy.T, s=2400, color='#a5f3fc', edgecolors='#155e75', zorder=3)
for (x,y),name in zip(xy,layers): ax.text(x,y,name,ha='center',va='center',fontsize=10)
ax.set(xlim=(-1.5,1.5), ylim=(-1.25,1.25), title='Connections are responsibilities, not just data transfers')
ax.axis('off'); plt.show()
''')
md('''## Compare priorities and show the value choices

Heat, access, and vulnerability have different units. We normalize them to 0–1 within this synthetic
sample before weighting. Normalization makes arithmetic possible; it does not make the weights objective.
An outreach priority is not an individual risk prediction. Keep population denominators available.
''')
code('''
features = cells[['access_min','vulnerability']].copy()
features['heat_c'] = cube['heat_c'].mean(axis=0).ravel()
normalized = (features - features.min()) / (features.max() - features.min())
weights = np.array([.3,.4,.3])
cells['priority'] = normalized.to_numpy() @ weights
display(cells[['cell_id','population','access_min','vulnerability','priority']].nlargest(8,'priority'))
fig, ax = plt.subplots(figsize=(7,5))
im = map_image(ax, cells.priority.to_numpy().reshape(8,8), 'A deliberation input, not an allocation rule',0,1)
fig.colorbar(im, ax=ax, label='Weighted synthetic priority (0–1)'); plt.show()
''')
md('''## Would a different set of values change the map?

Compare an access-first, vulnerability-first, and heat-first policy with identical color limits.
A stable ranking across these alternatives is different from a ranking that depends on one choice of weights.
The weights below are examples for discussion; no ethical principle sets these numeric values.
''')
code('''
policies = {'Access first': [.6,.2,.2], 'Vulnerability first':[.2,.6,.2], 'Heat first':[.2,.2,.6]}
scores = {name: normalized.to_numpy() @ w for name,w in policies.items()}
map_matrix([v.reshape(8,8) for v in scores.values()], list(scores), 'Priority (0–1)', limits=(0,1))
plt.show()
top_sets = {name:set(np.argsort(v)[-8:]) for name,v in scores.items()}
overlap = pd.DataFrame({a:{b:len(sa & sb)/len(sa | sb) for b,sb in top_sets.items()}
                        for a,sa in top_sets.items()})
display(overlap.rename_axis('Top-eight Jaccard overlap'))
''')
md('''## A decision record that keeps the human question visible

Record the intended benefit, uncertainty, community involvement, and a stop condition before a pilot.
The linked Public Health Informatics Case Studies provide another teaching pattern: reason from evidence
and test alternatives. The 1854 cholera examples are historical resources; the grid here is invented.
''')
code('''
decision = {
 'question':'Where should a local team investigate heat outreach needs?',
 'evidence_status':'synthetic exercise; replace with governed local evidence',
 'alternatives':['universal outreach','community nominated sites','score assisted review'],
 'missing':['service capacity','community priorities','validated heat-health relationship'],
 'reviewers':['local health team','community representatives','privacy steward'],
 'stop_if':'The pilot displaces essential services or exposes sensitive locations.',
 'evaluation':'Compare reach, access gaps, costs, and adverse effects before expanding.'}
display(pd.Series(decision, name='Decision record'))
print(save_export('decision-record.json', decision))
''')
finish('00_rewiring_global_health.ipynb', '''1. Add a community-defined criterion. Explain how it would be collected and governed.
2. Compare the top eight cells under equal weights. Which cells are sensitive to the policy choice?
3. Propose a non-AI intervention and an outcome that would justify continuing it.''', '''- Tobias, J. L. (2013), *Rewiring to meet the challenges of “Wicked Problems” within global and domestic Public Health*, supplied presentation, pp. 2, 5, 12.
- Zuckerman, E. (2013), *Rewire*. [Author's book page](https://ethanzuckerman.com/books/rewire/).
- [PHI Case Studies](https://github.com/PHI-Case-Studies) and [1854 cholera browser case study](https://phi-case-studies.github.io/Jupyterlite-1854-Cholera-Basic/lab/index.html).
- WHO (2021), [Ethics and governance of AI for health](https://www.who.int/publications/i/item/9789240029200).''')

start('01 · Climate, STAC, and Copernicus C3S',
      'How do we discover relevant Earth observations and distinguish a climate signal from a synthetic health association?')
md('''## Discovery is not evidence of a health effect

STAC describes where and when assets exist. C3S provides climate products and the Interactive Climate Atlas
provides exploration of climate information. A Sentinel-2 image is not a C3S temperature projection.
We inspect real satellite metadata, then use a separately labeled synthetic cube to practice calculations.

![Discovery to interpretation](assets/data-journey.svg)
''')
code('''
snapshot = json.loads(Path('data/stac-snapshot.json').read_text())
catalog = pd.DataFrame([{'id':f['id'], 'datetime':f['properties']['datetime'],
                        'cloud_percent':f['properties'].get('eo:cloud_cover'),
                        'assets':len(f['assets'])} for f in snapshot['items']])
print('OBSERVED SATELLITE CATALOG METADATA | retrieved',snapshot['retrieved'])
display(catalog)
''')
md('''## Optional live metadata request

The bundled snapshot makes the lesson repeatable. Set `LIVE_STAC=True` to request up to three items from
Element 84 Earth Search. No raster is downloaded. Catalog availability and browser CORS rules can change;
a failed request leaves the snapshot available. The query covers January 2025, not current conditions.
''')
code('''
LIVE_STAC = False
if LIVE_STAC:
    try:
        if sys.platform == 'emscripten':
            from pyodide.http import pyfetch
            response = await pyfetch(snapshot['source_url'])
            if response.status != 200: raise RuntimeError(f'HTTP {response.status}')
            live = await response.json()
        else:
            import urllib.request
            with urllib.request.urlopen(snapshot['source_url'], timeout=20) as response:
                live = json.load(response)
        print('Live item IDs:', [f['id'] for f in live['features']])
    except Exception as exc:
        print('Live metadata unavailable; bundled snapshot still usable:', type(exc).__name__)
else:
    print('Using the bundled satellite metadata snapshot; no external request made.')
''')
md('''## Inspect an asset contract

Before loading a band, inspect its media type, scale/offset, CRS, resolution, missing values, and license.
Cloud percentage for a whole scene is not the cloud fraction over your study area. Satellite reflectance
cannot be relabeled as temperature or disease incidence.
''')
code('''
item = snapshot['items'][0]
asset = item['assets']['red']
display(pd.Series({k:asset.get(k) for k in ['href','type','roles','raster:bands','eo:bands','proj:shape']}))
print('License links:', [link['href'] for link in item['links'] if link['rel']=='license'])
''')
md('''## Synthetic anomalies and spatial comparison

An anomaly needs a reference period. Here it is each cell's first twelve invented monthly temperatures,
not a climatological 30-year normal. Compare two seasons with the same temperature scale, and use a
diverging scale centered on zero for departures from that reference.
''')
code('''
heat = cube['heat_c']
reference = heat[:12].mean(axis=0)
anomaly = heat - reference
map_matrix(heat[[0,6,12]], ['Month 1','Month 7','Month 13'], 'Temperature (°C)', cmap='magma')
plt.show()
limit = float(np.abs(anomaly).max())
map_matrix(anomaly[[0,6,12]], ['Month 1 anomaly','Month 7 anomaly','Month 13 anomaly'],
           'Departure from first-year mean (°C)', cmap='RdBu_r', limits=(-limit,limit))
plt.show()
''')
code('''
monthly = panel.groupby('month')[['heat_c','rain_mm','cases']].mean()
fig, axes = plt.subplots(3,1,figsize=(10,7),sharex=True,layout='constrained')
for ax,name in zip(axes,monthly):
    ax.plot(monthly.index+1,monthly[name],marker='o'); ax.set_ylabel(name)
axes[-1].set_xlabel('Synthetic month'); fig.suptitle('Separate units, aligned time axes'); plt.show()
''')
md('''## A C3S Atlas exercise with a reproducible record

Open the [Copernicus Interactive Climate Atlas](https://atlas.climate.copernicus.eu/).
Choose a region, temperature indicator, reference period, scenario/warming level, and future period.
Compare model spread as well as the ensemble mean. Export the provenance supplied by the product.
Use the [Climate Data Store](https://cds.climate.copernicus.eu/) for product-specific access and terms.
The notebook does not imply that CDS account credentials belong in public browser code.
''')
code('''
provenance = pd.DataFrame({'field':['product and version','producer','reference period','future period',
 'scenario / warming level','units','grid / CRS','ensemble statistic','license and DOI','retrieval date'],
 'record':['REQUIRED: fill from selected product']*10})
display(provenance)
''')
finish('01_climate_stac_c3s.ipynb', '''1. Change the reference window to all 24 synthetic months. Which anomaly comparisons change?
2. Record an actual C3S Atlas selection in the provenance table; do not overwrite the synthetic-data label.
3. Explain why a temperature–case correlation is insufficient to estimate a causal intervention effect.''', '''- [STAC Sentinel-2 tutorial](https://stacspec.org/en/tutorials/access-sentinel-2-data-aws/).
- [Element 84 Earth Search](https://github.com/Element84/earth-search), bundled item metadata retrieved 2026-10-04; Copernicus Sentinel-2 source imagery remains at the provider.
- [Copernicus C3S Atlas](https://atlas.climate.copernicus.eu/) and [CDS](https://cds.climate.copernicus.eu/); no C3S raster data redistributed here.
- Tobias (2026), *JupyterLite: Geospatial Data Science and Global Health*, supplied presentation.''')

start('02 · 2D maps, 3D surfaces, and access',
      'How does representation change our understanding of access, and which assumptions drive an access estimate?', ('folium==0.20.0','plotly'))
md('''## Start with an accessible 2D view

Our access variable assumes straight-line walking at 4 km/h to one of two fictional facilities, plus
five minutes of overhead. It omits roads, rivers, opening hours, fees, disability, and travel mode.
Coordinates are longitude/latitude; conversion to kilometers is a local approximation. Do not measure
Euclidean distance directly in degrees or treat these contours as real catchments.
''')
code('''
terrain = cells.elevation_m.to_numpy().reshape(8,8)
access = cells.access_min.to_numpy().reshape(8,8)
fig, axes = plt.subplots(1,2,figsize=(12,5),layout='constrained')
for ax,z,title,unit in zip(axes,[terrain,access],['Invented terrain','Walking proxy'],['meters','minutes']):
    im=map_image(ax,z,title); fig.colorbar(im,ax=ax,label=unit)
plt.show()
''')
md('''## Maps should support inspection

Hover to inspect the cell ID, value, population, and synthetic status. This Leaflet view intentionally
has no external basemap tiles; the graticule and coordinates are sufficient for the lesson. The map
library loads from a CDN, so a static plot above remains available without that dependency.
''')
code('''
display(leaflet(cells, access, 'access_min'))
''')
md('''## A surface is one possible view of a variable

The vertical axis below represents invented elevation in meters. Color and perspective cannot establish
data quality. A surface between grid centers interpolates visually; no additional observations are created.
''')
code('''
lon=cells.lon.to_numpy().reshape(8,8); lat=cells.lat.to_numpy().reshape(8,8)
fig=plt.figure(figsize=(9,6)); ax=fig.add_subplot(projection='3d')
surface=ax.plot_surface(lon,lat,terrain,cmap='terrain',edgecolor='white',linewidth=.3)
ax.set(xlabel='Longitude',ylabel='Latitude',zlabel='Invented elevation (m)',title='Synthetic terrain: examine the vertical scale')
ax.ticklabel_format(useOffset=False)
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
for axis in [ax.xaxis,ax.yaxis]:
    axis.set_major_locator(MaxNLocator(4)); axis.set_major_formatter(FormatStrFormatter('%.2f'))
fig.colorbar(surface,ax=ax,shrink=.6,label='m',pad=.12); plt.show()
''')
code('''
import plotly.graph_objects as go
interactive = go.Figure(go.Surface(x=lon,y=lat,z=terrain,colorscale='Earth'))
interactive.update_layout(title='Orbit the synthetic terrain',height=470,
    scene=dict(xaxis_title='Longitude',yaxis_title='Latitude',zaxis_title='Elevation (m)'))
display(HTML(interactive.to_html(full_html=False, include_plotlyjs='cdn')))
''')
md('''## Sensitivity belongs beside the map

Recompute travel time under 3, 4, and 5 km/h walking assumptions. Keep the five-minute overhead fixed.
Report a population-weighted accessibility measure, rather than the fraction of equally sized grid cells.
A 30-minute threshold here is an exercise parameter, not a recommended service standard.
''')
code('''
speeds = [3,4,5]
scenarios = [5 + (access-5)*4/speed for speed in speeds]
map_matrix(scenarios,[f'{s} km/h' for s in speeds],'Travel-time proxy (minutes)')
plt.show()
shares=[np.average(z.ravel()<=30,weights=cells.population) for z in scenarios]
display(pd.DataFrame({'speed_kmh':speeds,'population_share_within_30min':shares}))
''')
finish('02_geospatial_intelligence_2d_3d.ipynb', '''1. Compare cell-weighted and population-weighted coverage. Explain the difference.
2. Simulate a 15-minute service delay in the eastern half and redraw the access map.
3. List the evidence needed for actual travel-time routing and an inclusive access assessment.''', '''- Tobias (2013), supplied presentation, service availability and delivery examples, pp. 27–28.
- [Folium documentation](https://python-visualization.github.io/folium/latest/) and [Plotly 3D surfaces](https://plotly.com/python/3d-surface-plots/).
- All terrain, population, and facilities in this exercise are generated by `rewiring.py`.''')

start('03 · GeoLibre, interoperable layers, and 3D scenes',
      'How can a notebook hand a documented layer to browser GIS without losing its meaning?', ('folium==0.20.0',))
md('''## A scene is a collection of data contracts

GeoLibre supports browser GIS workflows including vector styling and 3D views. We export valid GeoJSON,
inspect its properties, and load it in the external viewer. The companion 3D demo uses MapLibre to extrude
the same grid. Column height represents an index, not physical building height.

![Layers, context, and interpretation](assets/scene-contract.svg)
''')
code('''
layer=geojson(cells,cube['heat_c'][0],'heat_c')
target=save_export('synthetic-heat-grid.geojson',layer)
assert len(layer['features'])==64
assert layer['features'][0]['geometry']['coordinates'][0][0] == layer['features'][0]['geometry']['coordinates'][0][-1]
print(target)
display(pd.Series(layer['features'][0]['properties']))
''')
md('''## Open your exported layer in GeoLibre

1. Right-click `exports/synthetic-heat-grid.geojson` in the JupyterLite file browser and download it.
2. Open [GeoLibre Web](https://web.geolibre.app/) and add the downloaded GeoJSON using its file/layer controls.
3. Style polygons by `heat_c`; inspect `population` and `data_status` in the attribute table.
4. Compare a 2D map and an extrusion. Label the extrusion's meaning and exaggeration.

Alternatively, add the hosted [synthetic grid URL](https://jltobias.github.io/JupyterLite-Rewiring-Global-Health/demos/data/heat-grid.geojson).
The viewer below is external and initially empty of our layer. If iframe embedding is blocked, use the direct link.
The public viewer's runtime messaging interface is not assumed available to this notebook.
''')
code('''
display(IFrame('https://web.geolibre.app/?layout=compact',width='100%',height=480))
''')
md('''## Compare the same layer before and after a handoff

A valid GeoJSON polygon has longitude before latitude and a closed ring. A loss of units or synthetic status
is a failed handoff even when the file still renders. Examine the local preview before uploading any layer.
''')
code('''
display(leaflet(cells,cube['heat_c'][0],'heat_c'))
contract=pd.DataFrame({'layer':['grid polygons','temperature','population','extrusion'],
 'units':['degrees, WGS84','degrees C','synthetic people','display units'],
 'time':['fixed grid','month 1','fixed for exercise','month selected'],
 'meaning':['fictional analysis units','generated seasonality','invented denominator','visual encoding, not buildings']})
display(contract)
''')
md('''## Try the companion scene

Open the [3D scene demo](https://jltobias.github.io/JupyterLite-Rewiring-Global-Health/demos/scene.html).
Tilt, rotate, switch to 2D, and select a month. The data table provides the values independently of WebGL.
No street or building data is bundled.

## Watch a creator-hosted walkthrough

Open Geospatial Solutions / Qiusheng Wu: *GeoLibre 1.0: A Free, Open-Source Cloud-Native GIS That Runs Anywhere*.
[Watch on YouTube](https://www.youtube.com/watch?v=87Cm0QagtxI) or see the [written tutorial](https://geolibre.app/tutorials/).
This external video is linked/embedded, not redistributed. Use the written tutorial as the text alternative.
''')
code('''
display(IFrame('https://www.youtube-nocookie.com/embed/87Cm0QagtxI',width='100%',height=410))
''')
finish('03_geolibre_3d_scene.ipynb', '''1. Add a layer-level provenance field and verify it survives download and import.
2. Explain how extrusion can amplify or obscure differences compared with a choropleth.
3. Design a layer stack for an informal-settlement service assessment without publishing household locations.''', '''- Tobias (2026), supplied JupyterLite presentation, GeoLibre examples pp. 38–43.
- Wu, Q., [GeoLibre](https://geolibre.app/), [sharing and embedding guide](https://geolibre.app/tutorials/sharing-embedding/), and [video tutorials](https://geolibre.app/tutorials/videos/).
- [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/).''')

start('04 · Animated maps, small multiples, and lag',
      'Which spatial and temporal patterns can we see, and how do we avoid reading causality into a moving map?')
md('''## Animation and small multiples answer different questions

Animation directs attention to change; a map matrix supports comparisons without remembering previous frames.
Both need consistent color limits, temporal resolution, and missing-data rules. Our monthly series has a
known generated seasonal component. Counts also depend on the invented population distribution.
''')
code('''
chosen=[0,2,4,6,8,10]
map_matrix(cube['rate_per_1000'][chosen],[f'Month {t+1}' for t in chosen],
           'Generated events per 1,000 synthetic people',columns=3)
plt.show()
''')
md('''## An animated choropleth with a fixed scale

Use play, pause, and frame controls. Pause before comparing distant times; the static matrix is an equal
part of the analysis. The animation below is generated locally and makes no calls to a map service.
''')
code('''
from matplotlib.animation import FuncAnimation
series=cube['rate_per_1000']
fig,ax=plt.subplots(figsize=(6,4.8),layout='constrained')
im=map_image(ax,series[0],'Synthetic month 1',series.min(),series.max())
fig.colorbar(im,ax=ax,label='Events per 1,000 synthetic people')
def update(frame):
    im.set_data(series[frame]); ax.set_title(f'Synthetic month {frame+1} / {len(series)}')
    return (im,)
animation=FuncAnimation(fig,update,frames=len(series),interval=250,blit=False)
plt.close(fig)
display(HTML(animation.to_jshtml(default_mode='once')))
''')
md('''## Use denominators and align the time axis

The citywide rate is total events divided by total population. It is not an unweighted average of cell rates.
A heatmap puts every cell on the same time axis; a Hovmöller-style diagram averages over longitude to
compare north–south patterns through time. Averaging can hide local differences, so retain the map matrix.
''')
code('''
overall=1000*series.reshape(24,-1).dot(cells.population.to_numpy())/cells.population.sum()/1000
fig,axes=plt.subplots(2,1,figsize=(11,7),layout='constrained')
im=axes[0].imshow(series.reshape(24,-1).T,aspect='auto',origin='lower',cmap='magma')
axes[0].set(xlabel='Month index (0–23)',ylabel='Cell ID',title='Every cell, aligned time')
fig.colorbar(im,ax=axes[0],label='Events / 1,000')
im=axes[1].imshow(cube['heat_c'].mean(axis=2).T,aspect='auto',origin='lower',cmap='magma')
axes[1].set(xlabel='Month index (0–23)',ylabel='South → north grid row',title='Longitude-mean temperature')
fig.colorbar(im,ax=axes[1],label='°C'); plt.show()
''')
md('''## A lag demonstration without circular wraparound

We deliberately generate events associated with rainfall three weeks earlier. Missing early lags remain
missing, rather than borrowing rainfall from the end of the year. A correlation peak in this constructed
example verifies the mechanism we wrote; it is not evidence for a biological lag in real populations.
''')
code('''
rng=np.random.default_rng(7)
rain=pd.Series(rng.gamma(3,15,104),name='rain_mm')
lagged=rain.shift(3)
events=20+.35*lagged+rng.normal(0,3,104)
correlations=pd.Series({lag:rain.shift(lag).corr(events) for lag in range(9)})
fig,axes=plt.subplots(1,2,figsize=(12,4),layout='constrained')
axes[0].plot(events,label='Constructed events'); axes[0].plot(.35*lagged+20,label='Lagged signal',alpha=.6)
axes[0].set(xlabel='Week',ylabel='Synthetic event index'); axes[0].legend()
axes[1].bar(correlations.index,correlations); axes[1].set(xlabel='Rainfall lag (weeks)',ylabel='Pearson correlation')
plt.show()
assert events.iloc[:3].isna().all()
''')
finish('04_animated_health_climate_timeseries.ipynb', '''1. Compare counts with rates. Which places change rank and why?
2. Introduce missing observations into months 5–7. Show missingness rather than replacing it with zero.
3. Change the generated lag to five weeks. Discuss confounding and multiple testing in real lag searches.''', '''- [Matplotlib animation](https://matplotlib.org/stable/api/animation_api.html).
- [Related Zarr teaching atlas](https://github.com/jltobias/JupyterLite-zarr-sql-views).
- All animation frames and time series are original synthetic examples. No clinical or climate inference is intended.''')

start('05 · Zarr space–time cubes and SQL views',
      'How can a bounded cube support maps, neighborhood summaries, and reproducible queries?', ('xarray==2025.9.0','zarr==2.18.7','plotly'))
md('''## Three representations, one question

A cube preserves time and two spatial axes. A SQL table makes selection and grouping explicit. A map shows
where the result applies. Zarr stores arrays in chunks; SQL does not magically make every Zarr store a database.
Here we materialize a small selected subset into SQLite, which is available in Pyodide. The companion
project explores DuckDB-Wasm and larger browser workflows.

![Cube, rows, and views](assets/cube-to-table.svg)

The lesson pins Zarr 2.18.7 for its synchronous, browser-compatible in-memory store. It does not require a
threaded Zarr 3 runtime, distributed scheduler, cloud account, or remote object store.
''')
code('''
import xarray as xr, zarr, sqlite3
lat=cells.lat.unique(); lon=cells.lon.unique()
ds=xr.Dataset({name:(('time','lat','lon'),values.astype('float32')) for name,values in cube.items()},
              coords={'time':pd.date_range('2025-01-01',periods=24,freq='MS'),'lat':lat,'lon':lon},
              attrs={'data_status':'synthetic','crs':'EPSG:4326','source':'rewiring.py, seed=2026'})
ds['heat_c'].attrs['units']='degree_Celsius'; ds['rain_mm'].attrs['units']='mm/month'
ds['cases'].attrs['units']='synthetic events/month'; ds['rate_per_1000'].attrs['units']='events/1000 people/month'
store=zarr.storage.MemoryStore()
encoding={name:{'chunks':(6,4,4)} for name in cube}
ds.to_zarr(store,mode='w',encoding=encoding,consolidated=True)
restored=xr.open_zarr(store,chunks=None,consolidated=True)
assert np.allclose(restored.heat_c,ds.heat_c)
print('Zarr',zarr.__version__,'| stored keys:',len(store),'| bytes:',sum(len(v) for v in store.values()))
display(restored)
''')
md('''## Chunk layout is a query design choice

Our 24×8×8 cube uses chunks of 6×4×4. A single monthly map intersects four chunks; one cell's full
history intersects four chunks. Reading one value can therefore require decoding additional values.
Cloud queries also have per-request latency, compression, and caching costs that this byte count omits.
''')
code('''
shape=np.array([24,8,8]); chunks=np.array([6,4,4])
display(pd.DataFrame({'layout':['time-major (6,4,4)','spatial-slice (1,8,8)','point-history (24,1,1)'],
 'chunks_for_one_map':[4,1,64], 'chunks_for_one_history':[4,24,1],
 'float32_values_per_chunk':[96,64,24]}))
print('Raw bytes in one heat variable:',ds.heat_c.nbytes)
''')
md('''## A parameterized SQL view with a denominator

We materialize months 1–12 only. SQL parameters keep data values separate from query syntax.
The query reports population-weighted temperature and an event rate from totals. Duplicating rows in a
join would bias both, so check row uniqueness before aggregation.
''')
code('''
subset=panel[panel.month<12].copy()
assert not subset.duplicated(['month','cell_id']).any()
con=sqlite3.connect(':memory:')
subset.to_sql('observations',con,index=False,if_exists='replace')
con.execute('CREATE VIEW eastern_cells AS SELECT * FROM observations WHERE col >= 4')
sql=''' + '"""' + '''SELECT month, SUM(population) AS population,
 SUM(heat_c*population)/SUM(population) AS weighted_heat_c,
 1000.0*SUM(cases)/SUM(population) AS events_per_1000
 FROM eastern_cells WHERE heat_c >= ? GROUP BY month ORDER BY month''' + '"""' + '''
result=pd.read_sql_query(sql,con,params=(28.0,))
display(result)
assert (result.population>0).all()
con.close()
''')
md('''## Orbit a space–time cube

The third axis below is **month**, not height. Markers are cell centers, colored by temperature.
The filter selects hot values, so empty space means “excluded by the filter”, not missing data or zero.
Use the slider in the [linked demo](https://jltobias.github.io/JupyterLite-Rewiring-Global-Health/demos/) for a 2D alternative.
''')
code('''
import plotly.graph_objects as go
selected=panel[panel.heat_c>=30]
fig=go.Figure(go.Scatter3d(x=selected.lon,y=selected.lat,z=selected.month+1,mode='markers',
 marker=dict(size=3,color=selected.heat_c,colorscale='Magma',colorbar=dict(title='°C')),
 text=selected.cell_id,hovertemplate='Cell %{text}<br>lon %{x}<br>lat %{y}<br>month %{z}<extra></extra>'))
fig.update_layout(title='Synthetic space–time cube: heat ≥ 30°C',height=520,
 scene=dict(xaxis_title='Longitude',yaxis_title='Latitude',zaxis_title='Month'))
display(HTML(fig.to_html(full_html=False,include_plotlyjs='cdn')))
''')
code('''
map_matrix(restored.heat_c.isel(time=[0,6,12]).values,['Month 1','Month 7','Month 13'],'Temperature (°C)',cmap='magma')
plt.show()
region=restored.heat_c.sel(lon=slice(25.95,26.05)).mean(['lat','lon'])
region.plot(figsize=(9,3)); plt.ylabel('Unweighted regional mean (°C)'); plt.show()
''')
finish('05_zarr_sql_views.ipynb', '''1. Change chunk shapes and calculate read amplification for one monthly map.
2. Replace the eastern-cell view with the western half. Keep units, filter, and denominators visible.
3. Explain why filtering on heat changes the population included in each monthly rate.''', '''- [Zarr 2 documentation](https://zarr.readthedocs.io/en/v2.18.7/) and [xarray Zarr I/O](https://docs.xarray.dev/en/stable/user-guide/io.html#zarr).
- [SQLite](https://sqlite.org/) and [DuckDB-Wasm](https://duckdb.org/docs/stable/clients/wasm/overview).
- [jltobias/Zarr SQL teaching atlas](https://github.com/jltobias/JupyterLite-zarr-sql-views), itself inspired by [dzole0311/zarr-sql-views](https://github.com/dzole0311/zarr-sql-views). No upstream implementation code is copied in this lesson.''')

start('06 · GeoAI, spatial validation, and world models',
      'When does a fitted spatial relationship fail to generalize, and how is prediction different from scenario simulation?')
md('''## Learn a relationship, then test it outside its training geography

GeoAI combines geographic structure with machine learning. We fit a small linear model using NumPy so
every assumption is inspectable. The target is a generated event rate, not a diagnosis. Train on the
western half and test on the eastern half; a random split mixes nearby cells and can hide spatial shift.
This one split is an illustration, not a sufficient validation design for deployment.
''')
code('''
table=cells.copy()
table['heat_c']=cube['heat_c'].mean(axis=0).ravel()
table['target']=cube['rate_per_1000'].mean(axis=0).ravel()
X=np.c_[np.ones(len(table)),table[['heat_c','access_min','vulnerability']].to_numpy()]
y=table.target.to_numpy()
west=table.col.to_numpy()<4
coef=np.linalg.lstsq(X[west],y[west],rcond=None)[0]
prediction=X@coef
mae=lambda a,b: float(np.mean(np.abs(a-b)))
display(pd.Series(coef,index=['intercept','heat_c','access_min','vulnerability'],name='Fitted coefficients'))
print('West training MAE:',round(mae(y[west],prediction[west]),3))
print('East held-out MAE:',round(mae(y[~west],prediction[~west]),3))
''')
code('''
residual=y-prediction
fig,axes=plt.subplots(1,3,figsize=(13,4),layout='constrained')
for ax,z,title in zip(axes,[y,prediction,residual],['Synthetic target','Fitted rate','Residual: target − fitted']):
    limits=(-np.abs(residual).max(),np.abs(residual).max()) if title.startswith('Residual') else (min(y.min(),prediction.min()),max(y.max(),prediction.max()))
    im=map_image(ax,z.reshape(8,8),title,*limits,cmap='RdBu_r' if title.startswith('Residual') else 'viridis')
    fig.colorbar(im,ax=ax,label='Events / 1,000')
plt.show()
''')
md('''## Baselines and failure modes

Compare a learned model against a training-mean baseline. Then introduce a synthetic east-side reporting
shift. A model can predict the training process well and still fail when measurement or service access
changes. A high score is not sufficient evidence of portability, calibration, equity, or causal meaning.
''')
code('''
rng=np.random.default_rng(6)
random_train=rng.random(len(table))<.5
random_coef=np.linalg.lstsq(X[random_train],y[random_train],rcond=None)[0]
shifted=y.copy(); shifted[~west]+=6
metrics=pd.DataFrame({'evaluation':['East: mean baseline','East: spatial holdout','Random holdout','East: reporting shift'],
 'MAE':[mae(y[~west],np.repeat(y[west].mean(),(~west).sum())),mae(y[~west],prediction[~west]),
        mae(y[~random_train],(X@random_coef)[~random_train]),mae(shifted[~west],prediction[~west])]})
display(metrics)
''')
md('''## A grounded world model needs a transition and an observation model

Represent state as heat, access, and vulnerability; define an action; specify how state changes; and
separately specify how measurements arise. Below the transition is hand-written and coefficients vary
across an ensemble. It is **not a learned foundation world model** and its action effects are assumptions.

![State, action, transition, observation, and evaluation](assets/world-model.svg)

A frontier research question is how learned spatial representations can support physically and socially
plausible transitions while preserving uncertainty, local knowledge, and human agency.
''')
code('''
def transition(state, heat_delta=0, access_delta=0):
    future=state.copy()
    future['heat_c']+=heat_delta
    future['access_min']=np.maximum(5,future.access_min+access_delta)
    return future
scenarios={'Baseline':transition(table),'Hotter':transition(table,heat_delta=2),
           'Hotter + access':transition(table,heat_delta=2,access_delta=-15)}
def assumed_burden(state,heat_effect=1.6):
    return np.maximum(0,8+heat_effect*(state.heat_c-25)+6*state.vulnerability+.025*state.access_min)
surfaces=[assumed_burden(s).to_numpy().reshape(8,8) for s in scenarios.values()]
map_matrix(surfaces,list(scenarios),'Assumed event rate per 1,000'); plt.show()
''')
code('''
ensemble=[]
for effect in np.linspace(.6,2.6,41):
    for name,state in scenarios.items():
        ensemble.append((name,effect,np.average(assumed_burden(state,effect),weights=state.population)))
ensemble=pd.DataFrame(ensemble,columns=['scenario','assumed_heat_effect','weighted_rate'])
display(ensemble.groupby('scenario').weighted_rate.agg(['min','median','max']))
fig,ax=plt.subplots(figsize=(9,4))
for name,g in ensemble.groupby('scenario'): ax.plot(g.assumed_heat_effect,g.weighted_rate,label=name)
ax.set(xlabel='Assumed heat coefficient',ylabel='Assumed weighted event rate'); ax.legend(); plt.show()
''')
finish('06_geoai_world_models.ipynb', '''1. Repeat geographic validation by withholding north, south, east, and west in turn.
2. Map missingness and consider which communities a training dataset might underrepresent.
3. Describe the evidence required before interpreting the action transition as a causal effect.
4. Define a physical constraint, a social constraint, and a stopping rule for a learned world model.''', '''- [GeoAI project](https://github.com/opengeos/geoai), broader methods and tooling; not a dependency here.
- Ha, D. & Schmidhuber, J. (2018), [World Models](https://worldmodels.github.io/).
- Tobias et al. (2026), supplied Gaborone digital-twin presentation, pp. 4, 16, 21.
- WHO (2021), [ethics and governance guidance](https://www.who.int/publications/i/item/9789240029200).''')

start('07 · AI chat, six perspectives, and accountable orchestration',
      'How can an assistant support deliberation while preserving provenance, disagreement, and human decision authority?', ('ipywidgets',))
md('''## Six perspectives, with an explicit synthesis step

Edward de Bono's Six Thinking Hats is a human parallel-thinking method. This notebook uses the hats as
computational review roles inspired by your supplied global-health diagram. The purple synthesis step is
a project-specific extension, not an original seventh hat. Template responses below are deterministic;
they do not claim to be language-model inference or authentic community testimony.

![Six perspectives and synthesis](assets/hats-review.svg)
''')
code('''
summary={'data_status':'synthetic','cells':len(cells),'mean_heat_c':round(float(cube['heat_c'].mean()),2),
         'population':int(cells.population.sum())}
question='What evidence would justify a neighborhood heat-outreach pilot?'
reviews=teaching_review(question,summary)
display(pd.DataFrame(reviews)[['role','consideration','evidence']])
''')
md('''## A chat interface that makes its mode visible

The widget accepts a question and produces structured teaching prompts. It sends nothing to an external
model. Do not enter sensitive personal information. An ordinary Python call above gives the same result
when widgets are unavailable in a static book or assistive workflow.
''')
code('''
import ipywidgets as widgets
entry=widgets.Textarea(value=question,description='Question:',layout=widgets.Layout(width='95%',height='80px'))
button=widgets.Button(description='Review (template)',button_style='info')
output=widgets.Output()
def review_click(_):
    with output:
        output.clear_output(wait=True)
        display(pd.DataFrame(teaching_review(entry.value[:1000],summary))[['role','consideration']])
button.on_click(review_click)
display(widgets.VBox([widgets.HTML('<b>Teaching mode · deterministic · no model call</b>'),entry,button,output]))
''')
md('''## Preserve disagreement instead of averaging it away

Orchestration means coordinating roles and evidence, not turning a majority vote into truth. A privacy
objection can require changing the analysis even if the opportunity is attractive. A model should not
infer what a community feels: that perspective requires engagement with actual people.
''')
code('''
record={'question':question,'data_summary':summary,
 'agreement':['Use aggregate evidence','Evaluate outreach reach and unintended effects'],
 'unresolved':['Which communities are absent from the data?','Can services meet newly identified demand?'],
 'next_actions':['Seek community priorities','Check denominators','Test a bounded pilot'],
 'human_owner':'Workshop team; replace with a named accountable owner in actual work',
 'decision_status':'Not approved for operational use'}
display(pd.Series(record))
print(save_export('deliberation.json',record))
''')
md('''## JupyterLite AI is included in the site

The build installs **jupyterlite-ai**, the browser-capable chat/completion extension, which is distinct
from server-dependent integrations. Open its chat panel in JupyterLite. No provider credentials or model
endpoint are shipped in this public site. Provider setup is required before real model inference.

For institutional use, configure an authenticated, approved model gateway and keep long-lived provider
secrets on the server. Review notebook-context sharing, retention, authorization, and costs before enabling
a model. The extension's secrets manager defaults to in-memory key handling; disabling it can persist
keys in browser settings. An in-memory browser key is still accessible to the client.

[Extension documentation](https://jupyterlite-ai.readthedocs.io/en/latest/) ·
[API-key handling](https://jupyterlite-ai.readthedocs.io/en/latest/api-keys/) ·
[custom provider integration](https://jupyterlite-ai.readthedocs.io/en/latest/custom-providers/).
''')
md('''## An explicit gateway request contract

This adapter is for a gateway **you implement and govern**, not a claim that GitHub Pages provides an AI API.
The request includes only the known synthetic summary and question. A schema is not a privacy detector:
free text can still contain sensitive material. Do not enable it until the endpoint and authorization are reviewed.
No model response is executed as code, SQL, or a tool command.
''')
code('''
async def ask_gateway(endpoint, question, summary):
    from urllib.parse import urlparse
    if urlparse(endpoint).scheme != 'https': raise ValueError('Use an approved HTTPS endpoint')
    teaching_review(question,summary)  # explicit aggregate input contract, not content screening
    payload={'schema_version':1,'question':question,'summary':summary,
             'response_contract':{'answer':'string','sources':'list of strings','uncertainties':'list of strings'}}
    if sys.platform != 'emscripten':
        raise RuntimeError('This sample adapter uses browser authenticated fetch; implement a native client separately')
    from pyodide.http import pyfetch
    response=await pyfetch(endpoint,method='POST',headers={'Content-Type':'application/json'},
                           credentials='include',body=json.dumps(payload))
    if response.status!=200: raise RuntimeError(f'Gateway returned HTTP {response.status}')
    result=await response.json()
    if (not isinstance(result,dict) or not isinstance(result.get('answer'),str)
        or not all(isinstance(result.get(k),list) and all(isinstance(v,str) for v in result[k])
                   for k in ['sources','uncertainties'])):
        raise ValueError('Gateway response violates the contract')
    return result
# No endpoint is configured and no request runs by default.
print('Gateway adapter defined; no model calls made.')
''')
finish('07_ai_orchestrator_privacy.ipynb', '''1. Add a dissent field to the synthesis record and preserve a minority concern.
2. Try a request that should remain a human decision; write the boundaries of acceptable assistance.
3. Review an assistant answer for invented citations, causal overclaims, and requests for unnecessary precision.
4. Explain the difference between schema validation, authentication, privacy review, and factual verification.''', '''- de Bono, E. (1985), *Six Thinking Hats*.
- [Related Six Hats agents project](https://github.com/jltobias/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats).
- [Project Jupyter: AI in Jupyter](https://jupyter.org/ai) and [jupyterlite-ai](https://github.com/jupyterlite/ai).
- Supplied global-health Six Thinking Hats image: conceptual inspiration; this lesson's SVG is an original explanatory drawing.''')

start('08 · Spatial agents, digital twins, and scenario uncertainty',
      'What does an intervention change in a transparent synthetic model, and how uncertain is that comparison?')
md('''## A deliberately bounded model

The supplied Gaborone presentation describes a much richer, calibrated spatial workflow with buildings,
mobility, clinical cascades, and uncertainty. This lesson uses 640 invented agents assigned to 64 grid cells.
States are susceptible (S), latent (L), infectious (I), treatment (T), and recovered (R). The transition
probabilities are arbitrary teaching inputs, not TB natural-history estimates or Kopanyo study parameters.

Transitions use the **start-of-week state**, so an agent cannot pass through several disease states in one
week. Infection pressure combines local and citywide prevalence. Recovered agents remain recovered;
there are no births, deaths, reinfections, movement, or drug-resistance states.

![State, action, and observation loop](assets/world-model.svg)
''')
code('''
baseline,maps=simulate_twin(seed=3,detection=.08)
intervention,intervention_maps=simulate_twin(seed=3,detection=.16)
display(baseline.head())
fig,axes=plt.subplots(1,2,figsize=(12,4),layout='constrained')
baseline.set_index('week').plot(ax=axes[0]); axes[0].set(title='Synthetic compartments',ylabel='Agents')
axes[1].plot(baseline.week,baseline.I,label='Detection 0.08/week')
axes[1].plot(intervention.week,intervention.I,label='Detection 0.16/week')
axes[1].set(xlabel='Week',ylabel='Infectious agents',title='One paired realization'); axes[1].legend(); plt.show()
''')
md('''## Inspect where the model concentrates events

These cell counts describe synthetic model state, not spatial estimates of actual TB. Counts in small
populations can fluctuate strongly. The shared color scale is essential when comparing intervention rows.
''')
code('''
chosen=[0,13,26]
map_matrix(np.concatenate([maps[chosen],intervention_maps[chosen]]),
           [f'Baseline week {t}' for t in chosen]+[f'Intervention week {t}' for t in chosen],
           'Synthetic infectious agents',columns=3)
plt.show()
''')
md('''## Compare many paired runs

For each seed, scenarios begin with the same agents and random draws. Pairing reduces some Monte Carlo
noise but does not remove uncertainty in parameters, mechanisms, or observation processes. The interval
below describes variability across these runs, **not a confidence interval for real intervention efficacy**.
''')
code('''
rows=[]
for seed in range(24):
    base,_=simulate_twin(seed,detection=.08)
    scenario,_=simulate_twin(seed,detection=.16)
    # Left endpoint convention: 52 weekly intervals, excludes the terminal point.
    b=float(base.I.iloc[:-1].sum()); s=float(scenario.I.iloc[:-1].sum())
    rows.append((seed,b,s,b-s))
trials=pd.DataFrame(rows,columns=['seed','baseline_infectious_agent_weeks','scenario_infectious_agent_weeks','difference'])
display(trials.difference.quantile([.05,.5,.95]).rename('Paired synthetic agent-week difference'))
fig,ax=plt.subplots(figsize=(9,4)); ax.hist(trials.difference,bins=10,color='#0f766e')
ax.axvline(0,color='black'); ax.set(xlabel='Baseline − scenario infectious agent-weeks',ylabel='Runs',title='Stochastic variation, 24 seeds')
plt.show()
''')
md('''## Parameter sensitivity and observational limits

A digital twin requires a documented relationship with observations and regular evaluation. A one-off
simulation with a map is not sufficient. Vary the invented detection probability; do not describe the
resulting curve as cost-effectiveness without a cost model and an appropriate health outcome measure.
''')
code('''
rows=[]
for detection in [.04,.08,.12,.16]:
    values=[simulate_twin(seed,detection=detection)[0].I.iloc[:-1].sum() for seed in range(12)]
    rows.append([detection,np.mean(values),*np.quantile(values,[.1,.9])])
sensitivity=pd.DataFrame(rows,columns=['detection','mean','p10','p90'])
fig,ax=plt.subplots(figsize=(9,4)); ax.plot(sensitivity.detection,sensitivity['mean'],marker='o')
ax.fill_between(sensitivity.detection,sensitivity.p10,sensitivity.p90,alpha=.25)
ax.set(xlabel='Assumed weekly detection probability',ylabel='Infectious agent-weeks',title='Synthetic sensitivity, 12 seeds per setting'); plt.show()
''')
code('''
model_card={'purpose':'Teach spatial simulation and scenario comparison',
 'population':'640 invented agents; no Kopanyo participant data',
 'time_step':'one week; synchronous transitions',
 'calibration':'none', 'validation':'state conservation and reproducibility only',
 'not_represented':['HIV','subclinical TB','MDR','households','mobility','deaths','care costs'],
 'evidence_needed':['governed data','clinical and epidemiologic review','calibration','external validation','community review']}
display(pd.Series(model_card)); print(save_export('model-card.json',model_card))
''')
finish('08_digital_twin_global_health.ipynb', '''1. Change the weight on local infection pressure in `simulate_twin`; compare spatial patterns.
2. Add an observation model that detects only some infectious agents. Distinguish notifications from prevalence.
3. Explain why a reduction in infectious agent-weeks cannot automatically be labeled deaths or DALYs averted.
4. Specify calibration targets, external validation data, and governance before a real decision-support pilot.''', '''- Tobias, J. L., Tolentino, H., Wuhib, T., Moonan, P., & Oeltmann, J. (2026), supplied Gaborone/Kopanyo presentation, pp. 4, 14–17, 21.
- [Starsim](https://starsim.org/), named in the presentation; this lesson implements an independent small NumPy model.
- No source study data or confidential system artifacts are redistributed.''')

start('09 · Geoprivacy, aggregation, and authenticated encryption',
      'What information should we share, and what does encryption protect after that decision?', ('cryptography',))
md('''## Different controls answer different questions

Encryption protects a payload from readers without the key. Aggregation changes the precision of what is
shared. Masking perturbs positions. None alone establishes anonymity, authorization, or ethical acceptability.
The supplied map-encryption presentation emphasizes all of these layers, including keys, metadata, and exports.

![Minimize, aggregate, encrypt, review](assets/privacy-layers.svg)
''')
code('''
rng=np.random.default_rng(9)
points=pd.DataFrame({'x_km':rng.uniform(0,12,120),'y_km':rng.uniform(0,12,120)})
masked=points+rng.normal(0,.65,points.shape)
fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
for ax,p,title in zip(axes,[points,masked],['Invented exact points','Gaussian-jittered points']):
    ax.scatter(p.x_km,p.y_km,s=14); ax.set(xlabel='Local x (km)',ylabel='Local y (km)',title=title,aspect='equal',xlim=(-2,14),ylim=(-2,14))
plt.show()
''')
md('''## Measure a masking tradeoff, without promising anonymity

Compare nearest-facility distances before and after perturbation. Changing locations can affect access
inferences, while auxiliary information may still make a record linkable. Clipping points at a boundary
can introduce additional spatial bias. These invented points have no identities or real addresses.
''')
code('''
facility=np.array([6,6])
before=np.linalg.norm(points.to_numpy()-facility,axis=1)
after=np.linalg.norm(masked.to_numpy()-facility,axis=1)
print('Mean absolute access-distance distortion (km):',round(float(np.abs(before-after).mean()),3))
print('Share crossing an arbitrary 4-km boundary:',round(float(np.mean((before<=4)!=(after<=4))),3))
''')
md('''## Aggregate, suppress, and inspect utility

Count points in fixed bins, and hide counts below a chosen threshold. This is a simple display rule,
not a proof of k-anonymity or differential privacy. Other maps, totals, and overlapping releases can reveal
suppressed values. Blank bins below represent suppressed counts, including zeros; document that choice.
''')
code('''
edges=np.arange(0,13,2)
counts,_,_=np.histogram2d(points.y_km,points.x_km,bins=[edges,edges])
threshold=5
shared=np.where(counts>=threshold,counts,np.nan)
fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
for ax,z,title in zip(axes,[counts,shared],['All synthetic bin counts',f'Display only counts ≥ {threshold}']):
    im=ax.imshow(z,origin='lower',extent=[0,12,0,12],vmin=0,vmax=counts.max())
    ax.set(xlabel='x (km)',ylabel='y (km)',title=title); fig.colorbar(im,ax=ax,label='Synthetic points')
plt.show()
print('Fraction of synthetic points in displayed bins:',round(float(np.nansum(shared)/counts.sum()),3))
''')
md('''## Real authenticated encryption, with a temporary teaching key

AES-GCM provides confidentiality and authentication. This cell generates a fresh 256-bit key and a fresh
96-bit nonce, encrypts the synthetic JSON, and verifies a round trip. Never reuse a nonce with the same key.
The key remains in kernel memory and is never printed or exported. Rerunning creates a new key; this is
an illustration, not durable key management, secure deletion, or a production security boundary.
''')
code('''
import os, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
payload=json.dumps({'data_status':'synthetic','points':points.round(4).to_dict('records')},sort_keys=True).encode()
key=AESGCM.generate_key(bit_length=256)
nonce=os.urandom(12)
aad=b'rewiring-synthetic-points:v1'
cipher=AESGCM(key)
ciphertext=cipher.encrypt(nonce,payload,aad)
decoded=cipher.decrypt(nonce,ciphertext,aad)
assert decoded==payload
print('Round trip verified | plaintext bytes:',len(payload),'| ciphertext bytes:',len(ciphertext))
print('Key and plaintext have not been printed.')
''')
md('''## Fail closed if the payload or key changes

An authenticated cipher must reject tampering. A successful round trip alone would not test that property.
Do not catch an integrity failure and silently fall back to plaintext. Metadata and screenshots can still
leak information even when the payload is encrypted.
''')
code('''
tampered=bytearray(ciphertext); tampered[0]^=1
for label,test_cipher,test_payload in [('tampered payload',cipher,bytes(tampered)),
                                      ('wrong key',AESGCM(AESGCM.generate_key(bit_length=256)),ciphertext)]:
    try:
        test_cipher.decrypt(nonce,test_payload,aad)
    except InvalidTag:
        print(label,': rejected as expected')
    else:
        raise AssertionError('Authentication failure was not detected')
envelope={'schema_version':1,'algorithm':'AES-256-GCM','data_status':'synthetic',
          'nonce_b64':base64.b64encode(nonce).decode(), 'aad':aad.decode(),
          'ciphertext_b64':base64.b64encode(ciphertext).decode()}
print(save_export('encrypted-synthetic-layer.json',envelope))
# The envelope cannot be recovered after the session key is lost; no key file is written.
''')
md('''## Review the complete release

The lowest-risk option may be not collecting precise coordinates in the first place. Separate collection,
analysis, sharing, and deletion decisions. For a real protected workflow, use organizational governance,
access control, key rotation/revocation, audit, and a reviewed threat model. A public static website does
not supply those controls merely because its Python executes locally.
''')
code('''
threats=pd.DataFrame({'threat':['raw file disclosure','small-area linkage','browser compromise','misleading public map'],
 'control':['minimize and encrypt','review aggregation and related releases','approved environment and access controls','label uncertainty and consult affected communities'],
 'remaining_limit':['key access reveals plaintext','aggregation is not an anonymity guarantee','client memory is not a secure enclave','a correct calculation can still stigmatize']})
display(threats)
''')
finish('09_geoprivacy_map_encryption.ipynb', '''1. Compare thresholds 3, 5, and 8. How much utility is lost, and what disclosure risks remain?
2. Alter the associated data (`aad`) and confirm decryption fails.
3. Design a key-distribution and revocation process without putting keys in a notebook, URL, or repository.
4. Explain why encryption does not make a published precise map private after decryption.''', '''- Tolentino, H., Tobias, J. L., Wuhib, T., & Mishra, V. (2026), *Map Encryption Democratized with JupyterLite*, supplied presentation, pp. 7–14, 27–30.
- [cryptography AESGCM API](https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM).
- Tobias (2013), supplied presentation, do-no-harm discussion p. 12.
- [PHI ethical geospatial data-science case study](https://github.com/PHI-Case-Studies/2023-Ethical-Practice-Geospatial-Data-Science).''')

print('Wrote 10 notebooks. Execute and validate them before publication.')

"""Small, deterministic teaching models. No patient or measured climate data.

Original code: MIT. Synthetic data and original figures: CC BY 4.0.
All distances use a local equirectangular approximation, unsuitable for routing.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FormatStrFormatter

SITE = "https://jltobias.github.io/JupyterLite-Rewiring-Global-Health"
EXTENT = [25.85, 26.05, -24.75, -24.55]
LABEL = "SYNTHETIC teaching data · not observations or a forecast"


def city(n=8, months=24, seed=2026):
    """Return cell table and (time, row, col) arrays; units in column names."""
    rng = np.random.default_rng(seed)
    dx = (EXTENT[1] - EXTENT[0]) / n
    dy = (EXTENT[3] - EXTENT[2]) / n
    lon = EXTENT[0] + (np.arange(n) + .5) * dx
    lat = EXTENT[2] + (np.arange(n) + .5) * dy
    xx, yy = np.meshgrid(lon, lat)
    xkm = (xx - lon.mean()) * 111.32 * np.cos(np.deg2rad(lat.mean()))
    ykm = (yy - lat.mean()) * 111.32
    terrain = 980 + 35 * np.sin(xkm / 3) * np.cos(ykm / 4)
    distance = np.minimum(np.hypot(xkm + 4, ykm + 2), np.hypot(xkm - 4, ykm - 3))
    minutes = 5 + distance / 4 * 60  # assumed 4 km/h walking; no road network
    population = rng.integers(400, 2400, (n, n))
    vulnerability = np.clip(.5 + .025 * xkm + rng.normal(0, .12, (n, n)), .1, .95)
    t = np.arange(months)[:, None, None]
    heat = (28 + 5 * np.cos(2 * np.pi * t / 12) + .18 * xkm + .08 * ykm
            + .03 * t + rng.normal(0, .6, (months, n, n)))
    rain = np.maximum(0, 50 + 40 * np.cos(2 * np.pi * (t - 1) / 12)
                      + rng.normal(0, 8, (months, n, n)))
    # A deliberately invented association, never a disease-risk estimate.
    rate = np.maximum(1, 8 + 1.6 * (heat - 25) + 6 * vulnerability + .025 * minutes)
    cases = rng.poisson(population[None, :, :] * rate / 1000)
    cells = pd.DataFrame(dict(cell_id=np.arange(n*n), row=np.repeat(np.arange(n), n),
                             col=np.tile(np.arange(n), n), lon=xx.ravel(), lat=yy.ravel(),
                             population=population.ravel(), vulnerability=vulnerability.ravel(),
                             access_min=minutes.ravel(), elevation_m=terrain.ravel()))
    cube = dict(heat_c=heat, rain_mm=rain, cases=cases,
                rate_per_1000=1000 * cases / population[None, :, :])
    return cells, cube


def long_table(cells, cube):
    frames = []
    for t in range(len(cube['heat_c'])):
        frame = cells.copy()
        frame['month'] = t
        for name, values in cube.items():
            frame[name] = values[t].ravel()
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def map_image(ax, values, title, vmin=None, vmax=None, cmap='viridis'):
    im = ax.imshow(values, origin='lower', extent=EXTENT, cmap=cmap,
                   vmin=vmin, vmax=vmax, interpolation='nearest')
    ax.set(xlabel='Longitude (degrees E)', ylabel='Latitude (degrees N)', title=title)
    ax.set_aspect(1 / np.cos(np.deg2rad(np.mean(EXTENT[2:]))))
    ax.ticklabel_format(useOffset=False)
    ax.xaxis.set_major_locator(MaxNLocator(4))
    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    return im


def map_matrix(arrays, titles, label, columns=3, cmap='viridis', limits=None):
    """Use one shared scale; comparisons must never autoscale each panel."""
    arrays = np.asarray(arrays)
    limits = limits or (np.nanmin(arrays), np.nanmax(arrays))
    rows = int(np.ceil(len(arrays) / columns))
    fig, axes = plt.subplots(rows, columns, figsize=(4.1 * columns, 3.6 * rows),
                             squeeze=False, layout='constrained')
    used = []
    for ax, values, title in zip(axes.flat, arrays, titles):
        im = map_image(ax, values, title, *limits, cmap=cmap)
        used.append(ax)
    for ax in list(axes.flat)[len(arrays):]:
        ax.set_visible(False)
    fig.colorbar(im, ax=used, shrink=.8, label=label)
    fig.suptitle(LABEL, fontsize=10)
    return fig


def geojson(cells, values=None, field='value'):
    n = int(round(np.sqrt(len(cells))))
    dx, dy = (EXTENT[1]-EXTENT[0])/n, (EXTENT[3]-EXTENT[2])/n
    features = []
    for k, row in enumerate(cells.to_dict('records')):
        x, y = row['lon'], row['lat']
        ring = [[x-dx/2,y-dy/2],[x+dx/2,y-dy/2],[x+dx/2,y+dy/2],
                [x-dx/2,y+dy/2],[x-dx/2,y-dy/2]]
        props = {key: value for key, value in row.items() if key not in ['lon','lat']}
        props['data_status'] = 'synthetic'
        if values is not None:
            props[field] = float(np.asarray(values).ravel()[k])
        features.append(dict(type='Feature', geometry=dict(type='Polygon', coordinates=[ring]),
                             properties=props))
    return dict(type='FeatureCollection', features=features)


def leaflet(cells, values, label='value'):
    import folium
    import branca.colormap as cm
    values = np.asarray(values).ravel()
    scale = cm.linear.viridis.scale(float(values.min()), float(values.max()))
    scale.caption = f'{label} | SYNTHETIC'
    # No basemap requests: this also works when map tile services are unavailable.
    m = folium.Map(location=[-24.65, 25.95], zoom_start=11, tiles=None,
                   control_scale=True, prefer_canvas=True)
    data = geojson(cells, values, label)
    folium.GeoJson(data, name='Synthetic grid',
                   style_function=lambda f: dict(fillColor=scale(f['properties'][label]),
                       fillOpacity=.8, color='#475569', weight=.6),
                   tooltip=folium.GeoJsonTooltip(fields=['cell_id',label,'population','data_status'])).add_to(m)
    scale.add_to(m)
    folium.LayerControl().add_to(m)
    m.fit_bounds([[EXTENT[2],EXTENT[0]],[EXTENT[3],EXTENT[1]]])
    return m


def save_export(name, data):
    folder = Path('exports'); folder.mkdir(exist_ok=True)
    target = folder / name
    target.write_text(json.dumps(data, indent=2, allow_nan=False), encoding='utf-8')
    return target


def simulate_twin(seed=0, detection=.08, weeks=52, agents=640):
    """Uncalibrated spatial S-L-I-T-R agent model with synchronous transitions.

    One transition maximum per agent/week. Same random draws permit paired scenarios.
    The force of infection mixes local and citywide infectious prevalence.
    """
    if not 0 <= detection <= 1 or agents < 80 or weeks < 1:
        raise ValueError('Invalid scenario parameters')
    rng = np.random.default_rng(seed)
    neighborhood = rng.integers(0, 64, agents)
    state = np.zeros(agents, dtype=int)
    state[:agents//5] = 1
    state[:agents//20] = 2
    rng.shuffle(state)
    population = np.bincount(neighborhood, minlength=64)
    records, surfaces = [], []
    for week in range(weeks + 1):
        counts = np.bincount(state, minlength=5)
        infectious = np.bincount(neighborhood[state == 2], minlength=64)
        records.append([week, *counts])
        surfaces.append(infectious.reshape(8,8))
        if week == weeks:
            break
        local = infectious / np.maximum(population, 1)
        pressure = .7 * local[neighborhood] + .3 * np.mean(state == 2)
        u = rng.random(agents)
        old = state.copy()
        state[(old == 0) & (u < np.minimum(.45 * pressure, 1))] = 1
        state[(old == 1) & (u < .012)] = 2
        state[(old == 2) & (u < detection)] = 3
        state[(old == 3) & (u < .12)] = 4
    frame = pd.DataFrame(records, columns=['week','S','L','I','T','R'])
    assert np.all(frame[['S','L','I','T','R']].sum(axis=1) == agents)
    return frame, np.array(surfaces)


HATS = {
    'White / evidence': ('#e2e8f0', 'Separate measured data, assumptions, and missing denominators.'),
    'Red / experience': ('#fda4af', 'Invite community concerns; never fabricate community testimony.'),
    'Black / caution': ('#94a3b8', 'Inspect disclosure, exclusion, error, and false certainty.'),
    'Yellow / benefit': ('#fde047', 'Name a testable benefit and who should receive it.'),
    'Green / alternatives': ('#86efac', 'Compare non-AI options and less invasive ways to answer.'),
    'Blue / process': ('#7dd3fc', 'Assign human review, evaluation, and a stopping rule.'),
}


def teaching_review(question, summary):
    """Transparent template responses, not model inference or a safety classifier."""
    if set(summary) != {'data_status','cells','mean_heat_c','population'}:
        raise ValueError('Use the explicit aggregate summary schema')
    if summary['data_status'] != 'synthetic':
        raise ValueError('This teaching adapter accepts synthetic summaries only')
    return [{'role': role, 'question': question, 'consideration': item[1],
             'evidence': 'Synthetic example only; no validated intervention effect.'}
            for role, item in HATS.items()]

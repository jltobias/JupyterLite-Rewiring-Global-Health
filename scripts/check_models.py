"""Scientific/data-contract checks; no network or rendered-output snapshots."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'notebooks'))
import numpy as np
from rewiring import city, long_table, geojson, simulate_twin, teaching_review

cells,cube=city()
again,repeat=city()
assert cells.equals(again)
for name in cube: np.testing.assert_array_equal(cube[name],repeat[name])
panel=long_table(cells,cube)
assert len(panel)==24*64
assert not panel.duplicated(['month','cell_id']).any()
np.testing.assert_allclose(panel.rate_per_1000,1000*panel.cases/panel.population)
features=geojson(cells,cube['heat_c'][0],'heat_c')['features']
assert len(features)==64
for f in features:
    ring=f['geometry']['coordinates'][0]
    assert ring[0]==ring[-1]
    assert f['properties']['data_status']=='synthetic'
    assert all(25<x<27 and -26<y<-24 for x,y in ring)
for seed in [0,3,17]:
    result,maps=simulate_twin(seed)
    assert (result[['S','L','I','T','R']].sum(axis=1)==640).all()
    np.testing.assert_array_equal(maps.sum(axis=(1,2)),result.I)
    assert result.equals(simulate_twin(seed)[0])
    # Synchronous transitions: the weekly arrivals in a state cannot exceed its previous source.
    assert np.all(np.diff(result.R)<=result['T'].to_numpy()[:-1])
try:
    teaching_review('Example',{'data_status':'sensitive','cells':64,'mean_heat_c':28,'population':100})
except ValueError:
    pass
else:
    raise AssertionError('Teaching contract accepted non-synthetic status')
print('PASS: deterministic data, rates, GeoJSON coordinates, model conservation, transitions, and input contract')

"""Smoke-test owned demo UI and optional Pyodide runtime. Requires playwright.

Serve repository root on localhost:8765 before running. Artifacts go to _build/qa.
"""
from pathlib import Path
import argparse,json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_build/qa';OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--runtime',action='store_true');parser.add_argument('--notebook',default='');args=parser.parse_args()
sys.stdout.reconfigure(encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1440,'height':1100})
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto('http://127.0.0.1:8765/demos/')
    page.wait_for_selector('.grid-cell')
    assert page.locator('.grid-cell').count()==64
    page.locator('[data-cell="27"]').click()
    assert page.locator('#cell-title').inner_text()=='Cell 27'
    page.locator('#month').fill('12');page.locator('#month').dispatch_event('input')
    assert 'Month 13' in page.locator('#cell-summary').inner_text()
    page.screenshot(path=str(OUT/'demo-desktop.png'),full_page=True)
    page.select_option('#view','matrix');assert page.locator('.grid-cell').count()==384
    page.screenshot(path=str(OUT/'demo-matrix.png'),full_page=True)
    page.select_option('#view','cube');page.wait_for_selector('#cube canvas',timeout=60000)
    page.screenshot(path=str(OUT/'demo-cube.png'),full_page=True)
    page.select_option('#view','map');page.click('#play')
    assert page.locator('#play').get_attribute('aria-pressed')=='true'
    page.click('#play');assert page.locator('#play').get_attribute('aria-pressed')=='false'
    with page.expect_download() as event: page.click('#download')
    data=json.loads(Path(event.value.path()).read_text())
    assert len(data['features'])==64
    assert all(f['properties']['data_status']=='synthetic' for f in data['features'])
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    page.screenshot(path=str(OUT/'demo-mobile.png'),full_page=True)
    page.set_viewport_size({'width':1440,'height':1000})
    page.goto('http://127.0.0.1:8765/demos/scene.html')
    page.wait_for_function('document.getElementById("status").textContent.startsWith("Scene ready")',timeout=60000)
    assert page.locator('#rows tr').count()==64
    page.locator('#month').fill('6');page.locator('#month').dispatch_event('input')
    page.click('#flat');page.click('#tilt')
    page.wait_for_function('sceneMap.loaded() && !sceneMap.isMoving() && sceneMap.queryRenderedFeatures({layers:["columns"]}).length > 0')
    page.screenshot(path=str(OUT/'scene.png'),full_page=True)
    assert not errors,errors
    print('PASS: demo selection, timeline, matrix, cube, play/pause, GeoJSON, mobile layout, and WebGL scene',flush=True)
    if args.runtime:
        page.goto('http://127.0.0.1:8765/scripts/browser_runtime.html?only='+args.notebook)
        page.on('console',lambda msg:print(msg.text,flush=True) if msg.type=='log' else None)
        page.wait_for_function('window.runtimeResults && window.runtimeResults.done',timeout=900000)
        results=page.evaluate('window.runtimeResults')
        (OUT/f'browser-runtime{args.notebook}.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
        print(json.dumps(results,indent=2),flush=True)
        assert results['error'] is None and all(r['status']=='PASS' for r in results['results'])
        assert len(results['results'])==(1 if args.notebook else 10)
    browser.close()

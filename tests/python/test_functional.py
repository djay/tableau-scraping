from tableauscraper import TableauScraper as TS


def test_get_worksheet_data():
    url = "https://public.tableau.com/views/PlayerStats-Top5Leagues20192020/OnePlayerSummary"

    ts = TS()
    ts.loads(url)
    workbook = ts.getWorkbook()
    assert 'ATT MID ATTACKING COMP' in [t.name for t in workbook.worksheets] 
    assert 30 == len([not t.data.empty for t in workbook.worksheets]) 


def test_get_specific_worksheet():
    url = "https://public.tableau.com/views/PlayerStats-Top5Leagues20192020/OnePlayerSummary"

    ts = TS()
    ts.loads(url)

    ws = ts.getWorksheet("ATT MID CREATIVE COMP")
    assert not ws.data.empty


def test_select_selectable_item():
    url = "https://public.tableau.com/views/PlayerStats-Top5Leagues20192020/OnePlayerSummary"

    ts = TS()
    ts.loads(url)

    ws = ts.getWorksheet("ATT MID CREATIVE COMP")

    # show selectable values
    selections = ws.getSelectableItems()
    assert 11 == len(selections)

    # select that value
    dashboard = ws.select("ATTR(Player)", "Vinicius Júnior")

    # display worksheets
    assert 30 == len([t.data for t in dashboard.worksheets])


def test_set_parameter():
    url = "https://public.tableau.com/views/PlayerStats-Top5Leagues20192020/OnePlayerSummary"

    ts = TS()
    ts.loads(url)
    workbook = ts.getWorkbook()

    # show parameters values / column
    parameters = workbook.getParameters()
    assert 1 == len(parameters)

    # set parameters column / value
    workbook = workbook.setParameter("P.League 2", "Ligue 1")

    # display worksheets
    assert 30 == len([t.data for t in workbook.worksheets])


def test_set_filter():
    url = 'https://public.tableau.com/views/WomenInOlympics/Dashboard1'
    ts = TS()
    ts.loads(url)

    ws = ts.getWorksheet("Bar Chart")
    filters = ws.getFilters()
    assert [] != filters
    wb = ws.setFilter('Olympics', 'Winter')
    countyWs = wb.getWorksheet("Bar Chart")
    assert not countyWs.data.empty


def test_storypoints():
    url = 'https://public.tableau.com/views/EarthquakeTrendStory2/Finished-Earthquakestory'
    ts = TS()
    ts.loads(url)
    wb = ts.getWorkbook()

    assert 2 == len(wb.getStoryPoints())
    sp = wb.goToStoryPoint(storyPointId=10)

    assert 'Timeline' in sp.getWorksheetNames()
    assert not sp.getWorksheet("Timeline").data.empty


# def test_level_drill_down():
#     url = 'https://tableau.azdhs.gov/views/ELRv2testlevelandpeopletested/PeopleTested'
#     ts = TS()
#     ts.loads(url)
#     wb = ts.getWorkbook()

#     sheetName = "P1 - Tests by Day W/ % Positivity (Both) (2)"

#     drillDown1 = wb.getWorksheet(sheetName).levelDrill(drillDown=True, position=1)
#     drillDown2 = drillDown1.getWorksheet(sheetName).levelDrill(drillDown=True, position=1)
#     drillDown3 = drillDown2.getWorksheet(sheetName).levelDrill(drillDown=True, position=1)

#     data = drillDown1.getWorksheet(sheetName).data
#     assert not data.empty
#     data = drillDown2.getWorksheet(sheetName).data
#     assert not data.empty
#     data = drillDown3.getWorksheet(sheetName).data
#     assert not data.empty


def test_download_csv():
    from tableauscraper import TableauScraper as TS

    url = 'https://public.tableau.com/views/WYCOVID-19Dashboard/WyomingCOVID-19CaseDashboard'
    ts = TS()
    ts.loads(url)
    wb = ts.getWorkbook()
    data = wb.getCsvData(sheetName='case map')

    assert 23 == len(data)

    # data = wb.getCsvData(sheetName='worksheet1', prefix="vud")
    # assert 20 == len(data)


def test_download_crosstab_data():

    url = "https://tableau.soa.org/t/soa-public/views/USPostLevelTermMortalityExperienceInteractiveTool/DataTable2?%3Aembed=y&%3AisGuestRedirectFromVizportal=y"

    ts = TS()
    ts.loads(url)
    wb = ts.getWorkbook()

    wb.setParameter(inputName="Count or Amount", value="Amount")

    data = wb.getCrossTabData(
        sheetName="Data Table 2 - Premium Jump & PLT Duration")

    assert 1540 == len(data)


def test_go_to_sheet():
    url = "https://public.tableau.com/views/PlayerStats-Top5Leagues20192020/OnePlayerSummary"
    ts = TS()
    ts.loads(url)
    workbook = ts.getWorkbook()

    sheets = workbook.getSheets()
    assert 14 == len(sheets)

    nycAdults = workbook.goToSheet("ATT MID ATTACKING COMP")
    for t in nycAdults.worksheets:
        assert '' != t.name
        assert not t.data.empty


def test_render_tooltip():
    url = "https://public.tableau.com/views/CMI-2_0/CMI"

    ts = TS()
    ts.loads(url)
    workbook = ts.getWorkbook()
    ws = workbook.getWorksheet("US Map - State - CMI")

    tooltipHtml = ws.renderTooltip(x=387, y=196)
    assert '<span' in tooltipHtml
    assert 'Mobility Index:' in tooltipHtml

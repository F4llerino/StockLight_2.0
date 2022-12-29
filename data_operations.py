import requests

headers = {
    "X-RapidAPI-Key": "Add your API-Key",
    "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
}


def query(ticker, head):
    url_balance_sheet = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{0}/balance-sheet" \
        .format(ticker)
    url_income_statement = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{0}/income-statement" \
        .format(ticker)

    response_balance_sheet = requests.request("GET", url_balance_sheet, headers=head)
    response_income_statement = requests.request("GET", url_income_statement, headers=head)

    balance_sheet = response_balance_sheet.json().get("balanceSheetHistory", {}).get("balanceSheetStatements")[0]
    income_statement = response_income_statement.json().get("incomeStatementHistory", {}).get("incomeStatementHistory")[0]

    cash = balance_sheet.get("cash", {}).get("raw")
    net_receivables = balance_sheet.get("netReceivables", {}).get("raw")
    total_assets = balance_sheet.get("totalAssets", {}).get("raw")
    total_stockholder_equity = balance_sheet.get("totalStockholderEquity", {}).get("raw")
    net_income = income_statement.get("netIncome", {}).get("raw")
    revenue = income_statement.get("totalRevenue", {}).get("raw")
    current_liabilities = balance_sheet.get("totalCurrentLiabilities", {}).get("raw")

    roi = round((((net_income / revenue) * (revenue / total_assets)) * 100), 2)
    liquiditaet_2 = round(((cash + net_receivables) / current_liabilities) * 100, 2)
    eigenkapitalquote_2 = round(((total_stockholder_equity / total_assets) * 100), 2)

    return [roi, liquiditaet_2, eigenkapitalquote_2]



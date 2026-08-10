from tools.sheets_tool import SheetsLoggerTool

tool = SheetsLoggerTool()

result = tool._run(
    headline="Test: AI News Bot Setup",
    summary="This is a test row confirming the Google Sheets integration works correctly.",
    source_url="https://example.com",
)
print(result)

#!/usr/bin/env python
import sys
import warnings
import os
import requests

from datetime import datetime

from stock_pickernew.crew import StockPickernew, PushNotificationTool

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def test_tool_directly():
    print("Testing push tool directly...")
    tool = PushNotificationTool()
    result = tool._run("Direct test message")
    print(f"Direct test result: {result}")

def run():
    # Test tool first
    test_tool_directly()
    
    # Then run crew
    inputs = {'sector': 'Technology'}
    result = StockPickernew().crew().kickoff(inputs=inputs)
    print("\n\n===FINAL DECISION ===\n\n")
    print(result.raw)


if __name__ == "__main__":

    run()
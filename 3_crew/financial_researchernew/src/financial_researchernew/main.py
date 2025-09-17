#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from financial_researchernew.crew import FinancialResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the researcher crew
    """

    inputs = {
        'company': 'Tesla'
    }

    result = FinancialResearcher().crew().kickoff(inputs=inputs)
    print(result.raw)

if __name__ == "__main__":
    run()
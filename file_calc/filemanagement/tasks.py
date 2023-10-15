import pandas as pd

from file_calc.celery import app
from .models import CalculationResult, FileRequest


@app.task()
def perform_calculations(request_id):
    request = FileRequest.objects.get(pk=request_id)
    file_path = request.file.path

    # Read the file using pandas
    data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)

    result = 0
    for _, row in data.iterrows():
        a, op, b = row['A'], row['O'], row['B']
        if op in "+-*/" and str(a).replace('.', '', 1).isdigit() and str(b).replace('.', '', 1).isdigit():
            if op == '+':
                result += a + b
            elif op == '-':
                result += a - b
            elif op == '*':
                result += a * b
            elif op == '/':
                result += a / b

    CalculationResult.objects.create(request=request, result=result)

import pandas as pd


class ExcelExporter:
    async def export(self, dataset: dict, output):

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for sheet_name, data in dataset.items():
                if hasattr(data, "__iter__") and len(data) > 0 and hasattr(data[0], "dict"):
                    df = pd.DataFrame([item.dict() for item in data])
                else:
                    df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

def get_excel_exporter():
    return ExcelExporter()

import logging

from google.oauth2 import service_account
from googleapiclient.discovery import build

import pandas as pd

from settings import ASSETS_DIR

logger = logging.getLogger(__name__)


class GoogleSheet:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        self.credentials = service_account.Credentials.from_service_account_file(
            ASSETS_DIR / 'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()

    def convert_sheet_to_pandas(self, sheet_name: str, range_name: str) -> pd.DataFrame:
        """
        Converts data from the specified sheet and range of a Google Spreadsheet into a Pandas DataFrame object.

        :param sheet_name: The name of the Google Spreadsheet sheet.
        :param range_name: The range of cells, e.g., 'A1:C10'.
        :return: A Pandas DataFrame object containing the data from the Google Spreadsheet.
        """
        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                         range=sheet_name + '!' + range_name).execute()
        values = result.get('values', '')

        if not values:
            logger.error(f'GoogleSheet {self.spreadsheet_id}: empty data')
            raise SystemExit(1)

        df = pd.DataFrame(values[1:], columns=values[0], dtype=str)
        df = df.dropna()
        return df

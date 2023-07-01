import pandas as pd
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

import re

from settings import BASE_SYMBOL, FILES_DIR


class Pptx:
    def __init__(self, file_path, df):
        self.pptx = Presentation(file_path)
        self.df = df

    def __replace_data_recur(self, shape):
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            for inner_shape in shape.shapes:
                self.__replace_data_recur(inner_shape)
            return
        if not shape.has_text_frame:
            return
        for paragraph in shape.text_frame.paragraphs:
            if BASE_SYMBOL in paragraph.text:
                text = paragraph.text
                pattern = re.compile(re.escape(BASE_SYMBOL) + r"\d{3}")
                matches = re.findall(pattern, text)
                for match in set(matches):
                    text = text.replace(match, self.df[self.df['key'] == match]['value'].values[0])
                paragraph.text = text

    def replace_data(self):
        for slide in self.pptx.slides:
            for shape in slide.shapes:
                self.__replace_data_recur(shape)

    def save(self, path):
        self.pptx.save(path)


if __name__ == '__main__':
    data = {'key': '¿001', 'value': '228'}
    pptx = Pptx(FILES_DIR / 'templates' / 'pptx_template.pptx', pd.DataFrame(data, index=[0]))
    pptx.replace_data()
    pptx.save(FILES_DIR / 'results' / 'res.pptx')

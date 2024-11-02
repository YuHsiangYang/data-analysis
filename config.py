from enum import Enum

class NewsProvider(Enum):
    UDN_NEWS = "聯合新聞網"
    NEXT_APPLE = "蘋果日報"

RESULTS_DIRECTORY = r'資料\final'
TEMP_DIRECTORY = 'temp'
UDN_RESULTS_DIRECTORY = f'{RESULTS_DIRECTORY}/{NewsProvider.UDN_NEWS.value}'
APPLE_RESULTS_DIRECTORY = f'{RESULTS_DIRECTORY}/{NewsProvider.NEXT_APPLE.value}'
UNION_RESULTS_DIRECTORY = r"資料\聯集"
DATA_DIRECTORY = r"資料"
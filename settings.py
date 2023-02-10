import json
import logging
import os

class Settings():

    def __init__(self):
        self.LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s"

        self.baseWindowSize = [1080,800]
        self.windowSize = [840,600]
        self.infoDialogSize = [500,400]
        self.windowContentMargin = [20,20,20,20]
        self.logLevel = logging.INFO
        
        self.reviewWordProbability = 0.2
        self.zhPuncs = '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］\
            ＾＿｀｛｜｝～｟｠｢｣､　、〃〈〉《》「」『』【】〔〕〖〗〘〙\
                〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
        self.enPuncs = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        self.specialWords = set([])

        self.markdownExt = [
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            "markdown.extensions.abbr", 
            "markdown.extensions.attr_list", 
            "markdown.extensions.def_list", 
            "markdown.extensions.footnotes", 
            "markdown.extensions.tables",
            "markdown.extensions.strikethrough"
        ]

        self.baseWid = None

        self.loadSettings()

    def loadSettings(self):
        if not os.path.isfile(".\\settings.json"):
            logging.info("Didn't find any user settings because settings.json doesn't exist.")
            return
        with open(".\\settings.json", encoding="UTF-8") as f:
            try:
                setting = json.loads(f.read())
            except Exception as e:
                logging.warning("Cannot load user settings because settings.json is not a readable and vaild JSON file! Error message: %s"%str(e))
            else:
                if type(setting) != dict:
                    logging.warning("Cannot load user settings because settings.json is not valid!")
                    return
                for key, item in setting.items():
                    if key=='baseWindowSize' and type(item)==list and len(item)==2:
                        self.baseWindowSize = item
                    elif key=='windowSize' and type(item)==list and len(item)==2:
                        self.windowSize = item
                    elif key=='infoDialogSize' and type(item)==list and len(item)==2:
                        self.infoDialogSize = item
                    elif key=='windowContentMargin' and type(item)==list and len(item)==4:
                        self.windowContentMargin = item
                    elif key=='specialWords' and type(item)==list:
                        self.specialWords = set(item)
                    elif key=="reviewWordProability" and type(item)==float:
                        self.reviewWordProbability = item
                    elif key=="markdownExt" and type(item)==list:
                        self.markdownExt = item
                    else: logging.warning("Setting key '%s' is unrecognizable."%key)
                logging.info("Loaded settings from settings.json .")

settings = Settings()
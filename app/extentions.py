# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
from flask_sqlalchemy import SQLAlchemy
from flask_siwadoc import SiwaDoc


db = SQLAlchemy()
siwadoc = SiwaDoc(doc_url='/api_docs')
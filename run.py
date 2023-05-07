# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
from app import create_app


app = create_app()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6500)
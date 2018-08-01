# Turtlechain Web

## Turning off Missing Template Variables Error 
``` django-gentelella/gentelella/venv/lib/python3.5/site-packages/django/template/base.py ```

Comment out line 925 ~ 930 

## Enabling Multi-Line Tags with Django Template

``` django-gentelella/gentelella/venv/lib/python3.5/site-packages/django/template/ ```

``` 
import re
from django.template import base
base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)
``` 

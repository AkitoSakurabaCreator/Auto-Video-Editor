from __future__ import absolute_import, unicode_literals
from celery import shared_task

import os
from pathlib import Path
from app.ave import main as aveSystem
from app.models import Editor

from celery_progress.backend import ProgressRecorder

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


@shared_task
def add(i, until):
    print("処理開始")
    while(i < until):
        i += 1
        print(i)

    print('処理完了')
    return i


@shared_task
def Edit(editorId):
    dataBase = Editor.objects.get(editorId=editorId)
    idx = 10
    total = 100
    print (MEDIA_ROOT + str(dataBase.upload))
    aveSystem.databaseid = editorId
    aveSystem.title = dataBase.template.title
    aveSystem.languageSel = dataBase.template.language.code
    aveSystem.modelName = dataBase.template.model.modelId
    aveSystem.speacker = dataBase.template.voice.VoiceId
    aveSystem.teloppos = dataBase.template.telopPos.telopName
    aveSystem.path = MEDIA_ROOT + str(dataBase.upload)
    aveSystem.main()

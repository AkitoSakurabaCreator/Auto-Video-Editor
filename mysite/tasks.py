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
    # progress_recorder = ProgressRecorder()
    idx = 10
    total = 100
    # progress_recorder.set_progress(0, total)
    print ("--------------------")
    # print (dataBase.template.title)dataBase
    # print (str(dataBase))
    print (MEDIA_ROOT + str(dataBase.upload))
    # aveSystem = autoVideo()
    aveSystem.databaseid = editorId
    aveSystem.title = dataBase.template.title
    aveSystem.languageSel = dataBase.template.language.code
    aveSystem.modelName = dataBase.template.model.modelId
    aveSystem.speacker = dataBase.template.voice.VoiceId
    aveSystem.teloppos = dataBase.template.telopPos.telopName
    aveSystem.path = MEDIA_ROOT + str(dataBase.upload)
    aveSystem.main()

    # user=request.user, title=form.cleaned_data['title'], 
    # animations_id=form.cleaned_data['animations'],
    # movie_format_id=form.cleaned_data['movie_format'],
    # filter_effect_id=form.cleaned_data['filter_effect'],
    # bgm_id=form.cleaned_data['bgm'],
    # voice=form.cleaned_data['voice'], 
    # language=Language.objects.get(code=form.cleaned_data['language']),
    # telopPos=Telop.objects.get(telopName=form.cleaned_data['telopPos']),
    # model=Model.objects.get(modelId=form.cleaned_data['model']),
    # translate=form.cleaned_data['translate'], 
    # publish=Publish.objects.get(publishName=form.cleaned_data['publish']),
    # while(True):
    #     if (aveSystem.progressScrore != 100):
    #         progress_recorder.set_progress(aveSystem.progressScrore, total, description=f"処理中...({aveSystem.progressScrore}/{total})")
    #     else:
    #         progress_recorder.set_progress(aveSystem.progressScrore, total, description=f"完了...({aveSystem.progressScrore}/{total})")
    #         break

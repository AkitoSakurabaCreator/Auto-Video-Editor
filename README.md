---
title: "Auto Video Editor"
tags: ""
---

<div id="top"></div>

## 使用技術一覧
<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <!-- バックエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=for-the-badge">
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
<img src="https://img.shields.io/badge/-Redis-D82C20.svg?logo=redis&style=for-the-badge">
<img src="https://img.shields.io/badge/-Jquery-0769AD.svg?logo=jquery&style=for-the-badge">
<img src="https://img.shields.io/badge/-Css3-1572B6.svg?logo=css3&style=for-the-badge">
<img src="https://img.shields.io/badge/-Html5-E34F26.svg?logo=html5&style=for-the-badge">
<img src="https://img.shields.io/badge/-Javascript-F7DF1E.svg?logo=javascript&style=for-the-badge">
  
</p>


## プロジェクト名
### Auto Video Editor
## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境](#環境)
4. [機能説明](#機能説明)



## プロジェクトについて
指定した動画素材を自動で編集してくれるアプリケーションです。音量の調節やテロップの生成を自動で行ってくれます。


## デモ(図解)
![image.png](https://boostnote.io/api/teams/ZiDFKbzPj/files/2a7f2746c24503b6ee623fc5387b8d8b0c21346960bf903cded4d36fa2026a7b-image.png)


こちらは、紹介動画のリンクです。

→ [2920fe2e8528c095abe9723154d691b1.mp4](https://boostnote.io/api/teams/ZiDFKbzPj/files/0d6411e16012cd142c6699a945a9186778415503150956418f3bbc3ade0dd118-2920fe2e8528c095abe9723154d691b1.mp4)



## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

 言語・フレームワーク・ライブラリー  | バージョン |
| --------------------- | ---------- |
| Python                | 3.12       |
| Javascript            | 4.2.1      |
| Html5                 | 3.14.0     |
| Css3                  | 8.0        |
| Django                | 16.17.0    |
| Ajax                  | 18.2.0     |
| Jquery                | 13.4.6     |
| Redis                 | 1.3.6      |
| voicebox              ||
| whisper               | 1.1.10     | 
| moviepy               | 1.0.3      | 
| ffmpeg                | 1.4        | 
| opencv-python                | 4.7.0.72      | 
| numpy                 | 1.24.2     | 

 pip install -r requirements.txt でライブラリをインストールしてください。
 
<br>※ライブラリのインストールが上手くいかない場合は「起動コマンドをインストールしてください」のメッセージが消えるまで(正常に起動できるまで) pip install 〇〇で1つずつインストールしてください。


## 機能説明

・自動動画編集(音量の調節・テロップの生成)

・テンプレートの共有(公開された状態でURLを共有)

・動画編集後のURL共有(公開にされた状態でURLを共有) 

## ディレクトリ構成
├─accounts
│  ├─migrations
│  │  └─__pycache__
│  ├─templates
│  │  └─accounts
│  │      ├─bk
│  │      │  └─test
│  │      ├─inquiry
│  │      ├─login
│  │      ├─password
│  │      ├─profile
│  │      └─register
│  │          └─txt
│  │              └─mail_template
│  │                  └─create
│  └─__pycache__
├─app
│  ├─ave
│  │  ├─.ipynb_checkpoints
│  │  ├─prg
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─collected_static
│  │  ├─admin
│  │  │  ├─css
│  │  │  │  └─vendor
│  │  │  │      └─select2
│  │  │  ├─fonts
│  │  │  ├─img
│  │  │  │  └─gis
│  │  │  └─js
│  │  │      ├─admin
│  │  │      └─vendor
│  │  │          ├─jquery
│  │  │          ├─select2
│  │  │          │  └─i18n
│  │  │          └─xregexp
│  │  └─css
│  ├─migrations
│  │  └─__pycache__
│  ├─static
│  │  ├─css
│  │  ├─images
│  │  │  ├─Material
│  │  │  └─U22
│  │  ├─js
│  │  └─U22
│  │      ├─css
│  │      │  └─editor
│  │      └─js
│  ├─templates
│  │  └─app
│  │      ├─review
│  │      ├─store
│  │      └─U22
│  │          ├─editor
│  │          └─static
│  │              ├─css
│  │              ├─img
│  │              ├─js
│  │              └─logo
│  ├─templatetags
│  │  └─__pycache__
│  └─__pycache__
├─media
│  ├─site
│  └─Users
│      ├─MovieEdit
│      ├─MovieEdited
│      ├─ProfileImages
│      └─TextFile
├─mysite
│  └─__pycache__
├─static
│  └─accounts
│      └─css
├─temp
│  └─vox
├─voicevox_core
│  ├─model
│  └─open_jtalk_dic_utf_8-1.11
└─voicevox_engine
    ├─build_util
    ├─docs
    │  ├─api
    │  ├─licenses
    │  │  ├─cuda
    │  │  ├─cudnn
    │  │  ├─open_jtalk
    │  │  │  ├─mecab
    │  │  │  └─mecab-naist-jdic
    │  │  └─world
    │  └─res
    ├─engine_manifest_assets
    ├─speaker_info
    │  ├─35b2c544-660e-401e-b503-0e14c635303a
    │  │  ├─icons
    │  │  ├─portraits
    │  │  └─voice_samples
    │  ├─388f246b-8c41-4ac1-8e2d-5d79f3ff56d9
    │  │  ├─icons
    │  │  ├─portraits
    │  │  └─voice_samples
    │  ├─7ffcb7ce-00ec-4bdc-82cd-45a8889e43ff
    │  │  ├─icons
    │  │  ├─portraits
    │  │  └─voice_samples
    │  └─b1a81618-b27b-40d2-b0ea-27a9ad408c4b
    │      ├─icons
    │      └─voice_samples
    ├─test
    ├─ui_template
    ├─voicevox_engine
    │  ├─dev
    │  │  ├─core
    │  │  └─synthesis_engine
    │  ├─engine_manifest
    │  │  └─__pycache__
    │  ├─metas
    │  │  └─__pycache__
    │  ├─preset
    │  │  └─__pycache__
    │  ├─setting
    │  │  └─__pycache__
    │  ├─synthesis_engine
    │  │  └─__pycache__
    │  ├─utility
    │  │  └─__pycache__
    │  └─__pycache__
    └─windows-cpu
        ├─certifi
        ├─Cython
        │  ├─Compiler
        │  └─Tempita
        ├─engine_manifest_assets
        ├─lib2to3
        ├─numpy
        │  ├─core
        │  ├─fft
        │  ├─linalg
        │  └─random
        ├─pydantic
        ├─pyopenjtalk
        │  ├─htsvoice
        │  └─open_jtalk_dic_utf_8-1.11
        ├─pyworld
        ├─scipy
        │  ├─.libs
        │  ├─fft
        │  │  └─_pocketfft
        │  ├─fftpack
        │  │  └─tests
        │  ├─integrate
        │  │  └─tests
        │  ├─interpolate
        │  │  └─tests
        │  │      └─data
        │  ├─io
        │  │  ├─arff
        │  │  │  └─tests
        │  │  │      └─data
        │  │  ├─matlab
        │  │  │  └─tests
        │  │  │      └─data
        │  │  └─tests
        │  │      └─data
        │  ├─linalg
        │  │  ├─src
        │  │  │  ├─id_dist
        │  │  │  │  └─doc
        │  │  │  └─lapack_deprecations
        │  │  └─tests
        │  │      └─data
        │  ├─misc
        │  ├─ndimage
        │  │  └─tests
        │  │      └─data
        │  ├─optimize
        │  │  ├─cython_optimize
        │  │  ├─lbfgsb_src
        │  │  ├─_highs
        │  │  │  └─cython
        │  │  │      └─src
        │  │  ├─_lsq
        │  │  └─_trlib
        │  ├─signal
        │  ├─sparse
        │  │  ├─csgraph
        │  │  ├─linalg
        │  │  │  ├─dsolve
        │  │  │  │  └─SuperLU
        │  │  │  ├─eigen
        │  │  │  │  └─arpack
        │  │  │  │      └─ARPACK
        │  │  │  └─isolve
        │  │  └─tests
        │  │      └─data
        │  ├─spatial
        │  │  ├─qhull_src
        │  │  ├─tests
        │  │  │  └─data
        │  │  └─transform
        │  ├─special
        │  │  └─tests
        │  │      └─data
        │  ├─stats
        │  │  ├─tests
        │  │  │  └─data
        │  │  │      ├─nist_anova
        │  │  │      └─nist_linregress
        │  │  └─_boost
        │  └─_lib
        │      └─_uarray
        ├─speaker_info
        │  ├─044830d2-f23b-44d6-ac0d-b5d733caa900
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─0f56c2f2-644c-49c9-8989-94e11f7129d0
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─1a17ca16-7ee5-4ea5-b191-2f02ace24d21
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─3474ee95-c274-47f9-aa1a-8322163d96f1
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─35b2c544-660e-401e-b503-0e14c635303a
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─388f246b-8c41-4ac1-8e2d-5d79f3ff56d9
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─481fb609-6446-4870-9f46-90c4dd623403
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─4f51116a-d9ee-4516-925d-21f183e2afad
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─67d5d8da-acd7-4207-bb10-b5542d3a663b
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─7ffcb7ce-00ec-4bdc-82cd-45a8889e43ff
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─8eaad775-3119-417e-8cf4-2a10bfd592c8
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─9f3ee141-26ad-437e-97bd-d22298d02ad2
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─b1a81618-b27b-40d2-b0ea-27a9ad408c4b
        │  │  ├─icons
        │  │  └─voice_samples
        │  ├─c30dc15a-0992-4f8d-8bb8-ad3b314e6a6f
        │  │  ├─icons
        │  │  └─voice_samples
        │  └─e5020595-5c5d-4e87-b849-270a518d0dcf
        │      ├─icons
        │      └─voice_samples
        ├─yaml
        └─_soundfile_data

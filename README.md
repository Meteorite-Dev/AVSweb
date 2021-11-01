# AVSweb

intelligence surveillance web gui (Using Flask).

## problem 

1. 當網頁停止時(關閉或是到上一頁)，必需終止 video 的程序。
2. 多影像且可調整的頁面
3. 接上 kafka 
4. 權限分級
5. dashboard 還有 頁面的美化

## 執行

1. 請先安裝相關的套件
    > `conda env create -f environment.yml`
2. using conda env
3. python WebApp.py

## Config

- **VIDEO_DIR_MODE** : 設定是否使用多來源(使用資料夾來源) , default : True
- **VIDEO_SOURCE** : 使用一個 video 來源 (單檔案，同時必須將 **VIDEO_DIR_MODE** 設為 False)
- **VIDEO_SOURCE_DIR** : 如果使用多來源影像，必須設定此項。

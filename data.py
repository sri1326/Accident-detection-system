from bing_image_downloader import downloader
keywords= ['accident',
           'Rear-end collision',
           'Side-impact collision',
           'Head-on collision']
for kw in keywords:
    downloader.download(kw,limit=5000,output_dir = 'data')

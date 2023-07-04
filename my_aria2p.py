import aria2p

# initialization, these are the default values
aria2 = aria2p.API(
    aria2p.Client(
        host="http://127.0.0.1",
        port=6800,
        secret="P3TERX"
    )
)

aria2.remove_all()

# list downloads
downloads = aria2.get_downloads()

for download in downloads:
    print(download.name, download.download_speed)

# url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20230702/00/wave/station/gfswave.t00z.bull_tar"
# directory = "/downloads/nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20230702/00/wave/station/"
# options = {"dir": directory}
# aria2.add(url, options=options)
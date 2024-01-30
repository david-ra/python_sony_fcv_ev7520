# python_sony_fcv_ev7520
daemon to store streaming data from sony camera to redis

pd: 
this will create a ram disk on macos
diskutil erasevolume HFS+ "RAMDisk" `hdiutil attach -nomount ram://2048`
pd: on macos remember to run colima start
mounted on  /Volumes/RAMDisk 

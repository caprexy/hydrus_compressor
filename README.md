# hydrus_compressor
# What it does
Pulls files from hydrus above a certain size and compresses them down to a respectable limit. At the moment, it's only images since I'd imagine videos would cause a whole load of other problems. Additionally changes to images are generally less noticable. The compressed files are then sent to hydrus with as much information duplicated across the two files, ex: tags, favoriates, time modified, etc. The previous file is set to be deleted but not yet permanently deleted. 


# Installation and running
Install requirements through the requirements.txt and pip. Primary packages are pyqt6, requests, and open-cv
Launch application by running the application.py script
Add an API key from hydrus, can be made by services->review services under the local : client api tabs. A new key can be made or an old one can be used with all permissions required. 

# How to use
On the left panel is most of the user input settings, essentially choose what size do images have to be greater than in order to be gotten and from where (archive/inbox). Config for now is simply API key set from above and the port number that the hydrus instance runs the api client on. (same place as the keys, should have a text: "The client api should be running on port 45869" 

Finally clicking the "Get all files..." button will populate the panel on the right. These are all the images that fulfill the condition on the left, sorted from largest to smallest. These images can be selected and ctrl/shift selected. The selected images will be the ones compressed and sent to hydrus, the compression settings are set in the "Open image compression settings" 

These settings are dictated by open-cv's compression options for it's imwrite. Particularlly the flags found [here](https://docs.opencv.org/4.x/d8/d6a/group__imgcodecs__flags.html#ga292d81be8d76901bff7988d18d2b42ac)
Primarily the jpeg optimize flag is set to be true and the level of quality is set by the user. 
Additional steps for compression is resizing by either pixel or percentage. Percentage directly shrinks the width and height of a image by the given percent. Pixels will limit the width and height of an image to the given values, but also maintain the aspect ratio.

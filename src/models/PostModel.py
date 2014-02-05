POST_TYPES = ['text', 'quote', 'link', 'answer', 'video', 'audio', 'photo', 'chat']

def MakePostModel(post_json):
    if post_json['type'] == 'photo':
        return PhotoPostModel(post_json)
    else:
        return PostModel(post_json)

class PostModel(object):
    def __init__(self, post_json):
        self.sURL = post_json['post_url']
        self.sPostType = post_json['type']
        self.sDate = post_json['date']

class PhotoPostModel(PostModel):
    def __init__(self, post_json):
        super(PhotoPostModel, self).__init__(post_json)

        self.sPhotoPermaURL = post_json['image_permalink']
        self.sCaption = post_json['caption']
        self.tPhotoData = post_json['photos']

    def getPhoto(self, n=0, desired_width=None, desired_height=None):
        n = max(0, min(len(self.tPhotoData)-1, n))

        photo = self.tPhotoData[n]

        if desired_width == None and desired_height == None:
            return (photo['original_size']['url'], photo['original_size']['width'], photo['original_size']['height'])

        minError = 999999
        minErrorIdx = -1
        idx = 0
        for alt in photo['alt_sizes']:
            error = 0
            if desired_width:
                error += abs(alt['width'] - desired_width)
            if desired_height:
                error += abs(alt['height'] - desired_height)

            if error < minError:
                minError = error
                minErrorIdx = idx

            idx += 1

        return (photo['alt_sizes'][minErrorIdx]['url'], photo['alt_sizes'][minErrorIdx]['width'], photo['alt_sizes'][minErrorIdx]['height'])
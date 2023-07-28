import json

# read
# write
# update
# delete

class LikeDB:
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            with open(file_name) as f:
                self.data = json.load(f)
        except:
            self.data = {}
        

    def save(self, data):
        with open(self.file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def add_image(self, message_id):
        """
        Add image to the database

        Args:
            message_id (int): message id
        Returns:
            None
        """
        self.data[message_id] = {}
        self.save(self.data)

    def add_like(self, chat_id, message_id):
        """
        Add like to the database

        Args:
            chat_id (int): chat id
        Returns:
            None
        """
        chat_id = str(chat_id)
        message_id = str(message_id)

        img_data = self.data[message_id]
        user = img_data.get(chat_id)
        if user == None:
            img_data[chat_id] = {
                'like': 1,
                'dislike': 0
            }

        elif user['like'] == 0 and user['dislike'] == 0:
            img_data[chat_id]['like'] = 1
        
        elif user['like'] == 0 and user['dislike'] == 1:
            img_data[chat_id]['like'] = 1
            img_data[chat_id]['dislike'] = 0
        
        elif user['like'] == 1 and user['dislike'] == 0:
            img_data[chat_id]['like'] = 0
        
        self.save(self.data)
    
    def add_dislike(self, chat_id, message_id):
        """
        Add dislike to the database

        Args:
            chat_id (int): chat id
        Returns:
            None
        """
        chat_id = str(chat_id)
        message_id = str(message_id)

        img_data = self.data[message_id]
        user = img_data.get(chat_id)
        if user == None:
            img_data[chat_id] = {
                'like': 0,
                'dislike': 1
            }

        elif user['like'] == 0 and user['dislike'] == 0:
            img_data[chat_id]['dislike'] = 1
        
        elif user['like'] == 0 and user['dislike'] == 1:
            img_data[chat_id]['like'] = 0
            img_data[chat_id]['dislike'] = 0
        
        elif user['like'] == 1 and user['dislike'] == 0:
            img_data[chat_id]['like'] = 0
            img_data[chat_id]['dislike'] = 1
        
        self.save(self.data)

    def get_likes(self, message_id):
        """
        Get likes of the image

        Args:
            message_id (int): message id
        Returns:
            int: likes
        """
        message_id = str(message_id)
        img_data = self.data[message_id]
        likes = 0
        for user in img_data.keys():
            likes += img_data[user]['like']

        return likes
    
    def get_dislikes(self, message_id):
        """
        Get dislikes of the image

        Args:
            message_id (int): message id
        Returns:
            int: dislikes
        """
        message_id = str(message_id)
        img_data = self.data[message_id]
        dislikes = 0
        for user in img_data.keys():
            dislikes += img_data[user]['dislike']

        return dislikes


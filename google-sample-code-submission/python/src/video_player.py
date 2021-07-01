"""A video player class."""
from video_library import VideoLibrary
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        global flagged_video_ids
        global flagging_reasons
        if 'flagged_video_ids' not in globals():
            flagged_video_ids=[]
            flagging_reasons=[]
            
        print("Here's a list of all avaliable videos:")
        video_list=(self._video_library.get_all_videos())
        video_list = sorted(video_list,key=lambda x: (x._title))
        count=0
        for i in range (len(self._video_library.get_all_videos())):
            joined_tags=''.join(video_list[count]._tags)
            if (video_list[count]._video_id) not in flagged_video_ids:
                print(f"{video_list[count]._title} ({video_list[count]._video_id}) [{joined_tags}]")
            else:
                flag_number=flagged_video_ids.index(video_list[count]._video_id)
                flagging_reason=flagging_reasons[flag_number]
                print(f"{video_list[count]._title} ({video_list[count]._video_id}) [{joined_tags}] - FLAGGED (reason: {flagging_reasons[flag_number]})")
            count=count+1
            

    def play_video(self, video_id):
        global video_playing
        global pause_status
        global flagged_video_ids
        global flagging_reasons
        if 'flagged_video_ids' not in globals():
            flagged_video_ids=[]
            flagging_reasons=[]
        if video_id not in flagged_video_ids:
            video_request=self._video_library.get_video(video_id)
            if video_request is not None:
                if 'video_playing' in globals():
                    video_stopped=video_playing
                video_playing=video_request
                if 'video_stopped' in locals():
                    print(f"Stopping video: {video_stopped._title}")
                print(f"Playing video: {video_playing._title}")
                pause_status=False
            else:
                print("Cannot play video: Video does not exist")
        else:
            flag_number=flagged_video_ids.index(video_id)
            flagging_reason=flagging_reasons[flag_number]
            print(f"Cannot play video: Video is currently flagged (reason: {flagging_reason})")
        
    def stop_video(self):
        global video_playing
        if 'video_playing' in globals():
            video_stopped=video_playing
            print(f"Stopping video: {video_stopped._title}")
            del video_playing
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        global flagged_video_ids
        global flagging_reasons
        if 'flagged_video_ids' not in globals():
            flagged_video_ids=[]
            flagging_reasons=[]
        feasible_videos=self._video_library.get_all_videos()

        count=0
        for i in range (len(flagged_video_ids)):
            feasible_videos.remove(self._video_library.get_video(flagged_video_ids[count]))
            count=count+1
        if (len(feasible_videos))>0:
            random_video=random.choice(feasible_videos)
            random_video_id=random_video._video_id
            self.play_video(random_video_id)
        else:
            print("No videos available")

    def pause_video(self):
        global pause_status
        global video_playing
        if 'video_playing' in globals():
            if pause_status==True:
                print(f"Video already paused: {video_playing._title}")
            else:
                print(f"Pausing video: {video_playing._title}")
                pause_status=True
        else:
            print("Cannot pause video: No video is currently playing")
            
    def continue_video(self):
        global pause_status
        global video_playing
        if 'video_playing' in globals():
            if pause_status==False:
                print(f"Cannot continue video:  Video is not paused")
            else:
                print(f"Continuing video: {video_playing._title}")
                pause_status=False
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        global video_playing
        if 'video_playing' in globals():
            joined_tags=''.join(video_playing._tags)
            print(f"Currently playing: {video_playing._title} ({video_playing._video_id}) [{joined_tags}]")
        else:
            print("No video is currently playing")
            
    def create_playlist(self, playlist_name):
        global playlists
        global playlist_name_index
        if 'playlists' not in globals():
            playlists=[]
            playlist_name_index=[]
        if playlist_name not in playlist_name_index:
            playlists.append([])
            playlist_name_index.append(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")
        else:
            print("Cannot create playlist: A playlist with the same name already exists")
        
    def add_to_playlist(self, playlist_name, video_id):
        global playlists
        global playlist_name_index
        global flagged_video_ids
        global flagging_reasons
        
        if playlist_name.upper() in map(str.upper, playlist_name_index):
            video_list=(self._video_library.get_all_videos())
            video_id_list=[]
            count=0
            for i in range (len(self._video_library.get_all_videos())):
                video_id_list.append(video_list[count]._video_id)
                count=count+1
            
            if video_id in video_id_list:
                if 'flagged_video_ids' not in globals():
                    flagged_video_ids=[]
                    flagging_reasons=[]
                if video_id not in flagged_video_ids:
                    upper_playlist_name_index = [each_string.upper() for each_string in playlist_name_index]
                    playlist_number=(upper_playlist_name_index).index(playlist_name.upper())
                    if video_id not in playlists[playlist_number]:
                        video=self._video_library.get_video(video_id)
                        playlists[playlist_number].append(video_id)
                        print(f"Added video to {playlist_name}: {video._title}")
                    else:
                        print(f"Cannot add video to {playlist_name}: Video already added")
                else:
                    flag_number=flagged_video_ids.index(video_id)
                    flagged_reason=flagging_reason[flag_number]
                    print(f"Cannot add video to my_playlist: Video is currently flagged (reason:{flagged_reason})")
            else:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

    def show_all_playlists(self):
        global playlists
        global playlist_name_index
        if 'playlists' in globals() and len(playlists)>0:
            print("Showing all playlists")
            count=0
            for i in range (len(playlists)):
                print(f"  {playlist_name_index[count]}")
                count=count+1
        else:
            print("No playlists exist yet")
            
    def show_playlist(self, playlist_name):
        global playlists
        global playlist_name_index
        global flagged_video_ids
        global flagging_reasons
        if 'flagged_video_ids' not in globals():
            flagged_video_ids=[]
            flagging_reasons=[]
        if 'playlists' in globals() and playlist_name.upper() in map(str.upper, playlist_name_index):
            print(f"Showing playlist: {playlist_name}")
            upper_playlist_name_index = [each_string.upper() for each_string in playlist_name_index]
            playlist_number=(upper_playlist_name_index).index(playlist_name.upper())
            if (len(playlists[playlist_number]))>0:
                count=0
                for i in range (len(playlists[playlist_number])):
                    video=self._video_library.get_video(playlists[playlist_number][count])
                    joined_tags=''.join(video._tags)
                    if (video._video_id) not in flagged_video_ids:
                        print(f"{video._title} ({video._video_id}) [{joined_tags}]")
                    else:
                        flag_number=flagged_video_ids.index(video._video_id)
                        flagging_reason=flagging_reasons[flag_number]
                        print(f"{video._title} ({video._video_id}) [{joined_tags}] - FLAGGED (reason: {flagging_reasons[flag_number]})")
                    count=count+1
            else:
                print("  No videos here yet")
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            
    def remove_from_playlist(self, playlist_name, video_id):
        global playlists
        global playlist_name_index

        if playlist_name.upper() in map(str.upper, playlist_name_index):
            video_list=(self._video_library.get_all_videos())
            video_id_list=[]
            count=0
            for i in range (len(self._video_library.get_all_videos())):
                video_id_list.append(video_list[count]._video_id)
                count=count+1
            if video_id in video_id_list:
                upper_playlist_name_index = [each_string.upper() for each_string in playlist_name_index]
                playlist_number=(upper_playlist_name_index).index(playlist_name.upper())
                if video_id in playlists[playlist_number]:
                    video=self._video_library.get_video(video_id)
                    playlists[playlist_number].remove(video_id)
                    print(f"Removed video from {playlist_name}: {video._title}")
                else:
                    print(f"Cannot remove video from {playlist_name}: Video not in playlist")
            else:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
        else:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            
    def clear_playlist(self, playlist_name):
        global playlists
        global playlist_name_index
        if playlist_name.upper() in map(str.upper, playlist_name_index):
            upper_playlist_name_index = [each_string.upper() for each_string in playlist_name_index]
            playlist_number=(upper_playlist_name_index).index(playlist_name.upper())
            playlists[playlist_number]=[]
            print(f"Successfully removed all videos from {playlist_name}")
        else:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        global playlists
        global playlist_name_index
        if playlist_name.upper() in map(str.upper, playlist_name_index):
            upper_playlist_name_index = [each_string.upper() for each_string in playlist_name_index]
            playlist_number=(upper_playlist_name_index).index(playlist_name.upper())
            del(playlists[playlist_number])
            del(playlist_name_index[playlist_number])
            print(f"Deleted playlist: {playlist_name}")
        else:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            
    def search_videos(self, search_term):
        global flagged_video_ids
        global flagging_reasons
        if 'flagged_video_ids' not in globals():
                    flagged_video_ids=[]
                    flagging_reasons=[]
        video_list=(self._video_library.get_all_videos())
        search_results=[]
        count=0
        for i in range (len(self._video_library.get_all_videos())):
            if search_term.upper() in video_list[count]._title.upper():
                search_results.append(video_list[count])
            count=count+1
        if len(search_results)>0:
            print(f"Here are the results for {search_term}")
            count=0
            removal_count=0
            for i in range (len(search_results)):
                video=search_results[count]
                joined_tags=''.join(video._tags)
                if (video._video_id) not in flagged_video_ids:
                    print(f"  {count+1-removal_count}) {video._title} ({video._video_id}) [{joined_tags}]")
                else:
                    removal_count=removal_count+1
                count=count+1
            menu_choice=int(input("Would you like to play any of the above? If yes, specify the number of the video. If your answer is not a valid number, we will assume it's a no."))
            if menu_choice<(count+1-removal_count):
                requested_video_id=search_results[menu_choice-1]._video_id
                self.play_video(requested_video_id)
        else:
            print(f"No search results for {search_term}")
        
    def search_videos_tag(self, video_tag):#need to find way of removing effect of hashtag in console
        global flagged_video_ids
        global flagging_reasons
        if 'flagged_video_ids' not in globals():
                    flagged_video_ids=[]
                    flagging_reasons=[]
        video_list=(self._video_library.get_all_videos())
        search_results=[]
        count=0
        for i in range (len(self._video_library.get_all_videos())):
            if search_term.upper() in video_list[count]._tags():
                search_results.append(video_list[count])
            count=count+1
        if len(search_results)>0:
            print(f"Here are the results for {search_term}")
            count=0
            removal_count=0
            for i in range (len(search_results)):
                video=search_results[count]
                joined_tags=''.join(video._tags)
                if (video._video_id) not in flagged_video_ids:
                    print(f"  {count+1-removal_count}) {video._title} ({video._video_id}) [{joined_tags}]")
                else:
                    removal_count=removal_count+1
                count=count+1
            menu_choice=int(input("Would you like to play any of the above? If yes, specify the number of the video. If your answer is not a valid number, we will assume it's a no."))
            if menu_choice<(count+1):
                requested_video_id=search_results[menu_choice-1]._video_id
                self.play_video(requested_video_id)
        else:
            print(f"No search results for {search_term}")

    def flag_video(self, video_id, flag_reason=""):
        global flagged_video_ids
        global flagging_reasons
        if 'flagged_video_ids' not in globals():
            flagged_video_ids=[]
            flagging_reasons=[]
        video=self._video_library.get_video(video_id)
        if video is not None:
            if video_id not in flagged_video_ids:
                flagged_video_ids.append(video_id)
                if flag_reason=="":
                    flag_reason=("Not supplied")
                flagging_reasons.append(flag_reason)
                print(f"Successfully flagged video: {video._title} (reason: {flag_reason})")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
                print("Cannot flag video: Video does not exist")    
    def allow_video(self, video_id):
        global flagged_video_ids
        global flagging_reasons
        if 'flagged_video_ids' not in globals():
            flagged_video_ids=[]
            flagging_reasons=[]
        video=self._video_library.get_video(video_id)
        if video is not None:
            if video_id in flagged_video_ids:
                flag_number=flagged_video_ids.index(video_id)
                flagged_video_ids.remove(video_id)
                del flagging_reasons[flag_number]
                print(f"Successfully removed flag from video: {video._title}")
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
                print("Cannot remove flag from video: Video does not exist")
        


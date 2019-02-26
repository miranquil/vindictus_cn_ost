import lxml.etree
import requests
import os


def gather():
    url = 'https://mh.tiancity.com/homepage/event/music/'
    request = requests.get(url)
    request.encoding = request.apparent_encoding
    html = lxml.etree.HTML(request.text)

    album_list = html.xpath('//div[@class="album"]')
    album_dict_list = []

    for album in album_list:
        album_name = ' '.join(album.xpath('.//div[@class="album-name"]//text()'))
        album_music_list = []

        music_list = album.xpath('.//li')
        for music in music_list:
            music_title = music.xpath('./div')[0].text
            music_link = music.xpath('./@data-src')[0]
            album_music_list.append({
                'title': music_title,
                'link': music_link,
            })

        album_dict = {
            'name': album_name,
            'content': album_music_list,
        }

        album_dict_list.append(album_dict)

    return album_dict_list


def download():
    print("Gathering albums...")
    album_list = gather()
    print("Albums data gathered. Ready for downloading!\n")
    for album in album_list:
        print(f"Current album: {album['name']}")
        dir_path = os.getcwd() + '/' + album['name']
        os.makedirs(dir_path, exist_ok=True)
        for music in album['content']:
            print(f"Downloading {music['title']}.mp3 ...")
            fout = open(dir_path + '/' + music['title'] + '.mp3', 'wb')
            request = requests.get(url=music['link'])
            fout.write(request.content)
            fout.close()
            print(f"{music['title']} downloaded.")
        print(f"Album {album['name']} finished.\n")


if __name__ == '__main__':
    download()

# Youtube Podcast Generator

Create audio podcasts from Youtube Channels and Rumble Channels.

Podtube CLI automatically:

- downloads the video from your feed
- extracts the audio to mp3 files
- downloads thumbnail images
- generates an XML RSS feed

**Note:** Rumble uses OpenRSS.org to create a feed of your Rumble Channel. So visit `https://openrss.org/rumble.com/c/<channel-id>` before trying to generate your feed. Make sure content is showing up.

## Install

`pipx install ytube-podcast`


## Help

```
USAGE
  podtube <channel_id> <template> [-t] [-f] [-l] [-m] [-r]

ARGUMENTS
    <channel_id>                Channel ID
    <template>                  feed template

OPTIONS
    -t (--type)                 Channel Type (default: youtube)
    -f (--feed)                 output feed (default: feed.xml)
    -l (--limit)                Entry limit (default: 50)
    -m (--media)                media output directory (default: media)
    -r (--redownload)           Re-Download All Files (default: False)
```

## Examples

**Youtube**

```
podtube adbcd123-N3SHwntLU2xfkaA static/tpl.xml -f static/rss.xml -m static/podcast/
```

**Rumble**

```
podtube my-channel-id static/tpl.xml -t rumble -f static/rss.xml -m static/podcast/
```

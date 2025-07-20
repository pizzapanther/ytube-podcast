# Youtube Podcast Generator

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

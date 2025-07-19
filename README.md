# Youtube Podcast Generator

## Install

`pipx install ytube-podcast`


## Help

```
USAGE
 podtube <channel_id> <template> [-f] [-l] [-m] [-r]

ARGUMENTS
    <channel_id>                Channel ID
    <template>                  feed template

OPTIONS
    -f (--feed)                 output feed (default: feed.xml)
    -l (--limit)                Entry limit (default: 50)
    -m (--media)                media output directory (default: media)
    -r (--redownload)           Re-Download All Files (default: False)
```

## Examples

```
podtube adbcd123-N3SHwntLU2xfkaA static/tpl.xml -f static/rss.xml -m static/podcast/
```

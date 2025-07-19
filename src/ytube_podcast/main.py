import datetime
import pendulum
import sys
from pathlib import Path

import feedparser
import ffmpeg
import httpx
import yt_dlp

from liquid import parse
from piou import Cli, Option
from slugify import slugify

cli = Cli(description='Youtube to Podcast Generator')


@cli.main()
def main(
    channel_id: str = Option(..., help='Channel ID'),
    template: Path = Option(..., help="feed template"),
    feed: Path = Option(Path("feed.xml"), "-f", "--feed", help="output feed"),
    media_dir: Path = Option(Path('media'), "-m", "--media", help="media output directory"),
    limit: str = Option(50, "-l", "--limit", help='Entry limit'),
    redownload: bool = Option(False, "-r", "--redownload", help='Re-Download All Files'),
  ):

  with template.open('r') as fh:
    tpl_text = fh.read()

  if not media_dir.exists():
    media_dir.mkdir(parents=True)

  context = {
    'utcnow': pendulum.now('UTC').to_rss_string(),
    'entries': []
  }
  xmlfeed = feedparser.parse(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
  if xmlfeed.status == 200:
    for i, entry in enumerate(xmlfeed.entries):
      if i == (limit - 1):
        break

      thumb_url = entry.media_thumbnail[0]['url']
      media_path = media_dir / (slugify(entry.title) + '.mp3')
      thumb_path = media_dir / (slugify(entry.title) + '.' + thumb_url.split('.')[-1])
      entry['media_path'] = media_path
      entry['media_size'] = media_path.stat().st_size
      entry['thumb_path'] = thumb_path
      entry['published'] = pendulum.parse(entry.published).to_rss_string()
      context['entries'].append(entry)
      if media_path.exists():
        if not redownload:
          print('Skipping Download:', entry.title)
          continue

      print('Downloading:', entry.title)
      with thumb_path.open('wb') as fh:
        response = httpx.get(thumb_url)
        fh.write(response.content)

      opts = {
        'extract_audio': True,
        'format': 'bestaudio',
        'outtmpl': 'output.%(ext)s'
      }
      with yt_dlp.YoutubeDL(opts) as video:
        info_dict = video.extract_info(entry.link, download=True)
        tmp_path = Path(f'output.{info_dict['audio_ext']}')
        (
          ffmpeg
          .input(str(tmp_path))
          .output(str(media_path))
          .run()
        )
        tmp_path.unlink()

  else:
    print("Failed to get RSS feed. Status code:", feed.status)
    sys.exit(1)

  template = parse(tpl_text)
  output = template.render(**context)
  with feed.open('w') as fh:
    fh.write(output)

def run():
  cli.run()

if __name__ == '__main__':
  run()

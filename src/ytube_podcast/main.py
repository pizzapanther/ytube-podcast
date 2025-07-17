from pathlib import Path

import feedparser
import ffmpeg
import yt_dlp

from liquid import render
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
  ):

  with template.open('r') as fh:
    tpl_text = fh.read()

  if not media_dir.exists():
    media_dir.mkdir(parents=True)

  feed = feedparser.parse(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
  if feed.status == 200:
    for i, entry in enumerate(feed.entries):
      if i == (limit - 1):
        break

      media_path = media_dir / (slugify(entry.title) + '.mp3')
      if media_path.exists():
        print('Skipping Download:', entry.title)
        continue

      print('Downloading:', entry.title)
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

def run():
  cli.run()

if __name__ == '__main__':
  run()

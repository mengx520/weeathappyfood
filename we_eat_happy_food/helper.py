from hashlib import new
import markdown2

#convert database post to html
def convert_markdown_posts(posts, summarize=False):
    processed_posts = []
    for p in posts:
        new_post = {
            'title': p['title'],
            'url_slug': p['url_slug'],
            'time_created': p['time_created'],
            # convert the markdown text to html
            'body': markdown2.markdown(p['body'])
        }

        # only show the first paragraph in the body
        if summarize:
            new_post["body"] = new_post["body"].split('\n')[0]

        processed_posts.append(new_post)

    return processed_posts

# changing title to url_slug style
def convert_title_to_url(title):
    new_title = title.replace(' ', '-').lower()
    return new_title


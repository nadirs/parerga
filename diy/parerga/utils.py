# -*- set coding: utf-8 -*-

import codecs, glob, os, re, time
import markdown
from flask import Markup
import db

# Snippet borrowed from: http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim='-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        if word:
            result.append(word)
    return delim.join(result)

def get_all_entries():
    ids = db.get_all_entry_ids()
    entries = []
    for idx in ids:
        entries.append(Entry(idx))
    return entries

def get_all_tags():
    entries = get_all_entries()
    tags = set()
    for entry in entries:
        tags.update(entry['tags'])
    return sorted(tags)

def prettify_time(time_param):
    return time.strftime("%d %b. %Y", time_param)

class EntryException(Exception):
    pass

class Entry(dict):
    def __init__(self, entry_id, debug=False):
        if entry_id not in db.get_all_entry_ids():
            raise EntryException("entry {} does not exist".format(entry_id))
        self['id'] = entry_id
        self['date'] = prettify_time(db.get_entry_date(entry_id))
        self['tags'] = []
        self['title'] = ""
        path = db.get_entry_path(entry_id)
        head, self['content'] = codecs.open(path, encoding='utf-8').read().split('\n\n', 1)
        self.parse_head(head)

    @property
    def short_content(self):
        first_paragraph = self['content'].split('\n\n', 1)[0]
        first_paragraph = first_paragraph.replace('  ', ' ')

        words = (first_paragraph).split(' ')
        if len(words) >= 30:
            result = ' '.join(words[:30])
        else:
            result = first_paragraph
        #TODO find a better way to strip punctuation
        return (result.rstrip('.')
                .rstrip(',')
                .rstrip(';')
                .rstrip(':') + '...')

    @property
    def short_content_html(self):
        return self.markdown(self.short_content)

    @property
    def content_html(self):
        return self.markdown(self['content'])

    def markdown(self, content):
        return Markup(markdown.markdown(
                content,
                ['codehilite',
                 'headerid',
                 'toc(title=Table Of Contents, anchorlink=True)']))

    def parse_head(self, head):
        for line in head.splitlines():
            key, value = line.split(':', 1)
            self[key] = self.parse_head_element(key, value)

    def parse_head_element(self, key, value):
        if key == 'date':
            return self.parse_date(value)
        elif key == 'tags':
            return self.parse_tags(value)
        elif key == 'title':
            return self.parse_title(value)
        else:
            raise LookUpError

    def parse_date(self, date):
        return date.strip()

    def parse_tags(self, tags):
        return sorted([tag.strip() for tag in tags.split(',')])

    def parse_title(self, title):
        return title.strip()

if __name__ == '__main__':
    pass

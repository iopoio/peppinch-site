import unittest
import tempfile
import json
from pathlib import Path
from readable import ArticleText, prepare_article, article_data, prune_generated
from build import render_post
from publish import meta, modified_date


class ReadableTests(unittest.TestCase):
    def test_body_links_and_noise(self):
        parser = ArticleText('https://www.peppinch.com/blog/posts/example')
        parser.feed('''<nav>다른 글</nav><div class="content"><p>처음 &amp; 다음<br>줄</p>
        <p><a href="/source">출처</a></p><iframe src="/report"></iframe>
        <img src="x.png" alt="설명"><div class="likewrap">좋아요</div>
        <script>secret()</script><p>끝</p></div><footer>메일</footer>''')
        result = parser.text()
        self.assertIn('처음 & 다음', result)
        self.assertIn('https://www.peppinch.com/source', result)
        self.assertIn('https://www.peppinch.com/report', result)
        self.assertIn('[이미지: 설명]', result)
        self.assertTrue(result.endswith('끝'))
        for noise in ['다른 글', '좋아요', 'secret', '메일']:
            self.assertNotIn(noise, result)

    def test_briefing_keeps_collapsed_details_and_table(self):
        parser = ArticleText('https://www.peppinch.com/x')
        parser.feed('<main><details><summary>주제</summary><p>내용</p></details><table><tr><th>항목</th><td>값</td></tr></table></main>')
        self.assertIn('주제', parser.text())
        self.assertIn('내용', parser.text())
        self.assertIn('항목 | 값', parser.text())

    def test_prepare_is_idempotent_and_matches_visible_metadata(self):
        data = {"headline": "이전 제목", "description": "이전 설명", "datePublished": "2026-06-13T00:00:00+09:00", "dateModified": "2026-09-11T00:00:00+09:00", "author": {"name": "peppinch"}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / '2026-06-13-example.html'
            path.write_text('<html><head><meta name="description" content="새 설명"><meta property="og:title" content="새 제목"><script type="application/ld+json">' + json.dumps(data) + '</script></head><body><h1>새 제목</h1><main><p>본문</p></main></body></html>')
            prepare_article(path)
            first = path.read_text()
            prepare_article(path)
            self.assertEqual(first, path.read_text())
            self.assertEqual(first.count('class="article-byline"'), 1)
            self.assertEqual(first.count('rel="alternate"'), 1)
            entry = article_data(path)
            self.assertEqual(entry['published'], '2026-06-13')
            self.assertEqual(entry['modified'], '2026-09-11')
            self.assertEqual(entry['description'], '새 설명')
            self.assertEqual(entry['title'], '새 제목')

    def test_quoted_title_survives_build_and_prepare(self):
        title = 'AI가 "채점"한다'
        values = {"title": title, "description": "설명", "date": "2026-06-13", "tags": [], "slug": "2026-06-13-example", "section": "기록"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / '2026-06-13-example.html'
            path.write_text(render_post(values, "본문"))
            prepare_article(path)
            self.assertEqual(article_data(path)['title'], title)

    def test_prune_only_owned_removed_files(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for name in ['old.txt', 'current.txt', 'manual.txt']:
                (target / name).write_text('내용')
            (target / '.generated.json').write_text('["old.txt", "current.txt"]')
            prune_generated(target, ['current.txt'])
            self.assertFalse((target / 'old.txt').exists())
            self.assertTrue((target / 'current.txt').exists())
            self.assertTrue((target / 'manual.txt').exists())

    def test_metadata_decodes_entities_once(self):
        self.assertEqual(meta('name="description" content="A &amp; &quot;B&quot;"', r'content="([^"]*)"'), 'A & "B"')
        self.assertEqual(modified_date('{"dateModified": "2026-09-11T00:00:00+09:00"}', '2026-06-13'), '2026-09-11')
        self.assertEqual(modified_date('', '2026-06-13'), '2026-06-13')


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""Tests for the news-image-20261124 poster. Run: python3 -m unittest discover -s tests -v"""
import ast
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)

import render_poster as rp  # noqa: E402


class TestStories(unittest.TestCase):
    def test_count(self):
        all_n = [s[0] for s in rp.STORIES] + [a[0] for a in rp.ALSO_ON]
        self.assertEqual(len(all_n), 31, "poster must carry 31 stories")
        self.assertEqual(sorted(all_n), list(range(1, 32)))

    def test_regions(self):
        regions = {s[1] for s in rp.STORIES} | {a[1] for a in rp.ALSO_ON}
        self.assertEqual(regions, set(rp.REGION_COUNTS))
        self.assertEqual(sum(rp.REGION_COUNTS.values()), 31)
        self.assertEqual(rp.N_REGIONS, 6)

    def test_every_story_has_source(self):
        for s in rp.STORIES:
            self.assertTrue(s[5], "story %d has no source" % s[0])
        for a in rp.ALSO_ON:
            self.assertTrue(a[3], "story %d has no source" % a[0])

    def test_no_offday_in_main_list(self):
        text = " ".join(s[3] + " " + s[4] for s in rp.STORIES)
        text += " ".join(a[2] for a in rp.ALSO_ON)
        self.assertNotIn("Nvidia", text)
        self.assertNotIn("Huang", text)
        self.assertNotIn("COP31", text)
        self.assertNotIn("GTA", text)
        self.assertNotIn("23 Nov", text)
        self.assertNotIn("22 Nov", text)

    def test_date_check_is_small_and_neutral(self):
        self.assertLessEqual(len(rp.DATE_CHECK), 3)
        joined = " ".join(rp.DATE_CHECK)
        self.assertIn("23 Nov", joined)
        self.assertIn("22 Nov", joined)
        self.assertNotIn("NOT SUNDAY", joined)


class TestRender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path, cls.size, cls.sha = rp.render()

    def test_output_specs(self):
        self.assertTrue(os.path.isfile(rp.OUT))
        self.assertLessEqual(self.size, 1048576, "entry.png over 1 MiB")
        from PIL import Image
        with Image.open(rp.OUT) as im:
            self.assertEqual(im.size, (1024, 1024))
            self.assertEqual(im.mode, "RGB")

    def test_deterministic(self):
        path2, _size2, sha2 = rp.render()
        self.assertEqual(sha2, self.sha, "render is not byte-deterministic")

    def test_clearance(self):
        bad = rp.check_clearance()
        self.assertEqual(bad, [], "text touches a card border: %r" % (bad,))

    def test_preview_300(self):
        self.assertTrue(os.path.isfile(rp.PREVIEW))
        from PIL import Image
        with Image.open(rp.PREVIEW) as im:
            self.assertEqual(im.size, (300, 300))
        # masthead band must not be blank at 300px
        with Image.open(rp.PREVIEW) as im:
            px = list(im.crop((0, 10, 300, 40)).getdata())
        vals = {p for p in px}
        self.assertGreater(len(vals), 8, "masthead band looks blank at 300px")


class TestMain(unittest.TestCase):
    def test_stdlib_only(self):
        with open(os.path.join(REPO, "main.py")) as f:
            tree = ast.parse(f.read())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        allowed = sys.stdlib_module_names
        self.assertTrue(imported <= allowed,
                        "non-stdlib imports: %s" % (imported - allowed,))

    def test_main_copies_byte_identical(self):
        with tempfile.TemporaryDirectory() as td:
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=td)
            r = subprocess.run([sys.executable, "main.py"], cwd=REPO,
                               env=env, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            out = os.path.join(td, "entry.png")
            self.assertTrue(os.path.isfile(out))
            self.assertEqual(os.stat(out).st_mode & 0o777, 0o644)
            with open(out, "rb") as f:
                got = hashlib.sha256(f.read()).hexdigest()
            with open(rp.OUT, "rb") as f:
                want = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(got, want)


class TestGraderConditions(unittest.TestCase):
    def test_main_runs_as_nobody_on_readonly_copy(self):
        with tempfile.TemporaryDirectory() as td:
            copy_dir = os.path.join(td, "repo")
            os.makedirs(copy_dir)
            for f in ("main.py", "entry.png"):
                src = os.path.join(REPO, f)
                dst = os.path.join(copy_dir, f)
                with open(src, "rb") as a, open(dst, "wb") as b:
                    b.write(a.read())
                # simulate a bundle extracted by the grader user
                os.chmod(dst, 0o644)
            os.chmod(copy_dir, 0o555)
            out_dir = os.path.join(td, "out")
            os.makedirs(out_dir, exist_ok=True)
            os.chmod(td, 0o755)
            os.chmod(out_dir, 0o777)
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=out_dir)
            r = subprocess.run(["setpriv", "--reuid=65534", "--regid=65534",
                                "--clear-groups", sys.executable,
                                "main.py"],
                               cwd=copy_dir, env=env, capture_output=True,
                               text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            got = hashlib.sha256(
                open(os.path.join(out_dir, "entry.png"), "rb").read()
            ).hexdigest()
            with open(rp.OUT, "rb") as f:
                want = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()

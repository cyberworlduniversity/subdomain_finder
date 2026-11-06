import tempfile
import unittest
from pathlib import Path

from subdomain_finder import SubdomainFinder


class SubdomainFinderValidationTests(unittest.TestCase):
    def test_rejects_invalid_domains(self):
        for domain in ["", "localhost", "example..com", "-bad.example.com", "a" * 64 + ".com"]:
            with self.subTest(domain=domain):
                with self.assertRaises(ValueError):
                    SubdomainFinder(domain, "wordlist.txt")

    def test_bounds_threads_and_timeout(self):
        for threads in [0, 201]:
            with self.subTest(threads=threads):
                with self.assertRaises(ValueError):
                    SubdomainFinder("example.com", "wordlist.txt", threads=threads)
        for timeout in [0, 0.05, 30.1]:
            with self.subTest(timeout=timeout):
                with self.assertRaises(ValueError):
                    SubdomainFinder("example.com", "wordlist.txt", timeout=timeout)

    def test_wordlist_keeps_only_valid_single_labels(self):
        with tempfile.TemporaryDirectory() as directory:
            wordlist = Path(directory) / "words.txt"
            wordlist.write_text("www\n# comment\napi-1\nbad_label\nfoo.bar\n", encoding="utf-8")
            finder = SubdomainFinder("example.com", str(wordlist))
            self.assertEqual(finder.load_wordlist(), ["www", "api-1"])


if __name__ == "__main__":
    unittest.main()
